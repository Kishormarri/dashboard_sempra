"""
================================================================================
  ORCHESTRATOR — MASTER RUNNER
  Script 3 of 3 — Global Data Migration Automation Framework

  Purpose : Runs both SAP source extraction and target DB extraction,
            then merges results into a single Reference List Excel file
            with both Source Count and Target Count columns populated.
            Also generates a dashboard-ready JSON file.

  Usage   : python 03_orchestrator.py [--source-only] [--target-only] [--schedule]
================================================================================
"""

import sys
import os
import json
import logging
import argparse
import pandas as pd
from datetime import datetime
from pathlib import Path

# ── LOGGING ──────────────────────────────────────────────────────────────────
os.makedirs("automation/logs",   exist_ok=True)
os.makedirs("automation/output", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  [%(levelname)s]  %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("automation/logs/orchestrator.log", mode="a")
    ]
)
log = logging.getLogger(__name__)

# ══════════════════════════════════════════════════════════════════════════════
#  ▶ MASTER CONFIGURATION — Edit once, run everywhere
# ══════════════════════════════════════════════════════════════════════════════
CONFIG = {
    # ── Input Reference List ──────────────────────────────────────────────
    "ref_file"          : r"C:\Migration\Reference_List.xlsx",
    "sheet_name"        : "Sheet1",
    "table_name_col"    : "Table Name",
    "source_count_col"  : "Source Count",
    "target_count_col"  : "Target Count",

    # ── Output ────────────────────────────────────────────────────────────
    "output_dir"        : r"C:\Migration\Output",
    "dashboard_json"    : r"C:\Migration\Output\dashboard_ref_counts.json",

    # ── Schedule (used with --schedule flag) ──────────────────────────────
    "schedule_interval_minutes" : 60,   # run every 60 minutes

    # ── Notifications ─────────────────────────────────────────────────────
    "email_on_complete" : False,
    "email_to"          : "your.email@company.com",
    "email_from"        : "automation@company.com",
    "smtp_server"       : "smtp.company.com",
    "smtp_port"         : 587,
}
# ══════════════════════════════════════════════════════════════════════════════


def print_banner():
    log.info("")
    log.info("╔══════════════════════════════════════════════════════════════════╗")
    log.info("║   🤖  GLOBAL DATA MIGRATION AUTOMATION FRAMEWORK                ║")
    log.info("║   Reference List Count Extractor — SAP Source + Target DB       ║")
    log.info("║   Started: %-52s  ║", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    log.info("╚══════════════════════════════════════════════════════════════════╝")
    log.info("")


def run_source_extraction():
    """Import and run SAP source count script."""
    log.info("▶ STEP 1: Running SAP Source Count Extraction...")
    try:
        sys.path.insert(0, os.path.dirname(__file__))
        import importlib.util
        spec = importlib.util.spec_from_file_location("sap_source", "automation/01_sap_source_count.py")
        mod  = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        output_file = mod.run_sap_extraction()
        log.info("✔ SAP source extraction complete: %s", output_file)
        return output_file
    except Exception as e:
        log.error("✘ SAP source extraction failed: %s", e)
        return None


def run_target_extraction():
    """Import and run target DB count script."""
    log.info("▶ STEP 2: Running Target DB Count Extraction...")
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("target_count", "automation/02_target_count.py")
        mod  = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        output_file = mod.run_target_extraction()
        log.info("✔ Target extraction complete: %s", output_file)
        return output_file
    except Exception as e:
        log.error("✘ Target extraction failed: %s", e)
        return None


def merge_and_save(source_file, target_file):
    """Merge source and target counts into one final Reference List."""
    log.info("▶ STEP 3: Merging Source + Target counts...")

    cfg = CONFIG
    ref_file = cfg["ref_file"]

    # Load original reference list
    df_ref = pd.read_excel(ref_file, sheet_name=cfg["sheet_name"])

    # Load source counts if available
    if source_file and Path(source_file).exists():
        df_src = pd.read_excel(source_file, sheet_name=cfg["sheet_name"])
        if cfg["source_count_col"] in df_src.columns:
            df_ref[cfg["source_count_col"]] = df_src[cfg["source_count_col"]].values
            log.info("  ✔ Source counts merged.")

    # Load target counts if available
    if target_file and Path(target_file).exists():
        df_tgt = pd.read_excel(target_file, sheet_name=cfg["sheet_name"])
        if cfg["target_count_col"] in df_tgt.columns:
            df_ref[cfg["target_count_col"]] = df_tgt[cfg["target_count_col"]].values
            log.info("  ✔ Target counts merged.")

    # Compute variance column
    if cfg["source_count_col"] in df_ref.columns and cfg["target_count_col"] in df_ref.columns:
        df_ref["Variance (Src-Tgt)"] = pd.to_numeric(df_ref[cfg["source_count_col"]], errors="coerce") \
                                      - pd.to_numeric(df_ref[cfg["target_count_col"]], errors="coerce")
        df_ref["Match Status"] = df_ref["Variance (Src-Tgt)"].apply(
            lambda v: "✔ Match" if v == 0 else ("✘ Mismatch" if pd.notna(v) else "⚠ Missing")
        )

    # Save final merged file
    os.makedirs(cfg["output_dir"], exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    final_file = os.path.join(cfg["output_dir"], f"Reference_List_FINAL_{ts}.xlsx")
    df_ref.to_excel(final_file, sheet_name=cfg["sheet_name"], index=False)
    log.info("  ✔ Final merged file saved: %s", final_file)

    return df_ref, final_file


def write_dashboard_json(df, final_file):
    """
    Write a dashboard-ready JSON file that the HTML dashboard can load
    to auto-populate Source Count and Target Count columns.
    """
    log.info("▶ STEP 4: Writing dashboard JSON...")

    cfg = CONFIG
    records = []

    for _, row in df.iterrows():
        table = str(row.get(cfg["table_name_col"], "")).strip()
        if not table or table.lower() == "nan":
            continue
        records.append({
            "table"       : table,
            "sourceCount" : int(row[cfg["source_count_col"]]) if pd.notna(row.get(cfg["source_count_col"])) else None,
            "targetCount" : int(row[cfg["target_count_col"]]) if pd.notna(row.get(cfg["target_count_col"])) else None,
            "variance"    : int(row["Variance (Src-Tgt)"]) if "Variance (Src-Tgt)" in row and pd.notna(row["Variance (Src-Tgt)"]) else None,
            "status"      : str(row.get("Match Status", ""))
        })

    matched   = sum(1 for r in records if r["status"] == "✔ Match")
    mismatched= sum(1 for r in records if r["status"] == "✘ Mismatch")
    missing   = sum(1 for r in records if r["status"] == "⚠ Missing")

    payload = {
        "generated"  : datetime.now().isoformat(),
        "source_file": final_file,
        "summary"    : {
            "total"     : len(records),
            "matched"   : matched,
            "mismatched": mismatched,
            "missing"   : missing,
            "matchPct"  : round((matched / len(records)) * 100, 1) if records else 0
        },
        "tables": records
    }

    json_path = cfg["dashboard_json"]
    with open(json_path, "w") as f:
        json.dump(payload, f, indent=2)

    log.info("  ✔ Dashboard JSON written: %s", json_path)
    log.info("  ✔ Total: %d | Match: %d | Mismatch: %d | Missing: %d",
             len(records), matched, mismatched, missing)
    return json_path


def send_email_notification(final_file, json_path):
    """Optional: send email notification on completion."""
    if not CONFIG["email_on_complete"]:
        return
    try:
        import smtplib
        from email.mime.text import MIMEText
        msg = MIMEText(f"✔ Automation complete.\nFile: {final_file}\nJSON: {json_path}")
        msg["Subject"] = "✔ Migration Count Automation Complete"
        msg["From"]    = CONFIG["email_from"]
        msg["To"]      = CONFIG["email_to"]
        with smtplib.SMTP(CONFIG["smtp_server"], CONFIG["smtp_port"]) as s:
            s.starttls()
            s.send_message(msg)
        log.info("✔ Email notification sent to %s", CONFIG["email_to"])
    except Exception as e:
        log.warning("Email notification failed: %s", e)


def run_scheduled():
    """Run on a schedule using the schedule library."""
    try:
        import schedule
        import time
        interval = CONFIG["schedule_interval_minutes"]
        log.info("⏰ Scheduled mode: running every %d minutes.", interval)
        schedule.every(interval).minutes.do(run_all)
        run_all()   # run immediately on start
        while True:
            schedule.run_pending()
            time.sleep(30)
    except ImportError:
        log.error("schedule library not installed. Run: pip install schedule")
        sys.exit(1)


def run_all(source_only=False, target_only=False):
    """Run full extraction pipeline."""
    print_banner()
    source_file = None
    target_file = None

    if not target_only:
        source_file = run_source_extraction()
    if not source_only:
        target_file = run_target_extraction()

    df, final_file = merge_and_save(source_file, target_file)
    json_path = write_dashboard_json(df, final_file)
    send_email_notification(final_file, json_path)

    log.info("")
    log.info("╔══════════════════════════════════════════════════════════════════╗")
    log.info("║  ✅  AUTOMATION COMPLETE                                         ║")
    log.info("║  Final file : %-51s  ║", Path(final_file).name)
    log.info("║  JSON file  : %-51s  ║", Path(json_path).name)
    log.info("╚══════════════════════════════════════════════════════════════════╝")
    log.info("")
    return final_file, json_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Migration Count Orchestrator")
    parser.add_argument("--source-only", action="store_true", help="Run SAP source extraction only")
    parser.add_argument("--target-only", action="store_true", help="Run target DB extraction only")
    parser.add_argument("--schedule",    action="store_true", help="Run on a schedule (every N minutes)")
    args = parser.parse_args()

    if args.schedule:
        run_scheduled()
    else:
        run_all(source_only=args.source_only, target_only=args.target_only)
