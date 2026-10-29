"""
================================================================================
  Sempra DM Dashboard — Documentation Generator
  Produces:
    1. Sempra_DM_Dashboard_Documentation.docx  (Word)
    2. Sempra_DM_Dashboard_Documentation.pdf   (PDF via fpdf2)
  Run: python generate_docs.py
================================================================================
"""

import os
from datetime import datetime

OUT_DOCX = "Sempra_DM_Dashboard_Documentation.docx"
OUT_PDF  = "Sempra_DM_Dashboard_Documentation.pdf"

# ─────────────────────────────────────────────────────────────────────────────
# SHARED CONTENT STRUCTURE
# ─────────────────────────────────────────────────────────────────────────────
SECTIONS = [
    {
        "num": "01",
        "title": "Executive Summary",
        "subtitle": "Business value and purpose — for leadership audiences",
        "colour": "BIZ",
        "content": [
            ("plain", "GREEN", "In Plain English",
             "This dashboard is Sempra's single source of truth for SAP data migration health. "
             "It automatically reads migration data files, counts how many SAP tables were "
             "successfully moved from the old system to the new one, and shows a live "
             "reconciliation score — all in real time, with no manual effort beyond clicking one button."),
            ("kpis", [
                ("3",      "Migration Cycles",  "DM1 → DM2 → DM3"),
                ("5",      "Source Files",       "Auto-read from disk"),
                ("100%",   "Local Processing",   "Zero cloud dependency"),
                ("<10s",   "Full Sync Time",      "All 3 cycles at once"),
                ("2 min",  "Auto-Refresh",        "Always current"),
                ("0",      "Manual Steps",        "Fully automated"),
            ]),
            ("plain", "BLUE", "What Leadership Needs to Know",
             "• The dashboard replaces hours of manual Excel reconciliation with a single button click.\n"
             "• It covers all three migration waves (DM1, DM2, DM3) on one screen, with per-cycle drill-down.\n"
             "• Data never leaves the Sempra laptop — processed entirely in the browser.\n"
             "• No licences, no cloud subscriptions, no third-party costs for core functionality.\n"
             "• Mismatches, missing exports, and incomplete migrations are flagged automatically."),
        ],
    },
    {
        "num": "02",
        "title": "What Problem It Solves",
        "subtitle": "The Before vs After",
        "colour": "BIZ",
        "content": [
            ("compare",
             ("BEFORE — Manual Process",
              "Migration teams manually opened multiple Excel files, cross-referenced them by hand, "
              "and produced status reports that were already out of date before they were finished. "
              "Double-counting of records inflated match numbers. No single view existed across all three cycles."),
             ("AFTER — This Dashboard",
              "One click reads all five source files, deduplicates records using a DISTINCT algorithm, "
              "calculates reconciliation percentages for all three cycles in parallel, and displays live "
              "colour-coded health indicators — auto-refreshing every 2 minutes.")),
            ("table",
             ["Aspect", "Manual Approach (Before)", "This Dashboard (After)"],
             [
                 ["Time to reconcile",     "30–60 minutes per cycle",                      "Under 10 seconds — all 3 cycles"],
                 ["Accuracy",              "Prone to double-counting & formula errors",    "DISTINCT dedup algorithm — always correct"],
                 ["Coverage",              "One cycle at a time",                          "All 3 cycles simultaneously"],
                 ["Data freshness",        "Updated only when someone runs it manually",   "Auto-refreshes every 2 minutes"],
                 ["Flagging issues",       "Manual — easy to miss",                        "Automatic colour-coded health indicators"],
                 ["Leadership visibility", "Email attachments or verbal updates",           "Live dashboard, printable, PDF-ready"],
                 ["SAP source counts",     "Manual SE16N queries per table",               "Automated via SE16N-style RFC, 3 fallbacks"],
                 ["Data security",         "Files emailed between team members",           "Never leaves the local machine"],
             ]),
        ],
    },
    {
        "num": "03",
        "title": "The Three Migration Cycles",
        "subtitle": "DM1 / DM2 / DM3 — what each wave covers",
        "colour": "BIZ",
        "content": [
            ("plain", "BLUE", "Context",
             "Sempra's SAP migration runs in three progressive waves. Each wave moves a batch of SAP "
             "tables from the source system (ES2) to the target system (SQ1). The dashboard tracks "
             "each wave independently and shows a cross-cycle comparison on the master screen."),
            ("cycle_cards", [
                ("DM1 — Cycle 1", "Wave 1", "DM1 BLUE",
                 "First migration wave. Reference List: Reflist_m1.xlsx plus Export/Import file: "
                 "DM1_ES2-SQ1 Export-Import.xlsx. Both EXP and IMP data available — full reconciliation possible."),
                ("DM2 — Cycle 2", "Wave 2", "DM2 PURPLE",
                 "Second migration wave. Uses DM2 REF.xlsx and EXPORT IMPORT_DM2.xlsx. "
                 "Same full reconciliation structure as DM1 — all EXP and IMP data present."),
                ("DM3 — Cycle 3", "Wave 3", "DM3 GREEN",
                 "Third wave — currently in progress. Only ref dm3.xlsx available; "
                 "it contains both export and import rows in combined format. "
                 "Dashboard shows amber 'Migration In Progress' banner automatically."),
            ]),
            ("table",
             ["Cycle", "Brand Colour", "Reference File", "EXP/IMP File", "Status"],
             [
                 ["DM1", "Blue",   "Reflist_m1.xlsx",    "DM1_ES2-SQ1 Export-Import.xlsx", "Full data — reconcilable"],
                 ["DM2", "Purple", "DM2 REF.xlsx",       "EXPORT IMPORT_DM2.xlsx",         "Full data — reconcilable"],
                 ["DM3", "Green",  "ref dm3.xlsx",       "Combined in REF file",            "In progress — REF only"],
             ]),
        ],
    },
    {
        "num": "04",
        "title": "Step-by-Step User Guide",
        "subtitle": "How to launch and use the dashboard — no technical knowledge required",
        "colour": "STEPS",
        "content": [
            ("plain", "AMBER", "Prerequisites",
             "Ensure data files are in: C:\\Users\\KishorMarri\\.bob\\DM1\\, DM2\\ and DM3\\\n"
             "Python 3.8+ must be installed.\n"
             "Run once: pip install flask flask-cors openpyxl pandas xlrd"),
            ("steps", [
                ("1", "Launch the Dashboard",
                 "Open PowerShell in the project folder and run:\n  python launch_dashboard.py\n\n"
                 "This starts two background services and opens the master dashboard automatically at:\n"
                 "http://localhost:5003/Sempra_CrossCycle_Summary_MASTER.html\n\n"
                 "TIP: A new PowerShell window opens for the File Bridge — leave it running. "
                 "The browser opens automatically in ~5 seconds."),
                ("2", "Run Full 3-Cycle Automation",
                 "Click the ⚡ Auto-Sync All Cycles button in the top toolbar.\n"
                 "The button animates with a rainbow sweep while running.\n"
                 "Three coloured sync circles appear (blue/purple/green) — one per cycle — "
                 "spinning while reading and showing match % when done.\n\n"
                 "TIP: The full sync completes in under 10 seconds."),
                ("3", "Read the Results on Screen",
                 "Each cycle card shows:\n"
                 "• A large semicircle gauge — the reconciliation match %\n"
                 "• Total tables in scope vs tables fully reconciled\n"
                 "• Mismatched, not-exported, and not-imported counts\n"
                 "• A badge box: green border = healthy, red border = issues found\n\n"
                 "The cross-cycle comparison table lets you compare DM1, DM2, and DM3 side by side."),
                ("4", "Switch Views: Business / Technical / Performance",
                 "Three tabs at the top switch the dashboard:\n"
                 "• Business View — RAG scorecards and insight boxes for leadership\n"
                 "• Technical View — per-table detail with source/target counts and variance\n"
                 "• Performance View — timing metrics, file sizes, cache hit rates\n\n"
                 "TIP: Business View is best for leadership presentations and printed reports."),
                ("5", "Drill Down to Individual Cycle Dashboards",
                 "Click DM1 / DM2 / DM3 navigation buttons to open that cycle's detail page:\n"
                 "• Upload new Excel files via drag-and-drop\n"
                 "• See a searchable per-table breakdown with EXP/IMP record counts\n"
                 "• Download filtered sub-sets (mismatches only, etc.) as CSV or Excel\n\n"
                 "TIP: Results are saved in localStorage — persist across page reloads."),
                ("6", "Export Reports & Prints",
                 "Use browser Print (Ctrl+P) → Save as PDF for a leadership-ready document.\n"
                 "The dashboard switches to a clean white background with all colours preserved.\n\n"
                 "For Excel exports with SAP SE16N source counts, use the\n"
                 "📥 Download SE16N Counts button in the Automation panel (Step 4)."),
            ]),
        ],
    },
    {
        "num": "05",
        "title": "Colour & Status Key",
        "subtitle": "What every colour and indicator means — consistent across all screens",
        "colour": "NONE",
        "content": [
            ("plain", "BLUE", "Universal Colour Conventions",
             "These colours are used consistently across every screen, table, badge, and indicator "
             "in the dashboard. Learn them once — read any view instantly."),
            ("colour_key", [
                ("GREEN",  "Green — Fully Reconciled",      "Source = Target AND EXP = IMP. Table migrated successfully."),
                ("AMBER",  "Amber — In Progress / Warning", "Source ≠ Target, or migration not yet complete. Needs monitoring."),
                ("RED",    "Red — Mismatch / Failed",       "EXP ≠ IMP record count, or table not migrated. Action required."),
                ("GREY",   "Grey — No Data / Excluded",     "Table in Reference List but no export/import data found yet."),
                ("BLUE",   "Blue — DM1 Cycle 1",            "All DM1 labels, borders, badges, and navigation elements."),
                ("PURPLE", "Purple — DM2 Cycle 2",          "All DM2 labels, borders, badges, and navigation elements."),
            ]),
            ("table",
             ["Indicator", "Where It Appears", "What It Means"],
             [
                 ["RAG Badge (Green/Amber/Red)", "Business View scorecards",      "Overall health — Green=on track, Amber=review, Red=critical"],
                 ["Semicircle Gauge",            "Each cycle card (MASTER)",      "Visual match % 0–100. Spins with READING… overlay during sync"],
                 ["Sync Circles (spinning)",     "Refresh toolbar",               "Appear during sync; spin in cycle colour; show % when done; auto-hide after 5s"],
                 ["Badge Box (green/red border)","Below each cycle gauge",        "Post-sync summary — green border =>95% match, red border = issues"],
                 ["Rainbow Button Animation",    "Auto-Sync All Cycles button",   "Sweeping rainbow glow while running — stops when all 3 cycles complete"],
                 ["Amber Migration Banner",      "DM3 dashboard",                 "Shown when only Reference List loaded — EXP/IMP not yet available"],
                 ["Red Dot on Countdown",        "Auto-refresh countdown badge",  "Next refresh within 60 seconds — data about to update automatically"],
             ]),
        ],
    },
    {
        "num": "06",
        "title": "Dashboard Features",
        "subtitle": "Complete feature catalogue — everything the system can do",
        "colour": "BIZ",
        "content": [
            ("table",
             ["Feature", "Where", "Description"],
             [
                 ["3-Cycle Side-by-Side View",       "MASTER dashboard",          "DM1/DM2/DM3 cards on one page with gauge, KPIs, match counts"],
                 ["⚡ Auto-Sync All Cycles",          "Toolbar button",            "One click reads all 5 Excel files, parses in-browser, updates all cards — under 10 seconds"],
                 ["Semicircle Match Gauges",          "Each cycle card",           "Animated SVG arc 0–100%. Spins with READING… overlay during sync"],
                 ["Business/Technical/Perf Tabs",    "MASTER dashboard",          "Switch between executive RAG, per-table detail, system performance views"],
                 ["Business Insights Panel",         "Business View",             "Auto-generated flags: missing exports, mismatches, DM3 status, overall match rate"],
                 ["Auto-Refresh (2-min interval)",   "Toolbar",                   "Countdown badge with pause/resume. Red dot when <60 seconds. Amber when paused"],
                 ["Sync Status Circles",             "Refresh bar",               "Spin per cycle during automation — show match % when done, auto-hide after 5s"],
                 ["Inline Badge Boxes",              "Below each gauge",          "Non-disruptive post-sync summary — no popups, no modal interruptions"],
                 ["Per-Cycle Detail Dashboards",     "DM1/DM2/DM3 pages",        "Drag-and-drop upload, searchable table, KPI strip, rainbow progress bar"],
                 ["DISTINCT Deduplication",          "All 6 aggregation points", "DISTINCT on (Type, Table, Record Count) — prevents double-counting EXP/IMP"],
                 ["Count Validation Column",         "Per-cycle dashboards",     "EXP vs IMP record count difference per table — highlights inconsistencies"],
                 ["Cross-Cycle Comparison Table",    "MASTER — Technical View",  "All tables across DM1/DM2/DM3 with per-cycle source/target/variance columns"],
                 ["Print / PDF Export",              "Browser Ctrl+P",           "Full print CSS — white background, colours preserved, clean leadership output"],
                 ["SE16N SAP Source Counts",         "Automation Panel (opt.)",  "RFC connection to SAP, counts every table — 3 fallback methods"],
                 ["Excel Export (colour-coded)",     "Automation Panel Step 4",  "Source vs Target count XLSX with green/red/amber colouring + Summary sheet"],
                 ["localStorage Persistence",        "All dashboards",           "Results survive page reloads — no need to re-sync if data unchanged"],
                 ["Dynamic Bridge URL",              "All dashboards (JS)",      "Uses window.location.hostname — works on any machine or IP"],
                 ["DM3 REF-Only Mode",               "DM3 dashboard",            "Gracefully handles no separate EXP/IMP file — shows amber migration banner"],
             ]),
        ],
    },
    {
        "num": "07",
        "title": "Technical Architecture",
        "subtitle": "How the system works under the hood — for technical reviewers",
        "colour": "TECH",
        "content": [
            ("plain", "PURPLE", "Architecture Overview",
             "The system is a three-layer local stack: a static HTML/JS browser layer, a lightweight "
             "Python file-serving bridge, and the local file system where Excel data files live. "
             "Nothing is sent to any external server — all calculation happens in the browser using SheetJS."),
            ("code",
             "BROWSER LAYER (HTML + JavaScript + SheetJS v0.18.5)\n"
             "  Sempra_CrossCycle_Summary_MASTER.html  ← Main dashboard, all 3 cycles\n"
             "  Sempra_DM1_Dashboard.html              ← DM1 per-table detail\n"
             "  Sempra_DM2_Dashboard.html              ← DM2 per-table detail\n"
             "  Sempra_DM3_Dashboard.html              ← DM3 per-table detail\n"
             "          |\n"
             "          | fetch(http://localhost:5002/file?cycle=DM1&type=ref)\n"
             "          | gzip-compressed Excel bytes ← ETag 304 caching\n"
             "          v\n"
             "FILE WATCHER BRIDGE  (Python Flask — port 5002)\n"
             "  automation/file_watcher_bridge.py\n"
             "    • In-memory file cache     — no repeated disk reads\n"
             "    • Gzip compression         — 60-70% smaller transfers\n"
             "    • ETag / 304 Not Modified  — skips read if unchanged\n"
             "    • Bulk /files/all endpoint — manifest before bytes\n"
             "          |\n"
             "          | reads raw Excel bytes from disk\n"
             "          v\n"
             "LOCAL FILE SYSTEM\n"
             "  C:\\Users\\KishorMarri\\.bob\\DM1\\Reflist_m1.xlsx\n"
             "  C:\\Users\\KishorMarri\\.bob\\DM1\\DM1_ES2-SQ1 Export-Import.xlsx\n"
             "  C:\\Users\\KishorMarri\\.bob\\DM2\\DM2 REF.xlsx\n"
             "  C:\\Users\\KishorMarri\\.bob\\DM2\\EXPORT IMPORT_DM2.xlsx\n"
             "  C:\\Users\\KishorMarri\\.bob\\DM3\\ref dm3.xlsx\n\n"
             "SAP BRIDGE (Optional — Python Flask — port 5001)\n"
             "  automation/sap_bridge.py\n"
             "    • Method 1: EM_GET_NUMBER_OF_ENTRIES  (SE16N internal FM)\n"
             "    • Method 2: RFC_READ_TABLE            (standard fallback)\n"
             "    • Method 3: BBP_RFC_READ_TABLE        (alternative fallback)\n"
             "    • Demo mode: simulated counts without pyrfc\n"
             "    • /export_excel: colour-coded XLSX + Summary sheet"),
            ("table",
             ["Layer", "Technology", "Port", "Role"],
             [
                 ["Browser Frontend",     "HTML5, Vanilla JS, SheetJS v0.18.5, SVG", "5003 (static)", "Excel parsing, reconciliation, rendering, localStorage"],
                 ["File Bridge",          "Python 3.8+, Flask, Flask-CORS, gzip",    "5002",          "Serves Excel bytes with gzip compression and ETag caching"],
                 ["Static Server",        "Python http.server (built-in)",           "5003",          "Serves HTML over HTTP — avoids CORS issues with file://"],
                 ["SAP Bridge (opt.)",    "Python, Flask, pyrfc, openpyxl",          "5001",          "RFC to SAP for SE16N-style table counts + Excel export"],
                 ["Launcher",             "Python subprocess, threading, webbrowser","—",             "Starts all services and opens the browser automatically"],
             ]),
        ],
    },
    {
        "num": "08",
        "title": "File & Component Inventory",
        "subtitle": "Every file in the project — what it does and when to edit it",
        "colour": "TECH",
        "content": [
            ("table",
             ["File", "Type", "Purpose", "Edit Required?"],
             [
                 ["Sempra_CrossCycle_Summary_MASTER.html", "HTML/JS/CSS", "Main dashboard — 3-cycle cross view, automation, all view tabs",      "Rarely — labels only"],
                 ["Sempra_DM1_Dashboard.html",            "HTML/JS/CSS", "DM1 per-table detail — upload, search, KPI strip, download",          "Rarely"],
                 ["Sempra_DM2_Dashboard.html",            "HTML/JS/CSS", "DM2 per-table detail — same structure as DM1",                        "Rarely"],
                 ["Sempra_DM3_Dashboard.html",            "HTML/JS/CSS", "DM3 detail — REF-only mode with amber migration banner",              "Rarely"],
                 ["launch_dashboard.py",                  "Python",      "One-click launcher — starts bridge + static server + opens browser",  "No changes needed"],
                 ["automation/file_watcher_bridge.py",    "Python/Flask","Local HTTP bridge port 5002 — serves Excel bytes, gzip + ETag",       "Only if file paths change"],
                 ["automation/sap_bridge.py",             "Python/Flask","SAP RFC bridge port 5001 — SE16N counts, Excel export",               "Only if SAP details change"],
                 ["automation/01_sap_source_count.py",    "Python",      "Standalone SAP source count extractor (batch use)",                   "Configuration only"],
                 ["automation/02_target_count.py",        "Python",      "Standalone target system count extractor (batch use)",                "Configuration only"],
                 ["automation/03_orchestrator.py",        "Python",      "Full pipeline orchestrator for scheduled batch runs",                 "Configuration only"],
                 ["automation/output/",                   "Folder",      "Auto-created — stores ref_tables.json, dashboard_ref_counts.json",    "Auto-managed"],
                 ["automation/logs/",                     "Folder",      "Auto-created — bridge.log, file_watcher.log for diagnostics",         "Auto-managed"],
             ]),
        ],
    },
    {
        "num": "09",
        "title": "Data Flow & Deduplication Logic",
        "subtitle": "How records are counted correctly — critical for accuracy",
        "colour": "TECH",
        "content": [
            ("plain", "BLUE", "Why Deduplication Matters",
             "The migration Excel files contain separate rows for each Export and Import operation. "
             "Without deduplication, the same table appears multiple times, inflating counts. "
             "The dashboard uses a DISTINCT algorithm — equivalent to SQL's SELECT DISTINCT — to ensure "
             "each unique (Type, Table Name, Record Count) combination is counted only once before summing. "
             "EXP and IMP rows are processed SEPARATELY to avoid cross-type errors. "
             "This fix was applied to all 6 aggregation points across 4 files."),
            ("code",
             "RECONCILIATION DATA FLOW — STEP BY STEP\n\n"
             "Step 1: FETCH\n"
             "  Browser → GET /file?cycle=DM1&type=ref → bridge returns gzipped .xlsx\n"
             "  Browser → GET /file?cycle=DM1&type=exp → bridge returns gzipped .xlsx\n"
             "  (ETag: if unchanged, 304 Not Modified — zero re-read)\n\n"
             "Step 2: PARSE\n"
             "  SheetJS.read(arrayBuffer) → XLSX workbook in memory (100% browser-side)\n"
             "  sheet_to_json() → array of row objects\n\n"
             "Step 3: DEDUPLICATE\n"
             "  EXP rows: DISTINCT(Type=EXP, TableName, RecordCount) → SUM\n"
             "  IMP rows: DISTINCT(Type=IMP, TableName, RecordCount) → SUM\n"
             "  (EXP and IMP processed SEPARATELY)\n\n"
             "Step 4: RECONCILE\n"
             "  GREEN  if EXP_count == IMP_count AND src_count == tgt_count\n"
             "  AMBER  if counts exist but do not match\n"
             "  RED    if EXP ≠ IMP OR migration not started\n"
             "  GREY   if no EXP/IMP data found for this table\n\n"
             "Step 5: AGGREGATE\n"
             "  Match % = (fully reconciled) / (total in REF list) * 100\n\n"
             "Step 6: RENDER\n"
             "  Update SVG gauge, KPI numbers, badge box, sync circles\n"
             "  Save summary to localStorage for persistence"),
            ("plain", "GREEN", "DM3 Special Case — Combined File",
             "DM3 has no separate EXP/IMP file. The Reference file contains both Export and Import rows "
             "in a combined format. The parser handles this automatically by setting impData = expData. "
             "The same DISTINCT deduplication logic is applied. This is why DM3 shows an amber "
             "'Migration In Progress' banner until a separate EXP/IMP file becomes available."),
        ],
    },
    {
        "num": "10",
        "title": "Security & Data Privacy",
        "subtitle": "No cloud, no external calls — data stays on the Sempra laptop at all times",
        "colour": "ARCH",
        "content": [
            ("plain", "GREEN", "Security Statement",
             "No Sempra data ever leaves the local machine. All Excel files are read from a local "
             "directory, served via a localhost-only Flask server (bound to 127.0.0.1 — not reachable "
             "from the network), parsed entirely in the browser using SheetJS, and results are stored "
             "only in the browser's localStorage. There is no cloud API, no telemetry, no external network calls."),
            ("table",
             ["Risk Vector", "Mitigation in Place"],
             [
                 ["Data leaving the machine",   "All Flask servers bind to 127.0.0.1 only — not accessible from the network"],
                 ["External API calls",         "SheetJS is a one-time JS library fetch from CDN — no data sent. Replaceable with local copy"],
                 ["SAP credentials",            "Entered in-browser only; passed to localhost only; never written to disk"],
                 ["File access control",        "Only config-listed files accessible; no directory traversal possible"],
                 ["Persistent data storage",    "Only reconciliation summary numbers in localStorage — no raw data, no credentials"],
                 ["Network port exposure",      "Ports 5001/5002/5003 all bind to 127.0.0.1 (loopback only) — no firewall changes needed"],
             ]),
        ],
    },
    {
        "num": "11",
        "title": "Risks & Mitigations",
        "subtitle": "Risk register for leadership review",
        "colour": "APPROVE",
        "content": [
            ("risks", [
                ("LOW",    "SheetJS CDN Unavailability",         "Download SheetJS locally and change the <script src> to the local path. One-line change in HTML."),
                ("LOW",    "Python Not Installed on Machine",    "Python 3.8+ is a standard IT install. Document as prerequisite. HTML dashboards can open manually via file:// with reduced functionality."),
                ("LOW",    "Data File Path Changes",             "Update DEFAULT_CONFIG in file_watcher_bridge.py or POST to /config endpoint — no code restart needed."),
                ("MEDIUM", "Excel Column Structure Changes",     "Column index constants (COL_TABLE, COL_SRC, COL_TGT) are at the top of each dashboard script. Updating them requires no deep code knowledge."),
                ("MEDIUM", "SAP RFC Connection Failure",         "Bridge tries 3 RFC methods in sequence. If all fail, demo mode provides simulated counts for testing. Real file-based reconciliation unaffected."),
                ("LOW",    "Port Conflicts (5001/5002/5003)",    "Port numbers are constants at the top of each Python file. Change in one place — all references update."),
                ("LOW",    "Browser Compatibility",             "Chrome 90+ and Edge 90+ fully tested. SheetJS requires ES2017+. Firefox and Safari also work."),
            ]),
        ],
    },
    {
        "num": "12",
        "title": "Approval & Sign-Off",
        "subtitle": "Leadership approval section — print and sign",
        "colour": "APPROVE",
        "content": [
            ("plain", "AMBER", "Approval Request",
             "This document provides full visibility into the Sempra SAP Data Migration Tracking Dashboard — "
             "its purpose, functionality, technical design, security posture, and risk profile. "
             "The undersigned confirm they have reviewed this document and approve the solution for "
             "continued use in the SAP migration programme."),
            ("approval", [
                "Project Sponsor",
                "Programme / IT Manager",
                "Security / Compliance",
            ]),
            ("table",
             ["Document Metadata", "Value"],
             [
                 ["Document Title",      "Sempra SAP Data Migration Tracking Dashboard — Leadership Documentation"],
                 ["Document Version",    "v2.0"],
                 ["Project",             "SAP Data Migration — Sempra Energy"],
                 ["System Name",         "Sempra DM Dashboard v1.0"],
                 ["Components",          "1x MASTER + 3x cycle dashboards + 2x Python bridges + 1x launcher"],
                 ["Classification",      "Internal Use Only"],
                 ["Prepared by",         "Kishor Marri — SAP Migration Team"],
                 ["Technology Stack",    "HTML5, Vanilla JS, SheetJS v0.18.5, Python 3.8+, Flask, openpyxl, pandas"],
                 ["Deployment Model",    "Local laptop only — no cloud, no network dependencies, no licences"],
                 ["Ports Used",          "5001 (SAP Bridge opt.), 5002 (File Bridge), 5003 (Static) — all 127.0.0.1"],
                 ["SAP Systems",         "ES2 (Source) → SQ1 (Target)"],
             ]),
        ],
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# WORD DOCUMENT GENERATOR
# ─────────────────────────────────────────────────────────────────────────────

def make_word():
    from docx import Document
    from docx.shared import Pt, RGBColor, Cm, Inches
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
    import copy

    doc = Document()

    # ── Page margins ──────────────────────────────────────────────────────────
    for section in doc.sections:
        section.top_margin    = Cm(2.0)
        section.bottom_margin = Cm(2.0)
        section.left_margin   = Cm(2.2)
        section.right_margin  = Cm(2.2)

    # ── Style helpers ─────────────────────────────────────────────────────────
    def rgb(hex_str):
        h = hex_str.lstrip("#")
        return RGBColor(int(h[0:2],16), int(h[2:4],16), int(h[4:6],16))

    COLOURS = {
        "BLUE":   "#1d4ed8", "PURPLE": "#7c3aed", "GREEN":  "#059669",
        "AMBER":  "#b45309", "RED":    "#b91c1c",  "TEAL":   "#0f766e",
        "ARCH":   "#0369a1", "APPROVE":"#9a3412",  "TECH":   "#7c3aed",
        "BIZ":    "#0f766e", "STEPS":  "#b45309",  "NONE":   "#374151",
        "DM1 BLUE":   "#3b5bdb", "DM2 PURPLE": "#7c3aed", "DM3 GREEN": "#2f9e44",
    }

    def set_cell_bg(cell, hex_colour):
        tc   = cell._tc
        tcPr = tc.get_or_add_tcPr()
        shd  = OxmlElement("w:shd")
        shd.set(qn("w:val"),   "clear")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:fill"),  hex_colour.lstrip("#"))
        tcPr.append(shd)

    def add_heading(text, level=1, colour_hex="#1a202c"):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14 if level==1 else 8)
        p.paragraph_format.space_after  = Pt(4)
        run = p.add_run(text)
        run.bold      = True
        run.font.size = Pt(18 if level==1 else 13)
        run.font.color.rgb = rgb(colour_hex)
        return p

    def add_body(text, indent=False):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after  = Pt(4)
        if indent:
            p.paragraph_format.left_indent = Cm(0.6)
        run = p.add_run(text)
        run.font.size = Pt(10)
        run.font.color.rgb = rgb("#374151")
        return p

    def add_plain_box(colour_key, title, text):
        box_colours = {
            "GREEN":  ("#f0fdf4", "#15803d"),
            "BLUE":   ("#eff6ff", "#1d4ed8"),
            "AMBER":  ("#fffbeb", "#92400e"),
            "PURPLE": ("#faf5ff", "#7e22ce"),
            "RED":    ("#fff1f2", "#be123c"),
        }
        bg, fg = box_colours.get(colour_key, ("#f8fafc","#374151"))
        tbl = doc.add_table(rows=1, cols=1)
        tbl.style = "Table Grid"
        tbl.alignment = WD_TABLE_ALIGNMENT.LEFT
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.3)
        set_cell_bg(cell, bg)
        cell.paragraphs[0].clear()
        tp = cell.paragraphs[0]
        tp.paragraph_format.space_before = Pt(2)
        tp.paragraph_format.space_after  = Pt(2)
        r1 = tp.add_run(title.upper() + "\n")
        r1.bold = True; r1.font.size = Pt(9); r1.font.color.rgb = rgb(fg)
        r2 = tp.add_run(text)
        r2.font.size = Pt(10); r2.font.color.rgb = rgb("#374151")
        doc.add_paragraph()

    def add_table(headers, rows, col_widths=None):
        tbl = doc.add_table(rows=1 + len(rows), cols=len(headers))
        tbl.style = "Table Grid"
        tbl.alignment = WD_TABLE_ALIGNMENT.LEFT
        # Header row
        hdr_row = tbl.rows[0]
        for i, h in enumerate(headers):
            cell = hdr_row.cells[i]
            set_cell_bg(cell, "1e293b")
            p = cell.paragraphs[0]
            run = p.add_run(h)
            run.bold = True; run.font.size = Pt(9)
            run.font.color.rgb = rgb("#f8fafc")
        # Data rows
        for ri, row_data in enumerate(rows):
            tr = tbl.rows[ri+1]
            bg = "#f8fafc" if ri % 2 == 1 else "#ffffff"
            for ci, val in enumerate(row_data):
                cell = tr.cells[ci]
                set_cell_bg(cell, bg)
                p = cell.paragraphs[0]
                run = p.add_run(str(val))
                run.font.size = Pt(9)
                run.font.color.rgb = rgb("#374151")
        doc.add_paragraph()
        return tbl

    def add_code_block(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after  = Pt(8)
        run = p.add_run(text)
        run.font.name = "Courier New"
        run.font.size = Pt(8)
        run.font.color.rgb = rgb("#94a3b8")
        # grey background via table trick
        tbl = doc.add_table(rows=1, cols=1)
        tbl.style = "Table Grid"
        cell = tbl.cell(0,0)
        set_cell_bg(cell, "1e293b")
        p2 = cell.paragraphs[0]
        r = p2.add_run(text)
        r.font.name = "Courier New"; r.font.size = Pt(8)
        r.font.color.rgb = rgb("#94a3b8")
        doc.add_paragraph()

    # ── COVER PAGE ───────────────────────────────────────────────────────────
    cover_tbl = doc.add_table(rows=1, cols=1)
    cover_tbl.style = "Table Grid"
    cover_cell = cover_tbl.cell(0,0)
    set_cell_bg(cover_cell, "0f3460")
    cp = cover_cell.paragraphs[0]
    cp.alignment = WD_ALIGN_PARAGRAPH.LEFT

    r = cp.add_run("SEMPRA ENERGY — IT PROGRAMME\n")
    r.bold = True; r.font.size = Pt(10); r.font.color.rgb = rgb("#7dd3fc")

    r2 = cp.add_run("\nSAP Data Migration\nTracking Dashboard\n")
    r2.bold = True; r2.font.size = Pt(24); r2.font.color.rgb = rgb("#f8fafc")

    r3 = cp.add_run(
        "\nA self-contained, browser-based control room for tracking all three Data Migration cycles "
        "(DM1 → DM2 → DM3) — measuring how many SAP tables have been successfully exported, imported, "
        "and reconciled across source and target systems. No cloud. No manual effort. One click.\n"
    )
    r3.font.size = Pt(11); r3.font.color.rgb = rgb("#94a3b8")

    r4 = cp.add_run(
        "\n● DM1 — Cycle 1    ● DM2 — Cycle 2    ● DM3 — Cycle 3    ● Release v1.0\n"
        "● 100% Local — Zero Cloud    ● Internal Use Only\n\n"
        "Project: SAP Data Migration — Sempra\n"
        f"Documentation Version: 2.0    |    Generated: {datetime.now().strftime('%d %b %Y %H:%M')}\n"
    )
    r4.font.size = Pt(10); r4.font.color.rgb = rgb("#64748b")

    doc.add_page_break()

    # ── SECTIONS ─────────────────────────────────────────────────────────────
    for sec in SECTIONS:
        sec_colour = COLOURS.get(sec["colour"], "#1d4ed8")
        add_heading(f"Section {sec['num']} — {sec['title']}", level=1, colour_hex=sec_colour)
        p_sub = doc.add_paragraph(sec["subtitle"])
        p_sub.runs[0].font.size = Pt(10)
        p_sub.runs[0].font.color.rgb = rgb("#94a3b8")
        p_sub.paragraph_format.space_after = Pt(8)

        for item in sec["content"]:
            kind = item[0]

            if kind == "plain":
                _, col, title, text = item
                add_plain_box(col, title, text)

            elif kind == "kpis":
                _, kpi_list = item
                tbl = doc.add_table(rows=1, cols=len(kpi_list))
                tbl.style = "Table Grid"
                for ci, (num, lbl, sub) in enumerate(kpi_list):
                    cell = tbl.cell(0, ci)
                    set_cell_bg(cell, "eff6ff")
                    p = cell.paragraphs[0]
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    r1 = p.add_run(num + "\n")
                    r1.bold = True; r1.font.size = Pt(18); r1.font.color.rgb = rgb("#0369a1")
                    r2 = p.add_run(lbl + "\n")
                    r2.bold = True; r2.font.size = Pt(8); r2.font.color.rgb = rgb("#64748b")
                    r3 = p.add_run(sub)
                    r3.font.size = Pt(8); r3.font.color.rgb = rgb("#94a3b8")
                doc.add_paragraph()

            elif kind == "table":
                _, headers, rows = item
                add_table(headers, rows)

            elif kind == "code":
                _, text = item
                add_code_block(text)

            elif kind == "compare":
                _, (b_title, b_text), (a_title, a_text) = item
                tbl = doc.add_table(rows=1, cols=2)
                tbl.style = "Table Grid"
                bc = tbl.cell(0,0); ac = tbl.cell(0,1)
                set_cell_bg(bc, "fff1f2"); set_cell_bg(ac, "f0fdf4")
                for cell, title, text, fg in [(bc, b_title, b_text, "#b91c1c"), (ac, a_title, a_text, "#059669")]:
                    p = cell.paragraphs[0]
                    r1 = p.add_run(title + "\n")
                    r1.bold = True; r1.font.size = Pt(10); r1.font.color.rgb = rgb(fg)
                    r2 = p.add_run(text)
                    r2.font.size = Pt(9); r2.font.color.rgb = rgb("#374151")
                doc.add_paragraph()

            elif kind == "steps":
                _, step_list = item
                for num, title, text in step_list:
                    tbl = doc.add_table(rows=1, cols=2)
                    tbl.style = "Table Grid"
                    num_cell = tbl.cell(0,0)
                    txt_cell = tbl.cell(0,1)
                    num_cell.width = Cm(1.0)
                    set_cell_bg(num_cell, "1d4ed8")
                    p = num_cell.paragraphs[0]
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    r = p.add_run(num)
                    r.bold = True; r.font.size = Pt(14); r.font.color.rgb = rgb("#ffffff")
                    set_cell_bg(txt_cell, "eff6ff")
                    p2 = txt_cell.paragraphs[0]
                    r1 = p2.add_run(title + "\n")
                    r1.bold = True; r1.font.size = Pt(11); r1.font.color.rgb = rgb("#1a202c")
                    r2 = p2.add_run(text)
                    r2.font.size = Pt(9); r2.font.color.rgb = rgb("#475569")
                    doc.add_paragraph()

            elif kind == "colour_key":
                _, ck_list = item
                colour_map = {
                    "GREEN":  "#22c55e", "AMBER":  "#f59e0b", "RED":    "#ef4444",
                    "GREY":   "#94a3b8", "BLUE":   "#3b5bdb", "PURPLE": "#7c3aed",
                }
                rows = [[name, desc] for _, name, desc in ck_list]
                hdr = ["Colour / Status", "Meaning"]
                add_table(hdr, rows)

            elif kind == "cycle_cards":
                _, cards = item
                for cname, wave, col_key, text in cards:
                    c_hex = COLOURS.get(col_key, "#1d4ed8")
                    add_plain_box("BLUE", f"{cname} ({wave})", text)

            elif kind == "risks":
                _, risk_list = item
                rows = [[level, title, mitigation] for level, title, mitigation in risk_list]
                add_table(["Level", "Risk", "Mitigation"], rows)

            elif kind == "approval":
                _, roles = item
                tbl = doc.add_table(rows=4, cols=len(roles))
                tbl.style = "Table Grid"
                labels = ["Role", "Name / Signature", "", "Date"]
                for ri, lbl in enumerate(labels):
                    for ci, role in enumerate(roles):
                        cell = tbl.cell(ri, ci)
                        if ri == 0:
                            set_cell_bg(cell, "1e293b")
                            p = cell.paragraphs[0]
                            r = p.add_run(role if ri==0 else "")
                            r.bold = True; r.font.size = Pt(9); r.font.color.rgb = rgb("#f8fafc")
                            # show role in first row
                            p.clear()
                            rr = p.add_run(role)
                            rr.bold = True; rr.font.size = Pt(9); rr.font.color.rgb = rgb("#f8fafc")
                        else:
                            if ri == 1:
                                cell.paragraphs[0].add_run(lbl).font.size = Pt(9)
                            elif ri == 3:
                                cell.paragraphs[0].add_run("Date: _______________").font.size = Pt(9)
                doc.add_paragraph()

        doc.add_page_break()

    # ── SAVE ─────────────────────────────────────────────────────────────────
    doc.save(OUT_DOCX)
    print(f"  ✅ Word saved → {OUT_DOCX}  ({os.path.getsize(OUT_DOCX)//1024} KB)")


# ─────────────────────────────────────────────────────────────────────────────
# PDF GENERATOR (fpdf2)
# ─────────────────────────────────────────────────────────────────────────────

def make_pdf():
    from fpdf import FPDF, XPos, YPos

    def s(text):
        if not isinstance(text, str):
            text = str(text)
        return (text
            .replace("\u2014", "-").replace("\u2013", "-")
            .replace("\u2019", "'").replace("\u2018", "'")
            .replace("\u201c", '"').replace("\u201d", '"')
            .replace("\u2192", "->").replace("\u2190", "<-")
            .replace("\u2022", "*").replace("\u25cf", "*")
            .replace("\u2260", "!=").replace("\u2248", "~")
            .replace("\u2265", ">=").replace("\u2264", "<=")
            .replace("\u00b7", ".").replace("\u00a0", " ")
            .replace("\u25a0", "[X]").replace("\u2715", "x")
            .replace("\u2713", "OK").replace("\u21d2", "=>")
            .replace("\u25b6", ">").replace("\u00e9", "e")
        )

    # Colours
    C = {
        "bg":       (245, 246, 250),
        "white":    (255, 255, 255),
        "navy":     ( 15,  52,  96),
        "darktext": ( 26,  32,  44),
        "mutedtext":( 71,  85, 105),
        "greytext": (148, 163, 184),
        "border":   (226, 232, 240),
        "blue":     ( 29,  78, 216),
        "purple":   (124,  58, 237),
        "green":    ( 5, 150, 105),
        "amber":    (180,  83,   9),
        "red":      (185,  28,  28),
        "teal":     ( 15, 118, 110),
        "lightblue":(239, 246, 255),
        "lightgrn": (240, 253, 244),
        "lightamb": (255, 251, 235),
        "lightpur": (250, 245, 255),
        "lightnav": ( 15,  23,  42),
        "roweven":  (248, 250, 252),
        "rowalt":   (239, 246, 255),
        "hdrbg":    ( 30,  41,  59),
        "hdrfg":    (248, 250, 252),
    }

    SEC_COLOURS = {
        "BIZ":     C["teal"],
        "TECH":    C["purple"],
        "STEPS":   C["amber"],
        "ARCH":    C["blue"],
        "APPROVE": C["red"],
        "NONE":    C["blue"],
    }

    class PDF(FPDF):
        def header(self):
            pass

        def footer(self):
            self.set_y(-14)
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(*C["greytext"])
            self.cell(0, 8,
                      s("Sempra SAP Data Migration Dashboard - Leadership Documentation v2.0 - Internal Use Only"),
                      new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
            self.set_text_color(*C["mutedtext"])
            self.cell(0, 4, f"Page {self.page_no()}", align="C")

    pdf = PDF()
    pdf.set_margins(20, 18, 20)
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_font("Helvetica", size=10)

    # Auto-sanitize all text passed to cell/multi_cell so Helvetica core font works
    _orig_cell = pdf.cell
    _orig_mc   = pdf.multi_cell
    def _cell(*args, **kwargs):
        args = list(args)
        if len(args) >= 3 and isinstance(args[2], str): args[2] = s(args[2])
        if "text" in kwargs: kwargs["text"] = s(kwargs["text"])
        return _orig_cell(*args, **kwargs)
    def _mc(*args, **kwargs):
        args = list(args)
        if len(args) >= 3 and isinstance(args[2], str): args[2] = s(args[2])
        if "text" in kwargs: kwargs["text"] = s(kwargs["text"])
        return _orig_mc(*args, **kwargs)
    pdf.cell       = _cell
    pdf.multi_cell = _mc

    # ── helpers ───────────────────────────────────────────────────────────────
    def add_cover():
        pdf.add_page()
        # dark background
        pdf.set_fill_color(*C["navy"])
        pdf.rect(0, 0, 210, 297, "F")
        pdf.set_y(40)
        pdf.set_x(20)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(125, 211, 252)
        pdf.cell(0, 7, "SEMPRA ENERGY — IT PROGRAMME", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(6)
        pdf.set_font("Helvetica", "B", 28)
        pdf.set_text_color(248, 250, 252)
        pdf.set_x(20)
        pdf.multi_cell(170, 12, "SAP Data Migration\nTracking Dashboard")
        pdf.ln(6)
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(148, 163, 184)
        pdf.set_x(20)
        pdf.multi_cell(170, 6,
            "A self-contained, browser-based control room for tracking all three Data Migration cycles "
            "(DM1 → DM2 → DM3) — measuring how many SAP tables have been successfully exported, "
            "imported, and reconciled. No cloud. No manual effort. One click.")
        pdf.ln(10)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(165, 180, 252)
        pdf.set_x(20)
        pdf.cell(0, 6, "● DM1 — Cycle 1    ● DM2 — Cycle 2    ● DM3 — Cycle 3    ● Release v1.0    ● 100% Local",
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(24)
        pdf.set_draw_color(*C["greytext"])
        pdf.line(20, pdf.get_y(), 190, pdf.get_y())
        pdf.ln(6)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(100, 116, 139)
        pdf.set_x(20)
        pdf.cell(85, 5, f"Project: SAP Data Migration — Sempra")
        pdf.cell(85, 5, "Classification: Internal Use Only", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_x(20)
        pdf.cell(85, 5, "Documentation Version: 2.0")
        pdf.cell(85, 5, f"Generated: {datetime.now().strftime('%d %b %Y %H:%M')}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def sec_header(num, title, subtitle, colour):
        pdf.add_page()
        # coloured top bar
        r, g, b = colour
        pdf.set_fill_color(r, g, b)
        pdf.rect(0, 0, 210, 18, "F")
        pdf.set_y(4)
        pdf.set_x(20)
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(0, 10, f"  {num}  {title}")
        pdf.ln(16)
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(*C["mutedtext"])
        pdf.set_x(20)
        pdf.cell(0, 6, subtitle, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(3)

    def plain_box(col_key, title, text):
        box_c = {
            "GREEN":  (C["lightgrn"], C["green"]),
            "BLUE":   (C["lightblue"], C["blue"]),
            "AMBER":  (C["lightamb"], C["amber"]),
            "PURPLE": (C["lightpur"], C["purple"]),
            "RED":    ((255,241,242), C["red"]),
        }
        bg, fg = box_c.get(col_key, (C["lightblue"], C["blue"]))
        x = pdf.get_x()
        w = 170
        pdf.set_fill_color(*bg)
        pdf.set_draw_color(*C["border"])
        y_start = pdf.get_y()
        # measure text height
        pdf.set_font("Helvetica", "B", 8)
        lines_t = 1
        pdf.set_font("Helvetica", "", 9)
        lines_b = len(pdf.multi_cell(w-8, 5, text, dry_run=True, output="LINES"))
        box_h = 6 + lines_t*5 + lines_b*5 + 4
        pdf.rect(20, y_start, w, box_h, "FD")
        pdf.set_y(y_start + 3)
        pdf.set_x(24)
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_text_color(*fg)
        pdf.cell(w-8, 5, title.upper(), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_x(24)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*C["darktext"])
        pdf.multi_cell(w-8, 5, text)
        pdf.ln(4)

    def draw_table(headers, rows):
        w_total = 170
        w_col   = w_total / len(headers)
        # header
        pdf.set_fill_color(*C["hdrbg"])
        pdf.set_text_color(*C["hdrfg"])
        pdf.set_font("Helvetica", "B", 8)
        for h in headers:
            pdf.set_x(pdf.get_x() if headers.index(h)>0 else 20)
            pdf.cell(w_col, 7, h, border=1, fill=True)
        pdf.set_x(20); pdf.ln(7)
        # rows
        pdf.set_font("Helvetica", "", 8)
        for ri, row in enumerate(rows):
            bg = C["roweven"] if ri % 2 == 1 else C["white"]
            pdf.set_fill_color(*bg)
            pdf.set_text_color(*C["darktext"])
            row_y = pdf.get_y()
            # measure max height
            max_h = 6
            for ci, val in enumerate(row):
                lines = len(pdf.multi_cell(w_col, 5, str(val), dry_run=True, output="LINES"))
                max_h = max(max_h, lines * 5 + 2)
            # draw cells
            for ci, val in enumerate(row):
                pdf.set_xy(20 + ci*w_col, row_y)
                pdf.multi_cell(w_col, max_h/max(1, len(pdf.multi_cell(w_col, 5, str(val), dry_run=True, output="LINES"))),
                               str(val), border=1, fill=True, max_line_height=5)
                pdf.set_y(row_y)
            pdf.set_xy(20, row_y + max_h)
        pdf.ln(4)

    def code_block(text):
        pdf.set_fill_color(*C["lightnav"])
        pdf.set_draw_color(*C["hdrbg"])
        lines = text.split("\n")
        h_total = len(lines) * 4.5 + 6
        y0 = pdf.get_y()
        pdf.rect(20, y0, 170, h_total, "FD")
        pdf.set_y(y0 + 3)
        pdf.set_x(23)
        pdf.set_font("Courier", "", 7.5)
        pdf.set_text_color(*C["greytext"])
        for line in lines:
            pdf.set_x(23)
            pdf.cell(0, 4.5, line[:100], new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(4)
        pdf.set_text_color(*C["darktext"])

    def risk_rows(risk_list):
        risk_colours = {"LOW": (240,253,244), "MEDIUM": (255,251,235), "HIGH": (255,241,242)}
        risk_text_c  = {"LOW": C["green"], "MEDIUM": C["amber"], "HIGH": C["red"]}
        for level, title, mitigation in risk_list:
            bg = risk_colours.get(level, C["white"])
            tc = risk_text_c.get(level, C["darktext"])
            y0 = pdf.get_y()
            pdf.set_fill_color(*bg)
            pdf.set_draw_color(*C["border"])
            lines = len(pdf.multi_cell(140, 4.5, mitigation, dry_run=True, output="LINES"))
            box_h = max(14, lines * 4.5 + 10)
            pdf.rect(20, y0, 170, box_h, "FD")
            pdf.set_xy(24, y0+3)
            pdf.set_fill_color(*tc)
            pdf.rect(24, y0+3, 16, 5, "F")
            pdf.set_xy(24, y0+3)
            pdf.set_font("Helvetica", "B", 7)
            pdf.set_text_color(255,255,255)
            pdf.cell(16, 5, level, align="C")
            pdf.set_xy(44, y0+3)
            pdf.set_font("Helvetica", "B", 9)
            pdf.set_text_color(*C["darktext"])
            pdf.cell(0, 5, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_x(44)
            pdf.set_font("Helvetica", "", 8)
            pdf.set_text_color(*C["mutedtext"])
            pdf.multi_cell(146, 4.5, mitigation)
            pdf.set_y(y0 + box_h + 2)
        pdf.ln(2)

    def approval_boxes(roles):
        w = 170 / len(roles)
        y0 = pdf.get_y()
        pdf.set_fill_color(*C["white"])
        pdf.set_draw_color(*C["border"])
        for ci, role in enumerate(roles):
            x0 = 20 + ci * w
            pdf.rect(x0, y0, w, 50, "FD")
            pdf.set_xy(x0+3, y0+3)
            pdf.set_font("Helvetica", "B", 8)
            pdf.set_text_color(*C["mutedtext"])
            pdf.cell(w-6, 5, role.upper())
            pdf.set_xy(x0+3, y0+30)
            pdf.set_draw_color(*C["border"])
            pdf.line(x0+3, y0+40, x0+w-3, y0+40)
            pdf.set_font("Helvetica", "", 8)
            pdf.set_text_color(*C["greytext"])
            pdf.set_xy(x0+3, y0+42)
            pdf.cell(w-6, 5, "Signature")
            pdf.set_xy(x0+3, y0+47)
            pdf.cell(w-6, 5, "Date: ___________")
        pdf.set_y(y0 + 55)
        pdf.ln(4)

    # ── BUILD PDF ─────────────────────────────────────────────────────────────
    add_cover()

    for sec in SECTIONS:
        colour = SEC_COLOURS.get(sec["colour"], C["blue"])
        sec_header(sec["num"], sec["title"], sec["subtitle"], colour)

        for item in sec["content"]:
            kind = item[0]

            if kind == "plain":
                _, col, title, text = item
                plain_box(col, title, text)

            elif kind == "kpis":
                _, kpi_list = item
                w_each = 170 / len(kpi_list)
                y0 = pdf.get_y()
                pdf.set_fill_color(*C["lightblue"])
                pdf.set_draw_color(*C["border"])
                for ci, (num, lbl, sub) in enumerate(kpi_list):
                    x0 = 20 + ci*w_each
                    pdf.rect(x0, y0, w_each, 22, "FD")
                    pdf.set_xy(x0+2, y0+2)
                    pdf.set_font("Helvetica", "B", 14)
                    pdf.set_text_color(*C["blue"])
                    pdf.cell(w_each-4, 8, num, align="C")
                    pdf.set_xy(x0+2, y0+10)
                    pdf.set_font("Helvetica", "B", 6.5)
                    pdf.set_text_color(*C["mutedtext"])
                    pdf.cell(w_each-4, 5, lbl, align="C")
                    pdf.set_xy(x0+2, y0+15)
                    pdf.set_font("Helvetica", "", 6)
                    pdf.set_text_color(*C["greytext"])
                    pdf.cell(w_each-4, 4, sub, align="C")
                pdf.set_y(y0 + 26)
                pdf.ln(2)

            elif kind == "table":
                _, headers, rows = item
                draw_table(headers, rows)

            elif kind == "code":
                _, text = item
                code_block(text)

            elif kind == "compare":
                _, (b_title, b_text), (a_title, a_text) = item
                y0 = pdf.get_y()
                w = 84
                # BEFORE
                pdf.set_fill_color(255,241,242); pdf.set_draw_color(*C["border"])
                lines_b = len(pdf.multi_cell(w-6, 4.5, b_text, dry_run=True, output="LINES"))
                h = max(30, lines_b*4.5+12)
                pdf.rect(20, y0, w, h, "FD")
                pdf.set_xy(23, y0+3)
                pdf.set_font("Helvetica","B",9); pdf.set_text_color(*C["red"])
                pdf.cell(w-6, 5, b_title)
                pdf.set_xy(23, y0+9); pdf.set_font("Helvetica","",8)
                pdf.set_text_color(*C["darktext"]); pdf.multi_cell(w-6, 4.5, b_text)
                # AFTER
                pdf.set_fill_color(*C["lightgrn"]); pdf.set_draw_color(*C["border"])
                lines_a = len(pdf.multi_cell(w-6, 4.5, a_text, dry_run=True, output="LINES"))
                h2 = max(30, lines_a*4.5+12)
                h_final = max(h, h2)
                pdf.rect(20+w+2, y0, w, h_final, "FD")
                pdf.set_xy(23+w+2, y0+3)
                pdf.set_font("Helvetica","B",9); pdf.set_text_color(*C["green"])
                pdf.cell(w-6, 5, a_title)
                pdf.set_xy(23+w+2, y0+9); pdf.set_font("Helvetica","",8)
                pdf.set_text_color(*C["darktext"]); pdf.multi_cell(w-6, 4.5, a_text)
                pdf.set_y(y0 + h_final + 3)
                pdf.ln(2)

            elif kind == "steps":
                _, step_list = item
                for num, title, text in step_list:
                    y0 = pdf.get_y()
                    lines = len(pdf.multi_cell(148, 4.5, text, dry_run=True, output="LINES"))
                    h = max(18, lines*4.5+12)
                    # circle
                    pdf.set_fill_color(*C["blue"])
                    pdf.ellipse(20, y0, 10, 10, "F")
                    pdf.set_xy(20, y0+2)
                    pdf.set_font("Helvetica","B",9); pdf.set_text_color(255,255,255)
                    pdf.cell(10, 6, num, align="C")
                    # content
                    pdf.set_fill_color(*C["lightblue"]); pdf.set_draw_color(*C["border"])
                    pdf.rect(33, y0, 157, h, "FD")
                    pdf.set_xy(36, y0+3)
                    pdf.set_font("Helvetica","B",10); pdf.set_text_color(*C["darktext"])
                    pdf.cell(150, 6, title)
                    pdf.set_xy(36, y0+10); pdf.set_font("Helvetica","",8)
                    pdf.set_text_color(*C["mutedtext"]); pdf.multi_cell(150, 4.5, text)
                    pdf.set_y(y0 + h + 3)

            elif kind == "colour_key":
                _, ck_list = item
                rows = [[name, desc] for _, name, desc in ck_list]
                draw_table(["Colour / Status", "Meaning"], rows)

            elif kind == "cycle_cards":
                _, cards = item
                for cname, wave, col_key, text in cards:
                    plain_box("BLUE", f"{cname} ({wave})", text)

            elif kind == "risks":
                _, risk_list = item
                risk_rows(risk_list)

            elif kind == "approval":
                _, roles = item
                approval_boxes(roles)

    # ── SAVE ─────────────────────────────────────────────────────────────────
    pdf.output(OUT_PDF)
    print(f"  [OK] PDF  saved -> {OUT_PDF}  ({os.path.getsize(OUT_PDF)//1024} KB)")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
def _sanitize_for_pdf(obj):
    """Recursively replace all non-latin-1 characters in SECTIONS data."""
    REPLACEMENTS = [
        ("\u2014","-"), ("\u2013","-"), ("\u2019","'"), ("\u2018","'"),
        ("\u201c",'"'), ("\u201d",'"'), ("\u2192","->"), ("\u2190","<-"),
        ("\u2022","*"), ("\u25cf","*"), ("\u2260","!="), ("\u2248","~"),
        ("\u2265",">="), ("\u2264","<="), ("\u00b7","."), ("\u00a0"," "),
        ("\u25a0","[X]"), ("\u2715","x"), ("\u2713","OK"), ("\u21d2","=>"),
        ("\u25b6",">"), ("\u00e9","e"), ("\u26a1","[!]"), ("\u2022","-"),
        ("\u2764","[heart]"), ("\u2728","[star]"), ("\u2705","[OK]"),
        ("\u274c","[X]"), ("\u27a1","->"), ("\u1f4e5","[dl]"),
        # catch-all: strip remaining high codepoints
    ]
    if isinstance(obj, str):
        for bad, good in REPLACEMENTS:
            obj = obj.replace(bad, good)
        # strip any remaining chars outside latin-1
        obj = obj.encode("latin-1", errors="replace").decode("latin-1")
        return obj
    elif isinstance(obj, list):
        return [_sanitize_for_pdf(i) for i in obj]
    elif isinstance(obj, tuple):
        return tuple(_sanitize_for_pdf(i) for i in obj)
    elif isinstance(obj, dict):
        return {k: _sanitize_for_pdf(v) for k, v in obj.items()}
    return obj


if __name__ == "__main__":
    print("=" * 60)
    print("  Sempra DM Dashboard - Documentation Generator")
    print("=" * 60)
    print("\n[1/2] Generating Word document...")
    make_word()
    print("\n[2/2] Generating PDF document...")
    # Sanitize SECTIONS data for PDF (Helvetica is latin-1 only)
    import copy
    _PDF_SECTIONS = _sanitize_for_pdf(copy.deepcopy(SECTIONS))
    _orig_sections = SECTIONS[:]
    SECTIONS.clear()
    SECTIONS.extend(_PDF_SECTIONS)
    make_pdf()
    SECTIONS.clear()
    SECTIONS.extend(_orig_sections)
    print(f"\n  Both files saved in: {os.path.abspath('.')}")
    print("=" * 60)
