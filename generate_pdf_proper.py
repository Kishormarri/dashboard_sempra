"""
================================================================================
  Sempra DM Dashboard — Professional PDF Generator (ReportLab)
  Output: Sempra_DM_Dashboard_Documentation_FULL.pdf
  Run:    python generate_pdf_proper.py
================================================================================
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.platypus.flowables import Flowable
from reportlab.pdfbase import pdfmetrics

OUT = "Sempra_DM_Dashboard_Documentation_FULL.pdf"

# ── Colour palette ─────────────────────────────────────────────────────────
NAVY       = colors.HexColor("#091e3a")
NAVY2      = colors.HexColor("#0f3460")
NAVY3      = colors.HexColor("#164e63")
BLUE       = colors.HexColor("#1d4ed8")
BLUE_LT    = colors.HexColor("#eff6ff")
BLUE_BD    = colors.HexColor("#bfdbfe")
PURPLE     = colors.HexColor("#7c3aed")
PURPLE_LT  = colors.HexColor("#faf5ff")
PURPLE_BD  = colors.HexColor("#e9d5ff")
TEAL       = colors.HexColor("#0f766e")
TEAL_LT    = colors.HexColor("#f0fdf4")
TEAL_BD    = colors.HexColor("#bbf7d0")
AMBER      = colors.HexColor("#b45309")
AMBER_LT   = colors.HexColor("#fffbeb")
AMBER_BD   = colors.HexColor("#fde68a")
RED        = colors.HexColor("#9a3412")
RED_LT     = colors.HexColor("#fff1f2")
RED_BD     = colors.HexColor("#fecdd3")
ARCH_BLUE  = colors.HexColor("#0369a1")
DM1        = colors.HexColor("#3b5bdb")
DM2        = colors.HexColor("#7c3aed")
DM3        = colors.HexColor("#2f9e44")
GREEN_OK   = colors.HexColor("#059669")
GREEN_LT   = colors.HexColor("#f0fdf4")
AMBER_OK   = colors.HexColor("#d97706")
RED_OK     = colors.HexColor("#dc2626")
SLATE      = colors.HexColor("#1e293b")
SLATE_TEXT = colors.HexColor("#f8fafc")
BODY_TEXT  = colors.HexColor("#374151")
MUTED      = colors.HexColor("#64748b")
LIGHT_MUTED= colors.HexColor("#94a3b8")
ROW_EVEN   = colors.HexColor("#f8fafc")
ROW_ODD    = colors.white
HDR_BG     = colors.HexColor("#1e293b")
HDR_FG     = colors.HexColor("#f8fafc")
PAGE_BG    = colors.HexColor("#f5f6fa")
CODE_BG    = colors.HexColor("#0f172a")
CODE_TEXT  = colors.HexColor("#94a3b8")

# ── Typography ─────────────────────────────────────────────────────────────
def build_styles():
    s = {}
    base = getSampleStyleSheet()

    s["cover_tag"]   = ParagraphStyle("cover_tag",   fontName="Helvetica-Bold",   fontSize=9,  textColor=colors.HexColor("#7dd3fc"), spaceAfter=6,  letterSpacing=1.5)
    s["cover_h1"]    = ParagraphStyle("cover_h1",    fontName="Helvetica-Bold",   fontSize=28, textColor=colors.white,               spaceAfter=10, leading=34)
    s["cover_sub"]   = ParagraphStyle("cover_sub",   fontName="Helvetica",        fontSize=11, textColor=colors.HexColor("#94a3b8"), spaceAfter=14, leading=17)
    s["cover_meta"]  = ParagraphStyle("cover_meta",  fontName="Helvetica",        fontSize=9,  textColor=colors.HexColor("#64748b"), spaceAfter=4)

    s["sec_num"]     = ParagraphStyle("sec_num",     fontName="Helvetica-Bold",   fontSize=9,  textColor=colors.white,               spaceAfter=0)
    s["sec_title"]   = ParagraphStyle("sec_title",   fontName="Helvetica-Bold",   fontSize=18, textColor=colors.HexColor("#1a202c"), spaceAfter=3,  leading=22)
    s["sec_sub"]     = ParagraphStyle("sec_sub",     fontName="Helvetica-Oblique",fontSize=10, textColor=LIGHT_MUTED,                spaceAfter=12)

    s["box_title"]   = ParagraphStyle("box_title",   fontName="Helvetica-Bold",   fontSize=8,  spaceAfter=5,  letterSpacing=0.8)
    s["box_body"]    = ParagraphStyle("box_body",    fontName="Helvetica",        fontSize=10, textColor=BODY_TEXT, spaceAfter=3,  leading=15)

    s["step_num"]    = ParagraphStyle("step_num",    fontName="Helvetica-Bold",   fontSize=14, textColor=colors.white, alignment=TA_CENTER)
    s["step_title"]  = ParagraphStyle("step_title",  fontName="Helvetica-Bold",   fontSize=11, textColor=colors.HexColor("#1a202c"), spaceAfter=4)
    s["step_body"]   = ParagraphStyle("step_body",   fontName="Helvetica",        fontSize=9.5,textColor=colors.HexColor("#475569"), leading=14, spaceAfter=3)

    s["tbl_hdr"]     = ParagraphStyle("tbl_hdr",     fontName="Helvetica-Bold",   fontSize=8,  textColor=HDR_FG,    leading=11)
    s["tbl_cell"]    = ParagraphStyle("tbl_cell",    fontName="Helvetica",        fontSize=8.5,textColor=BODY_TEXT, leading=12)
    s["tbl_cell_ok"] = ParagraphStyle("tbl_cell_ok", fontName="Helvetica-Bold",   fontSize=8.5,textColor=GREEN_OK,  leading=12)
    s["tbl_cell_wn"] = ParagraphStyle("tbl_cell_wn", fontName="Helvetica-Bold",   fontSize=8.5,textColor=AMBER_OK,  leading=12)
    s["tbl_mono"]    = ParagraphStyle("tbl_mono",    fontName="Courier",          fontSize=8,  textColor=BLUE,      leading=11)

    s["code"]        = ParagraphStyle("code",        fontName="Courier",          fontSize=8,  textColor=CODE_TEXT, leading=13, spaceAfter=2)
    s["code_hl"]     = ParagraphStyle("code_hl",     fontName="Courier-Bold",     fontSize=8,  textColor=colors.HexColor("#22d3ee"), leading=13)

    s["kpi_num"]     = ParagraphStyle("kpi_num",     fontName="Helvetica-Bold",   fontSize=22, alignment=TA_CENTER, textColor=BLUE, spaceAfter=2)
    s["kpi_lbl"]     = ParagraphStyle("kpi_lbl",     fontName="Helvetica-Bold",   fontSize=7,  alignment=TA_CENTER, textColor=MUTED, spaceAfter=1, letterSpacing=0.5)
    s["kpi_sub"]     = ParagraphStyle("kpi_sub",     fontName="Helvetica",        fontSize=7,  alignment=TA_CENTER, textColor=LIGHT_MUTED)

    s["toc_num"]     = ParagraphStyle("toc_num",     fontName="Helvetica-Bold",   fontSize=9,  textColor=LIGHT_MUTED)
    s["toc_lbl"]     = ParagraphStyle("toc_lbl",     fontName="Helvetica-Bold",   fontSize=10, textColor=BODY_TEXT)
    s["toc_sec"]     = ParagraphStyle("toc_sec",     fontName="Helvetica",        fontSize=8,  textColor=LIGHT_MUTED, spaceAfter=1)

    s["normal"]      = ParagraphStyle("normal",      fontName="Helvetica",        fontSize=10, textColor=BODY_TEXT, leading=15, spaceAfter=6)
    s["footer"]      = ParagraphStyle("footer",      fontName="Helvetica-Oblique",fontSize=7.5,textColor=LIGHT_MUTED, alignment=TA_CENTER)

    return s

ST = build_styles()
W, H = A4  # 595 x 842 pts
MARGIN = 20*mm
CONTENT_W = W - 2*MARGIN

# ── Page template with header/footer ──────────────────────────────────────
def on_page(canvas, doc):
    canvas.saveState()
    # subtle top line
    canvas.setStrokeColor(colors.HexColor("#e2e8f0"))
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, H - 14*mm, W - MARGIN, H - 14*mm)
    # header text
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(LIGHT_MUTED)
    canvas.drawString(MARGIN, H - 11*mm, "SEMPRA ENERGY  |  SAP Data Migration Dashboard  |  Leadership Documentation v2.0")
    canvas.drawRightString(W - MARGIN, H - 11*mm, "INTERNAL USE ONLY")
    # footer line
    canvas.line(MARGIN, 14*mm, W - MARGIN, 14*mm)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(MARGIN, 10*mm, f"Sempra SAP DM Dashboard Documentation  |  Generated {datetime.now().strftime('%d %b %Y')}")
    canvas.drawRightString(W - MARGIN, 10*mm, f"Page {doc.page}")
    canvas.restoreState()

def on_cover_page(canvas, doc):
    canvas.saveState()
    # full-page dark background
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    # subtle gradient overlay (lighter stripe)
    canvas.setFillColor(NAVY2)
    canvas.rect(0, H*0.35, W, H*0.65, fill=1, stroke=0)
    # accent bar top
    canvas.setFillColor(DM1)
    canvas.rect(0, H - 6*mm, W/3, 6*mm, fill=1, stroke=0)
    canvas.setFillColor(DM2)
    canvas.rect(W/3, H - 6*mm, W/3, 6*mm, fill=1, stroke=0)
    canvas.setFillColor(DM3)
    canvas.rect(2*W/3, H - 6*mm, W/3, 6*mm, fill=1, stroke=0)
    # bottom meta bar
    canvas.setFillColor(colors.HexColor("#0a0a0a"))
    canvas.rect(0, 0, W, 28*mm, fill=1, stroke=0)
    canvas.restoreState()

# ── Helper flowables ───────────────────────────────────────────────────────
def spacer(h=4):
    return Spacer(1, h*mm)

def hline(color=colors.HexColor("#e2e8f0"), thickness=0.5):
    return HRFlowable(width="100%", thickness=thickness, color=color, spaceAfter=4*mm, spaceBefore=2*mm)

def plain_box(title, body, bg, border, title_color):
    """A coloured callout box with a title and body text."""
    title_p = Paragraph(title.upper(), ParagraphStyle("_", fontName="Helvetica-Bold",
        fontSize=8, textColor=title_color, letterSpacing=0.7, spaceAfter=4))
    body_p  = Paragraph(body, ParagraphStyle("_", fontName="Helvetica",
        fontSize=10, textColor=BODY_TEXT, leading=15))
    tbl = Table([[title_p], [body_p]], colWidths=[CONTENT_W - 4*mm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), bg),
        ("BOX",        (0,0), (-1,-1), 1, border),
        ("LEFTPADDING",  (0,0), (-1,-1), 10),
        ("RIGHTPADDING", (0,0), (-1,-1), 10),
        ("TOPPADDING",   (0,0), (-1,-1), 8),
        ("BOTTOMPADDING",(0,0), (-1,-1), 8),
        ("ROWBACKGROUNDS",(0,0),(-1,-1),[bg]),
    ]))
    return KeepTogether([tbl, spacer(3)])

def green_box(title, body):  return plain_box(title, body, TEAL_LT,  TEAL_BD,  TEAL)
def blue_box(title, body):   return plain_box(title, body, BLUE_LT,  BLUE_BD,  BLUE)
def amber_box(title, body):  return plain_box(title, body, AMBER_LT, AMBER_BD, AMBER)
def purple_box(title, body): return plain_box(title, body, PURPLE_LT,PURPLE_BD,PURPLE)

def section_header(num, title, subtitle, badge_color):
    """Coloured section badge + large title."""
    badge = Table([[Paragraph(num, ST["sec_num"])]],
                  colWidths=[12*mm], rowHeights=[7*mm])
    badge.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), badge_color),
        ("ALIGN",      (0,0), (-1,-1), "CENTER"),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 2),
        ("BOTTOMPADDING",(0,0),(-1,-1),2),
        ("LEFTPADDING",(0,0),(-1,-1),4),
        ("RIGHTPADDING",(0,0),(-1,-1),4),
    ]))
    title_col = Table([
        [Paragraph(title, ST["sec_title"])],
        [Paragraph(subtitle, ST["sec_sub"])],
    ], colWidths=[CONTENT_W - 18*mm])
    title_col.setStyle(TableStyle([("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0)]))
    row = Table([[badge, title_col]], colWidths=[14*mm, CONTENT_W - 14*mm])
    row.setStyle(TableStyle([
        ("VALIGN",       (0,0),(-1,-1),"MIDDLE"),
        ("LINEBELOW",    (0,0),(-1,-1),1.5,colors.HexColor("#e2e8f0")),
        ("BOTTOMPADDING",(0,0),(-1,-1),8),
        ("LEFTPADDING",  (0,0),(-1,-1),0),
    ]))
    return KeepTogether([row, spacer(2)])

def data_table(headers, rows, col_widths=None, ok_cols=None, warn_cols=None, mono_cols=None):
    """A styled data table with dark header."""
    ok_cols   = ok_cols   or []
    warn_cols = warn_cols or []
    mono_cols = mono_cols or []
    n = len(headers)
    if col_widths is None:
        col_widths = [CONTENT_W / n] * n

    hdr_cells = [Paragraph(h, ST["tbl_hdr"]) for h in headers]
    data = [hdr_cells]
    for row in rows:
        cells = []
        for ci, val in enumerate(row):
            txt = str(val)
            if ci in ok_cols and ("OK" in txt or "Full" in txt or "reconcil" in txt.lower() or "No change" in txt):
                st = ST["tbl_cell_ok"]
            elif ci in warn_cols and ("In progress" in txt or "Only if" in txt or "Rarely" in txt):
                st = ST["tbl_cell_wn"]
            elif ci in mono_cols:
                st = ST["tbl_mono"]
            else:
                st = ST["tbl_cell"]
            cells.append(Paragraph(txt, st))
        data.append(cells)

    tbl = Table(data, colWidths=col_widths, repeatRows=1)
    style = [
        ("BACKGROUND",   (0,0), (-1,0),  HDR_BG),
        ("TEXTCOLOR",    (0,0), (-1,0),  HDR_FG),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [ROW_ODD, ROW_EVEN]),
        ("GRID",         (0,0), (-1,-1), 0.4, colors.HexColor("#e2e8f0")),
        ("TOPPADDING",   (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0), (-1,-1), 5),
        ("LEFTPADDING",  (0,0), (-1,-1), 8),
        ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("VALIGN",       (0,0), (-1,-1), "TOP"),
    ]
    tbl.setStyle(TableStyle(style))
    return KeepTogether([tbl, spacer(3)])

def kpi_strip(items):
    """Row of KPI boxes: [(number, label, sub, color)]"""
    n = len(items)
    w = CONTENT_W / n
    cells = []
    for num, lbl, sub, col in items:
        np = Paragraph(num, ParagraphStyle("_", fontName="Helvetica-Bold", fontSize=20,
                        alignment=TA_CENTER, textColor=col, spaceAfter=2))
        lp = Paragraph(lbl.upper(), ParagraphStyle("_", fontName="Helvetica-Bold", fontSize=7,
                        alignment=TA_CENTER, textColor=MUTED, letterSpacing=0.4, spaceAfter=1))
        sp = Paragraph(sub, ParagraphStyle("_", fontName="Helvetica", fontSize=7,
                        alignment=TA_CENTER, textColor=LIGHT_MUTED))
        cell_tbl = Table([[np],[lp],[sp]], colWidths=[w - 4*mm])
        cell_tbl.setStyle(TableStyle([
            ("BACKGROUND", (0,0),(-1,-1), colors.white),
            ("BOX",        (0,0),(-1,-1), 0.5, colors.HexColor("#e2e8f0")),
            ("TOPPADDING", (0,0),(-1,-1), 8),
            ("BOTTOMPADDING",(0,0),(-1,-1),8),
        ]))
        cells.append(cell_tbl)
    row = Table([cells], colWidths=[w]*n)
    row.setStyle(TableStyle([("LEFTPADDING",(0,0),(-1,-1),2),("RIGHTPADDING",(0,0),(-1,-1),2)]))
    return KeepTogether([row, spacer(3)])

def compare_pair(before_title, before_text, after_title, after_text):
    """Side-by-side BEFORE/AFTER boxes."""
    hw = (CONTENT_W - 4*mm) / 2
    def make(title, text, bg, tc):
        tp = Paragraph(title, ParagraphStyle("_", fontName="Helvetica-Bold", fontSize=10, textColor=tc, spaceAfter=5))
        bp = Paragraph(text, ParagraphStyle("_", fontName="Helvetica", fontSize=9.5, textColor=BODY_TEXT, leading=14))
        t = Table([[tp],[bp]], colWidths=[hw - 6*mm])
        t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),bg),("BOX",(0,0),(-1,-1),0.5,colors.HexColor("#e2e8f0")),
                                ("TOPPADDING",(0,0),(-1,-1),10),("BOTTOMPADDING",(0,0),(-1,-1),10),
                                ("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10)]))
        return t
    b = make(before_title, before_text, RED_LT,  RED_OK)
    a = make(after_title,  after_text,  TEAL_LT, TEAL)
    row = Table([[b, a]], colWidths=[hw, hw])
    row.setStyle(TableStyle([("LEFTPADDING",(0,0),(-1,-1),2),("RIGHTPADDING",(0,0),(-1,-1),2)]))
    return KeepTogether([row, spacer(3)])

def step_row(num, title, body, badge_color=BLUE):
    """A numbered step with circle badge."""
    circle = Table([[Paragraph(num, ParagraphStyle("_", fontName="Helvetica-Bold", fontSize=13,
                     textColor=colors.white, alignment=TA_CENTER))]],
                   colWidths=[9*mm], rowHeights=[9*mm])
    circle.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), badge_color),
        ("ROUNDEDCORNERS",(0,0),(-1,-1),4),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ]))
    content = Table([
        [Paragraph(title, ST["step_title"])],
        [Paragraph(body,  ST["step_body"])],
    ], colWidths=[CONTENT_W - 16*mm])
    content.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), BLUE_LT),
        ("BOX",(0,0),(-1,-1),0.5,BLUE_BD),
        ("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8),
        ("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10),
    ]))
    row = Table([[circle, content]], colWidths=[12*mm, CONTENT_W - 12*mm])
    row.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),
                              ("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),0),
                              ("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),4)]))
    return KeepTogether([row, spacer(2)])

def colour_key_row(dot_color, name, desc):
    dot = Table([[""]], colWidths=[6*mm], rowHeights=[6*mm])
    dot.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),dot_color),
                              ("ROUNDEDCORNERS",(0,0),(-1,-1),2)]))
    n = Paragraph(f"<b>{name}</b>", ParagraphStyle("_", fontName="Helvetica-Bold",fontSize=10,textColor=BODY_TEXT))
    d = Paragraph(desc, ParagraphStyle("_", fontName="Helvetica",fontSize=9,textColor=MUTED,leading=13))
    content = Table([[n],[d]], colWidths=[CONTENT_W - 18*mm])
    content.setStyle(TableStyle([("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0)]))
    row = Table([[dot, content]], colWidths=[10*mm, CONTENT_W - 10*mm])
    row.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                              ("BACKGROUND",(0,0),(-1,-1),colors.white),
                              ("BOX",(0,0),(-1,-1),0.4,colors.HexColor("#e2e8f0")),
                              ("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),
                              ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7)]))
    return KeepTogether([row, spacer(1.5)])

def code_block(lines):
    """Monospace dark background code block."""
    paras = [Paragraph(line if line.strip() else " ", ST["code"]) for line in lines]
    tbl = Table([[p] for p in paras], colWidths=[CONTENT_W])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), CODE_BG),
        ("LEFTPADDING",(0,0),(-1,-1),12),("RIGHTPADDING",(0,0),(-1,-1),12),
        ("TOPPADDING",(0,0),(0,0),10),("BOTTOMPADDING",(0,-1),(-1,-1),10),
        ("TOPPADDING",(0,1),(-1,-1),1),("BOTTOMPADDING",(0,0),(-1,-2),1),
    ]))
    return KeepTogether([tbl, spacer(3)])

def risk_row(level, title, mitigation):
    level_colours = {"LOW":(GREEN_LT,TEAL_BD,TEAL), "MEDIUM":(AMBER_LT,AMBER_BD,AMBER), "HIGH":(RED_LT,RED_BD,RED)}
    bg, bd, tc = level_colours.get(level, (BLUE_LT,BLUE_BD,BLUE))
    badge = Table([[Paragraph(level, ParagraphStyle("_", fontName="Helvetica-Bold", fontSize=8,
                    textColor=colors.white, alignment=TA_CENTER))]],
                  colWidths=[16*mm], rowHeights=[6*mm])
    badge.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),tc),("ALIGN",(0,0),(-1,-1),"CENTER"),
                                ("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
    content = Table([
        [Paragraph(f"<b>{title}</b>", ParagraphStyle("_",fontName="Helvetica-Bold",fontSize=10,textColor=BODY_TEXT,spaceAfter=3))],
        [Paragraph(mitigation,        ParagraphStyle("_",fontName="Helvetica",fontSize=9,textColor=MUTED,leading=13))],
    ], colWidths=[CONTENT_W - 24*mm])
    content.setStyle(TableStyle([("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0)]))
    row = Table([[badge, content]], colWidths=[20*mm, CONTENT_W - 20*mm])
    row.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),bg),("BOX",(0,0),(-1,-1),0.5,bd),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8),
        ("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),
    ]))
    return KeepTogether([row, spacer(2)])

def approval_boxes(roles):
    boxes = []
    w = CONTENT_W / len(roles)
    for role in roles:
        rp = Paragraph(role.upper(), ParagraphStyle("_", fontName="Helvetica-Bold", fontSize=8,
                        textColor=MUTED, alignment=TA_CENTER, letterSpacing=0.5))
        sig = Table([[""],[""],[""],["Signature"],[""],["Date: _______________"]], colWidths=[w - 8*mm])
        sig.setStyle(TableStyle([
            ("FONTNAME",(0,0),(-1,-1),"Helvetica"),("FONTSIZE",(0,0),(-1,-1),8),
            ("TEXTCOLOR",(0,0),(-1,-1),LIGHT_MUTED),("ALIGN",(0,0),(-1,-1),"CENTER"),
            ("LINEBELOW",(0,2),(-1,2),0.5,colors.HexColor("#e2e8f0")),
            ("ROWHEIGHT",(0,0),(0,0),12),("ROWHEIGHT",(0,1),(0,1),12),
            ("ROWHEIGHT",(0,2),(0,2),12),
        ]))
        b = Table([[rp],[sig]], colWidths=[w - 4*mm])
        b.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,-1),colors.white),("BOX",(0,0),(-1,-1),0.5,colors.HexColor("#e2e8f0")),
            ("TOPPADDING",(0,0),(-1,-1),10),("BOTTOMPADDING",(0,0),(-1,-1),10),
            ("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),
        ]))
        boxes.append(b)
    row = Table([boxes], colWidths=[w]*len(roles))
    row.setStyle(TableStyle([("LEFTPADDING",(0,0),(-1,-1),2),("RIGHTPADDING",(0,0),(-1,-1),2)]))
    return KeepTogether([row, spacer(4)])

# ── Document build ─────────────────────────────────────────────────────────
def build():
    doc = SimpleDocTemplate(
        OUT, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=20*mm, bottomMargin=22*mm,
        title="Sempra SAP Data Migration Dashboard - Leadership Documentation v2.0",
        author="Kishor Marri - SAP Migration Team",
        subject="SAP Data Migration Tracking Dashboard",
    )

    story = []

    # ══════════════════════════════════════════════════════════════════════════
    # COVER PAGE
    # ══════════════════════════════════════════════════════════════════════════
    story.append(spacer(18))
    story.append(Paragraph("SEMPRA ENERGY  |  IT PROGRAMME", ST["cover_tag"]))
    story.append(spacer(4))
    story.append(Paragraph("SAP Data Migration<br/>Tracking Dashboard", ST["cover_h1"]))
    story.append(spacer(3))
    story.append(Paragraph(
        "A self-contained, browser-based control room for tracking all three Data Migration "
        "cycles (DM1 &rarr; DM2 &rarr; DM3) &mdash; measuring how many SAP tables have been "
        "successfully exported, imported, and reconciled across source and target systems. "
        "No cloud. No manual effort. One click.", ST["cover_sub"]))
    story.append(spacer(6))

    # cycle badges
    badges_data = [
        ("DM1 - Cycle 1", DM1), ("DM2 - Cycle 2", DM2), ("DM3 - Cycle 3", DM3),
        ("100% Local - Zero Cloud", ARCH_BLUE), ("Release v1.0", SLATE),
    ]
    badge_cells = []
    for text, col in badges_data:
        bp = Paragraph(text, ParagraphStyle("_", fontName="Helvetica-Bold", fontSize=9,
                        textColor=colors.white, alignment=TA_CENTER))
        bt = Table([[bp]], colWidths=[None])
        bt.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),col),("ROUNDEDCORNERS",(0,0),(-1,-1),4),
                                  ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
                                  ("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10)]))
        badge_cells.append(bt)
    brow = Table([badge_cells])
    brow.setStyle(TableStyle([("LEFTPADDING",(0,0),(-1,-1),3),("RIGHTPADDING",(0,0),(-1,-1),3)]))
    story.append(brow)
    story.append(spacer(16))

    # meta bar
    meta_rows = [
        [Paragraph("<b>Project:</b> SAP Data Migration - Sempra", ST["cover_meta"]),
         Paragraph("<b>Doc Version:</b> 2.0", ST["cover_meta"]),
         Paragraph("<b>Classification:</b> Internal Use Only", ST["cover_meta"])],
        [Paragraph("<b>Audience:</b> Leadership, PM, Technical Teams", ST["cover_meta"]),
         Paragraph(f"<b>Generated:</b> {datetime.now().strftime('%d %b %Y %H:%M')}", ST["cover_meta"]),
         Paragraph("<b>Prepared by:</b> Kishor Marri - SAP Migration Team", ST["cover_meta"])],
    ]
    mt = Table(meta_rows, colWidths=[CONTENT_W/3]*3)
    mt.setStyle(TableStyle([
        ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
        ("LINEBEFORE",(1,0),(1,-1),0.3,colors.HexColor("#334155")),
        ("LINEBEFORE",(2,0),(2,-1),0.3,colors.HexColor("#334155")),
    ]))
    story.append(mt)
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # TABLE OF CONTENTS
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("TABLE OF CONTENTS", ParagraphStyle("_", fontName="Helvetica-Bold",
        fontSize=8, textColor=MUTED, letterSpacing=1.5, spaceAfter=10)))
    toc_items = [
        ("01","Executive Summary","Business value & purpose"),
        ("02","What Problem It Solves","Before vs After comparison"),
        ("03","The Three Migration Cycles","DM1 / DM2 / DM3 explained"),
        ("04","Step-by-Step User Guide","How to use the dashboard"),
        ("05","Colour & Status Key","What every colour means"),
        ("06","Dashboard Features","Complete feature catalogue"),
        ("07","Technical Architecture","How it works under the hood"),
        ("08","File & Component Inventory","Every file explained"),
        ("09","Data Flow & Deduplication","How records are counted correctly"),
        ("10","Security & Data Privacy","No cloud, no risk"),
        ("11","Risks & Mitigations","Risk register"),
        ("12","Approval & Sign-Off","Leadership approval page"),
    ]
    toc_rows = []
    for i, (num, lbl, sub) in enumerate(toc_items):
        bg = ROW_EVEN if i%2==1 else colors.white
        toc_rows.append([
            Paragraph(num, ParagraphStyle("_",fontName="Helvetica-Bold",fontSize=9,textColor=LIGHT_MUTED,alignment=TA_CENTER)),
            Paragraph(f"<b>{lbl}</b><br/><font size='8' color='#94a3b8'>{sub}</font>",
                      ParagraphStyle("_",fontName="Helvetica",fontSize=10,textColor=BODY_TEXT,leading=14)),
        ])
    toc_tbl = Table(toc_rows, colWidths=[14*mm, CONTENT_W-14*mm])
    toc_tbl.setStyle(TableStyle([
        ("ROWBACKGROUNDS",(0,0),(-1,-1),[colors.white, ROW_EVEN]),
        ("GRID",(0,0),(-1,-1),0.3,colors.HexColor("#e2e8f0")),
        ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7),
        ("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ]))
    story.append(toc_tbl)
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 01 — EXECUTIVE SUMMARY
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_header("01","Executive Summary","Business value and purpose - for leadership audiences", TEAL))
    story.append(green_box("In Plain English",
        "This dashboard is Sempra's single source of truth for SAP data migration health. "
        "It automatically reads migration data files, counts how many SAP tables were successfully "
        "moved from the old system to the new one, and shows a live reconciliation score - all in "
        "real time, with no manual effort beyond clicking one button."))
    story.append(kpi_strip([
        ("3",     "Migration Cycles",  "DM1 -> DM2 -> DM3",       DM1),
        ("5",     "Source Files",      "Auto-read from disk",      ARCH_BLUE),
        ("100%",  "Local Processing",  "Zero cloud dependency",    GREEN_OK),
        ("<10s",  "Full Sync Time",    "All 3 cycles at once",     AMBER_OK),
        ("2 min", "Auto-Refresh",      "Always current",           ARCH_BLUE),
        ("0",     "Manual Steps",      "Fully automated",          GREEN_OK),
    ]))
    story.append(blue_box("What Leadership Needs to Know",
        "- The dashboard replaces hours of manual Excel reconciliation with a single button click.<br/>"
        "- It covers all three migration waves (DM1, DM2, DM3) on one screen, with per-cycle drill-down.<br/>"
        "- Data never leaves the Sempra laptop - processed entirely in the browser.<br/>"
        "- No licences, no cloud subscriptions, no third-party costs for core functionality.<br/>"
        "- Mismatches, missing exports, and incomplete migrations are flagged automatically."))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 02 — WHAT PROBLEM IT SOLVES
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_header("02","What Problem It Solves","The Before vs After", TEAL))
    story.append(compare_pair(
        "BEFORE - Manual Process",
        "Migration teams manually opened multiple Excel files, cross-referenced them by hand, "
        "and produced status reports that were already out of date before they were finished. "
        "Double-counting of exported and imported records inflated match numbers. "
        "No single view existed across all three cycles.",
        "AFTER - This Dashboard",
        "One click reads all five source files automatically, deduplicates records using a "
        "DISTINCT algorithm, calculates reconciliation percentages for all three cycles in "
        "parallel, and displays live colour-coded health indicators - auto-refreshing every 2 minutes."
    ))
    story.append(data_table(
        ["Aspect","Manual Approach (Before)","This Dashboard (After)"],
        [
            ["Time to reconcile",     "30-60 minutes per cycle",                  "Under 10 seconds - all 3 cycles"],
            ["Accuracy",              "Prone to double-counting & formula errors", "DISTINCT dedup algorithm - always correct"],
            ["Coverage",              "One cycle at a time",                       "All 3 cycles simultaneously"],
            ["Data freshness",        "Updated only when run manually",            "Auto-refreshes every 2 minutes"],
            ["Flagging issues",       "Manual - easy to miss",                     "Automatic colour-coded indicators"],
            ["Leadership visibility", "Email attachments or verbal updates",       "Live dashboard, printable, PDF-ready"],
            ["SAP source counts",     "Manual SE16N queries per table",            "Automated RFC with 3 fallback methods"],
            ["Data security",         "Files emailed between team members",        "Never leaves the local machine"],
        ],
        col_widths=[38*mm, 72*mm, 72*mm],
        ok_cols=[2], warn_cols=[1],
    ))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 03 — THREE MIGRATION CYCLES
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_header("03","The Three Migration Cycles","DM1 / DM2 / DM3 - what each wave covers", TEAL))
    story.append(blue_box("Context",
        "Sempra's SAP migration runs in three progressive waves. Each wave moves a batch of SAP "
        "tables from the source system (ES2) to the target system (SQ1). The dashboard tracks "
        "each wave independently and shows a cross-cycle comparison on the master screen."))

    cycle_rows = [
        [Paragraph("<b>DM1 - Cycle 1 (Wave 1)</b>", ParagraphStyle("_",fontName="Helvetica-Bold",fontSize=10,textColor=DM1,spaceAfter=4)),
         Paragraph("First migration wave. Reference List: <i>Reflist_m1.xlsx</i> plus Export/Import file: "
                   "<i>DM1_ES2-SQ1 Export-Import.xlsx</i>. Both EXP and IMP data available - full reconciliation possible.",
                   ParagraphStyle("_",fontName="Helvetica",fontSize=9.5,textColor=BODY_TEXT,leading=14))],
        [Paragraph("<b>DM2 - Cycle 2 (Wave 2)</b>", ParagraphStyle("_",fontName="Helvetica-Bold",fontSize=10,textColor=DM2,spaceAfter=4)),
         Paragraph("Second migration wave. Uses <i>DM2 REF.xlsx</i> and <i>EXPORT IMPORT_DM2.xlsx</i>. "
                   "Same full reconciliation structure as DM1 - all EXP and IMP data present. Tables tracked separately.",
                   ParagraphStyle("_",fontName="Helvetica",fontSize=9.5,textColor=BODY_TEXT,leading=14))],
        [Paragraph("<b>DM3 - Cycle 3 (Wave 3)</b>", ParagraphStyle("_",fontName="Helvetica-Bold",fontSize=10,textColor=DM3,spaceAfter=4)),
         Paragraph("Third wave - currently in progress. Only <i>ref dm3.xlsx</i> available; it carries both export "
                   "and import rows in a combined format. Dashboard shows amber 'Migration In Progress' banner automatically.",
                   ParagraphStyle("_",fontName="Helvetica",fontSize=9.5,textColor=BODY_TEXT,leading=14))],
    ]
    cycle_tbl = Table(cycle_rows, colWidths=[48*mm, CONTENT_W-48*mm])
    cycle_tbl.setStyle(TableStyle([
        ("ROWBACKGROUNDS",(0,0),(-1,-1),[colors.white, ROW_EVEN]),
        ("GRID",(0,0),(-1,-1),0.4,colors.HexColor("#e2e8f0")),
        ("LEFTPADDING",(0,0),(0,-1),12),("LINEBEFORE",(0,0),(0,-1),4,DM1),
        ("TOPPADDING",(0,0),(-1,-1),10),("BOTTOMPADDING",(0,0),(-1,-1),10),
        ("LEFTPADDING",(1,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
    ]))
    # colour the left borders per cycle
    cycle_tbl.setStyle(TableStyle([
        ("LINEBEFORE",(0,0),(0,0),4,DM1),("LINEBEFORE",(0,1),(0,1),4,DM2),("LINEBEFORE",(0,2),(0,2),4,DM3),
    ]))
    story.append(KeepTogether([cycle_tbl, spacer(3)]))
    story.append(data_table(
        ["Cycle","Brand Colour","Reference File","EXP/IMP File","Status"],
        [
            ["DM1","Blue",  "Reflist_m1.xlsx",    "DM1_ES2-SQ1 Export-Import.xlsx","Full data - reconcilable"],
            ["DM2","Purple","DM2 REF.xlsx",        "EXPORT IMPORT_DM2.xlsx",        "Full data - reconcilable"],
            ["DM3","Green", "ref dm3.xlsx",         "Combined in REF file",          "In progress - REF only"],
        ],
        col_widths=[18*mm,28*mm,52*mm,62*mm,32*mm],
        ok_cols=[4], warn_cols=[4],
    ))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 04 — STEP-BY-STEP USER GUIDE
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_header("04","Step-by-Step User Guide","How to launch and use the dashboard - no technical knowledge required", AMBER))
    story.append(amber_box("Prerequisites",
        "Data files must be in: C:\\Users\\KishorMarri\\.bob\\DM1\\,  DM2\\  and  DM3\\\n"
        "Python 3.8+ must be installed. Run once: pip install flask flask-cors openpyxl pandas xlrd"))

    step_colors = [DM1, DM2, DM3, ARCH_BLUE, AMBER, TEAL]
    steps = [
        ("1","Launch the Dashboard",
         "Open PowerShell in the project folder and run:  python launch_dashboard.py\n\n"
         "This starts two background services and opens the master dashboard automatically at:\n"
         "http://localhost:5003/Sempra_CrossCycle_Summary_MASTER.html\n\n"
         "TIP: A new PowerShell window opens for the File Bridge - leave it running. "
         "The browser opens automatically in about 5 seconds once the bridge is ready."),
        ("2","Run Full 3-Cycle Automation",
         "Click the Auto-Sync All Cycles button in the top toolbar. "
         "The button animates with a rainbow sweep while running. "
         "Three coloured sync circles appear (blue/purple/green) - one per cycle - "
         "spinning while reading and showing the match % when done.\n\n"
         "TIP: The full sync completes in under 10 seconds."),
        ("3","Read the Results on Screen",
         "Each cycle card shows:\n"
         "- A large semicircle gauge showing the reconciliation match %\n"
         "- Total tables in scope vs tables fully reconciled\n"
         "- Mismatched, not-exported, and not-imported counts\n"
         "- A badge box: green border = healthy, red border = issues found\n\n"
         "The cross-cycle comparison table below lets you compare DM1, DM2, and DM3 side by side."),
        ("4","Switch Views: Business / Technical / Performance",
         "Three tabs at the top switch the dashboard:\n"
         "- Business View: RAG scorecards and insight boxes for leadership\n"
         "- Technical View: per-table detail with source/target counts and variance columns\n"
         "- Performance View: timing metrics, file sizes, cache hit rates\n\n"
         "TIP: Business View is the best view for leadership presentations and printed reports."),
        ("5","Drill Down to Individual Cycle Dashboards",
         "Click DM1 / DM2 / DM3 navigation buttons to open that cycle's detail page:\n"
         "- Upload new Excel files via drag-and-drop\n"
         "- See a searchable per-table breakdown with EXP/IMP record counts and variance\n"
         "- Download filtered sub-sets (mismatches only, not-exported only, etc.) as CSV or Excel\n\n"
         "TIP: Results are saved in localStorage so they persist across page reloads."),
        ("6","Export Reports & Prints",
         "Use browser Print (Ctrl+P) and choose Save as PDF for a leadership-ready document. "
         "The dashboard switches to a clean white background with all colours preserved.\n\n"
         "For Excel exports with SAP SE16N source counts, use the Download SE16N Counts button "
         "in the Automation panel (Step 4) - produces a colour-coded XLSX with a Summary sheet."),
    ]
    for i, (num, title, body) in enumerate(steps):
        story.append(step_row(num, title, body, step_colors[i]))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 05 — COLOUR KEY
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_header("05","Colour & Status Key","What every colour and indicator means - consistent across all screens", BLUE))
    story.append(blue_box("Universal Colour Conventions",
        "These colours are used consistently across every screen, table, badge, and indicator "
        "in the dashboard. Learn them once - read any view instantly."))

    ck_items = [
        (GREEN_OK,                        "Green - Fully Reconciled",      "Source = Target AND EXP = IMP. Table migrated successfully."),
        (colors.HexColor("#f59e0b"),      "Amber - In Progress / Warning", "Source does not equal Target, or migration not yet complete. Needs monitoring."),
        (colors.HexColor("#ef4444"),      "Red - Mismatch / Failed",       "EXP does not equal IMP record count, or table not migrated. Action required."),
        (colors.HexColor("#94a3b8"),      "Grey - No Data / Excluded",     "Table in Reference List but no export/import data found yet."),
        (DM1,                             "Blue - DM1 Cycle 1",            "All DM1 labels, borders, badges, and navigation elements."),
        (DM2,                             "Purple - DM2 Cycle 2",          "All DM2 labels, borders, badges, and navigation elements."),
    ]
    for dot, name, desc in ck_items:
        story.append(colour_key_row(dot, name, desc))

    story.append(spacer(4))
    story.append(data_table(
        ["Indicator","Where It Appears","What It Means"],
        [
            ["RAG Badge (Green/Amber/Red)","Business View scorecards",     "Overall health: Green=on track, Amber=review needed, Red=critical issues"],
            ["Semicircle Gauge",           "Each cycle card (MASTER)",     "Visual match % 0-100. Spins with READING overlay during sync"],
            ["Sync Circles (spinning)",    "Refresh toolbar",              "Appear during automation; spin in cycle colour; show % when done; auto-hide after 5s"],
            ["Badge Box (green/red border)","Below each cycle gauge",      "Post-sync summary: green border >95% match, red border = issues detected"],
            ["Rainbow Button Animation",   "Auto-Sync All Cycles button",  "Sweeping rainbow glow while running; stops when all 3 cycles complete"],
            ["Amber Migration Banner",     "DM3 dashboard",                "Shown when only Reference List loaded - EXP/IMP not yet available for DM3"],
            ["Red Dot on Countdown",       "Auto-refresh countdown badge", "Next refresh is within 60 seconds - data is about to update automatically"],
        ],
        col_widths=[52*mm, 52*mm, 78*mm],
    ))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 06 — DASHBOARD FEATURES
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_header("06","Dashboard Features","Complete feature catalogue - everything the system can do", TEAL))
    story.append(data_table(
        ["Feature","Where","Description"],
        [
            ["3-Cycle Side-by-Side View",      "MASTER dashboard",         "DM1, DM2, DM3 cards on one page with gauge, KPIs, and match counts"],
            ["Auto-Sync All Cycles",           "Toolbar button",           "One click reads all 5 Excel files, parses in-browser, updates all cards in under 10 seconds"],
            ["Semicircle Match Gauges",        "Each cycle card",          "Animated SVG arc 0-100%. Spins with READING overlay during sync, snaps to final value"],
            ["Business/Technical/Perf Tabs",  "MASTER dashboard",         "Switch between executive RAG view, per-table technical detail, and system performance metrics"],
            ["Business Insights Panel",        "Business View",            "Auto-generated flags: missing exports, count mismatches, DM3 status, overall match rate"],
            ["Auto-Refresh (2-min interval)",  "Toolbar",                  "Countdown badge with pause/resume. Red dot when under 60 seconds. Amber when paused"],
            ["Sync Status Circles",            "Refresh bar",              "Per-cycle circles during automation: spin in brand colour, show % when done, auto-hide after 5s"],
            ["Inline Badge Boxes",             "Below each gauge",         "Non-disruptive post-sync summary - no popups, no modal interruptions to workflow"],
            ["Per-Cycle Detail Dashboards",    "DM1 / DM2 / DM3 pages",   "Drag-and-drop file upload, searchable per-table breakdown, KPI strip, progress bar"],
            ["DISTINCT Deduplication",         "All 6 aggregation points", "DISTINCT on (Type, Table, Record Count) before SUM - prevents double-counting EXP/IMP rows"],
            ["Count Validation Column",        "Per-cycle dashboards",     "EXP vs IMP record count difference per table - highlights inconsistencies in migration files"],
            ["Cross-Cycle Comparison Table",   "MASTER - Technical View",  "All tables across DM1/DM2/DM3 with per-cycle source/target/variance columns in one table"],
            ["Print / PDF Export",             "Browser Ctrl+P",           "Full print CSS: white background, colours preserved, navigation hidden, clean output"],
            ["SE16N SAP Source Counts",        "Automation Panel",         "RFC connection to SAP, counts every table via SE16N-equivalent FM with 3 fallback methods"],
            ["Excel Export (colour-coded)",    "Automation Panel Step 4",  "Downloads Source vs Target count XLSX with green/red/amber row colouring + Summary sheet"],
            ["localStorage Persistence",       "All dashboards",           "Last-analysed results survive page reloads - no need to re-sync if data unchanged"],
            ["Dynamic Bridge URL",             "All dashboards (JS)",      "Uses window.location.hostname - works on any machine name or IP without code changes"],
            ["DM3 REF-Only Mode",              "DM3 dashboard",            "Gracefully handles no separate EXP/IMP file - shows amber migration-in-progress banner"],
        ],
        col_widths=[52*mm, 44*mm, 86*mm],
    ))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 07 — TECHNICAL ARCHITECTURE
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_header("07","Technical Architecture","How the system works under the hood - for technical reviewers", PURPLE))
    story.append(purple_box("Architecture Overview",
        "The system is a three-layer local stack: a static HTML/JS browser layer, a lightweight "
        "Python file-serving bridge, and the local file system where Excel data files live. "
        "Nothing is sent to any external server - all computation happens in the browser using SheetJS for Excel parsing."))

    story.append(code_block([
        "BROWSER LAYER  (HTML + JavaScript + SheetJS v0.18.5)",
        "  Sempra_CrossCycle_Summary_MASTER.html  <- Main dashboard, all 3 cycles + automation",
        "  Sempra_DM1_Dashboard.html              <- DM1 per-table detail",
        "  Sempra_DM2_Dashboard.html              <- DM2 per-table detail",
        "  Sempra_DM3_Dashboard.html              <- DM3 per-table detail (REF-only mode)",
        "         |",
        "         |  fetch(http://localhost:5002/file?cycle=DM1&type=ref)",
        "         |  gzip-compressed Excel bytes  <-  ETag 304 caching",
        "         v",
        "FILE WATCHER BRIDGE  (Python Flask - port 5002)",
        "  automation/file_watcher_bridge.py",
        "    * In-memory file cache     - eliminates repeated disk reads",
        "    * Gzip compression         - 60-70% smaller transfers",
        "    * ETag / 304 Not Modified  - skips read if file unchanged on disk",
        "    * Bulk /files/all endpoint - manifest check before fetching bytes",
        "    * Auto cache-warm on startup",
        "         |",
        "         |  reads raw Excel bytes from local disk",
        "         v",
        "LOCAL FILE SYSTEM",
        "  C:\\Users\\KishorMarri\\.bob\\DM1\\Reflist_m1.xlsx",
        "  C:\\Users\\KishorMarri\\.bob\\DM1\\DM1_ES2-SQ1 Export-Import.xlsx",
        "  C:\\Users\\KishorMarri\\.bob\\DM2\\DM2 REF.xlsx",
        "  C:\\Users\\KishorMarri\\.bob\\DM2\\EXPORT IMPORT_DM2.xlsx",
        "  C:\\Users\\KishorMarri\\.bob\\DM3\\ref dm3.xlsx",
        "",
        "SAP BRIDGE  (Optional - Python Flask - port 5001)",
        "  automation/sap_bridge.py",
        "    * Method 1: EM_GET_NUMBER_OF_ENTRIES  (SE16N internal FM - fastest)",
        "    * Method 2: RFC_READ_TABLE            (standard fallback)",
        "    * Method 3: BBP_RFC_READ_TABLE        (alternative fallback)",
        "    * Demo mode: deterministic simulated counts if pyrfc not installed",
        "    * /export_excel: colour-coded XLSX with Summary sheet",
    ]))

    story.append(data_table(
        ["Layer","Technology","Port","Role"],
        [
            ["Browser Frontend",   "HTML5, Vanilla JS, SheetJS v0.18.5, SVG",    "5003 (static)", "Excel parsing, reconciliation calculation, rendering, localStorage caching"],
            ["File Bridge",        "Python 3.8+, Flask, Flask-CORS, gzip",        "5002",          "Serves Excel file bytes to the browser with gzip compression and ETag caching"],
            ["Static Server",      "Python http.server (built-in stdlib)",        "5003",          "Serves HTML files over HTTP - avoids CORS issues with file:// protocol"],
            ["SAP Bridge (opt.)",  "Python, Flask, pyrfc (optional), openpyxl",   "5001",          "RFC connection to SAP for SE16N-style table counts + colour-coded Excel export"],
            ["Launcher",           "Python subprocess, threading, webbrowser",    "-",             "Orchestrates startup of all services and opens the browser automatically"],
        ],
        col_widths=[30*mm, 55*mm, 22*mm, 75*mm],
    ))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 08 — FILE INVENTORY
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_header("08","File & Component Inventory","Every file in the project - what it does and when to edit it", PURPLE))
    story.append(data_table(
        ["File","Type","Purpose","Edit Required?"],
        [
            ["Sempra_CrossCycle_Summary_MASTER.html","HTML/JS/CSS","Main dashboard - 3-cycle cross view, automation, all view tabs","Rarely - labels only"],
            ["Sempra_DM1_Dashboard.html",            "HTML/JS/CSS","DM1 per-table detail - upload, search, KPI strip, download",   "Rarely"],
            ["Sempra_DM2_Dashboard.html",            "HTML/JS/CSS","DM2 per-table detail - same structure as DM1",                 "Rarely"],
            ["Sempra_DM3_Dashboard.html",            "HTML/JS/CSS","DM3 detail - REF-only mode with amber migration banner",       "Rarely"],
            ["launch_dashboard.py",                  "Python",     "One-click launcher - starts bridge + static server + opens browser","No changes needed"],
            ["automation/file_watcher_bridge.py",    "Python/Flask","Local HTTP bridge port 5002 - serves Excel bytes, gzip + ETag","Only if file paths change"],
            ["automation/sap_bridge.py",             "Python/Flask","SAP RFC bridge port 5001 - SE16N counts, Excel export",       "Only if SAP details change"],
            ["automation/01_sap_source_count.py",    "Python",     "Standalone SAP source count extractor (batch use)",            "Configuration only"],
            ["automation/02_target_count.py",        "Python",     "Standalone target system count extractor (batch use)",         "Configuration only"],
            ["automation/03_orchestrator.py",        "Python",     "Full pipeline orchestrator for scheduled batch runs",          "Configuration only"],
            ["automation/output/",                   "Folder",     "Auto-created - stores ref_tables.json, dashboard_ref_counts.json","Auto-managed"],
            ["automation/logs/",                     "Folder",     "Auto-created - bridge.log and file_watcher.log for diagnostics","Auto-managed"],
        ],
        col_widths=[55*mm, 22*mm, 72*mm, 33*mm],
        ok_cols=[3], warn_cols=[3],
    ))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 09 — DATA FLOW & DEDUPLICATION
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_header("09","Data Flow & Deduplication Logic","How records are counted correctly - critical for accuracy", PURPLE))
    story.append(blue_box("Why Deduplication Matters",
        "The migration Excel files contain separate rows for each Export and Import operation. "
        "Without deduplication, the same table appears multiple times, inflating counts. "
        "The dashboard uses a DISTINCT algorithm - equivalent to SQL's SELECT DISTINCT - to ensure "
        "each unique (Type, Table Name, Record Count) combination is counted only once before summing. "
        "EXP and IMP rows are processed SEPARATELY to avoid cross-type errors. "
        "This fix was applied to all 6 aggregation points across 4 files."))
    story.append(code_block([
        "RECONCILIATION DATA FLOW - STEP BY STEP",
        "",
        "Step 1: FETCH",
        "  Browser -> GET /file?cycle=DM1&type=ref  ->  bridge returns gzipped .xlsx bytes",
        "  Browser -> GET /file?cycle=DM1&type=exp  ->  bridge returns gzipped .xlsx bytes",
        "  (ETag check: if file unchanged, bridge returns 304 Not Modified - zero disk re-read)",
        "",
        "Step 2: PARSE",
        "  SheetJS.read(arrayBuffer)  ->  XLSX workbook in memory (100% browser-side, no server needed)",
        "  sheet_to_json()            ->  array of row objects",
        "",
        "Step 3: DEDUPLICATE",
        "  EXP rows: DISTINCT on (Type=EXP, TableName, RecordCount)  ->  deduplicated set  ->  SUM",
        "  IMP rows: DISTINCT on (Type=IMP, TableName, RecordCount)  ->  deduplicated set  ->  SUM",
        "  NOTE: EXP and IMP processed SEPARATELY - prevents cross-type deduplication errors",
        "",
        "Step 4: RECONCILE",
        "  For each table in the Reference List:",
        "    Status = GREEN   if EXP_count == IMP_count  AND  src_count == tgt_count",
        "    Status = AMBER   if counts exist but do not match",
        "    Status = RED     if EXP != IMP  OR  migration not started",
        "    Status = GREY    if no EXP/IMP data found for this table",
        "",
        "Step 5: AGGREGATE",
        "  Match % = (fully reconciled tables) / (total tables in REF list) * 100",
        "",
        "Step 6: RENDER",
        "  Update SVG gauge arc, KPI numbers, badge box, sync circles on screen",
        "  Save summary to localStorage for persistence across page reloads",
    ]))
    story.append(green_box("DM3 Special Case - Combined File",
        "DM3 has no separate EXP/IMP file. The Reference file contains both Export and Import rows "
        "in a combined format. The parser handles this automatically by setting impData = expData "
        "(both EXP and IMP come from the same parsed data object). The same DISTINCT deduplication "
        "logic is applied. This is why DM3 shows an amber 'Migration In Progress' banner until a "
        "separate EXP/IMP file becomes available for the cycle."))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 10 — SECURITY
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_header("10","Security & Data Privacy","No cloud, no external calls - data stays on the Sempra laptop at all times", ARCH_BLUE))
    story.append(green_box("Security Statement",
        "No Sempra data ever leaves the local machine. All Excel files are read from a local "
        "directory, served via a localhost-only Flask server (bound to 127.0.0.1 - not reachable "
        "from the network), parsed entirely in the browser using SheetJS, and results are stored "
        "only in the browser's localStorage. There is no cloud API, no telemetry, and no "
        "external network calls of any kind."))
    story.append(data_table(
        ["Risk Vector","Mitigation in Place"],
        [
            ["Data leaving the machine",  "All Flask servers bind to 127.0.0.1 only - not accessible from any other machine on the network"],
            ["External API calls",        "SheetJS is a one-time JS library fetch from CDN - no data is sent. Replaceable with a local copy for air-gapped environments in one line"],
            ["SAP credentials",           "Entered in-browser only; passed to localhost SAP bridge only; never written to disk; bridge does not log or store credentials"],
            ["File access control",       "Only files matching the config paths are accessible; no directory traversal; wildcard patterns validated against allowed base folders"],
            ["Persistent data storage",   "Only reconciliation summary numbers stored in localStorage - no raw table data, no SAP credentials, no personally identifiable information"],
            ["Network port exposure",     "Ports 5001, 5002, 5003 all bind to 127.0.0.1 (loopback only) - no firewall rules need to be opened, no network exposure"],
        ],
        col_widths=[52*mm, CONTENT_W-52*mm],
    ))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 11 — RISKS
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_header("11","Risks & Mitigations","Risk register for leadership review", RED))
    risks = [
        ("LOW",    "SheetJS CDN Unavailability",
         "Download SheetJS locally and change the script src to the local path. One-line change in the HTML file. A pre-built local copy can be bundled as standard practice."),
        ("LOW",    "Python Not Installed on Machine",
         "Python 3.8+ is a standard IT install. Document as a prerequisite. If unavailable, the HTML dashboards can still be opened manually via file:// with reduced functionality (no auto-sync)."),
        ("LOW",    "Data File Path Changes",
         "Update DEFAULT_CONFIG in file_watcher_bridge.py, or POST to the /config endpoint from the dashboard Automation panel - no code restart needed, takes effect immediately."),
        ("MEDIUM", "Excel Column Structure Changes",
         "Column index constants (COL_TABLE, COL_SRC, COL_TGT, etc.) are defined at the top of each dashboard script block. Updating them requires no knowledge of the rest of the code."),
        ("MEDIUM", "SAP RFC Connection Failure",
         "The SAP bridge tries 3 RFC methods in sequence (EM_GET_NUMBER_OF_ENTRIES, RFC_READ_TABLE, BBP_RFC_READ_TABLE). If all fail, demo mode provides deterministic simulated counts for testing. The file-based reconciliation dashboard is completely unaffected."),
        ("LOW",    "Port Conflicts (5001 / 5002 / 5003)",
         "Port numbers are defined as constants at the top of each Python file. Change in one place - all references update automatically. No code changes elsewhere required."),
        ("LOW",    "Browser Compatibility",
         "Chrome 90+ and Edge 90+ are fully tested and recommended. SheetJS requires ES2017+ JavaScript support. Firefox and Safari also work but are not the primary test targets for Sempra's environment."),
    ]
    for level, title, mitigation in risks:
        story.append(risk_row(level, title, mitigation))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 12 — APPROVAL
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_header("12","Approval & Sign-Off","Leadership approval section - print and sign, or sign digitally", RED))
    story.append(amber_box("Approval Request",
        "This document provides full visibility into the Sempra SAP Data Migration Tracking Dashboard - "
        "its purpose, functionality, technical design, security posture, and risk profile. "
        "The undersigned confirm they have reviewed this document and approve the solution for "
        "continued use in the SAP migration programme."))
    story.append(approval_boxes(["Project Sponsor", "Programme / IT Manager", "Security / Compliance"]))
    story.append(data_table(
        ["Document Metadata","Value"],
        [
            ["Document Title",     "Sempra SAP Data Migration Tracking Dashboard - Leadership Documentation"],
            ["Document Version",   "v2.0"],
            ["Project",            "SAP Data Migration - Sempra Energy"],
            ["System Name",        "Sempra DM Dashboard v1.0"],
            ["Components",         "1x MASTER dashboard + 3x cycle dashboards + 2x Python bridges + 1x launcher"],
            ["Classification",     "Internal Use Only"],
            ["Prepared by",        "Kishor Marri - SAP Migration Team"],
            ["Technology Stack",   "HTML5, Vanilla JS, SheetJS v0.18.5 (free), Python 3.8+, Flask, Flask-CORS, openpyxl, pandas"],
            ["Deployment Model",   "Local laptop only - no cloud, no network dependencies, no licences required"],
            ["Ports Used",         "5001 (SAP Bridge - optional), 5002 (File Bridge), 5003 (Static) - all 127.0.0.1 loopback only"],
            ["Source System",      "ES2 (SAP Source) -> SQ1 (SAP Target)"],
            ["Generated",          datetime.now().strftime("%d %b %Y %H:%M")],
        ],
        col_widths=[52*mm, CONTENT_W-52*mm],
    ))

    # ══════════════════════════════════════════════════════════════════════════
    # BUILD
    # ══════════════════════════════════════════════════════════════════════════
    doc.build(
        story,
        onFirstPage=on_cover_page,
        onLaterPages=on_page,
    )
    size_kb = os.path.getsize(OUT) // 1024
    print(f"  [OK] PDF saved -> {OUT}  ({size_kb} KB, {doc.page} pages)")

if __name__ == "__main__":
    print("=" * 60)
    print("  Sempra DM Dashboard - Professional PDF Generator")
    print("  Using ReportLab", end=" ")
    import reportlab
    print(reportlab.Version)
    print("=" * 60)
    build()
    print("\n  Opening PDF...")
    os.startfile(os.path.abspath(OUT))
