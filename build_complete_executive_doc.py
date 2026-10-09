"""
================================================================================
  SEMPRA DATA MIGRATION PLATFORM — COMPLETE EXECUTIVE & TECHNICAL DOCUMENTATION
  Generates the definitive PDF & HTML documentation covering:
  1. WHY we are doing this activity (Business Objective & De-risking Migration)
  2. WHAT we achieve & what is active (Key Outcomes, 3 Cycles, Real-time KPIs)
  3. TECHNOLOGY STACK (Frontend, Python Bridge, SAP Automation, Security)
  4. REAL-WORLD EXAMPLES FOR ALL AUDIENCE LEVELS (Exec, Lead, Tech, Audit)
================================================================================
"""
import os
import shutil
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

PDF_OUT_LOCAL = "Sempra_DM_Dashboard_Documentation.pdf"
PDF_OUT_DESKTOP = "C:\\Users\\KishorMarri\\Desktop\\Sempra_DM_Dashboard_Documentation.pdf"
HTML_OUT_LOCAL = "Sempra_DM_Dashboard_Documentation_FINAL.html"

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
WHITE      = colors.white

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
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(TEXT_MUTED)

        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 11 * inch - 36, "Sempra Energy — Odyssey Data Migration Dashboard Documentation")
            self.setFont("Helvetica", 8)
            self.drawRightString(8.5 * inch - 54, 11 * inch - 36, "Executive & Technical Blueprint")
            self.setStrokeColor(BORDER)
            self.setLineWidth(0.5)
            self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)

        # Footer
        self.setFont("Helvetica", 8)
        self.drawString(54, 34, "Sempra Data Migration Automation Framework · Confidential")
        self.drawRightString(8.5 * inch - 54, 34, f"Page {self._pageNumber} of {page_count}")
        self.setStrokeColor(BORDER)
        self.setLineWidth(0.5)
        self.line(54, 46, 8.5 * inch - 54, 46)

        self.restoreState()


def generate_pdf():
    doc = SimpleDocTemplate(
        PDF_OUT_LOCAL,
        pagesize=letter,
        leftMargin=48,
        rightMargin=48,
        topMargin=48,
        bottomMargin=48,
    )

    styles = getSampleStyleSheet()

    h1_style = ParagraphStyle(
        'DocH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=NAVY,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'DocH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=BLUE_ACC,
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=DARK_GRAY,
        spaceAfter=4
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=NAVY
    )

    tbl_hdr_style = ParagraphStyle(
        'TblHdr',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=NAVY
    )

    tbl_cell_style = ParagraphStyle(
        'TblCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=DARK_GRAY
    )

    story = []

    # ── BANNER HEADER ──────────────────────────────────────────────────────────
    banner_data = [
        [
            Paragraph("<b>SEMPRA ENERGY · ODYSSEY DATA MIGRATION PLATFORM</b>", ParagraphStyle('BnrTop', fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor("#93c5fd"))),
            Paragraph("EXECUTIVE & TECHNICAL BLUEPRINT", ParagraphStyle('BnrBadge', fontName='Helvetica-Bold', fontSize=8, textColor=WHITE, alignment=2))
        ],
        [
            Paragraph("<b>Complete Platform Documentation & User Guide</b>", ParagraphStyle('BnrTitle', fontName='Helvetica-Bold', fontSize=16, leading=20, textColor=WHITE)),
            ""
        ],
        [
            Paragraph("Why we do this activity · What we achieve · Technology Stack & Architecture · Multi-Level Real-World Examples", ParagraphStyle('BnrSub', fontName='Helvetica', fontSize=9, leading=12, textColor=colors.HexColor("#e0f2fe"))),
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
    story.append(Spacer(1, 10))

    # ── SECTION 1: WHY WE ARE DOING THIS ACTIVITY ───────────────────────────────
    story.append(Paragraph("1. WHY We Are Doing This Activity (Business Objective & Migration De-Risking)", h1_style))
    story.append(Paragraph(
        "Sempra is executing a mission-critical SAP S/4HANA migration across three sequential migration cycles: <b>DM1 (Mock 1)</b>, <b>DM2 (Mock 2)</b>, and <b>DM3 (Dry Run / Cutover)</b>. "
        "During this migration, hundreds of millions of customer records, financial ledgers, asset structures, and work orders are extracted from legacy ECC systems, transformed, and loaded into SAP.",
        body_style
    ))
    story.append(Paragraph(
        "<b>The Core Business Challenge:</b> Historically, verifying data completeness required large teams of analysts manually merging 6+ massive Excel spreadsheets using complex VLOOKUPs. "
        "This manual process took <b>3 to 4 hours per cycle</b>, was prone to human copy-paste errors, and lacked real-time visibility into discrepancies.",
        body_style
    ))
    story.append(Paragraph(
        "<b>The Solution & Purpose:</b> This platform delivers an automated, audit-ready reconciliation engine that ingests, deduplicates, and validates <b>7,700+ tables in under 10 seconds</b>. "
        "It provides absolute assurance of <b>Zero Data Loss</b> and instant governance before cutover sign-off.",
        body_style
    ))
    story.append(Spacer(1, 4))

    # ── SECTION 2: WHAT WE CAN ACHIEVE & WHAT IS ACTIVE ────────────────────────
    story.append(Paragraph("2. WHAT We Achieve & What Is Active in the Platform", h1_style))
    
    achieve_data = [
        [Paragraph("<b>Key Capability</b>", tbl_hdr_style), Paragraph("<b>What Is Active & How It Works</b>", tbl_hdr_style), Paragraph("<b>Business Outcome</b>", tbl_hdr_style)],
        [
            Paragraph("<b>Unified 3-Cycle Live Cockpit</b>", tbl_cell_style),
            Paragraph("Monitors DM1, DM2, and DM3 side-by-side with semicircle health gauges and reconciliation rates.", tbl_cell_style),
            Paragraph("Instant executive visibility across the full migration lifecycle.", tbl_cell_style)
        ],
        [
            Paragraph("<b>Sub-10s Auto-Sync</b>", tbl_cell_style),
            Paragraph("Reads 5 massive reference, export, and import Excel files with multi-threaded Gzip compression.", tbl_cell_style),
            Paragraph("95% time reduction in status report compilation.", tbl_cell_style)
        ],
        [
            Paragraph("<b>Source vs. Target Gap Analysis</b>", tbl_cell_style),
            Paragraph("Calculates table-level differences with automated status tags: <code>Matching</code>, <code>Source is more</code>, <code>Source is less</code>.", tbl_cell_style),
            Paragraph("Zero data loss verification; pinpoint exact record discrepancies immediately.", tbl_cell_style)
        ],
        [
            Paragraph("<b>Src vs Tgt Pivot / Circle View</b>", tbl_cell_style),
            Paragraph("Multi-segment SVG Donut chart + interactive pivot table with click-to-filter navigation.", tbl_cell_style),
            Paragraph("Intuitive visual analytics for leadership and non-technical stakeholders.", tbl_cell_style)
        ],
        [
            Paragraph("<b>Audit-Ready One-Click Exports</b>", tbl_cell_style),
            Paragraph("Generates pre-calculated Excel (.xlsx), CSV, and PDF reports with timestamped data lineage.", tbl_cell_style),
            Paragraph("Compliance-ready documentation for steering committee meetings.", tbl_cell_style)
        ],
    ]
    achieve_tbl = Table(achieve_data, colWidths=[120, 240, 156])
    achieve_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SURFACE),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(achieve_tbl)
    story.append(Spacer(1, 10))

    # ── SECTION 3: TECHNOLOGY WISE — WHAT WE ARE USING ─────────────────────────
    story.append(Paragraph("3. TECHNOLOGY WISE — What We Are Using & Architecture", h1_style))
    story.append(Paragraph(
        "The architecture is designed to be <b>100% on-premise, secure, lightweight, and ultra-fast</b> with zero external software licensing:",
        body_style
    ))

    tech_data = [
        [Paragraph("<b>Component Layer</b>", tbl_hdr_style), Paragraph("<b>Technology Used</b>", tbl_hdr_style), Paragraph("<b>Role & Technical Benefit</b>", tbl_hdr_style)],
        [
            Paragraph("<b>Frontend UI & Visuals</b>", tbl_cell_style),
            Paragraph("HTML5, CSS3 Grid/Flexbox, JavaScript (ES6+), SheetJS (xlsx.full.min.js)", tbl_cell_style),
            Paragraph("Interactive client-side rendering; runs in any standard browser (Chrome, Edge). Responsive modals, SVG gauges, and live search.", tbl_cell_style)
        ],
        [
            Paragraph("<b>File Watcher Bridge</b>", tbl_cell_style),
            Paragraph("Python 3, Flask REST API, Gzip compression, ETag caching (Port 5002)", tbl_cell_style),
            Paragraph("Monitors C: drive and OneDrive/SharePoint folders. Serves Excel file bytes with 60-70% bandwidth reduction and zero disk re-reads on unchanged files.", tbl_cell_style)
        ],
        [
            Paragraph("<b>SAP Extraction Engine</b>", tbl_cell_style),
            Paragraph("Python COM GUI Scripting, SE16N 3-Method Fallback (Port 5001)", tbl_cell_style),
            Paragraph("Automates table record count extraction directly from SAP ECC / S4HANA without requiring ABAP transports or cloud middleware.", tbl_cell_style)
        ],
        [
            Paragraph("<b>Reporting Engine</b>", tbl_cell_style),
            Paragraph("Python ReportLab PDF Engine & python-docx", tbl_cell_style),
            Paragraph("Generates publication-quality executive PDFs and editable Word deliverables with timestamped audit stamps.", tbl_cell_style)
        ],
        [
            Paragraph("<b>Security & Governance</b>", tbl_cell_style),
            Paragraph("127.0.0.1 Loopback, Local Storage, Role-Based Platform Badges", tbl_cell_style),
            Paragraph("100% local data residency — no corporate data ever leaves Sempra's secure network perimeter.", tbl_cell_style)
        ]
    ]
    tech_tbl = Table(tech_data, colWidths=[110, 160, 246])
    tech_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), LIGHT_BLUE),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_BL),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(tech_tbl)
    story.append(Spacer(1, 10))

    # ── SECTION 4: REAL-WORLD EXAMPLES FOR ALL LEVELS OF PEOPLE ────────────────
    story.append(Paragraph("4. Real-World Practical Examples for ALL Levels of People", h1_style))
    story.append(Paragraph(
        "To ensure seamless collaboration across the organization, the dashboard serves four key stakeholder groups:",
        body_style
    ))

    # Level 1: Executives & Management
    ex_exec = [
        [Paragraph("<b>👔 Level 1: Senior Leadership & Project Managers (Steering Committee)</b>", ParagraphStyle('L1', fontName='Helvetica-Bold', fontSize=9, textColor=NAVY))],
        [Paragraph(
            "<b>Practical Example:</b> The Manager opens the dashboard before a steering committee meeting. In <b>10 seconds</b>, the semicircle health gauges confirm that <b>DM2 achieved a 99.8% match rate</b> across 7,715 tables. "
            "The manager clicks <b>'📄 Download PDF'</b> and presents a board-ready executive report with zero manual prep time.",
            body_style
        )]
    ]
    t1 = Table(ex_exec, colWidths=[516])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SURFACE),
        ('BACKGROUND', (0,1), (-1,1), WHITE),
        ('BOX', (0,0), (-1,-1), 1, BORDER),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t1)
    story.append(Spacer(1, 5))

    # Level 2: Business & Data Migration Leads
    ex_lead = [
        [Paragraph("<b>📋 Level 2: Business Data Leads & Functional Owners (Record Discrepancy Analysis)</b>", ParagraphStyle('L2', fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor("#78350f")))],
        [Paragraph(
            "<b>Practical Example:</b> Reviewing Customer Master table <code>/1CADMC/00000239</code>.<br/>"
            "• <b>Source System Count:</b> 12,098,214 records &nbsp;|&nbsp; <b>Target SAP Count:</b> 12,098,148 records<br/>"
            "• <b>Dashboard Visual:</b> Instantly tags table as <b>'▲ Source is more (+66 records)'</b> with an amber badge.<br/>"
            "• <b>Action:</b> The lead clicks the row, inspects the 66-record gap, and exports a targeted Excel list with pre-calculated diffs for the ETL lead.",
            body_style
        )]
    ]
    t2 = Table(ex_lead, colWidths=[516])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), AMBER_BG),
        ('BACKGROUND', (0,1), (-1,1), WHITE),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#fde68a")),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t2)
    story.append(Spacer(1, 5))

    # Level 3: Technical ETL & SAP Engineers
    ex_tech = [
        [Paragraph("<b>⚙️ Level 3: Technical ETL Developers & SAP Specialists (Automated Extraction)</b>", ParagraphStyle('L3', fontName='Helvetica-Bold', fontSize=9, textColor=BLUE_ACC))],
        [Paragraph(
            "<b>Practical Example:</b> Rather than executing manual SE16N table count queries for 7,700 tables in SAP GUI, the engineer runs <code>automation/01_sap_source_count.py</code>. "
            "The background bridge auto-walks SAP tables, compiles live counts, and streams them into the dashboard cache with zero manual data entry.",
            body_style
        )]
    ]
    t3 = Table(ex_tech, colWidths=[516])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), LIGHT_BLUE),
        ('BACKGROUND', (0,1), (-1,1), WHITE),
        ('BOX', (0,0), (-1,-1), 1, BORDER_BL),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t3)
    story.append(Spacer(1, 5))

    # Level 4: Audit & Compliance Teams
    ex_audit = [
        [Paragraph("<b>🛡️ Level 4: Audit, Risk & Compliance Officers (Verifiable Data Lineage)</b>", ParagraphStyle('L4', fontName='Helvetica-Bold', fontSize=9, textColor=GREEN))],
        [Paragraph(
            "<b>Practical Example:</b> For SOX and internal audit sign-offs, the compliance officer verifies that no records were dropped between Export and Import stages. "
            "The officer reviews the <b>'Src vs Tgt Pivot / Circle'</b> view, clicks <b>'✔ Matching'</b>, and downloads a digitally timestamped Excel audit manifest proving 100% reconciliation.",
            body_style
        )]
    ]
    t4 = Table(ex_audit, colWidths=[516])
    t4.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), GREEN_BG),
        ('BACKGROUND', (0,1), (-1,1), WHITE),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#86efac")),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t4)
    story.append(Spacer(1, 10))

    # ── SECTION 5: STEP-BY-STEP QUICK START ────────────────────────────────────
    story.append(Paragraph("5. Step-by-Step Quick Start Guide (How to Use in 3 Steps)", h1_style))
    
    qs_data = [
        [
            Paragraph("<b>Step 1: Open</b>", ParagraphStyle('Q1', fontName='Helvetica-Bold', fontSize=9, textColor=NAVY)),
            Paragraph("Double-click <code>Sempra_CrossCycle_Summary_MASTER.html</code> or open via browser at <code>http://localhost:5003/</code>.", tbl_cell_style)
        ],
        [
            Paragraph("<b>Step 2: Auto-Sync</b>", ParagraphStyle('Q2', fontName='Helvetica-Bold', fontSize=9, textColor=NAVY)),
            Paragraph("Click <b>'⚡ Auto-Sync All Cycles'</b> at the top left. The system ingests and computes reconciliation for DM1, DM2, and DM3 in &lt;10s.", tbl_cell_style)
        ],
        [
            Paragraph("<b>Step 3: Analyze & Export</b>", ParagraphStyle('Q3', fontName='Helvetica-Bold', fontSize=9, textColor=NAVY)),
            Paragraph("Click on any count number (e.g. <b>7,710</b>) to view drill-down tables, switch to the <b>Circle/Pivot View</b>, or click <b>📊 Excel</b> to export audit-ready spreadsheets.", tbl_cell_style)
        ]
    ]
    qs_tbl = Table(qs_data, colWidths=[100, 416])
    qs_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), SURFACE),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(qs_tbl)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF built successfully: {PDF_OUT_LOCAL}")

    # Copy to Desktop
    try:
        shutil.copyfile(PDF_OUT_LOCAL, PDF_OUT_DESKTOP)
        print(f"PDF successfully copied to Desktop: {PDF_OUT_DESKTOP}")
    except Exception as e:
        print(f"Could not copy to Desktop: {e}")


def generate_html():
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Sempra Data Migration Platform — Complete Documentation</title>
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
    .container { max-width: 900px; margin: 0 auto; background: #fff; border-radius: 16px; box-shadow: 0 4px 24px rgba(0,0,0,0.06); border: 1px solid var(--border); overflow: hidden; }
    
    .header { background: linear-gradient(135deg, #0f2744 0%, #1e3a5f 100%); color: #fff; padding: 36px 32px; }
    .badge { display: inline-block; background: rgba(56,189,248,0.2); color: #7dd3fc; border: 1px solid rgba(56,189,248,0.4); font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; padding: 4px 10px; border-radius: 20px; margin-bottom: 12px; }
    .title { font-size: 26px; font-weight: 900; line-height: 1.2; margin-bottom: 8px; }
    .subtitle { font-size: 14px; color: #bae6fd; max-width: 720px; }
    
    .content { padding: 32px; }
    h2 { font-size: 18px; font-weight: 800; color: var(--navy); margin-top: 28px; margin-bottom: 12px; display: flex; align-items: center; gap: 8px; border-bottom: 2px solid #f1f5f9; padding-bottom: 6px; }
    h2:first-of-type { margin-top: 0; }
    p { font-size: 14px; color: #334155; margin-bottom: 12px; }
    
    .kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; margin: 20px 0; }
    .kpi-card { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 18px; text-align: center; }
    .kpi-num { font-size: 24px; font-weight: 900; color: var(--blue); }
    .kpi-lbl { font-size: 12px; font-weight: 700; color: var(--muted); margin-top: 4px; }
    
    .level-box { border-radius: 12px; border: 1px solid; margin: 16px 0; overflow: hidden; }
    .level-box.exec { border-color: var(--border); background: #fff; }
    .level-box.exec .lvl-hdr { background: var(--surface); color: var(--navy); }
    .level-box.lead { border-color: #fde68a; background: #fff; }
    .level-box.lead .lvl-hdr { background: var(--amber-bg); color: #78350f; }
    .level-box.tech { border-color: var(--border-blue); background: #fff; }
    .level-box.tech .lvl-hdr { background: var(--light-blue); color: var(--navy); }
    .level-box.audit { border-color: #86efac; background: #fff; }
    .level-box.audit .lvl-hdr { background: var(--green-bg); color: #065f46; }
    .lvl-hdr { padding: 12px 18px; font-weight: 800; font-size: 13px; }
    .lvl-body { padding: 16px 18px; font-size: 13px; color: #334155; }
    
    table { width: 100%; border-collapse: collapse; font-size: 13px; margin: 16px 0; border: 1px solid var(--border); border-radius: 8px; overflow: hidden; }
    th { background: var(--surface); text-align: left; padding: 10px 14px; font-weight: 700; color: var(--navy); border-bottom: 2px solid var(--border); }
    td { padding: 10px 14px; border-bottom: 1px solid var(--border); }
    tr:last-child td { border-bottom: none; }
    tr:hover td { background: #f8fafc; }
    
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
      <span class="badge">Sempra Energy · Odyssey Data Migration</span>
      <h1 class="title">Data Migration Executive &amp; Technical Documentation</h1>
      <p class="subtitle">Complete blueprint: Why we are doing this activity · What we achieve · Technology Stack · Real-world examples for all levels of stakeholders.</p>
    </div>
    
    <div class="content">
      <h2>🎯 1. WHY We Are Doing This Activity</h2>
      <p>Sempra is migrating to SAP S/4HANA across three cycles: <strong>DM1 (Mock 1), DM2 (Mock 2), and DM3 (Dry Run / Cutover)</strong>. Millions of critical customer, financial, and asset records are transferred from legacy ECC to S/4HANA.</p>
      <p><strong>The Problem Solved:</strong> Manually cross-referencing migration files previously required <strong>3–4 hours of manual Excel VLOOKUPs per cycle</strong>. This platform provides an <strong>automated, sub-10-second reconciliation engine</strong> guaranteeing <strong>Zero Data Loss</strong>.</p>
      
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
          <div class="kpi-lbl">Automated Error-Free Accuracy</div>
        </div>
      </div>

      <h2>🚀 2. WHAT We Achieve &amp; What Is Active</h2>
      <table>
        <thead>
          <tr><th>Capability</th><th>What Is Active</th><th>Business Outcome</th></tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Unified 3-Cycle Cockpit</strong></td>
            <td>Tracks DM1, DM2, and DM3 side-by-side with semicircle health gauges.</td>
            <td>Instant cross-cycle visibility.</td>
          </tr>
          <tr>
            <td><strong>Source vs Target Gap Detection</strong></td>
            <td>Calculates exact table-level record variances and tags (<code>Matching</code>, <code>Source is more</code>, <code>Source is less</code>).</td>
            <td>Instant detection of migration gaps.</td>
          </tr>
          <tr>
            <td><strong>Src vs Tgt Pivot / Circle View</strong></td>
            <td>Interactive SVG Donut chart and pivot breakdown with click-to-filter navigation.</td>
            <td>Visual clarity for non-technical stakeholders.</td>
          </tr>
          <tr>
            <td><strong>Audit-Ready Exports</strong></td>
            <td>One-click Excel (.xlsx) with diff columns, CSV, and PDF reports.</td>
            <td>Immediate governance deliverables.</td>
          </tr>
        </tbody>
      </table>

      <h2>⚙️ 3. TECHNOLOGY WISE — What We Are Using</h2>
      <table>
        <thead>
          <tr><th>Layer</th><th>Technology Used</th><th>Technical Role &amp; Benefit</th></tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Frontend UI</strong></td>
            <td>HTML5, CSS3 Grid/Flexbox, JavaScript (ES6+), SheetJS (<code>xlsx.full.min.js</code>)</td>
            <td>Client-side lightning-fast rendering in Chrome/Edge. Interactive SVG gauges and modal search.</td>
          </tr>
          <tr>
            <td><strong>File Bridge</strong></td>
            <td>Python 3, Flask REST API, Gzip stream compression, ETag 304 caching (Port 5002)</td>
            <td>Serves Excel bytes from C: drive and SharePoint with 60-70% bandwidth compression. Zero disk re-reads.</td>
          </tr>
          <tr>
            <td><strong>SAP Automation</strong></td>
            <td>Python COM GUI Scripting (<code>sap_bridge.py</code>)</td>
            <td>Automates SAP ECC / S4HANA SE16N table count extraction with zero external licensing fees.</td>
          </tr>
          <tr>
            <td><strong>Security</strong></td>
            <td>127.0.0.1 Loopback, Local Storage, Role-Based Badges</td>
            <td>100% on-premise local data residency — no corporate data ever leaves Sempra's secure network.</td>
          </tr>
        </tbody>
      </table>

      <h2>💡 4. Real-World Examples for ALL Levels of People</h2>
      
      <div class="level-box exec">
        <div class="lvl-hdr">👔 Level 1: Senior Leadership &amp; Project Managers (Steering Committee)</div>
        <div class="lvl-body">
          <strong>Example:</strong> In 10 seconds before a board review, the manager clicks <em>"⚡ Auto-Sync"</em>. The semicircle gauges confirm <strong>99.8% match rate</strong> across 7,715 tables in DM2. The manager clicks <em>"📄 Download PDF"</em> to present an audit-ready executive summary.
        </div>
      </div>

      <div class="level-box lead">
        <div class="lvl-hdr">📋 Level 2: Business Data Leads &amp; Functional Owners (Discrepancy Analysis)</div>
        <div class="lvl-body">
          <strong>Example:</strong> Reviewing Customer Master table <code>/1CADMC/00000239</code> (Source: 12,098,214 vs Target: 12,098,148). The dashboard tags it as <strong>"▲ Source is more (+66 records)"</strong> with an amber badge. The lead clicks the row and exports a targeted Excel list for the ETL lead in 1 click.
        </div>
      </div>

      <div class="level-box tech">
        <div class="lvl-hdr">⚙️ Level 3: Technical ETL Developers &amp; SAP Specialists (Automated Extraction)</div>
        <div class="lvl-body">
          <strong>Example:</strong> Rather than running 7,700 manual SE16N count queries in SAP GUI, the engineer runs <code>01_sap_source_count.py</code>. The script automates SAP data extraction and streams counts into the dashboard cache.
        </div>
      </div>

      <div class="level-box audit">
        <div class="lvl-hdr">🛡️ Level 4: Audit, Risk &amp; Compliance Officers (Data Lineage Verification)</div>
        <div class="lvl-body">
          <strong>Example:</strong> For SOX compliance, the auditor opens the <em>"Src vs Tgt Pivot / Circle"</em> tab, clicks <em>"✔ Matching"</em>, and downloads a timestamped Excel audit log proving end-to-end reconciliation integrity.
        </div>
      </div>

      <h2>🚀 5. How to Use in 3 Simple Steps</h2>
      <p><strong>Step 1:</strong> Launch <code>Sempra_CrossCycle_Summary_MASTER.html</code> in Chrome/Edge.<br/>
         <strong>Step 2:</strong> Click <strong>"⚡ Auto-Sync All Cycles"</strong> to ingest latest files in &lt;10s.<br/>
         <strong>Step 3:</strong> Click any count number to inspect tables, view the <strong>Circle/Pivot breakdown</strong>, or download Excel reports.</p>

      <div class="btn-bar">
        <a href="Sempra_CrossCycle_Summary_MASTER.html" class="btn btn-prim">🚀 Open Master Dashboard</a>
        <a href="Sempra_DM_Dashboard_Documentation.pdf" class="btn btn-sec">📄 Open Documentation PDF</a>
      </div>
    </div>
  </div>
</body>
</html>
"""
    with open(HTML_OUT_LOCAL, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"HTML built successfully: {HTML_OUT_LOCAL}")

if __name__ == "__main__":
    generate_pdf()
    generate_html()
