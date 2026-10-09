"""
================================================================================
  SHAREPOINT FILE BRIDGE — Local Flask Server (port 5004)
  Sempra Data Migration Dashboard

  Reads Excel files DIRECTLY from SharePoint Online using OAuth2 device-flow.

  FIRST RUN:
    1. python automation/sp_bridge.py
    2. It prints a URL + code — open that URL in your browser, enter the code
    3. Log in with your Sempra account (KMarri@scgcontractor.com)
    4. Token is saved to automation/output/sp_token.json — never asked again

  SharePoint path:
    https://sempra.sharepoint.com/sites/OdysseyInternal/
    Shared Documents/General/05-Odyssey Phase 1 (Official)/02- Explore/
    02- Technical Workstreams/Data Migration/Dashboard_file_reader/
      DM1/   DM2/   DM3/

  Same endpoint contract as file_watcher_bridge.py (port 5002):
    GET /ping
    GET /scan?cycle=DM1
    GET /file?cycle=DM1&type=ref
    POST /cache/clear

  Requires:
    pip install flask flask-cors office365-REST-Python-Client
================================================================================
"""

import os, sys, gzip, hashlib, logging, threading, json
from datetime import datetime
from pathlib import Path

os.makedirs("automation/logs",   exist_ok=True)
os.makedirs("automation/output", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("automation/logs/sp_bridge.log", mode="a"),
    ],
)
log = logging.getLogger(__name__)

try:
    from flask import Flask, request, jsonify, Response
    from flask_cors import CORS
except ImportError:
    log.error("Run: pip install flask flask-cors"); sys.exit(1)

try:
    from office365.runtime.auth.token_response import TokenResponse
    from office365.sharepoint.client_context import ClientContext
except ImportError:
    log.error("Run: pip install office365-REST-Python-Client"); sys.exit(1)

app = Flask(__name__)
CORS(app)

# ════════════════════════════════════════════════════════════════════════
#  CONFIG
# ════════════════════════════════════════════════════════════════════════
_SP_SITE      = "https://sempra.sharepoint.com/sites/OdysseyInternal"
_SP_FOLDER    = ("Shared Documents/General"
                 "/05-Odyssey Phase 1 (Official)/02- Explore"
                 "/02- Technical Workstreams/Data Migration"
                 "/Dashboard_file_reader")
_TOKEN_FILE   = "automation/output/sp_token.json"
_CACHE_TTL    = 300   # seconds before re-fetching from SharePoint

# Microsoft Office client ID — pre-consented in every Azure AD tenant by default
_CLIENT_ID    = "d3590ed6-52b3-4102-aeff-aad2292ab01c"   # Microsoft Office
_TENANT       = "a2e7980c-11ea-4838-8f1a-2f497d8c4072"   # sempra.com tenant

# ── Keywords for REF vs EXP detection ────────────────────────────────────────
_REF_KW = ["ref", "reference", "reflist", "master", "table", "list"]
_EXP_KW = ["exp", "imp", "export", "import", "snp", "count", "transition", "log"]

def _classify(filename: str, file_type: str) -> bool:
    fn = filename.lower()
    if file_type == "ref":
        return any(k in fn for k in _REF_KW)
    return any(k in fn for k in _EXP_KW)

# ════════════════════════════════════════════════════════════════════════
#  AUTH — device-flow OAuth (ask user once, save token)
# ════════════════════════════════════════════════════════════════════════
_ctx      = None
_ctx_lock = threading.Lock()

def _get_ctx():
    global _ctx
    with _ctx_lock:
        if _ctx is not None:
            return _ctx
        _ctx = ClientContext(_SP_SITE).with_interactive(tenant=_TENANT, client_id=_CLIENT_ID)
        return _ctx

# ════════════════════════════════════════════════════════════════════════
#  SHAREPOINT FILE LISTING & DOWNLOAD
# ════════════════════════════════════════════════════════════════════════
def _list_files(cycle: str):
    """Return list of (name, server_relative_url) for xlsx files in the cycle folder."""
    ctx        = _get_ctx()
    folder_url = f"{_SP_FOLDER}/{cycle}"
    folder     = ctx.web.get_folder_by_server_relative_url(folder_url)
    files      = folder.files
    ctx.load(files)
    ctx.execute_query()
    result = []
    for f in files:
        name = f.properties.get("Name", "")
        url  = f.properties.get("ServerRelativeUrl", "")
        if name.endswith((".xlsx", ".xls")) and not name.startswith("~$"):
            result.append((name, url))
    return result


def _download_file(server_relative_url: str) -> bytes:
    """Download a file from SharePoint by its ServerRelativeUrl."""
    ctx = _get_ctx()
    import io
    buf = io.BytesIO()
    ctx.web.get_file_by_server_relative_url(server_relative_url).download(buf).execute_query()
    return buf.getvalue()


def _fetch_sp_file(cycle: str, file_type: str):
    """List cycle folder, pick best file, download and return (filename, bytes)."""
    log.info(f"Listing SharePoint [{cycle}] folder...")
    files = _list_files(cycle)
    if not files:
        raise FileNotFoundError(f"No .xlsx files found in SharePoint {cycle} folder.")

    matched  = [(n, u) for n, u in files if _classify(n, file_type)]
    name, url = matched[0] if matched else files[0]

    log.info(f"Downloading [{cycle}/{file_type}] {name}")
    raw = _download_file(url)
    log.info(f"Downloaded  [{cycle}/{file_type}] {name} ({len(raw)//1024} KB)")
    return name, raw

# ════════════════════════════════════════════════════════════════════════
#  IN-MEMORY CACHE
# ════════════════════════════════════════════════════════════════════════
_cache      = {}
_cache_lock = threading.Lock()

def _get_cached(cycle: str, file_type: str):
    key = (cycle, file_type)
    now = datetime.now().timestamp()
    with _cache_lock:
        entry = _cache.get(key)
        if entry and (now - entry["ts"]) < _CACHE_TTL:
            log.info(f"Cache HIT [{cycle}/{file_type}] {entry['filename']}")
            return entry

    filename, raw = _fetch_sp_file(cycle, file_type)
    compressed    = gzip.compress(raw, compresslevel=6)
    etag          = hashlib.md5(raw).hexdigest()
    entry = {
        "filename": filename,
        "size_kb":  round(len(raw) / 1024, 1),
        "gz_kb":    round(len(compressed) / 1024, 1),
        "data_raw": raw,
        "data_gz":  compressed,
        "etag":     etag,
        "ts":       now,
    }
    with _cache_lock:
        _cache[key] = entry
    return entry

# ════════════════════════════════════════════════════════════════════════
#  ROUTES
# ════════════════════════════════════════════════════════════════════════
@app.route("/ping", methods=["GET"])
def ping():
    with _cache_lock:
        cached = [f"{c}/{t}" for (c, t) in _cache.keys()]
    return jsonify({
        "status":      "ok",
        "service":     "sp_bridge",
        "data_source": "sharepoint",
        "sp_site":     _SP_SITE,
        "ts":          datetime.now().isoformat(),
        "cached":      cached,
    })


@app.route("/scan", methods=["GET"])
def scan():
    cycle = request.args.get("cycle", "DM1").upper()
    try:
        files   = _list_files(cycle)
        names   = [n for n, _ in files]
        ref_f   = next((n for n in names if _classify(n, "ref")), names[0] if names else None)
        exp_f   = next((n for n in names if _classify(n, "exp")), None)
        return jsonify({
            "cycle":     cycle,
            "source":    "sharepoint",
            "ref":       {"filename": ref_f, "available": ref_f is not None},
            "exp":       {"filename": exp_f, "available": exp_f is not None},
            "all_files": names,
        })
    except Exception as e:
        return jsonify({"error": str(e), "cycle": cycle}), 500


@app.route("/file", methods=["GET"])
def get_file():
    cycle     = request.args.get("cycle", "DM1").upper()
    file_type = request.args.get("type",  "ref").lower()
    try:
        entry = _get_cached(cycle, file_type)
    except Exception as e:
        log.error(f"SP error [{cycle}/{file_type}]: {e}")
        return jsonify({"error": str(e)}), 502

    if request.headers.get("If-None-Match", "") == entry["etag"]:
        return Response(status=304)

    mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    accepts_gz = "gzip" in request.headers.get("Accept-Encoding", "")
    if accepts_gz:
        resp = Response(entry["data_gz"], status=200, mimetype=mime)
        resp.headers["Content-Encoding"] = "gzip"
        resp.headers["Content-Length"]   = len(entry["data_gz"])
    else:
        resp = Response(entry["data_raw"], status=200, mimetype=mime)
        resp.headers["Content-Length"]   = len(entry["data_raw"])

    resp.headers["Content-Disposition"] = f'attachment; filename="{entry["filename"]}"'
    resp.headers["ETag"]                = entry["etag"]
    resp.headers["Cache-Control"]       = "no-cache"
    resp.headers["X-Source"]            = "sharepoint"
    return resp


@app.route("/cache/clear", methods=["POST"])
def cache_clear():
    with _cache_lock:
        _cache.clear()
    return jsonify({"ok": True})


# ════════════════════════════════════════════════════════════════════════
#  START
# ════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    log.info("=" * 64)
    log.info("  SharePoint File Bridge  port 5004")
    log.info(f"  Site : {_SP_SITE}")
    log.info(f"  Folder: {_SP_FOLDER}")
    log.info("  NOTE: On first run, a browser login prompt will appear.")
    log.info("        Log in with KMarri@scgcontractor.com (Sempra tenant)")
    log.info(f"  Tenant: {_TENANT}")
    log.info("=" * 64)
    # Trigger auth + first connection on a background thread so Flask starts immediately
    def _warmup():
        try:
            log.info("Connecting to SharePoint (device-flow login)...")
            _get_ctx().web.get().execute_query()
            log.info("SharePoint connection OK")
        except Exception as e:
            log.warning(f"SharePoint warmup: {e}")
    threading.Thread(target=_warmup, daemon=True).start()
    app.run(host="127.0.0.1", port=5004, debug=False, threaded=True, use_reloader=False)
