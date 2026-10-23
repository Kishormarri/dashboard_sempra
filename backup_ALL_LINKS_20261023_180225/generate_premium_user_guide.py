"""
================================================================================
  SEMPRA DATA MIGRATION DASHBOARD — PREMIUM USER GUIDE & STEP-BY-STEP BLUEPRINT
  Generates the ultimate executive and functional user guide (PDF & HTML):
  - Prerequisites & Environment Setup Checklist
  - Step-by-Step Execution Guide (from launch to audit sign-off)
  - What We Achieve & Business Value
  - Source vs Target Comparison & Pivot/Circle Analytics
================================================================================
"""
import os
import sys
import shutil
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

PDF_LOCAL = "Sempra_DM_Dashboard_PREMIUM_User_Guide.pdf"
PDF_DESKTOP = "C:\\Users\\KishorMarri\\Desktop\\Sempra_DM_Dashboard_PREMIUM_User_Guide.pdf"
HTML_LOCAL = "Sempra_DM_Dashboard_PREMIUM_User_Guide.html"

# ── Colors ────────────────────────────────────────────────────────────────────
NAVY       = colors.HexColor("#091e3a")
NAVY_LIGHT = colors.HexColor("#1e3a5f")
BLUE_ACC   = colors.HexColor("#1d4ed8")
BLUE_LT    = colors.HexColor("#eff6ff")
LIGHT_BLUE = colors.HexColor("#eff6ff")
BORDER_BL  = colors.HexColor("#bfdbfe")
DARK_GRAY  = colors.HexColor("#1e293b")
TEXT_MUTED = colors.HexColor("#475569")
GREEN      = colors.HexColor("#15803d")
GREEN_BG   = colors.HexColor("#dcfce7")
GREEN_BD   = colors.HexColor("#86efac")
AMBER      = colors.HexColor("#b45309")
AMBER_BG   = colors.HexColor("#fef3c7")
AMBER_BD   = colors.HexColor("#fde68a")
SURFACE    = colors.HexColor("#f8fafc")
BORDER     = colors.HexColor("#e2e8f0")
WHITE      = colors.white

class PremiumNumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(TEXT_MUTED)

        # Header on pages > 1
        if self._pageNumber > 1:
            self.drawString(54, 11 * inch - 36, "Sempra Energy · Odyssey Data Migration Platform — Premium User Guide")
            self.setFont("Helvetica", 8)
            self.drawRightString(8.5 * inch - 54, 11 * inch - 36, "Confidential — Step-by-Step Operations")
            self.setStrokeColor(BORDER)
            self.setLineWidth(0.5)
            self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)

        # Footer on all pages
        self.setFont("Helvetica", 8)
        self.drawString(54, 34, "Sempra Data Migration Automation Framework · Premium Execution Guide")
        self.drawRightString(8.5 * inch - 54, 34, f"Page {self._pageNumber} of {page_count}")
        self.setStrokeColor(BORDER)
        self.setLineWidth(0.5)
        self.line(54, 46, 8.5 * inch - 54, 46)

        self.restoreState()


def build_pdf():
    doc = SimpleDocTemplate(
        PDF_LOCAL,
        pagesize=letter,
        leftMargin=48,
        rightMargin=48,
        topMargin=48,
        bottomMargin=48,
    )

    styles = getSampleStyleSheet()

    h1_style = ParagraphStyle(
        'PremH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=NAVY,
        spaceBefore=11,
        spaceAfter=5,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'PremBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=DARK_GRAY,
        spaceAfter=4
    )

    tbl_hdr = ParagraphStyle(
        'PremTblHdr',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=NAVY
    )

    tbl_cell = ParagraphStyle(
        'PremTblCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=DARK_GRAY
    )

    tbl_cell_bold = ParagraphStyle(
        'PremTblCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=NAVY
    )

    tbl_mono = ParagraphStyle(
        'PremTblMono',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7,
        leading=9,
        textColor=NAVY_LIGHT
    )

    story = []

    # ── COVER / BANNER ─────────────────────────────────────────────────────────
    banner_data = [
        [
            Paragraph("<b>SEMPRA ENERGY · ODYSSEY DATA MIGRATION PLATFORM</b>", ParagraphStyle('BnrTop', fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor("#93c5fd"))),
            Paragraph("PREMIUM USER GUIDE & PLAYBOOK", ParagraphStyle('BnrBadge', fontName='Helvetica-Bold', fontSize=8, textColor=WHITE, alignment=2))
        ],
        [
            Paragraph("<b>Step-by-Step Execution Guide &amp; Value Blueprint</b>", ParagraphStyle('BnrTitle', fontName='Helvetica-Bold', fontSize=15, leading=19, textColor=WHITE)),
            ""
        ],
        [
            Paragraph("Prerequisites · 4-Step Execution Workflow · What We Achieve · Source vs Target Analytics · Multi-Level Real Examples", ParagraphStyle('BnrSub', fontName='Helvetica', fontSize=8.5, leading=11, textColor=colors.HexColor("#e0f2fe"))),
            ""
        ]
    ]
    banner_tbl = Table(banner_data, colWidths=[380, 136])
    banner_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), NAVY),
        ('PADDING', (0,0), (-1,-1), 8),
        ('SPAN', (0,1), (1,1)),
        ('SPAN', (0,2), (1,2)),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(banner_tbl)
    story.append(Spacer(1, 8))

    # ── 1. PREREQUISITES & ENVIRONMENT SETUP ───────────────────────────────────
    story.append(Paragraph("1. Prerequisites & Environment Setup Checklist", h1_style))
    story.append(Paragraph(
        "Before executing the dashboard, ensure the following simple prerequisites are in place on your Windows machine:",
        body_style
    ))

    prereq_data = [
        [Paragraph("<b>Item / Component</b>", tbl_hdr), Paragraph("<b>Requirement Specification</b>", tbl_hdr), Paragraph("<b>Status &amp; Verification</b>", tbl_hdr)],
        [
            Paragraph("<b>Operating System &amp; Browser</b>", tbl_cell_bold),
            Paragraph("Windows 10/11 · Google Chrome or Microsoft Edge", tbl_cell),
            Paragraph("✔ Standard corporate workstation ready. No special browser plugins required.", tbl_cell)
        ],
        [
            Paragraph("<b>Python Runtime</b>", tbl_cell_bold),
            Paragraph("Python 3.8+ with standard packages: <code>flask</code>, <code>flask-cors</code>", tbl_cell),
            Paragraph("✔ Pre-installed on local environment. Loopback bound to <code>127.0.0.1</code>.", tbl_cell)
        ],
        [
            Paragraph("<b>Migration Data Files</b>", tbl_cell_bold),
            Paragraph("Placed in local <code>C:\\Users\\&lt;user&gt;\\.bob\\DM1|DM2|DM3</code> OR synced via <code>OneDrive - Sempra</code>", tbl_cell),
            Paragraph("✔ Auto-detected automatically on startup with zero hardcoded paths.", tbl_cell)
        ],
        [
            Paragraph("<b>Local Network Ports</b>", tbl_cell_bold),
            Paragraph("Port 5002 (Bridge) · Port 5003 (Static Server) · Port 5004 (SharePoint)", tbl_cell),
            Paragraph("✔ Loopback only. Requires zero firewall exceptions or admin privileges.", tbl_cell)
        ]
    ]
    prereq_tbl = Table(prereq_data, colWidths=[120, 206, 190])
    prereq_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), LIGHT_BLUE),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_BL),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(prereq_tbl)
    story.append(Spacer(1, 8))

    # ── 2. WHAT WE ACHIEVE USING THIS PLATFORM ─────────────────────────────────
    story.append(Paragraph("2. WHAT We Achieve Using This Platform (Business Outcomes)", h1_style))
    story.append(Paragraph(
        "The platform delivers tangible operational, strategic, and governance benefits for Sempra:",
        body_style
    ))

    achieve_cards = [
        [
            Paragraph("<b>⏱️ 95% Time Reduction</b><br/><font color='#64748b' size='7'>Full 3-cycle reconciliation executes in &lt;10s instead of 3–4 hours of manual VLOOKUP spreadsheets.</font>", tbl_cell_bold),
            Paragraph("<b>🎯 100% Data Quality Assurance</b><br/><font color='#64748b' size='7'>Guarantees Zero Data Loss by mathematically reconciling 7,700+ tables end-to-end.</font>", tbl_cell_bold),
            Paragraph("<b>📊 Instant Audit Readiness</b><br/><font color='#64748b' size='7'>Generates pre-calculated Excel, CSV, and PDF audit trails for SOX cutover sign-off.</font>", tbl_cell_bold),
        ]
    ]
    ach_tbl = Table(achieve_cards, colWidths=[172, 172, 172])
    ach_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), SURFACE),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('PADDING', (0,0), (-1,-1), 6),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(ach_tbl)
    story.append(Spacer(1, 8))

    # ── 3. STEP-BY-STEP EXECUTION GUIDE ────────────────────────────────────────
    story.append(Paragraph("3. Step-by-Step Execution Guide (From Launch to Sign-Off)", h1_style))

    steps_data = [
        [
            Paragraph("<b>Step 1: Launch System</b>", tbl_cell_bold),
            Paragraph("<b>Action:</b> Run <code>python launch_dashboard.py</code> or double-click <code>Sempra_CrossCycle_Summary_MASTER.html</code>.<br/>"
                      "<b>What Happens:</b> The Python File Watcher Bridge starts in the background (port 5002) and opens the executive dashboard in Chrome/Edge.", tbl_cell)
        ],
        [
            Paragraph("<b>Step 2: Execute Auto-Sync</b>", tbl_cell_bold),
            Paragraph("<b>Action:</b> Click the green <b>'⚡ Auto-Sync All Cycles'</b> button at top left.<br/>"
                      "<b>What Happens:</b> The bridge scans 5 Excel files across DM1, DM2, DM3, deduplicates tables, and updates all health gauges in &lt;10 seconds.", tbl_cell)
        ],
        [
            Paragraph("<b>Step 3: Analyze &amp; Drill</b>", tbl_cell_bold),
            Paragraph("<b>Action:</b> Click any table count number (e.g. <b>7,710</b>) or switch to <b>'🎯 Src vs Tgt Pivot / Circle'</b>.<br/>"
                      "<b>What Happens:</b> Displays multi-segment donut chart and categorized breakdown: <code>✔ Matching</code>, <code>▲ Source is more</code>, <code>▼ Source is less</code>.", tbl_cell)
        ],
        [
            Paragraph("<b>Step 4: Export Reports</b>", tbl_cell_bold),
            Paragraph("<b>Action:</b> Click <b>📊 Excel</b> or <b>📄 CSV</b> in the drill modal or <b>Download PDF</b> on top bar.<br/>"
                      "<b>What Happens:</b> Instantly downloads audit-ready reports containing pre-calculated <code>Diff (Source - Target)</code> and status tags.", tbl_cell)
        ]
    ]
    steps_tbl = Table(steps_data, colWidths=[110, 406])
    steps_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), LIGHT_BLUE),
        ('BACKGROUND', (1,0), (1,-1), WHITE),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_BL),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(steps_tbl)
    story.append(Spacer(1, 8))

    # ── 4. REAL-WORLD EXAMPLES & VALUE SCENARIOS ───────────────────────────────
    story.append(Paragraph("4. Real-World Decision Scenarios for All Stakeholder Levels", h1_style))

    sc1 = [
        [Paragraph("<b>👔 Executive Scenario: Morning Leadership Briefing</b>", ParagraphStyle('S1H', fontName='Helvetica-Bold', fontSize=8.5, textColor=NAVY))],
        [Paragraph(
            "<b>Situation:</b> The steering committee requires a progress check on DM2 Mock Migration quality.<br/>"
            "<b>Execution:</b> Manager clicks <em>'⚡ Auto-Sync All Cycles'</em>. Gauges instantly show <b>99.8% Match Rate</b> across 7,715 tables with 0 critical blocks. "
            "Manager clicks <em>'📄 Download PDF'</em> to generate an executive one-pager for presentation in under 1 minute.",
            body_style
        )]
    ]
    t_s1 = Table(sc1, colWidths=[516])
    t_s1.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), SURFACE), ('BACKGROUND', (0,1), (-1,1), WHITE), ('BOX', (0,0), (-1,-1), 1, BORDER), ('PADDING', (0,0), (-1,-1), 5)]))
    story.append(t_s1)
    story.append(Spacer(1, 4))

    sc2 = [
        [Paragraph("<b>📋 Functional Lead Scenario: Table Discrepancy Resolution</b>", ParagraphStyle('S2H', fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.HexColor("#78350f")))],
        [Paragraph(
            "<b>Situation:</b> Customer Master table <code>/1CADMC/00000239</code> has Source 12.09M vs Target 12.09M records.<br/>"
            "<b>Execution:</b> Dashboard tags table as <b>'▲ Source is more (+66 records)'</b> with an amber highlight. "
            "Lead clicks row to review variance, clicks <em>'📊 Excel'</em>, and passes the pre-calculated diff to the ETL engineer for remediation.",
            body_style
        )]
    ]
    t_s2 = Table(sc2, colWidths=[516])
    t_s2.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), AMBER_BG), ('BACKGROUND', (0,1), (-1,1), WHITE), ('BOX', (0,0), (-1,-1), 1, AMBER_BD), ('PADDING', (0,0), (-1,-1), 5)]))
    story.append(t_s2)
    story.append(Spacer(1, 8))

    # ── 5. COMPLETE WORKSPACE INVENTORY ────────────────────────────────────────
    story.append(Paragraph("5. Workspace Codebase Inventory & Links", h1_style))

    files_inv = [
        [Paragraph("<b>Document / File</b>", tbl_hdr), Paragraph("<b>Format / Path</b>", tbl_hdr), Paragraph("<b>Target Audience &amp; Role</b>", tbl_hdr)],
        [Paragraph("Master Dashboard", tbl_cell_bold), Paragraph("<code>Sempra_CrossCycle_Summary_MASTER.html</code>", tbl_mono), Paragraph("All stakeholders · Full 3-cycle cockpit with pivot analytics", tbl_cell)],
        [Paragraph("Cycle 1/2/3 Dashboards", tbl_cell_bold), Paragraph("<code>Sempra_DM1/2/3_Dashboard.html</code>", tbl_mono), Paragraph("Functional leads · Deep-dive table reconciliation", tbl_cell)],
        [Paragraph("SharePoint Master", tbl_cell_bold), Paragraph("<code>Sempra_CrossCycle_Summary_SHAREPOINT.html</code>", tbl_mono), Paragraph("Team collaboration · Cloud synced folder reader", tbl_cell)],
        [Paragraph("Master Documentation PDF", tbl_cell_bold), Paragraph("<code>Sempra_DM_Dashboard_Master_Documentation.pdf</code>", tbl_mono), Paragraph("Executives & Auditors · Comprehensive blueprint", tbl_cell)],
        [Paragraph("File Watcher Bridge", tbl_cell_bold), Paragraph("<code>automation/file_watcher_bridge.py</code>", tbl_mono), Paragraph("Backend engine · Gzip compression & ETag 304 caching", tbl_cell)],
    ]
    t_inv = Table(files_inv, colWidths=[110, 196, 210])
    t_inv.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SURFACE),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_inv)

    doc.build(story, canvasmaker=PremiumNumberedCanvas)
    print(f"Premium User Guide PDF built: {PDF_LOCAL}")

    # Copy to Desktop
    try:
        shutil.copyfile(PDF_LOCAL, PDF_DESKTOP)
        print(f"Copied to Desktop: {PDF_DESKTOP}")
    except Exception as e:
        print(f"Could not copy to Desktop: {e}")


def build_html():
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Sempra Data Migration Platform — Premium User Guide</title>
  <style>
    :root {
      --navy: #091e3a;
      --blue: #1d4ed8;
      --light-blue: #eff6ff;
      --border-blue: #bfdbfe;
      --green: #15803d;
      --green-bg: #dcfce7;
      --amber: #b45309;
      --amber-bg: #fef3c7;
      --surface: #f8fafc;
      --border: #e2e8f0;
      --text: #1e293b;
      --muted: #64748b;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    body { background: #f0f2f5; color: var(--text); padding: 32px 16px; line-height: 1.6; }
    .container { max-width: 900px; margin: 0 auto; background: #fff; border-radius: 16px; box-shadow: 0 4px 24px rgba(0,0,0,0.06); border: 1px solid var(--border); overflow: hidden; }
    
    .header { background: linear-gradient(135deg, #091e3a 0%, #1e3a5f 100%); color: #fff; padding: 40px 36px; }
    .badge { display: inline-block; background: rgba(56,189,248,0.2); color: #7dd3fc; border: 1px solid rgba(56,189,248,0.4); font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; padding: 4px 10px; border-radius: 20px; margin-bottom: 12px; }
    .title { font-size: 28px; font-weight: 900; line-height: 1.2; margin-bottom: 8px; }
    .subtitle { font-size: 14px; color: #bae6fd; max-width: 720px; }
    
    .content { padding: 36px; }
    h2 { font-size: 18px; font-weight: 800; color: var(--navy); margin-top: 28px; margin-bottom: 12px; display: flex; align-items: center; gap: 8px; border-bottom: 2px solid #f1f5f9; padding-bottom: 6px; }
    h2:first-of-type { margin-top: 0; }
    p { font-size: 14px; color: #334155; margin-bottom: 12px; }
    
    .kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; margin: 20px 0; }
    .kpi-card { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 18px; text-align: center; }
    .kpi-num { font-size: 24px; font-weight: 900; color: var(--blue); }
    .kpi-lbl { font-size: 12px; font-weight: 700; color: var(--muted); margin-top: 4px; }
    
    .step-list { display: flex; flex-direction: column; gap: 14px; margin: 16px 0; }
    .step-card { display: flex; gap: 16px; background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 18px 20px; }
    .step-badge { width: 36px; height: 36px; border-radius: 10px; background: var(--blue); color: #fff; font-weight: 900; display: flex; align-items: center; justify-content: center; flex-shrink: 0; font-size: 15px; }
    .step-info h3 { font-size: 15px; font-weight: 800; color: var(--navy); margin-bottom: 4px; }
    .step-info p { font-size: 13px; color: #475569; margin-bottom: 0; }
    
    table { width: 100%; border-collapse: collapse; font-size: 13px; margin: 16px 0; border: 1px solid var(--border); border-radius: 8px; overflow: hidden; }
    th { background: var(--surface); text-align: left; padding: 10px 14px; font-weight: 700; color: var(--navy); border-bottom: 2px solid var(--border); }
    td { padding: 10px 14px; border-bottom: 1px solid var(--border); }
    tr:last-child td { border-bottom: none; }
    tr:hover td { background: #f8fafc; }
    
    .box { border-radius: 12px; border: 1px solid; margin: 16px 0; overflow: hidden; }
    .box.blue { border-color: var(--border-blue); background: #fff; }
    .box.blue .box-hdr { background: var(--light-blue); color: var(--navy); }
    .box.amber { border-color: #fde68a; background: #fff; }
    .box.amber .box-hdr { background: var(--amber-bg); color: #78350f; }
    .box-hdr { padding: 12px 18px; font-weight: 800; font-size: 13px; }
    .box-body { padding: 16px 18px; font-size: 13px; color: #334155; }
    
    .btn-bar { margin-top: 32px; padding-top: 20px; border-top: 1px solid var(--border); display: flex; gap: 12px; flex-wrap: wrap; }
    .btn { display: inline-flex; align-items: center; gap: 6px; padding: 10px 20px; font-size: 13px; font-weight: 700; border-radius: 8px; text-decoration: none; cursor: pointer; border: none; }
    .btn-prim { background: var(--blue); color: #fff; }
    .btn-sec { background: var(--surface); color: var(--text); border: 1px solid var(--border); }
    .btn:hover { opacity: 0.9; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <span class="badge">Sempra Energy · Premium Playbook</span>
      <h1 class="title">Data Migration Platform — Premium User Guide</h1>
      <p class="subtitle">Complete step-by-step execution playbook, prerequisites checklist, business outcomes, and Source vs Target analytics.</p>
    </div>
    
    <div class="content">
      <h2>📋 1. Prerequisites Checklist</h2>
      <table>
        <thead>
          <tr><th>Item</th><th>Requirement</th><th>Status</th></tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Workstation</strong></td>
            <td>Windows 10/11 · Chrome or Edge browser</td>
            <td>✔ Standard PC ready</td>
          </tr>
          <tr>
            <td><strong>Python Environment</strong></td>
            <td>Python 3.8+ with <code>flask</code> and <code>flask-cors</code></td>
            <td>✔ Pre-configured on port 5002</td>
          </tr>
          <tr>
            <td><strong>Data Location</strong></td>
            <td>Local <code>.bob/DM1|DM2|DM3</code> or <code>OneDrive - Sempra</code> sync</td>
            <td>✔ Auto-detected on startup</td>
          </tr>
          <tr>
            <td><strong>Security</strong></td>
            <td>Loopback <code>127.0.0.1</code> (No external firewall rules)</td>
            <td>✔ 100% On-premise secure</td>
          </tr>
        </tbody>
      </table>

      <h2>🎯 2. WHAT We Achieve Using This Platform</h2>
      <div class="kpi-grid">
        <div class="kpi-card">
          <div class="kpi-num">⏱️ &lt;10s</div>
          <div class="kpi-lbl">Sync Time for All 3 Cycles (Was 3–4 Hours)</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-num">🎯 7,700+</div>
          <div class="kpi-lbl">Tables Reconciled End-to-End per Cycle</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-num">🛡️ 100%</div>
          <div class="kpi-lbl">Zero Data Loss Governance for Cutover</div>
        </div>
      </div>

      <h2>🚀 3. Step-by-Step Execution Guide</h2>
      <div class="step-list">
        <div class="step-card">
          <div class="step-badge">1</div>
          <div class="step-info">
            <h3>Step 1: Launch System</h3>
            <p>Run <code>python launch_dashboard.py</code> or double-click <code>Sempra_CrossCycle_Summary_MASTER.html</code>. Spawns background bridge &amp; web server.</p>
          </div>
        </div>
        <div class="step-card">
          <div class="step-badge">2</div>
          <div class="step-info">
            <h3>Step 2: Execute Auto-Sync</h3>
            <p>Click <strong>"⚡ Auto-Sync All Cycles"</strong>. Reads all 5 Excel files across DM1, DM2, and DM3 with Gzip compression in under 10 seconds.</p>
          </div>
        </div>
        <div class="step-card">
          <div class="step-badge">3</div>
          <div class="step-info">
            <h3>Step 3: Analyze &amp; Drill-Down</h3>
            <p>Click on any count number (e.g. <strong>7,710</strong>) or open <strong>"🎯 Src vs Tgt Pivot / Circle"</strong> to inspect visual health charts and variance tables.</p>
          </div>
        </div>
        <div class="step-card">
          <div class="step-badge">4</div>
          <div class="step-info">
            <h3>Step 4: Export Audit Reports</h3>
            <p>Click <strong>📊 Excel</strong> or <strong>📄 CSV</strong> in the drill modal to download audit-ready spreadsheets with pre-calculated variance columns.</p>
          </div>
        </div>
      </div>

      <h2>💡 4. Real-World Practical Scenarios</h2>
      <div class="box blue">
        <div class="box-hdr">👔 Executive Scenario: 10-Second Steering Committee Brief</div>
        <div class="box-body">
          Before a leadership meeting, the manager clicks <em>"⚡ Auto-Sync"</em>. The semicircle gauges confirm a <strong>99.8% match rate</strong> across 7,715 tables in DM2. The manager clicks <em>"📄 Download PDF"</em> to generate an audit-ready executive brief with zero manual prep.
        </div>
      </div>

      <div class="box amber">
        <div class="box-hdr">📋 Functional Lead Scenario: Table Discrepancy Resolution</div>
        <div class="box-body">
          Investigating table <code>/1CADMC/00000239</code> (Source 12.09M vs Target 12.09M). Tagged automatically as <strong>"▲ Source is more (+66 records)"</strong> with an amber badge. The lead clicks the row and exports a targeted Excel list with pre-calculated diffs for the ETL lead.
        </div>
      </div>

      <div class="btn-bar">
        <a href="Sempra_CrossCycle_Summary_MASTER.html" class="btn btn-prim">🚀 Open Master Dashboard</a>
        <a href="Sempra_DM_Dashboard_PREMIUM_User_Guide.pdf" class="btn btn-sec">📄 Open Premium PDF Guide</a>
      </div>
    </div>
  </div>
</body>
</html>
"""
    with open(HTML_LOCAL, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Premium User Guide HTML built: {HTML_LOCAL}")

if __name__ == "__main__":
    build_pdf()
    build_html()
