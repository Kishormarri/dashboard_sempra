"""
================================================================================
  SAP SOURCE COUNT EXTRACTOR
  Script 1 of 3 — Global Data Migration Automation Framework
  
  Purpose : Connects to SAP source system via RFC and pulls SELECT COUNT(*)
            for every table listed in the Reference List Excel file.
            Writes the counts back into the "Source Count" column.

  Requires: pip install pyrfc openpyxl pandas
================================================================================
"""

import sys
import os
import logging
import pandas as pd
from datetime import datetime
from pathlib import Path

# ── LOGGING ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  [%(levelname)s]  %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("automation/logs/sap_source_count.log", mode="a")
    ]
)
log = logging.getLogger(__name__)

# ══════════════════════════════════════════════════════════════════════════════
#  ▶ CONFIGURE THESE SETTINGS BEFORE RUNNING
# ══════════════════════════════════════════════════════════════════════════════
SAP_CONFIG = {
    "ashost"  : "YOUR_SAP_HOST",        # SAP server hostname or IP
    "sysnr"   : "00",                   # System number (e.g. "00", "01")
    "client"  : "100",                  # SAP client (e.g. "100", "200")
    "user"    : "YOUR_SAP_USER",        # SAP username
    "passwd"  : "YOUR_SAP_PASSWORD",    # SAP password
    "lang"    : "EN",                   # Language
}

# Reference List Excel file path
REF_FILE = r"C:\Migration\Reference_List.xlsx"

# Sheet and column names in your Reference List
SHEET_NAME        = "Sheet1"           # Excel sheet name
TABLE_NAME_COL    = "Table Name"       # Column with SAP table names
SOURCE_COUNT_COL  = "Source Count"     # Column to write source counts into
# ══════════════════════════════════════════════════════════════════════════════


def connect_sap():
    """Establish SAP RFC connection."""
    try:
        import pyrfc
        log.info("Connecting to SAP system: %s (client %s)...", SAP_CONFIG["ashost"], SAP_CONFIG["client"])
        conn = pyrfc.Connection(**SAP_CONFIG)
        log.info("✔ SAP connection established.")
        return conn
    except ImportError:
        log.error("pyrfc not installed. Run: pip install pyrfc")
        sys.exit(1)
    except Exception as e:
        log.error("✘ SAP connection failed: %s", e)
        sys.exit(1)


def get_table_count_rfc(conn, table_name):
    """
    Get row count for a SAP table using RFC_READ_TABLE.
    Returns count as integer, or None on error.
    """
    try:
        result = conn.call(
            "RFC_READ_TABLE",
            QUERY_TABLE = table_name.strip().upper(),
            FIELDS      = [{"FIELDNAME": "MANDT"}] if True else [],   # minimal field
            OPTIONS     = [{"TEXT": "ROWNUM = 1"}],                    # dummy filter
            ROWCOUNT    = 0
        )
        # RFC_READ_TABLE doesn't return count directly — use SELECT COUNT via ABAP
        # Alternative: use custom ABAP function or ZFM_GET_TABLE_COUNT (see below)
        return None  # placeholder — replaced by get_table_count_abap()
    except Exception:
        return None


def get_table_count_abap(conn, table_name):
    """
    Get row count using standard RFC_READ_TABLE with COUNT trick.
    For production, replace with a custom ABAP function module
    ZFM_GET_TABLE_COUNT that runs SELECT COUNT(*) FROM <table>.
    """
    try:
        # Method 1: Use custom ABAP FM (recommended for large tables)
        # result = conn.call("ZFM_GET_TABLE_COUNT", TABLE_NAME=table_name)
        # return int(result["ROW_COUNT"])

        # Method 2: RFC_READ_TABLE to count rows (works for small/medium tables)
        result = conn.call(
            "RFC_READ_TABLE",
            QUERY_TABLE = table_name.strip().upper(),
            ROWCOUNT    = 0,         # 0 = all rows
            FIELDS      = [],
            OPTIONS     = []
        )
        count = len(result.get("DATA", []))
        return count

    except Exception as e:
        log.warning("  ⚠ Could not count %s: %s", table_name, str(e)[:80])
        return None


def get_table_count_se16n(conn, table_name):
    """
    Alternative: Use SUSR_USER_AUTH_FOR_OBJ / SE16N-style count via RFC.
    Use this when RFC_READ_TABLE is restricted.
    """
    try:
        result = conn.call(
            "SCMS_STRING_TO_XSTRING",   # placeholder — swap with your allowed FM
        )
    except Exception:
        return None


def run_sap_extraction():
    """Main extraction function."""
    log.info("=" * 70)
    log.info("  SAP SOURCE COUNT EXTRACTION — Started %s", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    log.info("=" * 70)

    # ── 1. Read Reference List ──────────────────────────────────────────────
    if not Path(REF_FILE).exists():
        log.error("✘ Reference file not found: %s", REF_FILE)
        sys.exit(1)

    log.info("Reading reference list: %s", REF_FILE)
    df = pd.read_excel(REF_FILE, sheet_name=SHEET_NAME)
    log.info("  → %d tables found in reference list.", len(df))

    if TABLE_NAME_COL not in df.columns:
        log.error("✘ Column '%s' not found. Available: %s", TABLE_NAME_COL, list(df.columns))
        sys.exit(1)

    # Ensure source count column exists
    if SOURCE_COUNT_COL not in df.columns:
        df[SOURCE_COUNT_COL] = None

    # ── 2. Connect to SAP ───────────────────────────────────────────────────
    conn = connect_sap()

    # ── 3. Loop through tables ──────────────────────────────────────────────
    results = {}
    total   = len(df)
    ok      = 0
    failed  = []

    for idx, row in df.iterrows():
        table = str(row[TABLE_NAME_COL]).strip()
        if not table or table.lower() in ("nan", ""):
            continue

        log.info("  [%d/%d] Counting: %s", idx + 1, total, table)
        count = get_table_count_abap(conn, table)

        if count is not None:
            df.at[idx, SOURCE_COUNT_COL] = count
            results[table] = count
            ok += 1
            log.info("    ✔ %s = %s rows", table, f"{count:,}")
        else:
            failed.append(table)
            log.warning("    ✘ %s — count failed", table)

    # ── 4. Close SAP connection ─────────────────────────────────────────────
    try:
        conn.close()
        log.info("SAP connection closed.")
    except Exception:
        pass

    # ── 5. Write back to Excel ──────────────────────────────────────────────
    output_file = REF_FILE.replace(".xlsx", f"_source_updated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
    df.to_excel(output_file, sheet_name=SHEET_NAME, index=False)
    log.info("✔ Updated file saved: %s", output_file)

    # ── 6. Summary ──────────────────────────────────────────────────────────
    log.info("")
    log.info("=" * 70)
    log.info("  SUMMARY")
    log.info("  Total tables  : %d", total)
    log.info("  ✔ Counted OK  : %d", ok)
    log.info("  ✘ Failed      : %d", len(failed))
    if failed:
        log.info("  Failed tables : %s", ", ".join(failed[:20]))
    log.info("  Output file   : %s", output_file)
    log.info("=" * 70)

    # ── 7. Write JSON summary for dashboard ────────────────────────────────
    write_dashboard_json(results, "source", output_file)

    return output_file


def write_dashboard_json(results, source_type, output_file):
    """Write a JSON file that the dashboard can load to auto-update counts."""
    import json
    summary = {
        "type"       : source_type,
        "timestamp"  : datetime.now().isoformat(),
        "output_file": output_file,
        "table_count": len(results),
        "tables"     : results
    }
    json_path = f"automation/output/{source_type}_counts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    os.makedirs("automation/output", exist_ok=True)
    with open(json_path, "w") as f:
        json.dump(summary, f, indent=2)
    log.info("Dashboard JSON written: %s", json_path)


if __name__ == "__main__":
    os.makedirs("automation/logs", exist_ok=True)
    run_sap_extraction()
