"""
================================================================================
  TARGET SYSTEM COUNT EXTRACTOR
  Script 2 of 3 — Global Data Migration Automation Framework

  Purpose : Connects to the target database (DB2 / Oracle / SQL Server / HANA)
            and pulls SELECT COUNT(*) for every table in the Reference List.
            Writes the counts into the "Target Count" column.

  Requires: pip install pandas openpyxl pyodbc cx_Oracle ibm_db sqlalchemy
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
        logging.FileHandler("automation/logs/target_count.log", mode="a")
    ]
)
log = logging.getLogger(__name__)

# ══════════════════════════════════════════════════════════════════════════════
#  ▶ CONFIGURE THESE SETTINGS BEFORE RUNNING
# ══════════════════════════════════════════════════════════════════════════════

# Target database type — choose one: "sqlserver" | "oracle" | "db2" | "hana" | "postgresql"
TARGET_DB_TYPE = "sqlserver"

# SQL Server config
SQLSERVER_CONFIG = {
    "server"  : "YOUR_TARGET_SERVER",   # e.g. "192.168.1.100" or "myserver.company.com"
    "database": "YOUR_DATABASE",        # e.g. "SAP_TARGET"
    "username": "YOUR_USERNAME",
    "password": "YOUR_PASSWORD",
    "driver"  : "ODBC Driver 17 for SQL Server",  # or "SQL Server"
}

# Oracle config
ORACLE_CONFIG = {
    "host"    : "YOUR_ORACLE_HOST",
    "port"    : 1521,
    "service" : "YOUR_SERVICE_NAME",    # e.g. "ORCL"
    "username": "YOUR_USERNAME",
    "password": "YOUR_PASSWORD",
}

# IBM DB2 config
DB2_CONFIG = {
    "database": "YOUR_DB2_DATABASE",
    "hostname": "YOUR_DB2_HOST",
    "port"    : 50000,
    "username": "YOUR_USERNAME",
    "password": "YOUR_PASSWORD",
}

# SAP HANA config
HANA_CONFIG = {
    "address" : "YOUR_HANA_HOST",
    "port"    : 30015,
    "user"    : "YOUR_USERNAME",
    "password": "YOUR_PASSWORD",
}

# PostgreSQL config
PG_CONFIG = {
    "host"    : "YOUR_PG_HOST",
    "port"    : 5432,
    "database": "YOUR_DATABASE",
    "user"    : "YOUR_USERNAME",
    "password": "YOUR_PASSWORD",
}

# Reference List Excel file path
REF_FILE = r"C:\Migration\Reference_List.xlsx"

# Sheet and column names
SHEET_NAME        = "Sheet1"
TABLE_NAME_COL    = "Table Name"
TARGET_COUNT_COL  = "Target Count"

# Optional: target schema/owner prefix (e.g. "SAPSR3." or "dbo.")
TARGET_SCHEMA     = ""   # leave empty if not needed
# ══════════════════════════════════════════════════════════════════════════════


def connect_target():
    """Connect to the target database based on TARGET_DB_TYPE."""
    log.info("Connecting to target %s database...", TARGET_DB_TYPE.upper())
    try:
        if TARGET_DB_TYPE == "sqlserver":
            return _connect_sqlserver()
        elif TARGET_DB_TYPE == "oracle":
            return _connect_oracle()
        elif TARGET_DB_TYPE == "db2":
            return _connect_db2()
        elif TARGET_DB_TYPE == "hana":
            return _connect_hana()
        elif TARGET_DB_TYPE == "postgresql":
            return _connect_postgresql()
        else:
            log.error("Unknown DB type: %s", TARGET_DB_TYPE)
            sys.exit(1)
    except Exception as e:
        log.error("✘ Target DB connection failed: %s", e)
        sys.exit(1)


def _connect_sqlserver():
    import pyodbc
    c = SQLSERVER_CONFIG
    conn_str = (
        f"DRIVER={{{c['driver']}}};"
        f"SERVER={c['server']};"
        f"DATABASE={c['database']};"
        f"UID={c['username']};"
        f"PWD={c['password']}"
    )
    conn = pyodbc.connect(conn_str)
    log.info("✔ SQL Server connected: %s / %s", c["server"], c["database"])
    return conn


def _connect_oracle():
    import cx_Oracle
    c = ORACLE_CONFIG
    dsn = cx_Oracle.makedsn(c["host"], c["port"], service_name=c["service"])
    conn = cx_Oracle.connect(c["username"], c["password"], dsn)
    log.info("✔ Oracle connected: %s:%s/%s", c["host"], c["port"], c["service"])
    return conn


def _connect_db2():
    import ibm_db
    import ibm_db_dbi
    c = DB2_CONFIG
    conn_str = (
        f"DATABASE={c['database']};"
        f"HOSTNAME={c['hostname']};"
        f"PORT={c['port']};"
        f"PROTOCOL=TCPIP;"
        f"UID={c['username']};"
        f"PWD={c['password']};"
    )
    ibm_conn = ibm_db.connect(conn_str, "", "")
    conn = ibm_db_dbi.Connection(ibm_conn)
    log.info("✔ DB2 connected: %s / %s", c["hostname"], c["database"])
    return conn


def _connect_hana():
    from hdbcli import dbapi
    c = HANA_CONFIG
    conn = dbapi.connect(address=c["address"], port=c["port"], user=c["user"], password=c["password"])
    log.info("✔ SAP HANA connected: %s:%s", c["address"], c["port"])
    return conn


def _connect_postgresql():
    import psycopg2
    c = PG_CONFIG
    conn = psycopg2.connect(host=c["host"], port=c["port"], database=c["database"], user=c["user"], password=c["password"])
    log.info("✔ PostgreSQL connected: %s / %s", c["host"], c["database"])
    return conn


def get_table_count(conn, table_name):
    """Run SELECT COUNT(*) on target table. Returns int or None."""
    full_table = f"{TARGET_SCHEMA}{table_name.strip().upper()}" if TARGET_SCHEMA else table_name.strip().upper()
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {full_table}")
        row = cursor.fetchone()
        cursor.close()
        return int(row[0]) if row else None
    except Exception as e:
        log.warning("  ⚠ COUNT failed for %s: %s", table_name, str(e)[:80])
        return None


def run_target_extraction():
    """Main extraction function."""
    log.info("=" * 70)
    log.info("  TARGET COUNT EXTRACTION — Started %s", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    log.info("  Target DB Type: %s", TARGET_DB_TYPE.upper())
    log.info("=" * 70)

    # ── 1. Read Reference List ──────────────────────────────────────────────
    if not Path(REF_FILE).exists():
        log.error("✘ Reference file not found: %s", REF_FILE)
        sys.exit(1)

    log.info("Reading reference list: %s", REF_FILE)
    df = pd.read_excel(REF_FILE, sheet_name=SHEET_NAME)
    log.info("  → %d tables found.", len(df))

    if TABLE_NAME_COL not in df.columns:
        log.error("✘ Column '%s' not found. Available: %s", TABLE_NAME_COL, list(df.columns))
        sys.exit(1)

    if TARGET_COUNT_COL not in df.columns:
        df[TARGET_COUNT_COL] = None

    # ── 2. Connect to target DB ─────────────────────────────────────────────
    conn = connect_target()

    # ── 3. Count each table ─────────────────────────────────────────────────
    results = {}
    total   = len(df)
    ok      = 0
    failed  = []

    for idx, row in df.iterrows():
        table = str(row[TABLE_NAME_COL]).strip()
        if not table or table.lower() in ("nan", ""):
            continue

        log.info("  [%d/%d] Counting: %s", idx + 1, total, table)
        count = get_table_count(conn, table)

        if count is not None:
            df.at[idx, TARGET_COUNT_COL] = count
            results[table] = count
            ok += 1
            log.info("    ✔ %s = %s rows", table, f"{count:,}")
        else:
            failed.append(table)

    # ── 4. Close connection ─────────────────────────────────────────────────
    try:
        conn.close()
        log.info("Target DB connection closed.")
    except Exception:
        pass

    # ── 5. Save updated Excel ───────────────────────────────────────────────
    output_file = REF_FILE.replace(".xlsx", f"_target_updated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
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

    # ── 7. Write JSON for dashboard ─────────────────────────────────────────
    write_dashboard_json(results, "target", output_file)

    return output_file


def write_dashboard_json(results, source_type, output_file):
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
    run_target_extraction()
