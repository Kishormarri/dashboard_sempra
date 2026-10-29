"""
Generate Sempra DM Dashboard User Manual as PDF using ReportLab
Run: python generate_manual_pdf.py
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, HRFlowable, PageBreak, KeepTogether)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
import datetime

OUT = "Sempra_DM_Dashboard_User_Manual.pdf"

# ── Colours ──────────────────────────────────────────────────────────────────
NAVY   = colors.HexColor("#0f2d4a")
BLUE   = colors.HexColor("#1e3a5f")
TEAL   = colors.HexColor("#0f766e")
LTBLUE = colors.HexColor("#eff6ff")
LTGREY = colors.HexColor("#f7f8fa")
BORDER = colors.HexColor("#e5e7eb")
MUTED  = colors.HexColor("#57606a")
WHITE  = colors.white
BLACK  = colors.HexColor("#1f2328")
GREEN  = colors.HexColor("#15803d")
AMBER  = colors.HexColor("#92400e")
RED    = colors.HexColor("#dc2626")

# ── Styles ────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def S(name, **kw):
    return ParagraphStyle(name, **kw)

H1  = S("H1",  fontSize=20, leading=26, textColor=WHITE,  fontName="Helvetica-Bold",  spaceAfter=4)
H2  = S("H2",  fontSize=14, leading=20, textColor=NAVY,   fontName="Helvetica-Bold",  spaceBefore=18, spaceAfter=6,  borderPad=4)
H3  = S("H3",  fontSize=11, leading=16, textColor=BLUE,   fontName="Helvetica-Bold",  spaceBefore=10, spaceAfter=4)
H4  = S("H4",  fontSize=10, leading=14, textColor=BLACK,  fontName="Helvetica-Bold",  spaceBefore=6,  spaceAfter=2)
BOD = S("BOD", fontSize=9,  leading=14, textColor=BLACK,  fontName="Helvetica",       spaceAfter=5)
BUL = S("BUL", fontSize=9,  leading=13, textColor=BLACK,  fontName="Helvetica",       leftIndent=14,  spaceAfter=2,  bulletIndent=4)
COD = S("COD", fontSize=8,  leading=12, textColor=colors.HexColor("#374151"), fontName="Courier",
        backColor=colors.HexColor("#f3f4f6"), borderPad=4, spaceAfter=4)
CAP = S("CAP", fontSize=8,  leading=12, textColor=MUTED,  fontName="Helvetica-Oblique", spaceAfter=6, alignment=TA_CENTER)
NUM = S("NUM", fontSize=9,  leading=13, textColor=BLACK,  fontName="Helvetica",       leftIndent=20, spaceAfter=3)

def h2(text):
    return [HRFlowable(width="100%", thickness=1.5, color=NAVY, spaceAfter=4),
            Paragraph(text, H2)]

def h3(text): return Paragraph(text, H3)
def h4(text): return Paragraph(text, H4)
def p(text):  return Paragraph(text, BOD)
def sp(n=6):  return Spacer(1, n)
def bul(text):return Paragraph(f"• {text}", BUL)
def num(i, text): return Paragraph(f"{i}.  {text}", NUM)
def code(text):   return Paragraph(text, COD)
def hr():    return HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=8)

def tbl(data, col_widths=None, header_bg=BLUE):
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style = [
        ("BACKGROUND",  (0,0), (-1,0),  header_bg),
        ("TEXTCOLOR",   (0,0), (-1,0),  WHITE),
        ("FONTNAME",    (0,0), (-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",    (0,0), (-1,0),  8),
        ("BOTTOMPADDING",(0,0),(-1,0),  6),
        ("TOPPADDING",  (0,0), (-1,0),  6),
        ("FONTNAME",    (0,1), (-1,-1), "Helvetica"),
        ("FONTSIZE",    (0,1), (-1,-1), 8),
        ("TOPPADDING",  (0,1), (-1,-1), 5),
        ("BOTTOMPADDING",(0,1),(-1,-1), 5),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE, colors.HexColor("#f7f8fa")]),
        ("GRID",        (0,0), (-1,-1), 0.4, BORDER),
        ("VALIGN",      (0,0), (-1,-1), "TOP"),
    ]
    t.setStyle(TableStyle(style))
    return t

def callout(text, bg=LTBLUE, border=colors.HexColor("#3b82f6")):
    d = [[Paragraph(text, S("cb", fontSize=9, leading=13, fontName="Helvetica", textColor=colors.HexColor("#1e40af")))]]
    t = Table(d, colWidths=[16.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), bg),
        ("LEFTPADDING",(0,0), (-1,-1), 10),
        ("RIGHTPADDING",(0,0),(-1,-1), 10),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING",(0,0),(-1,-1),8),
        ("LINEAFTER",  (0,0), (0,-1),  0, border),  # no, use box
        ("BOX",        (0,0), (-1,-1), 0.5, border),
        ("ROUNDEDCORNERS",[4]),
    ]))
    return t

# ── Cover page ────────────────────────────────────────────────────────────────
def cover_table():
    content = [
        Paragraph("📊", S("ico", fontSize=32, leading=40, textColor=WHITE, fontName="Helvetica-Bold")),
        Spacer(1, 8),
        Paragraph("Sempra Data Migration Dashboard", H1),
        Paragraph("Complete User Manual", S("sub", fontSize=13, leading=18, textColor=colors.HexColor("#94a3b8"), fontName="Helvetica")),
        Spacer(1, 14),
        Paragraph("Odyssey Phase 1 Project Team", S("t2", fontSize=10, leading=14, textColor=colors.HexColor("#cbd5e1"), fontName="Helvetica")),
        Paragraph(f"Version 1.0  ·  October 2026  ·  DM1 · DM2 · DM3", S("t3", fontSize=9, leading=13, textColor=colors.HexColor("#64748b"), fontName="Helvetica")),
    ]
    t = Table([[content]], colWidths=[17*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), NAVY),
        ("TOPPADDING",  (0,0), (-1,-1), 30),
        ("BOTTOMPADDING",(0,0),(-1,-1), 30),
        ("LEFTPADDING", (0,0), (-1,-1), 30),
        ("RIGHTPADDING",(0,0), (-1,-1), 30),
        ("ROUNDEDCORNERS",[8]),
    ]))
    return t

# ── Build PDF ─────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(OUT, pagesize=A4,
      leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm,
      title="Sempra DM Dashboard User Manual", author="Sempra Odyssey Team")

story = []

# Cover
story += [cover_table(), sp(20)]

# ── 1. OVERVIEW ───────────────────────────────────────────────────────────────
story += h2("1.  Overview & Purpose")
story += [p("The <b>Sempra Data Migration Dashboard</b> is a local web application built to track, analyse, "
            "and report on SAP data migration progress across three migration cycles — DM1, DM2, and DM3 — "
            "as part of the Odyssey Phase 1 project."), sp()]

story += [h3("What the tool does")]
for txt in [
    "<b>3-Cycle Tracking</b> — Track DM1, DM2, DM3 migration progress in one place with automatic cross-cycle comparison.",
    "<b>Table Reconciliation</b> — Automatically matches reference tables against exported/imported data to identify gaps.",
    "<b>RAG Status Reports</b> — Business-friendly Red/Amber/Green scorecards for each migration cycle.",
    "<b>Auto Column Detection</b> — Reads Excel files regardless of column name variations — no template required.",
    "<b>Drill-Down Analysis</b> — Click any table or metric to see individual record-level detail.",
    "<b>SAP Live Connection</b> — Optionally connects to SAP source and target to pull live record counts automatically.",
]:
    story.append(bul(txt))
story.append(sp())

# ── 2. ARCHITECTURE ───────────────────────────────────────────────────────────
story += h2("2.  System Architecture")
story += [p("The dashboard runs entirely on your local machine — no cloud, no external server required."), sp()]
story.append(tbl([
    ["Component", "Port", "Purpose"],
    ["Static HTTP Server",  "5003", "Serves HTML dashboard files to your browser"],
    ["File Watcher Bridge", "5002", "Reads Excel files from disk and serves them to the dashboard"],
    ["SAP Bridge (optional)","5001","Connects to SAP systems for live record count automation"],
], col_widths=[6*cm, 2.5*cm, 8*cm]))
story.append(sp())

# ── 3. SETUP ──────────────────────────────────────────────────────────────────
story += h2("3.  Setup & First Launch")
story += [h3("Install Dependencies (once only)")]
story.append(code("python -m pip install flask flask-cors openpyxl"))
story += [h3("Start the Dashboard")]
for i, t in enumerate([
    "Open PowerShell in the dashboard folder:   cd C:\\Users\\KishorMarri\\Documents\\Sempra_DM_Dashboard_v1.0",
    "Run the launcher:   python launch_dashboard.py",
    "Browser opens automatically at:   http://localhost:5003/Sempra_CrossCycle_Summary_MASTER.html",
    "Log in with your role credentials (see Section 5).",
], 1):
    story.append(num(i, t))
story.append(sp())

# ── 4. DATA FILES ─────────────────────────────────────────────────────────────
story += h2("4.  Data File Requirements")
story += [p("The dashboard reads two Excel files per migration cycle — a <b>Reference List</b> and an <b>Export/Import log</b>."), sp()]
story += [h3("Default File Locations")]
story.append(code(
    "C:\\Users\\&lt;user&gt;\\.bob\\DM1\\   — DM1 Reference List + Export/Import file\n"
    "C:\\Users\\&lt;user&gt;\\.bob\\DM2\\   — DM2 Reference List + Export/Import file\n"
    "C:\\Users\\&lt;user&gt;\\.bob\\DM3\\   — DM3 Reference List + Export/Import file"
))
story += [h3("File Requirements per Cycle")]
story.append(tbl([
    ["File Type", "What it contains", "Detected by filename"],
    ["Reference List (REF)", "Master list of all SAP tables expected to be migrated. Must have a Table Name column and a record count column.",
     "ref, reflist, master, table, list"],
    ["Export/Import Log (EXP)", "SNP migration tool output showing which tables were exported and imported, with record counts.",
     "exp, imp, export, import, snp, log"],
], col_widths=[3.5*cm, 8*cm, 5*cm]))
story.append(sp())
story += [h3("Supported Column Names (auto-detected)")]
story.append(tbl([
    ["Data Point", "Accepted Column Names"],
    ["Table Name",    "TABLE_NAME, TABLE, OBJECT_NAME, NAME"],
    ["Record Count",  "NUMBER OF RECORDS, RECORD_COUNT, COUNT, ROWS, VOLUME (20+ variants)"],
    ["Source Count",  "SOURCE_COUNT, SOURCE, SRC_COUNT"],
    ["Target Count",  "TARGET_COUNT, TARGET, TGT_COUNT"],
    ["Type",          "TYPE, DIRECTION, MOVE_TYPE"],
], col_widths=[4*cm, 12.5*cm]))

# ── 5. ROLES ──────────────────────────────────────────────────────────────────
story += h2("5.  User Roles & Login")
story.append(tbl([
    ["Role", "Username", "Permissions"],
    ["Admin",   "admin",   "Full access — upload, refresh, download, automation panel, manage paths"],
    ["Manager", "manager", "View dashboards, download PDF reports, view RAG scorecards"],
    ["Analyst", "analyst", "Upload files, view analysis, download CSV/Excel"],
    ["Viewer",  "viewer",  "Read-only — view dashboards and charts only"],
], col_widths=[2.5*cm, 3*cm, 11*cm]))

# ── 6. MASTER DASHBOARD ───────────────────────────────────────────────────────
story += h2("6.  Executive Summary Dashboard")
story += [p("Main page: <b>Sempra_CrossCycle_Summary_MASTER.html</b> — consolidated view across all three cycles."), sp()]
story += [h3("Three Views")]
story.append(tbl([
    ["View", "Audience", "What it shows"],
    ["📊 Business View", "Project Managers, Sponsors",
     "RAG scorecards per cycle, headline metrics, record volumes, key insight boxes"],
    ["🔧 Technical View", "Data Migration Leads, Analysts",
     "Table-level comparison, source vs target counts, export vs import gaps, drill-down"],
    ["⚡ Performance View", "Technical Team",
     "Cross-cycle comparison charts, trend analysis, cycle-over-cycle improvement metrics"],
], col_widths=[3.5*cm, 4.5*cm, 8.5*cm]))
story.append(sp())
story += [h3("RAG Status Explained")]
story.append(tbl([
    ["Status", "Meaning", "Threshold"],
    ["🟢 GREEN", "Migration on track",                   "≥ 95% match rate"],
    ["🟡 AMBER", "Minor gaps — attention needed",        "80–94% match rate"],
    ["🔴 RED",   "Significant issues — action required", "< 80% match rate"],
    ["⚫ GREY",  "No data loaded yet",                   "—"],
], col_widths=[3*cm, 8*cm, 5.5*cm]))

# ── 7. CYCLE DASHBOARDS ───────────────────────────────────────────────────────
story += h2("7.  Cycle Dashboards (DM1 / DM2 / DM3)")
story += [h3("Manual Upload Workflow")]
for i, t in enumerate([
    "Click 'Upload Reference List' — select the REF Excel file for that cycle",
    "Click 'Upload Export/Import File' — select the EXP/IMP Excel file",
    "Dashboard automatically detects columns, parses data, and runs analysis",
    "Results appear across four analysis sets",
], 1):
    story.append(num(i, t))
story.append(sp())
story += [h3("Four Analysis Sets")]
story.append(tbl([
    ["Set", "What it shows"],
    ["Set 1 — In Reference",          "Tables in Reference List AND with migration data. Shows EXP vs IMP count comparison."],
    ["Set 2 — Not in Reference",      "Tables found in EXP/IMP file NOT in the Reference List. Unexpected tables — needs investigation."],
    ["Set 3 — Missing from Migration","Tables in Reference List with NO export or import data at all. Never migrated."],
    ["Set 4 — Count Mismatches",      "Tables where Export count ≠ Import count. Data loss or duplication during migration."],
], col_widths=[4.5*cm, 12*cm]))

# ── 8. AUTO-LOAD ──────────────────────────────────────────────────────────────
story += h2("8.  Auto-Load from Shared Folder")
story += [p("Instead of manually uploading files each time, the Auto-Load Panel lets the bridge automatically "
            "pick up the latest files from a folder on your machine or a network share."), sp()]
story += [h3("How to Use")]
for i, t in enumerate([
    "Click 'Auto-Load' button in the cycle dashboard header",
    "Enter the folder path where the REF file lives (e.g. C:\\Files\\DM1\\  or  \\\\server\\share\\DM1\\)",
    "Enter the folder path where the EXP file lives",
    "Click 'Save Paths' — paths are remembered for future sessions",
    "Click 'Scan for Latest Files' — bridge finds the most recently modified matching file",
    "Click 'Load Both Files Now' — bridge streams both files directly into the dashboard",
], 1):
    story.append(num(i, t))

# ── 9. SAP AUTOMATION ─────────────────────────────────────────────────────────
story += h2("9.  SAP Count Automation")
story += [p("The SAP Count Automation Panel (Admin only) connects to SAP source and target systems "
            "to automatically pull SE16N record counts — no manual Excel extraction needed."), sp()]
story.append(tbl([
    ["Manual Process (before)", "Automated (with SAP bridge)"],
    ["Log into SAP manually for each system",          "Single credentials entry — bridge handles all connections"],
    ["Run SE16N for hundreds of tables one by one",    "All tables queried in one batch run"],
    ["Copy counts into Excel manually",                "Counts written directly to dashboard"],
    ["30–60 minutes per cycle",                        "5–10 minutes per cycle"],
], col_widths=[8*cm, 8.5*cm]))

# ── 10. EXPORTS ───────────────────────────────────────────────────────────────
story += h2("10.  Exporting Results")
story.append(tbl([
    ["Export Type", "What it contains", "How to generate"],
    ["📄 CSV",        "Raw table data for any analysis set",             "Click CSV button next to each set header"],
    ["📊 Excel",      "Formatted multi-sheet workbook with all sets",    "Click Excel button — generates in browser"],
    ["🖨️ PDF",        "Print-ready report of the current view",          "Click PDF or Ctrl+P"],
    ["📦 Full Export","All cycles, all sets in one Excel file",          "Available from Executive Summary dashboard"],
], col_widths=[3*cm, 7.5*cm, 6*cm]))

# ── 11. TROUBLESHOOT ──────────────────────────────────────────────────────────
story += h2("11.  Troubleshooting")
issues = [
    ("Bridge shows red dot / 'Bridge offline'",
     ["Open terminal in dashboard folder",
      "Run: python automation/file_watcher_bridge.py",
      "Verify: Running on http://127.0.0.1:5002",
      "Reload the dashboard page"]),
    ("Dashboard shows blank / no data after upload",
     ["Check the file has a Table Name column and a numeric count column",
      "Ensure the file is not open in Excel (~$filename.xlsx blocks reading)",
      "Try — the bridge reads the first sheet by default"]),
    ("'No file found' in Auto-Load scan",
     ["Verify the folder path is correct and accessible",
      "Check file pattern — default is *.xlsx",
      "Ensure filename contains a keyword: ref / exp / imp / log"]),
    ("Data not refreshing after file update",
     ["Click Refresh button or press Ctrl+Shift+R",
      "POST to http://localhost:5002/cache/clear to force bridge cache refresh"]),
]
for title, steps in issues:
    story.append(h4(title))
    for s in steps:
        story.append(bul(s))
    story.append(sp(4))

# ── 12. QUICK REFERENCE ───────────────────────────────────────────────────────
story += h2("12.  Quick Reference")
story += [h3("Dashboard URLs")]
story.append(tbl([
    ["Page", "URL"],
    ["Executive Summary",   "http://localhost:5003/Sempra_CrossCycle_Summary_MASTER.html"],
    ["DM1 Dashboard",       "http://localhost:5003/Sempra_DM1_Dashboard.html"],
    ["DM2 Dashboard",       "http://localhost:5003/Sempra_DM2_Dashboard.html"],
    ["DM3 Dashboard",       "http://localhost:5003/Sempra_DM3_Dashboard.html"],
    ["Bridge Health Check", "http://localhost:5002/ping"],
    ["File Status",         "http://localhost:5002/paths"],
], col_widths=[4.5*cm, 12*cm]))
story.append(sp())
story += [h3("Current Data Files on C: Drive")]
story.append(tbl([
    ["Cycle", "File", "Type"],
    ["DM1", r"C:\Users\KishorMarri\.bob\DM1\Reflist_m1.xlsx",                 "Reference List"],
    ["DM1", r"C:\Users\KishorMarri\.bob\DM1\DM1_ES2-SQ1 Export-Import.xlsx", "Export/Import"],
    ["DM2", r"C:\Users\KishorMarri\.bob\DM2\DM2 REF.xlsx",                   "Reference List"],
    ["DM2", r"C:\Users\KishorMarri\.bob\DM2\EXPORT IMPORT_DM2.xlsx",         "Export/Import"],
    ["DM3", r"C:\Users\KishorMarri\.bob\DM3\ref dm31.xlsx",                  "Reference List"],
    ["DM3", r"C:\Users\KishorMarri\.bob\DM3\DM3_EXPORT_IMPORT_LOG.xlsx",     "Export/Import"],
], col_widths=[1.5*cm, 11.5*cm, 3.5*cm]))

story.append(sp(20))
story.append(hr())
story.append(Paragraph(
    f"Sempra Data Migration Dashboard v1.0  ·  Odyssey Phase 1  ·  Generated {datetime.date.today().strftime('%B %Y')}",
    S("ft", fontSize=8, leading=12, textColor=MUTED, fontName="Helvetica", alignment=TA_CENTER)
))

doc.build(story)
print(f"PDF created: {OUT}")
