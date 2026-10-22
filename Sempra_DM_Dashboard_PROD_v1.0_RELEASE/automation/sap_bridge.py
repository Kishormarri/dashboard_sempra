"""
================================================================================
  SAP BRIDGE API — Local Flask Server
  Global Data Migration Automation Framework

  Purpose : Runs as a local API on http://localhost:5001
            The HTML dashboard calls this API to:
            1. Upload Reference List (Excel/CSV)
            2. Connect to SAP Source system → SE16N-style table counts
            3. Connect to SAP Target system → SE16N-style table counts
            4. Export merged Source + Target counts to Excel

  Usage   : python automation/sap_bridge.py
  Then open the dashboard and use the Automation panel.

  Requires: pip install flask flask-cors pandas openpyxl pyrfc
================================================================================
"""

import os
import sys
import json
import threading
import logging
from datetime import datetime
from pathlib import Path

# ── logging ──────────────────────────────────────────────────────────────────
os.makedirs("automation/logs",   exist_ok=True)
os.makedirs("automation/output", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout),
              logging.FileHandler("automation/logs/bridge.log", mode="a")]
)
log = logging.getLogger(__name__)

# ── Flask ─────────────────────────────────────────────────────────────────────
try:
    from flask import Flask, request, jsonify, send_file
    from flask_cors import CORS
except ImportError:
    log.error("Flask not installed. Run: python -m pip install flask flask-cors")
    sys.exit(1)

import pandas as pd

app  = Flask(__name__)
CORS(app)

# ── Global state ──────────────────────────────────────────────────────────────
_state = {
    "status"   : "idle",
    "step"     : "",
    "progress" : 0,
    "log"      : [],
    "tables"   : [],
    "results"  : {},   # {tableName: {"source": int|None, "target": int|None}}
    "summary"  : {}
}
_lock = threading.Lock()


def _log(msg, level="info"):
    ts = datetime.now().strftime("%H:%M:%S")
    entry = f"[{ts}] {msg}"
    with _lock:
        _state["log"].append(entry)
        if len(_state["log"]) > 200:
            _state["log"] = _state["log"][-200:]
    getattr(log, level)(msg)


def _set(key, val):
    with _lock:
        _state[key] = val


# ════════════════════════════════════════════════════════════════════════════
#  SE16N-STYLE COUNT — tries 3 methods in order, same as what SE16N shows
# ════════════════════════════════════════════════════════════════════════════

def _get_count_se16n(conn, table_name):
    """
    Get SE16N-equivalent row count for a SAP table.
    Tries 3 methods in order of reliability:
      1. EM_GET_NUMBER_OF_ENTRIES  — fast, used internally by SE16N
      2. RFC_READ_TABLE COUNT(*)   — standard, works on most systems
      3. RFC_READ_TABLE full read  — fallback for restricted systems
    Returns int count or None on failure.
    """
    table = table_name.strip().upper()

    # ── Method 1: EM_GET_NUMBER_OF_ENTRIES (SE16N internal FM) ───────────────
    try:
        result = conn.call("EM_GET_NUMBER_OF_ENTRIES", IT_OBJECTS=[{"TABNAME": table}])
        entries = result.get("ET_OBJECTS", [])
        if entries:
            return int(entries[0].get("TABECNT", 0))
    except Exception:
        pass

    # ── Method 2: RFC_READ_TABLE with WHERE 1=1, get DATA length ─────────────
    try:
        result = conn.call(
            "RFC_READ_TABLE",
            QUERY_TABLE = table,
            DELIMITER   = ";",
            ROWCOUNT    = 0,
            FIELDS      = [],
            OPTIONS     = []
        )
        return len(result.get("DATA", []))
    except Exception:
        pass

    # ── Method 3: BBP_RFC_READ_TABLE (alternative on some systems) ───────────
    try:
        result = conn.call(
            "BBP_RFC_READ_TABLE",
            QUERY_TABLE = table,
            ROWCOUNT    = 0,
            FIELDS      = [],
            OPTIONS     = []
        )
        return len(result.get("DATA", []))
    except Exception:
        pass

    return None


def _get_count_demo(table_name):
    """DEMO mode — returns simulated count when pyrfc not installed."""
    import random, hashlib
    h = int(hashlib.md5(table_name.encode()).hexdigest(), 16)
    return (h % 49900) + 100


# ════════════════════════════════════════════════════════════════════════════
#  ROUTES
# ════════════════════════════════════════════════════════════════════════════

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok", "version": "2.0", "ts": datetime.now().isoformat()})


@app.route("/upload_ref", methods=["POST"])
def upload_ref():
    """
    Upload Reference List Excel/CSV.
    Auto-detects table name column and stores table list in state.
    """
    try:
        if "file" not in request.files:
            return jsonify({"ok": False, "error": "No file uploaded"}), 400

        f     = request.files["file"]
        fname = f.filename.lower()

        if fname.endswith(".csv"):
            df = pd.read_csv(f)
        elif fname.endswith((".xlsx", ".xls")):
            df = pd.read_excel(f)
        else:
            return jsonify({"ok": False, "error": "Unsupported file type. Use .xlsx or .csv"}), 400

        # Auto-detect table name column
        is_ref = any(k in fname for k in ["reference", "reflist", "ref_list", "ref list", "ref_m"])
        tbl_col = None
        known = ["table_name", "tablename", "table", "object_name", "object", "name", "field", "key", "id"]
        for k in known:
            for col in df.columns:
                if col.strip().lower() == k:
                    tbl_col = col; break
            if tbl_col: break
        if not tbl_col:
            for col in df.columns:
                if "table" in col.lower(): tbl_col = col; break
        if not tbl_col:
            for col in df.columns:
                if "object" in col.lower(): tbl_col = col; break
        if not tbl_col and is_ref:
            for col in df.columns:
                if "name" in col.lower(): tbl_col = col; break
        if not tbl_col:
            tbl_col = df.columns[0]

        tables = [str(r).strip().upper() for r in df[tbl_col].dropna() if str(r).strip()]
        tables = [t for t in tables if t and t != "NAN"]

        _set("tables",  tables)
        _set("results", {t: {"source": None, "target": None} for t in tables})
        _set("status",  "idle")
        _set("log",     [])

        _log(f"✔ Reference list loaded: {len(tables)} tables from '{f.filename}' (column: {tbl_col})")

        out = {"tables": tables, "source_file": f.filename, "loaded_at": datetime.now().isoformat()}
        with open("automation/output/ref_tables.json", "w") as jf:
            json.dump(out, jf, indent=2)

        return jsonify({"ok": True, "table_count": len(tables), "tables": tables[:20], "column_used": tbl_col})

    except Exception as e:
        log.exception("upload_ref error")
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/connect_sap", methods=["POST"])
def connect_sap():
    """
    Receive SAP credentials + system type (source/target).
    Spawns background thread to fetch SE16N-style counts for all ref tables.
    """
    try:
        body     = request.get_json(force=True)
        sys_type = body.get("system", "source")
        creds    = {
            "ashost": body.get("host",   ""),
            "sysnr" : body.get("sysnr",  "00"),
            "client": body.get("client", "100"),
            "user"  : body.get("user",   body.get("username", "")),
            "passwd": body.get("passwd", body.get("password", "")),
            "lang"  : body.get("lang",   "EN")
        }

        # Tables can be passed directly from the browser
        browser_tables = body.get("tables", [])
        if browser_tables:
            _set("tables",  browser_tables)
            _set("results", {t: {"source": None, "target": None} for t in browser_tables})

        tables = _state.get("tables", [])
        if not tables:
            return jsonify({"ok": False, "error": "No reference list loaded. Upload a Reference List file first."}), 400

        if not creds["ashost"] or not creds["user"] or not creds["passwd"]:
            return jsonify({"ok": False, "error": "SAP Host, Username and Password are required."}), 400

        _set("status",   "running")
        _set("step",     f"Connecting to SAP {sys_type.upper()}…")
        _set("progress", 2)
        _state["log"].clear()
        _log(f"🔗 Starting SAP {sys_type.upper()} extraction (SE16N-style) — {len(tables)} tables")

        t = threading.Thread(target=_run_sap_counts, args=(creds, tables, sys_type), daemon=True)
        t.start()

        return jsonify({"ok": True, "message": f"SAP {sys_type} extraction started", "table_count": len(tables)})

    except Exception as e:
        log.exception("connect_sap error")
        return jsonify({"ok": False, "error": str(e)}), 500


def _run_sap_counts(creds, tables, sys_type):
    """Background worker — connects to SAP and counts each table via SE16N method."""
    _log(f"⚙ Connecting to SAP {creds['ashost']} (client {creds['client']})…")
    conn      = None
    demo_mode = False

    try:
        try:
            import pyrfc
            conn = pyrfc.Connection(**creds)
            _log(f"✔ SAP RFC connection established ({sys_type.upper()})")
        except ImportError:
            _log("⚠ pyrfc not installed — running in DEMO mode (simulated counts)", "warning")
            demo_mode = True
        except Exception as e:
            _log(f"✘ SAP connection failed: {str(e)[:120]}", "error")
            _set("status", "error")
            return

        total  = len(tables)
        ok     = 0
        failed = []

        for i, table in enumerate(tables):
            pct = int(((i + 1) / total) * 95)
            _set("progress", pct)
            _set("step", f"SE16N: {table} ({i+1}/{total})")

            if demo_mode:
                count = _get_count_demo(table)
            else:
                count = _get_count_se16n(conn, table)

            with _lock:
                if sys_type == "source":
                    _state["results"][table]["source"] = count
                else:
                    _state["results"][table]["target"] = count

            if count is not None:
                ok += 1
                if i % 50 == 0 or i < 5:
                    _log(f"  ✔ [{i+1}/{total}] {table} = {count:,}")
            else:
                failed.append(table)
                if len(failed) <= 10:
                    _log(f"  ✘ [{i+1}/{total}] {table} — count failed")

        results = _state["results"]
        matched = sum(1 for r in results.values()
                      if r["source"] is not None and r["target"] is not None
                      and r["source"] == r["target"])
        summary = {
            "total"    : total,
            "counted"  : ok,
            "failed"   : len(failed),
            "matched"  : matched,
            "generated": datetime.now().isoformat(),
            "system"   : sys_type,
            "demo_mode": demo_mode
        }
        _set("summary",  summary)
        _set("status",   "done")
        _set("progress", 100)
        _log(f"✅ {sys_type.upper()} SE16N extraction complete — {ok}/{total} tables counted"
             + (f" | {len(failed)} failed" if failed else ""))

        _save_output_json()

    except Exception as e:
        _log(f"✘ Extraction error: {e}", "error")
        _set("status", "error")
    finally:
        if conn:
            try: conn.close()
            except Exception: pass


def _save_output_json():
    """Save merged Source + Target results to JSON."""
    results = _state["results"]
    tables  = []
    for tbl, counts in results.items():
        src = counts.get("source")
        tgt = counts.get("target")
        var = (src - tgt) if src is not None and tgt is not None else None
        tables.append({
            "table"      : tbl,
            "sourceCount": src,
            "targetCount": tgt,
            "variance"   : var,
            "status"     : ("✔ Match" if var == 0
                            else "✘ Mismatch" if var is not None
                            else "⚠ Pending")
        })
    matched    = sum(1 for t in tables if t["status"] == "✔ Match")
    mismatched = sum(1 for t in tables if t["status"] == "✘ Mismatch")
    payload = {
        "generated": datetime.now().isoformat(),
        "summary"  : {
            "total"     : len(tables),
            "matched"   : matched,
            "mismatched": mismatched,
            "missing"   : len(tables) - matched - mismatched,
            "matchPct"  : round((matched / len(tables)) * 100, 1) if tables else 0
        },
        "tables": tables
    }
    out_path = "automation/output/dashboard_ref_counts.json"
    with open(out_path, "w") as f:
        json.dump(payload, f, indent=2)
    _log(f"💾 JSON saved → {out_path}")


# ════════════════════════════════════════════════════════════════════════════
#  EXCEL EXPORT — Source Count + Target Count side by side
# ════════════════════════════════════════════════════════════════════════════

@app.route("/export_excel", methods=["GET"])
def export_excel():
    """
    Export full Source + Target count table as Excel.
    Columns: Table Name | Source Count (SE16N) | Target Count (SE16N) | Variance | Status
    Green = Match, Red = Mismatch, Grey = Pending.
    """
    try:
        import openpyxl
        from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
        from openpyxl.utils import get_column_letter
        import io

        results = _state["results"]
        if not results:
            return jsonify({"ok": False, "error": "No data yet. Run Source and Target extraction first."}), 400

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "SAP Table Counts"

        # ── Styles ────────────────────────────────────────────────────────────
        hdr_fill   = PatternFill("solid", fgColor="1E3A5F")
        hdr_font   = Font(bold=True, color="FFFFFF", size=11)
        match_fill = PatternFill("solid", fgColor="052E16")
        match_font = Font(color="22C55E", bold=True)
        mis_fill   = PatternFill("solid", fgColor="450A0A")
        mis_font   = Font(color="F87171", bold=True)
        pend_fill  = PatternFill("solid", fgColor="1C1400")
        pend_font  = Font(color="FDE68A")
        num_align  = Alignment(horizontal="right")
        ctr_align  = Alignment(horizontal="center")
        thin       = Side(style="thin", color="2A2A2A")
        border     = Border(left=thin, right=thin, top=thin, bottom=thin)

        # ── Header row ────────────────────────────────────────────────────────
        headers = ["#", "Table Name", "Source Count\n(SE16N)", "Target Count\n(SE16N)", "Variance", "Status"]
        ws.append(headers)
        ws.row_dimensions[1].height = 32

        for c_idx, hdr in enumerate(headers, 1):
            cell = ws.cell(row=1, column=c_idx)
            cell.fill      = hdr_fill
            cell.font      = hdr_font
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            cell.border    = border

        # ── Data rows ─────────────────────────────────────────────────────────
        for row_num, (tbl, counts) in enumerate(results.items(), 2):
            src = counts.get("source")
            tgt = counts.get("target")
            var = (src - tgt) if src is not None and tgt is not None else None
            if var == 0:
                status = "✔ Match"
                fill, font = match_fill, match_font
            elif var is not None:
                status = "✘ Mismatch"
                fill, font = mis_fill, mis_font
            else:
                status = "⚠ Pending"
                fill, font = pend_fill, pend_font

            row_data = [
                row_num - 1,
                tbl,
                src if src is not None else "—",
                tgt if tgt is not None else "—",
                var if var is not None else "—",
                status
            ]
            ws.append(row_data)
            ws.row_dimensions[row_num].height = 18

            for c_idx, val in enumerate(row_data, 1):
                cell         = ws.cell(row=row_num, column=c_idx)
                cell.fill    = fill
                cell.font    = font
                cell.border  = border
                if c_idx in (1, 3, 4, 5):
                    cell.alignment = num_align
                elif c_idx == 6:
                    cell.alignment = ctr_align

        # ── Column widths ─────────────────────────────────────────────────────
        col_widths = [6, 32, 20, 20, 14, 18]
        for i, w in enumerate(col_widths, 1):
            ws.column_dimensions[get_column_letter(i)].width = w

        # ── Summary sheet ─────────────────────────────────────────────────────
        ws2 = wb.create_sheet("Summary")
        all_tables = list(results.values())
        total      = len(all_tables)
        matched    = sum(1 for r in all_tables if r["source"] is not None and r["target"] is not None and r["source"] == r["target"])
        mismatched = sum(1 for r in all_tables if r["source"] is not None and r["target"] is not None and r["source"] != r["target"])
        pending    = total - matched - mismatched
        match_pct  = round((matched / total) * 100, 1) if total else 0

        ws2.append(["SAP Table Count Summary — SE16N"])
        ws2.append(["Generated", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
        ws2.append([])
        ws2.append(["Metric", "Value"])
        ws2.append(["Total Tables",    total])
        ws2.append(["✔ Matched",        matched])
        ws2.append(["✘ Mismatched",     mismatched])
        ws2.append(["⚠ Pending",        pending])
        ws2.append(["Match %",          f"{match_pct}%"])

        ws2.column_dimensions["A"].width = 22
        ws2.column_dimensions["B"].width = 14

        # ── Stream to browser ─────────────────────────────────────────────────
        buf = io.BytesIO()
        wb.save(buf)
        buf.seek(0)

        ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"SAP_Table_Counts_SE16N_{ts}.xlsx"

        return send_file(
            buf,
            as_attachment=True,
            download_name=filename,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        log.exception("export_excel error")
        return jsonify({"ok": False, "error": str(e)}), 500


# ════════════════════════════════════════════════════════════════════════════
#  EXISTING ROUTES (unchanged)
# ════════════════════════════════════════════════════════════════════════════

@app.route("/progress", methods=["GET"])
def progress():
    with _lock:
        status = _state["status"]
        counts = {}
        if status == "done":
            for tbl, v in _state["results"].items():
                counts[tbl] = v.get("source") if v.get("source") is not None else v.get("target")
        return jsonify({
            "status"      : status,
            "pct"         : _state["progress"],
            "step"        : _state["step"],
            "status_label": _state["step"],
            "log"         : _state["log"][-20:],
            "summary"     : _state["summary"],
            "done"        : status in ("done", "error"),
            "error"       : _state["step"] if status == "error" else None,
            "counts"      : counts
        })


@app.route("/results", methods=["GET"])
def results():
    with _lock:
        tables = []
        for tbl, counts in _state["results"].items():
            src = counts.get("source")
            tgt = counts.get("target")
            var = (src - tgt) if src is not None and tgt is not None else None
            tables.append({
                "table"      : tbl,
                "sourceCount": src,
                "targetCount": tgt,
                "variance"   : var,
                "status"     : ("✔ Match" if var == 0 else "✘ Mismatch" if var is not None else "⚠ Pending")
            })
        matched    = sum(1 for t in tables if t["status"] == "✔ Match")
        mismatched = sum(1 for t in tables if t["status"] == "✘ Mismatch")
        return jsonify({
            "generated": datetime.now().isoformat(),
            "summary"  : {
                "total"     : len(tables),
                "matched"   : matched,
                "mismatched": mismatched,
                "missing"   : len(tables) - matched - mismatched,
                "matchPct"  : round((matched / len(tables)) * 100, 1) if tables else 0
            },
            "tables": tables
        })


@app.route("/reset", methods=["POST"])
def reset():
    with _lock:
        _state.update({"status":"idle","step":"","progress":0,"log":[],"tables":[],"results":{},"summary":{}})
    return jsonify({"ok": True})


@app.route("/config", methods=["GET", "POST"])
def config():
    """Passthrough config endpoint (used by dashboard Automation panel)."""
    return jsonify({"ok": True})


# ── START ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    log.info("=" * 64)
    log.info("  🤖 SAP Bridge API v2.0  —  http://localhost:5001")
    log.info("  SE16N-style table count extraction")
    log.info("  Endpoints:")
    log.info("    POST /upload_ref     — upload Reference List Excel")
    log.info("    POST /connect_sap    — start Source or Target extraction")
    log.info("    GET  /progress       — live progress polling")
    log.info("    GET  /results        — full results JSON")
    log.info("    GET  /export_excel   — download Source+Target Excel")
    log.info("    POST /reset          — clear state")
    log.info("=" * 64)
    app.run(host="127.0.0.1", port=5001, debug=False, threaded=True)
