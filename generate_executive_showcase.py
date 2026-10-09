"""
================================================================================
  SEMPRA DATA MIGRATION DASHBOARD — EXECUTIVE SHOWCASE GENERATOR
  Generates a polished, non-technical, business-first Executive User Guide (PDF & HTML)
  Focuses on business value, real-world examples, and executive workflows.
================================================================================
"""
import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

PDF_FILENAME = "Sempra_DM_Dashboard_Executive_Guide.pdf"
HTML_FILENAME = "Sempra_DM_Dashboard_Executive_Guide.html"

# ── Color Palette ─────────────────────────────────────────────────────────────
NAVY       = colors.HexColor("#0f2744")
BLUE_ACC   = colors.HexColor("#1d4ed8")
LIGHT_BLUE = colors.HexColor("#eff6ff")
BORDER_BL  = colors.HexColor("#bfdbfe")
DARK_GRAY  = colors.HexColor("#1e293b")
TEXT_MUTED = colors.HexColor("#475569")
GREEN      = colors.HexColor("#15803d")
GREEN_BG   = colors.HexColor("#dcfce7")
AMBER      = colors.HexColor("#b45309")
AMBER_BG   = colors.HexColor("#fef3c7")
SURFACE    = colors.HexColor("#f8fafc")
BORDER     = colors.HexColor("#e2e8f0")

class NumberedCanvas(canvas.Canvas):
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
        self.setFont("Helvetica", 8)
        self.setFillColor(TEXT_MUTED)

        # Running Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 11 * inch - 36, "Sempra Data Migration — Executive Showcase & User Guide")
            self.drawRightString(8.5 * inch - 54, 11 * inch - 36, "Confidential — Internal Management")
            self.setStrokeColor(BORDER)
            self.setLineWidth(0.5)
            self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)

        # Running Footer
        self.drawString(54, 34, "Sempra Odyssey Data Migration Platform · Executive Guide")
        self.drawRightString(8.5 * inch - 54, 34, f"Page {self._pageNumber} of {page_count}")
        self.setStrokeColor(BORDER)
        self.setLineWidth(0.5)
        self.line(54, 46, 8.5 * inch - 54, 46)

        self.restoreState()


def build_pdf():
    doc = SimpleDocTemplate(
        PDF_FILENAME,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=NAVY,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=BLUE_ACC,
        spaceAfter=14
    )

    h1_style = ParagraphStyle(
        'DocH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=NAVY,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'DocH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=BLUE_ACC,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=DARK_GRAY,
        spaceAfter=6
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=NAVY
    )

    story = []

    # ── HEADER BANNER ──────────────────────────────────────────────────────────
    banner_data = [
        [
            Paragraph("<b>SEMPRA ENERGY — DATA MIGRATION PLATFORM</b>", ParagraphStyle('BnrTop', fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor("#93c5fd"))),
            Paragraph("EXECUTIVE EDITION", ParagraphStyle('BnrBadge', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white, alignment=2))
        ],
        [
            Paragraph("<b>Executive Showcase & Non-Technical User Guide</b>", ParagraphStyle('BnrTitle', fontName='Helvetica-Bold', fontSize=18, leading=22, textColor=colors.white)),
            ""
        ],
        [
            Paragraph("A complete visual guide to 3-cycle data validation, automated reconciliations, and leadership reporting.", ParagraphStyle('BnrSub', fontName='Helvetica', fontSize=10, leading=13, textColor=colors.HexColor("#e0f2fe"))),
            ""
        ]
    ]
    banner_tbl = Table(banner_data, colWidths=[380, 124])
    banner_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), NAVY),
        ('PADDING', (0,0), (-1,-1), 10),
        ('SPAN', (0,1), (1,1)),
        ('SPAN', (0,2), (1,2)),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(banner_tbl)
    story.append(Spacer(1, 14))

    # ── 1. BUSINESS VALUE OVERVIEW ─────────────────────────────────────────────
    story.append(Paragraph("1. Executive Overview — What This Platform Solves", h1_style))
    story.append(Paragraph(
        "During large-scale SAP data migrations, leadership requires instant visibility into whether <b>100% of data from legacy systems was correctly extracted, migrated, and loaded into the target SAP system</b>. "
        "Traditionally, this requires teams of analysts spending several hours manually cross-referencing massive Excel sheets with VLOOKUPs.",
        body_style
    ))
    story.append(Paragraph(
        "This platform replaces that entire manual process with an <b>instant, automated, interactive executive dashboard</b> that consolidates all 3 Migration Cycles (DM1, DM2, DM3) into a single screen with real-time health indicators.",
        body_style
    ))

    # KPI summary cards
    kpi_data = [
        [
            Paragraph("<b>⚡ 10 Seconds</b><br/><font color='#64748b' size='8'>Full 3-Cycle Sync Time (Was 3+ Hours)</font>", callout_style),
            Paragraph("<b>🎯 7,700+ Tables</b><br/><font color='#64748b' size='8'>Reconciled End-to-End per Cycle</font>", callout_style),
            Paragraph("<b>✔ 100% Automated</b><br/><font color='#64748b' size='8'>Zero Manual Calculation Errors</font>", callout_style),
        ]
    ]
    kpi_tbl = Table(kpi_data, colWidths=[168, 168, 168])
    kpi_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), SURFACE),
        ('BOX', (0,0), (-1,-1), 1, BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER),
        ('PADDING', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(kpi_tbl)
    story.append(Spacer(1, 14))

    # ── 2. REAL-WORLD BUSINESS EXAMPLES ────────────────────────────────────────
    story.append(Paragraph("2. Real-World Business Examples (How It Works in Practice)", h1_style))
    story.append(Paragraph(
        "Here is how a manager or project lead uses the dashboard for everyday decision-making:",
        body_style
    ))

    # Example 1
    ex1_data = [
        [Paragraph("<b>Scenario A: Morning Executive Briefing in 3 Clicks</b>", ParagraphStyle('ExHdr', fontName='Helvetica-Bold', fontSize=10, textColor=NAVY))],
        [Paragraph(
            "<b>The Challenge:</b> Management needs an update on whether DM1, DM2, and DM3 datasets have been successfully refreshed.<br/>"
            "<b>The Solution:</b> Open the master dashboard and click <b>'⚡ Auto-Sync All Cycles'</b>. In under 10 seconds, all 5 reference and migration logs are scanned, validated, and visually summarized with clear green/amber health gauges.",
            body_style
        )]
    ]
    ex1_tbl = Table(ex1_data, colWidths=[504])
    ex1_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), LIGHT_BLUE),
        ('BACKGROUND', (0,1), (-1,1), colors.white),
        ('BOX', (0,0), (-1,-1), 1, BORDER_BL),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(ex1_tbl)
    story.append(Spacer(1, 8))

    # Example 2
    ex2_data = [
        [Paragraph("<b>Scenario B: Spotting Record Discrepancies Instantly (Source vs. Target)</b>", ParagraphStyle('ExHdr2', fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor("#78350f")))],
        [Paragraph(
            "<b>Example Table:</b> <code>/1CADMC/00000239</code> (Customer Master Extension)<br/>"
            "• <b>Source System Count:</b> 12,098,214 records<br/>"
            "• <b>Target SAP Count:</b> 12,098,148 records<br/>"
            "• <b>Dashboard Result:</b> Automatically tags this table as <b>'▲ Source is more (+66 records)'</b> with an amber highlight.<br/>"
            "• <b>Action:</b> The manager clicks on the table row to view full details or exports a clean Excel list for the migration team to review.",
            body_style
        )]
    ]
    ex2_tbl = Table(ex2_data, colWidths=[504])
    ex2_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), AMBER_BG),
        ('BACKGROUND', (0,1), (-1,1), colors.white),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#fde68a")),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(ex2_tbl)
    story.append(Spacer(1, 14))

    # ── 3. VISUAL SUMMARY & PIVOT CAPABILITIES ─────────────────────────────────
    story.append(Paragraph("3. Interactive Circle & Pivot Breakdown", h1_style))
    story.append(Paragraph(
        "When drilling into any cycle, leadership can switch to the <b>'🎯 Src vs Tgt Pivot / Circle'</b> view for an executive visual breakdown:",
        body_style
    ))

    # Status breakdown table
    breakdown_data = [
        [Paragraph("<b>Status Category</b>", ParagraphStyle('BH', fontName='Helvetica-Bold', fontSize=9, textColor=NAVY)),
         Paragraph("<b>Color Indicator</b>", ParagraphStyle('BH', fontName='Helvetica-Bold', fontSize=9, textColor=NAVY)),
         Paragraph("<b>Business Meaning</b>", ParagraphStyle('BH', fontName='Helvetica-Bold', fontSize=9, textColor=NAVY)),
         Paragraph("<b>Manager Action</b>", ParagraphStyle('BH', fontName='Helvetica-Bold', fontSize=9, textColor=NAVY))],
        [Paragraph("<b>✔ Matching</b>", body_style),
         Paragraph("<font color='#15803d'><b>Green</b></font>", body_style),
         Paragraph("Source and Target counts match 100% (Diff = 0).", body_style),
         Paragraph("Ready for sign-off.", body_style)],
        [Paragraph("<b>▲ Source is More</b>", body_style),
         Paragraph("<font color='#b45309'><b>Amber</b></font>", body_style),
         Paragraph("Source has extra records not yet reflected in Target.", body_style),
         Paragraph("Filter out and share with ETL leads.", body_style)],
        [Paragraph("<b>▼ Source is Less</b>", body_style),
         Paragraph("<font color='#0369a1'><b>Blue</b></font>", body_style),
         Paragraph("Target system contains additional created records.", body_style),
         Paragraph("Review configuration/initialization records.", body_style)],
        [Paragraph("<b>— N/A / Missing</b>", body_style),
         Paragraph("<font color='#64748b'><b>Grey</b></font>", body_style),
         Paragraph("Table not in current cycle scope.", body_style),
         Paragraph("No action required.", body_style)],
    ]
    breakdown_tbl = Table(breakdown_data, colWidths=[110, 80, 204, 110])
    breakdown_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SURFACE),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(breakdown_tbl)
    story.append(Spacer(1, 14))

    # ── 4. HOW TO USE IN 3 EASY STEPS ──────────────────────────────────────────
    story.append(Paragraph("4. How to Use the Dashboard in 3 Simple Steps", h1_style))
    
    steps_data = [
        [
            Paragraph("<b>Step 1: Launch</b>", ParagraphStyle('St1', fontName='Helvetica-Bold', fontSize=10, textColor=NAVY)),
            Paragraph("Open <code>Sempra_CrossCycle_Summary_MASTER.html</code> in any web browser (Chrome, Edge, etc.).", body_style)
        ],
        [
            Paragraph("<b>Step 2: Sync</b>", ParagraphStyle('St2', fontName='Helvetica-Bold', fontSize=10, textColor=NAVY)),
            Paragraph("Click the <b>'⚡ Auto-Sync All Cycles'</b> button at top left. The dashboard automatically scans all cycle files and updates all charts.", body_style)
        ],
        [
            Paragraph("<b>Step 3: Review & Export</b>", ParagraphStyle('St3', fontName='Helvetica-Bold', fontSize=10, textColor=NAVY)),
            Paragraph("Click on any number (e.g. <b>7,710</b>) to inspect individual tables, switch to the <b>Circle/Pivot View</b>, or click <b>📊 Excel</b> to export audit-ready spreadsheets.", body_style)
        ]
    ]
    steps_tbl = Table(steps_data, colWidths=[120, 384])
    steps_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), LIGHT_BLUE),
        ('BACKGROUND', (1,0), (1,-1), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_BL),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(steps_tbl)
    story.append(Spacer(1, 14))

    # ── 5. SUMMARY & BUSINESS BENEFITS ─────────────────────────────────────────
    story.append(Paragraph("5. Summary of Business Benefits for Sempra Leadership", h1_style))
    summary_bullets = [
        "• <b>Full 3-Cycle Governance:</b> Track DM1, DM2, and DM3 side-by-side to observe cycle-over-cycle data quality improvement.",
        "• <b>Audit-Ready Compliance:</b> Generates timestamped PDF, Excel, and CSV deliverables for steering committees and compliance sign-offs.",
        "• <b>100% On-Premise & Secure:</b> Runs locally inside Sempra's secure environment with zero external cloud dependencies or licensing fees.",
        "• <b>Intuitive for Non-Technical Users:</b> Clean color-coded gauges and single-click drill-downs allow any stakeholder to verify data migration health in seconds."
    ]
    for b in summary_bullets:
        story.append(Paragraph(b, body_style))
    
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF built successfully: {PDF_FILENAME}")


def build_html():
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Sempra Data Migration — Executive Showcase & User Guide</title>
  <style>
    :root {
      --navy: #0f2744;
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
    body { background: #f1f5f9; color: var(--text); padding: 32px 16px; line-height: 1.6; }
    .container { max-width: 860px; margin: 0 auto; background: #fff; border-radius: 16px; box-shadow: 0 4px 24px rgba(0,0,0,0.06); border: 1px solid var(--border); overflow: hidden; }
    
    .header { background: linear-gradient(135deg, #0f2744 0%, #1e3a5f 100%); color: #fff; padding: 36px 32px; }
    .badge { display: inline-block; background: rgba(56,189,248,0.2); color: #7dd3fc; border: 1px solid rgba(56,189,248,0.4); font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; padding: 4px 10px; border-radius: 20px; margin-bottom: 12px; }
    .title { font-size: 26px; font-weight: 900; line-height: 1.2; margin-bottom: 8px; }
    .subtitle { font-size: 14px; color: #bae6fd; max-width: 680px; }
    
    .content { padding: 32px; }
    h2 { font-size: 18px; font-weight: 800; color: var(--navy); margin-top: 28px; margin-bottom: 12px; display: flex; align-items: center; gap: 8px; border-bottom: 2px solid #f1f5f9; padding-bottom: 6px; }
    h2:first-of-type { margin-top: 0; }
    p { font-size: 14px; color: #334155; margin-bottom: 12px; }
    
    .kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; margin: 20px 0; }
    .kpi-card { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 18px; text-align: center; }
    .kpi-num { font-size: 24px; font-weight: 900; color: var(--blue); }
    .kpi-lbl { font-size: 12px; font-weight: 700; color: var(--muted); margin-top: 4px; }
    
    .scenario-box { border-radius: 12px; border: 1px solid; margin: 16px 0; overflow: hidden; }
    .scenario-box.blue { border-color: var(--border-blue); background: #fff; }
    .scenario-box.blue .sc-hdr { background: var(--light-blue); color: var(--navy); }
    .scenario-box.amber { border-color: #fde68a; background: #fff; }
    .scenario-box.amber .sc-hdr { background: var(--amber-bg); color: #78350f; }
    .sc-hdr { padding: 12px 18px; font-weight: 800; font-size: 13px; }
    .sc-body { padding: 16px 18px; font-size: 13px; color: #334155; }
    
    table { width: 100%; border-collapse: collapse; font-size: 13px; margin: 16px 0; border: 1px solid var(--border); border-radius: 8px; overflow: hidden; }
    th { background: var(--surface); text-align: left; padding: 10px 14px; font-weight: 700; color: var(--navy); border-bottom: 2px solid var(--border); }
    td { padding: 10px 14px; border-bottom: 1px solid var(--border); }
    tr:last-child td { border-bottom: none; }
    tr:hover td { background: #f8fafc; }
    
    .step-list { display: flex; flex-direction: column; gap: 12px; margin: 16px 0; }
    .step-item { display: flex; gap: 14px; background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 14px 18px; }
    .step-num { width: 32px; height: 32px; border-radius: 50%; background: var(--blue); color: #fff; font-weight: 800; display: flex; align-items: center; justify-content: center; flex-shrink: 0; font-size: 14px; }
    .step-content h3 { font-size: 14px; font-weight: 800; color: var(--navy); margin-bottom: 2px; }
    .step-content p { font-size: 12px; color: var(--muted); margin-bottom: 0; }
    
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
      <span class="badge">Sempra Energy · Executive Showcase</span>
      <h1 class="title">Data Migration Executive Showcase &amp; User Guide</h1>
      <p class="subtitle">A visual, non-technical overview of 3-cycle migration reconciliation, automated validation, and leadership decision-making.</p>
    </div>
    
    <div class="content">
      <h2>📊 1. Executive Summary — What This Platform Solves</h2>
      <p>During SAP data migration, management requires complete confidence that <strong>100% of legacy records have been successfully extracted, transformed, and loaded into SAP without record loss</strong>.</p>
      <p>This platform replaces manual, error-prone spreadsheets with an <strong>instant, automated executive dashboard</strong> that monitors <strong>DM1 (Mock 1), DM2 (Mock 2), and DM3 (Cutover/Dry Run)</strong> simultaneously.</p>
      
      <div class="kpi-grid">
        <div class="kpi-card">
          <div class="kpi-num">⚡ &lt;10s</div>
          <div class="kpi-lbl">Sync Time for All 3 Cycles (Was 3+ Hours)</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-num">🎯 7,700+</div>
          <div class="kpi-lbl">Tables Reconciled per Cycle</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-num">✔ 100%</div>
          <div class="kpi-lbl">Automated Error-Free Calculations</div>
        </div>
      </div>

      <h2>💡 2. Real-World Business Examples</h2>
      
      <div class="scenario-box blue">
        <div class="sc-hdr">Scenario A: Morning Status Update in 3 Clicks</div>
        <div class="sc-body">
          <strong>The Challenge:</strong> Leadership needs a status update on whether migration data files have been refreshed.<br/>
          <strong>The Dashboard Solution:</strong> Click <strong>"⚡ Auto-Sync All Cycles"</strong>. All reference and export logs are scanned, reconciled, and updated across DM1, DM2, and DM3 with color-coded health indicators in under 10 seconds.
        </div>
      </div>

      <div class="scenario-box amber">
        <div class="sc-hdr">Scenario B: Spotting Record Count Gaps Instantly (Source vs. Target)</div>
        <div class="sc-body">
          <strong>Example Table:</strong> <code>/1CADMC/00000239</code> (Customer Master Extension)<br/>
          • <strong>Source System:</strong> 12,098,214 records<br/>
          • <strong>Target SAP System:</strong> 12,098,148 records<br/>
          • <strong>Result:</strong> Tagged automatically as <strong>"▲ Source is more (+66 records)"</strong> with an amber badge.<br/>
          • <strong>Action:</strong> The manager clicks the row to inspect or exports a clean Excel list with pre-calculated variance for the ETL lead.
        </div>
      </div>

      <h2>🎯 3. Visual Health Indicators &amp; Pivot View</h2>
      <p>When reviewing any cycle, leadership can switch to the <strong>"🎯 Src vs Tgt Pivot / Circle"</strong> tab to view a visual breakdown:</p>
      
      <table>
        <thead>
          <tr>
            <th>Status Category</th>
            <th>Color Indicator</th>
            <th>Business Meaning</th>
            <th>Management Action</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>✔ Matching</strong></td>
            <td><strong style="color:var(--green)">Green</strong></td>
            <td>Source and Target counts match 100% (Diff = 0).</td>
            <td>Ready for sign-off.</td>
          </tr>
          <tr>
            <td><strong>▲ Source is More</strong></td>
            <td><strong style="color:var(--amber)">Amber</strong></td>
            <td>Source has extra records not yet in Target.</td>
            <td>Filter and assign to ETL lead.</td>
          </tr>
          <tr>
            <td><strong>▼ Source is Less</strong></td>
            <td><strong style="color:#0284c7">Blue</strong></td>
            <td>Target contains additional generated records.</td>
            <td>Verify target initialization data.</td>
          </tr>
          <tr>
            <td><strong>— N/A / Missing</strong></td>
            <td><strong style="color:var(--muted)">Grey</strong></td>
            <td>Table not in current cycle scope.</td>
            <td>No action required.</td>
          </tr>
        </tbody>
      </table>

      <h2>🚀 4. How to Use in 3 Simple Steps</h2>
      <div class="step-list">
        <div class="step-item">
          <div class="step-num">1</div>
          <div class="step-content">
            <h3>Open Dashboard</h3>
            <p>Launch <code>Sempra_CrossCycle_Summary_MASTER.html</code> in Chrome or Edge.</p>
          </div>
        </div>
        <div class="step-item">
          <div class="step-num">2</div>
          <div class="step-content">
            <h3>Click Auto-Sync</h3>
            <p>Click "⚡ Auto-Sync All Cycles" at the top-left to automatically ingest the latest files.</p>
          </div>
        </div>
        <div class="step-item">
          <div class="step-num">3</div>
          <div class="step-content">
            <h3>Review &amp; Export</h3>
            <p>Inspect visual health gauges, drill down into tables with 1 click, or export audit-ready Excel reports.</p>
          </div>
        </div>
      </div>

      <h2>🏆 5. Leadership Benefits</h2>
      <p>• <strong>Cross-Cycle Progress:</strong> Observe migration improvements directly across DM1 → DM2 → DM3.<br/>
         • <strong>Audit-Ready Deliverables:</strong> Downloadable PDF and Excel reports for steering committees.<br/>
         • <strong>Zero Cloud/Licensing Costs:</strong> Runs 100% locally on Sempra's secure workstations.</p>

      <div class="btn-bar">
        <a href="Sempra_CrossCycle_Summary_MASTER.html" class="btn btn-prim">🚀 Open Master Dashboard</a>
        <a href="Sempra_DM_Dashboard_Executive_Guide.pdf" class="btn btn-sec">📄 Download Executive PDF</a>
      </div>
    </div>
  </div>
</body>
</html>
"""
    with open(HTML_FILENAME, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"HTML built successfully: {HTML_FILENAME}")

if __name__ == "__main__":
    build_pdf()
    build_html()
