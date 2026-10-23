"""
Sempra DM Dashboard — Premium Client-Ready PDF Generator
Produces: Sempra_DM_Dashboard_PREMIUM.pdf
Run: python generate_premium_pdf.py
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, HRFlowable, PageBreak, KeepTogether,
                                 Flowable)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.graphics.shapes import Drawing, Rect, String, Circle, Line, Polygon
from reportlab.graphics import renderPDF
import datetime

OUT = "Sempra_DM_Dashboard_PREMIUM.pdf"
W, H = A4   # 595 x 842 pts
CONTENT_W = W - 4*cm

# ── Brand Colours ────────────────────────────────────────────────────────────
NAVY    = colors.HexColor("#0a1628")
BLUE    = colors.HexColor("#1e3a5f")
TEAL    = colors.HexColor("#0f766e")
SKY     = colors.HexColor("#38bdf8")
DM1C    = colors.HexColor("#3b82f6")
DM2C    = colors.HexColor("#a855f7")
DM3C    = colors.HexColor("#22c55e")
AMBER   = colors.HexColor("#f59e0b")
RED_C   = colors.HexColor("#ef4444")
GREEN_C = colors.HexColor("#22c55e")
LTGREY  = colors.HexColor("#f7f8fa")
BORDER  = colors.HexColor("#e5e7eb")
MUTED   = colors.HexColor("#57606a")
DARK    = colors.HexColor("#1f2328")
WHITE   = colors.white

# ── Style factory ────────────────────────────────────────────────────────────
def S(name, **kw): return ParagraphStyle(name, **kw)

COVER_TITLE = S("ct", fontSize=30, leading=38, textColor=WHITE,   fontName="Helvetica-Bold",  alignment=TA_LEFT)
COVER_SUB   = S("cs", fontSize=13, leading=18, textColor=colors.HexColor("#94a3b8"), fontName="Helvetica")
H1s         = S("H1", fontSize=18, leading=24, textColor=NAVY,    fontName="Helvetica-Bold",  spaceBefore=24, spaceAfter=6)
H2s         = S("H2", fontSize=13, leading=18, textColor=BLUE,    fontName="Helvetica-Bold",  spaceBefore=14, spaceAfter=4)
H3s         = S("H3", fontSize=10, leading=14, textColor=DARK,    fontName="Helvetica-Bold",  spaceBefore=8,  spaceAfter=3)
BODY        = S("BD", fontSize=9,  leading=14, textColor=DARK,    fontName="Helvetica",       spaceAfter=5,   alignment=TA_JUSTIFY)
BUL         = S("BU", fontSize=9,  leading=13, textColor=DARK,    fontName="Helvetica",       leftIndent=14,  spaceAfter=3)
NUMs        = S("NU", fontSize=9,  leading=13, textColor=DARK,    fontName="Helvetica",       leftIndent=22,  spaceAfter=4)
CAPN        = S("CA", fontSize=8,  leading=11, textColor=MUTED,   fontName="Helvetica-Oblique", alignment=TA_CENTER, spaceAfter=8)
CODE        = S("CO", fontSize=7.5,leading=11, textColor=colors.HexColor("#1e40af"),
                fontName="Courier", backColor=colors.HexColor("#eff6ff"),
                borderPad=6, spaceAfter=6)
LABEL_SM    = S("LS", fontSize=7,  leading=10, textColor=MUTED,   fontName="Helvetica-Bold",  alignment=TA_CENTER)
BIG_NUM     = S("BN", fontSize=22, leading=26, textColor=NAVY,    fontName="Helvetica-Bold",  alignment=TA_CENTER)
STEP_TITLE  = S("ST", fontSize=10, leading=14, textColor=WHITE,   fontName="Helvetica-Bold")
STEP_BODY   = S("SB", fontSize=8.5,leading=13, textColor=colors.HexColor("#1e293b"), fontName="Helvetica")

def p(t,st=None):  return Paragraph(t, st or BODY)
def h1(t):         return Paragraph(t, H1s)
def h2(t):         return Paragraph(t, H2s)
def h3(t):         return Paragraph(t, H3s)
def sp(n=8):       return Spacer(1, n)
def bul(t):        return Paragraph(f"<bullet>&bull;</bullet> {t}", BUL)
def hr(c=BORDER):  return HRFlowable(width="100%", thickness=0.5, color=c, spaceAfter=6, spaceBefore=6)
def num(i,t):      return Paragraph(f"<seq id='stp'/> &nbsp; {t}", NUMs)

# ── Custom Flowables ─────────────────────────────────────────────────────────

class GradientBanner(Flowable):
    """Full-width gradient heading banner"""
    def __init__(self, title, subtitle="", colour1=NAVY, colour2=BLUE, height=52):
        self.title = title; self.subtitle = subtitle
        self.colour1 = colour1; self.colour2 = colour2; self.height = height
    def wrap(self, w, h): self.w = w; return (w, self.height + 6)
    def draw(self):
        c = self.canv; w = self.w; h = self.height
        c.saveState()
        # Gradient via rectangles
        steps = 30
        for i in range(steps):
            t = i / steps
            r = self.colour1.red   + t*(self.colour2.red   - self.colour1.red)
            g = self.colour1.green + t*(self.colour2.green - self.colour1.green)
            b = self.colour1.blue  + t*(self.colour2.blue  - self.colour1.blue)
            c.setFillColorRGB(r, g, b)
            x0 = w * i / steps; x1 = w * (i+1) / steps
            c.rect(x0, 0, x1-x0, h, stroke=0, fill=1)
        # Accent bar
        c.setFillColor(SKY); c.rect(0, h-3, w, 3, stroke=0, fill=1)
        # Title
        c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 14)
        c.drawString(14, h-26, self.title)
        if self.subtitle:
            c.setFillColor(colors.HexColor("#94a3b8")); c.setFont("Helvetica", 9)
            c.drawString(14, h-38, self.subtitle)
        c.restoreState()

class DashboardMockup(Flowable):
    """Visual mockup of the dashboard UI"""
    def __init__(self, width=CONTENT_W, height=200):
        self.w = width; self.h = height
    def wrap(self, w, h): return (self.w, self.h)
    def draw(self):
        c = self.canv
        c.saveState()
        w, h = self.w, self.h

        # Background
        c.setFillColor(colors.HexColor("#0a0a0a"))
        c.roundRect(0, 0, w, h, 8, stroke=0, fill=1)

        # Top header bar
        c.setFillColor(colors.HexColor("#111827"))
        c.rect(0, h-32, w, 32, stroke=0, fill=1)
        c.setFillColor(SKY); c.setFont("Helvetica-Bold", 9)
        c.drawString(12, h-20, "Sempra Data Migration Dashboard  —  Executive Summary")
        # Status dot
        c.setFillColor(GREEN_C); c.circle(w-20, h-16, 4, stroke=0, fill=1)
        c.setFillColor(WHITE); c.setFont("Helvetica", 7)
        c.drawString(w-14, h-19, "Live")

        # View tabs
        tab_y = h - 54
        tabs = [("Business View", DM3C), ("Technical View", DM1C), ("Performance", DM2C)]
        tab_x = 12
        for label, col in tabs:
            c.setFillColor(col)
            c.roundRect(tab_x, tab_y, 90, 16, 4, stroke=0, fill=1)
            c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 6.5)
            c.drawCentredString(tab_x+45, tab_y+5, label)
            tab_x += 98

        # Three cycle cards
        card_w = (w - 30) / 3
        cards = [
            ("DM1", "Cycle 1", DM1C, 94, "MATCH RATE"),
            ("DM2", "Cycle 2", DM2C, 87, "MATCH RATE"),
            ("DM3", "Cycle 3", DM3C, 73, "IN PROGRESS"),
        ]
        card_y = 14
        for i, (name, sub, col, pct, status) in enumerate(cards):
            cx = 10 + i * (card_w + 5)
            cy = card_y
            cw = card_w
            ch = h - 72

            # Card background
            c.setFillColor(colors.HexColor("#111827"))
            c.roundRect(cx, cy, cw, ch, 6, stroke=0, fill=1)
            # Top colour bar
            c.setFillColor(col)
            c.rect(cx, cy+ch-4, cw, 4, stroke=0, fill=1)

            # Cycle name
            c.setFillColor(col); c.setFont("Helvetica-Bold", 9)
            c.drawCentredString(cx+cw/2, cy+ch-20, name)
            c.setFillColor(MUTED); c.setFont("Helvetica", 7)
            c.drawCentredString(cx+cw/2, cy+ch-30, sub)

            # Gauge arc (simplified as circle)
            gauge_cx = cx + cw/2
            gauge_cy = cy + ch/2 + 4
            r = 28
            c.setStrokeColor(colors.HexColor("#1f2937")); c.setLineWidth(5)
            c.circle(gauge_cx, gauge_cy, r, stroke=1, fill=0)
            c.setStrokeColor(col); c.setLineWidth(5)
            # Draw arc portion
            import math
            sweep = 3.14 * 2 * pct / 100
            c.arc(gauge_cx-r, gauge_cy-r, gauge_cx+r, gauge_cy+r,
                  startAng=90, extent=-(pct*3.6))

            # Percentage
            c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 14)
            c.drawCentredString(gauge_cx, gauge_cy-4, f"{pct}%")

            # Status badge
            badge_col = GREEN_C if pct >= 95 else (AMBER if pct >= 80 else RED_C)
            c.setFillColor(badge_col)
            bw = 60
            c.roundRect(cx+(cw-bw)/2, cy+10, bw, 14, 4, stroke=0, fill=1)
            c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 6)
            c.drawCentredString(cx+cw/2, cy+15, status)

        c.restoreState()

class RAGBadge(Flowable):
    """Inline RAG badge"""
    def __init__(self, status, label, width=120):
        self.status = status; self.label = label; self.width = width
        self.colours = {
            "GREEN": (colors.HexColor("#dcfce7"), colors.HexColor("#15803d"), colors.HexColor("#86efac")),
            "AMBER": (colors.HexColor("#fef9c3"), colors.HexColor("#92400e"), colors.HexColor("#fde047")),
            "RED":   (colors.HexColor("#fee2e2"), colors.HexColor("#dc2626"), colors.HexColor("#fca5a5")),
            "GREY":  (colors.HexColor("#f1f5f9"), colors.HexColor("#475569"), colors.HexColor("#cbd5e1")),
        }
    def wrap(self, w, h): return (self.width, 18)
    def draw(self):
        bg, fg, border = self.colours.get(self.status, self.colours["GREY"])
        c = self.canv; w = self.width
        c.setFillColor(bg); c.setStrokeColor(border); c.setLineWidth(0.5)
        c.roundRect(0, 1, w, 16, 8, stroke=1, fill=1)
        c.setFillColor(fg); c.setFont("Helvetica-Bold", 7.5)
        c.drawCentredString(w/2, 6, self.label)

class StepBox(Flowable):
    """Numbered step with coloured circle and body text"""
    def __init__(self, number, title, body, colour=TEAL, width=CONTENT_W):
        self.number = number; self.title = title; self.body = body
        self.colour = colour; self.width = width
        # Estimate height
        lines = len(body) // 80 + body.count("\n") + 2
        self.height = max(52, lines * 12 + 24)
    def wrap(self, w, h): return (self.width, self.height)
    def draw(self):
        c = self.canv; w = self.width
        c.saveState()
        # Card background
        c.setFillColor(colors.HexColor("#f7f8fa"))
        c.setStrokeColor(self.colour); c.setLineWidth(1)
        c.roundRect(0, 0, w, self.height, 6, stroke=1, fill=1)
        # Left colour bar
        c.setFillColor(self.colour)
        c.roundRect(0, 0, 6, self.height, 3, stroke=0, fill=1)
        # Number circle
        cx = 28; cy = self.height - 22
        c.setFillColor(self.colour)
        c.circle(cx, cy, 12, stroke=0, fill=1)
        c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 9)
        c.drawCentredString(cx, cy-3.5, str(self.number))
        # Title
        c.setFillColor(NAVY); c.setFont("Helvetica-Bold", 10)
        c.drawString(50, self.height-26, self.title)
        # Body
        c.setFillColor(DARK); c.setFont("Helvetica", 8.5)
        y = self.height - 40
        for line in self.body.split("\n"):
            if y < 8: break
            c.drawString(50, y, line[:95])
            y -= 12
        c.restoreState()

class FeatureCard(Flowable):
    """Feature highlight card"""
    def __init__(self, icon, title, desc, colour, width=86):
        self.icon=icon; self.title=title; self.desc=desc
        self.colour=colour; self.width=width; self.height=70
    def wrap(self,w,h): return (self.width, self.height)
    def draw(self):
        c=self.canv; w=self.width; h=self.height
        c.setFillColor(colors.HexColor("#f7f8fa"))
        c.setStrokeColor(self.colour); c.setLineWidth(1)
        c.roundRect(0,0,w,h,5,stroke=1,fill=1)
        c.setFillColor(self.colour); c.roundRect(0,h-4,w,4,2,stroke=0,fill=1)
        c.setFillColor(self.colour); c.setFont("Helvetica-Bold",14)
        c.drawCentredString(w/2,h-20,self.icon)
        c.setFillColor(NAVY); c.setFont("Helvetica-Bold",7.5)
        c.drawCentredString(w/2,h-32,self.title)
        c.setFillColor(MUTED); c.setFont("Helvetica",6.5)
        y=h-44
        for line in self.desc.split("|"):
            c.drawCentredString(w/2,y,line.strip()); y-=10

class BeforeAfter(Flowable):
    """Before vs After comparison visual"""
    def __init__(self, width=CONTENT_W):
        self.w=width; self.h=110
    def wrap(self,w,h): return (self.w, self.h)
    def draw(self):
        c=self.canv; w=self.w; h=self.h; hw=w/2-4
        # BEFORE panel
        c.setFillColor(colors.HexColor("#fff1f2"))
        c.setStrokeColor(RED_C); c.setLineWidth(1)
        c.roundRect(0,0,hw,h,5,stroke=1,fill=1)
        c.setFillColor(RED_C); c.roundRect(0,h-4,hw,4,2,stroke=0,fill=1)
        c.setFillColor(RED_C); c.setFont("Helvetica-Bold",9)
        c.drawString(10,h-18,"✗  BEFORE — Manual Process")
        items=["30–60 min per cycle","Double-counting errors","One cycle at a time",
               "Files emailed between team","Manual SE16N queries","Out-of-date reports"]
        c.setFont("Helvetica",7.5); y=h-32
        for it in items:
            c.setFillColor(RED_C); c.circle(8,y+2,2,stroke=0,fill=1)
            c.setFillColor(DARK); c.drawString(14,y,it); y-=11
        # AFTER panel
        x=hw+8
        c.setFillColor(colors.HexColor("#f0fdf4"))
        c.setStrokeColor(GREEN_C); c.setLineWidth(1)
        c.roundRect(x,0,hw,h,5,stroke=1,fill=1)
        c.setFillColor(GREEN_C); c.roundRect(x,h-4,hw,4,2,stroke=0,fill=1)
        c.setFillColor(GREEN_C); c.setFont("Helvetica-Bold",9)
        c.drawString(x+10,h-18,"✓  AFTER — This Dashboard")
        items2=["Under 10 seconds — all 3 cycles","DISTINCT dedup — always correct",
                "All 3 cycles simultaneously","Data never leaves the laptop",
                "Automated RFC batch queries","Live auto-refresh every 2 min"]
        c.setFont("Helvetica",7.5); y=h-32
        for it in items2:
            c.setFillColor(GREEN_C); c.circle(x+8,y+2,2,stroke=0,fill=1)
            c.setFillColor(DARK); c.drawString(x+14,y,it); y-=11

class ColourKey(Flowable):
    """Colour legend visual"""
    def __init__(self, items, width=CONTENT_W):
        self.items=items; self.w=width; self.h=26*len(items)+10
    def wrap(self,w,h): return (self.w,self.h)
    def draw(self):
        c=self.canv; y=self.h-18
        for col_hex, label, desc in self.items:
            col=colors.HexColor(col_hex)
            c.setFillColor(col); c.roundRect(0,y-4,52,16,4,stroke=0,fill=1)
            c.setFillColor(WHITE); c.setFont("Helvetica-Bold",7)
            c.drawCentredString(26,y+3.5,label)
            c.setFillColor(DARK); c.setFont("Helvetica",8.5)
            c.drawString(62,y+2,desc)
            y-=26

def tbl(data, col_widths=None, hdr_bg=BLUE, font_size=8):
    t = Table(data, colWidths=col_widths, repeatRows=1)
    n = len(data)
    style = [
        ("BACKGROUND",   (0,0),(-1,0), hdr_bg),
        ("TEXTCOLOR",    (0,0),(-1,0), WHITE),
        ("FONTNAME",     (0,0),(-1,0), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0),(-1,0), font_size),
        ("TOPPADDING",   (0,0),(-1,0), 6),
        ("BOTTOMPADDING",(0,0),(-1,0), 6),
        ("LEFTPADDING",  (0,0),(-1,-1),8),
        ("RIGHTPADDING", (0,0),(-1,-1),8),
        ("FONTNAME",     (0,1),(-1,-1),"Helvetica"),
        ("FONTSIZE",     (0,1),(-1,-1),font_size),
        ("TOPPADDING",   (0,1),(-1,-1),5),
        ("BOTTOMPADDING",(0,1),(-1,-1),5),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE, LTGREY]),
        ("GRID",         (0,0),(-1,-1),0.3, BORDER),
        ("VALIGN",       (0,0),(-1,-1),"MIDDLE"),
    ]
    t.setStyle(TableStyle(style)); return t

def callout(text, bg="#eff6ff", border="#3b82f6", text_col="#1e40af"):
    style = S("cb", fontSize=8.5, leading=13, fontName="Helvetica",
              textColor=colors.HexColor(text_col))
    t = Table([[Paragraph(text, style)]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), colors.HexColor(bg)),
        ("TOPPADDING",   (0,0),(-1,-1), 8),
        ("BOTTOMPADDING",(0,0),(-1,-1), 8),
        ("LEFTPADDING",  (0,0),(-1,-1), 12),
        ("RIGHTPADDING", (0,0),(-1,-1), 12),
        ("BOX",          (0,0),(-1,-1), 1, colors.HexColor(border)),
        ("ROUNDEDCORNERS",[5]),
    ])); return t

def kpi_row(items):
    """Row of KPI boxes"""
    cells = []
    for number, label, sub in items:
        inner = Table([[
            Paragraph(number, S("kn",fontSize=22,leading=26,fontName="Helvetica-Bold",textColor=NAVY,alignment=TA_CENTER)),
            Paragraph(label,  S("kl",fontSize=8, leading=10,fontName="Helvetica-Bold",textColor=DARK, alignment=TA_CENTER)),
            Paragraph(sub,    S("ks",fontSize=7, leading=9, fontName="Helvetica",     textColor=MUTED,alignment=TA_CENTER)),
        ]], colWidths=[CONTENT_W/len(items)])
        inner.setStyle(TableStyle([
            ("ALIGN",       (0,0),(-1,-1),"CENTER"),
            ("TOPPADDING",  (0,0),(-1,-1),8),
            ("BOTTOMPADDING",(0,0),(-1,-1),8),
            ("BACKGROUND",  (0,0),(-1,-1),LTGREY),
            ("BOX",         (0,0),(-1,-1),0.5,BORDER),
            ("ROUNDEDCORNERS",[4]),
        ]))
        cells.append(inner)
    row = Table([cells], colWidths=[CONTENT_W/len(items)]*len(items),
                hAlign="LEFT")
    row.setStyle(TableStyle([("LEFTPADDING",(0,0),(-1,-1),3),
                              ("RIGHTPADDING",(0,0),(-1,-1),3)]))
    return row

# ── Page numbering ────────────────────────────────────────────────────────────
PAGE_NUM = [0]
def on_page(canvas, doc):
    PAGE_NUM[0] += 1
    canvas.saveState()
    canvas.setFillColor(MUTED); canvas.setFont("Helvetica", 7)
    canvas.drawString(2*cm, 1.2*cm, "Sempra Data Migration Dashboard  ·  Confidential")
    canvas.drawRightString(W-2*cm, 1.2*cm, f"Page {doc.page}")
    canvas.setStrokeColor(BORDER); canvas.setLineWidth(0.3)
    canvas.line(2*cm, 1.5*cm, W-2*cm, 1.5*cm)
    canvas.restoreState()

# ════════════════════════════════════════════════════════════════════════════
#  BUILD STORY
# ════════════════════════════════════════════════════════════════════════════
story = []

# ── COVER PAGE ───────────────────────────────────────────────────────────────
cover = Table([[
    [
        Paragraph("📊", S("ci",fontSize=40,leading=48,textColor=WHITE,fontName="Helvetica-Bold")),
        sp(10),
        Paragraph("Sempra Data Migration Dashboard", COVER_TITLE),
        Paragraph("Client Presentation &amp; User Guide", COVER_SUB),
        sp(20),
        Table([[
            Paragraph("DM1", S("cb1",fontSize=10,fontName="Helvetica-Bold",textColor=WHITE,alignment=TA_CENTER)),
            Paragraph("DM2", S("cb2",fontSize=10,fontName="Helvetica-Bold",textColor=WHITE,alignment=TA_CENTER)),
            Paragraph("DM3", S("cb3",fontSize=10,fontName="Helvetica-Bold",textColor=WHITE,alignment=TA_CENTER)),
        ]], colWidths=[4*cm,4*cm,4*cm],
        style=[("BACKGROUND",(0,0),(0,0),DM1C),
               ("BACKGROUND",(1,0),(1,0),DM2C),
               ("BACKGROUND",(2,0),(2,0),DM3C),
               ("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8),
               ("ROUNDEDCORNERS",[5])]),
        sp(20),
        Paragraph("Odyssey Phase 1  ·  SAP Migration Tracking  ·  October 2026",
                  S("cd",fontSize=9,textColor=colors.HexColor("#475569"),fontName="Helvetica")),
        Paragraph("Prepared by: Kishor Marri — Sempra Migration Team",
                  S("cd2",fontSize=9,textColor=colors.HexColor("#475569"),fontName="Helvetica")),
    ]
]], colWidths=[CONTENT_W])
cover.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,-1),NAVY),
    ("TOPPADDING",(0,0),(-1,-1),50),
    ("BOTTOMPADDING",(0,0),(-1,-1),50),
    ("LEFTPADDING",(0,0),(-1,-1),40),
    ("RIGHTPADDING",(0,0),(-1,-1),40),
    ("ROWBACKGROUNDS",(0,0),(-1,-1),[NAVY]),
]))
story += [cover, PageBreak()]

# ── SECTION 1: EXECUTIVE SUMMARY ─────────────────────────────────────────────
story += [GradientBanner("01  Executive Summary",
          "Business value and purpose — for leadership audiences", NAVY, BLUE), sp(8)]
story += [p("The <b>Sempra Data Migration Dashboard</b> is Sempra's single source of truth for SAP data "
            "migration health across all three migration waves. It replaces hours of manual Excel "
            "reconciliation with a single button click — delivering live, colour-coded migration "
            "health indicators in under 10 seconds."), sp(6)]

story += [kpi_row([
    ("3",     "Migration Cycles",  "DM1 → DM2 → DM3"),
    ("<10s",  "Full Sync Time",    "All 3 cycles"),
    ("100%",  "Local Processing",  "Zero cloud"),
    ("0",     "Manual Steps",      "Fully automated"),
    ("2 min", "Auto-Refresh",      "Always current"),
    ("4",     "User Roles",        "Viewer to Admin"),
]), sp(10)]

story += [h2("What Leadership Needs to Know")]
for txt in [
    "Replaces 30–60 minutes of manual Excel reconciliation per cycle with a <b>single click</b>",
    "Covers all three migration waves <b>(DM1, DM2, DM3)</b> on one screen with per-cycle drill-down",
    "Data <b>never leaves the Sempra laptop</b> — processed entirely in the browser, no cloud, no licences",
    "Mismatches, missing exports, and incomplete migrations are <b>flagged automatically in colour</b>",
    "Printable, PDF-ready reports for leadership presentations with <b>one Ctrl+P</b>",
]:
    story.append(bul(txt))
story += [sp(8), PageBreak()]

# ── SECTION 2: DASHBOARD LOOK & FEEL ─────────────────────────────────────────
story += [GradientBanner("02  How the Dashboard Looks",
          "Visual walkthrough — what users see on screen", BLUE, colors.HexColor("#0369a1")), sp(8)]
story += [p("Below is a representation of the main Executive Summary screen. Three cycle cards sit "
            "side by side — each with a live match gauge, colour-coded status badge, and headline KPIs."), sp(6)]

story += [DashboardMockup(width=CONTENT_W, height=195), sp(4)]
story += [Paragraph("Figure 1 — Executive Summary Dashboard (DM1=Blue, DM2=Purple, DM3=Green)", CAPN), sp(8)]

story += [h2("Three Dashboard Views")]
story += [tbl([
    ["View", "Audience", "What It Shows"],
    ["📊  Business View",     "Project Managers · Sponsors · Client",
     "RAG scorecards, match %, record volumes, auto-generated insight boxes"],
    ["🔧  Technical View",    "Migration Leads · Analysts",
     "Per-table comparison — source vs target counts, EXP vs IMP gaps, variance column"],
    ["⚡  Performance View",  "Technical Team",
     "Cycle-over-cycle comparison, timing metrics, cache hit rates, file sizes"],
], col_widths=[3.5*cm, 4.5*cm, 8.5*cm]), sp(6)]

story += [h2("RAG Status — What Every Colour Means")]
story += [ColourKey([
    ("#22c55e", "●  GREEN",  "≥ 95% match rate — Migration on track, fully reconciled"),
    ("#f59e0b", "●  AMBER",  "80–94% match — Minor gaps, monitoring needed"),
    ("#ef4444", "●  RED",    "< 80% match — Critical issues, action required"),
    ("#64748b", "●  GREY",   "No data loaded yet — awaiting file upload"),
    ("#3b82f6", "●  DM1",    "All Cycle 1 labels, borders, cards and navigation"),
    ("#a855f7", "●  DM2",    "All Cycle 2 labels, borders, cards and navigation"),
    ("#22c55e", "●  DM3",    "All Cycle 3 labels, borders, cards and navigation"),
], width=CONTENT_W), sp(6), PageBreak()]

# ── SECTION 3: BEFORE & AFTER ─────────────────────────────────────────────────
story += [GradientBanner("03  The Problem It Solves",
          "Before vs After — the transformation in numbers", TEAL, colors.HexColor("#065f46")), sp(8)]
story += [p("Before this dashboard, reconciliation required opening multiple Excel files manually, "
            "cross-referencing by hand, and producing status reports that were already outdated. "
            "Double-counting inflated match numbers. No single view existed across all three cycles."), sp(8)]
story += [BeforeAfter(width=CONTENT_W), sp(10)]
story += [tbl([
    ["Aspect", "Manual (Before)", "Dashboard (After)"],
    ["Time to reconcile",     "30–60 min per cycle",                   "< 10 seconds — all 3 cycles"],
    ["Accuracy",              "Double-counting + formula errors",      "DISTINCT dedup — always correct"],
    ["Coverage",              "One cycle at a time",                   "All 3 cycles simultaneously"],
    ["Data freshness",        "Manual update only",                    "Auto-refresh every 2 minutes"],
    ["Issue flagging",        "Manual — easy to miss",                 "Auto colour-coded indicators"],
    ["Leadership visibility", "Email attachments",                     "Live dashboard + PDF export"],
    ["SAP source counts",     "Manual SE16N per table",                "Automated RFC — all tables"],
    ["Data security",         "Files emailed between team members",    "Never leaves the local machine"],
], col_widths=[3.8*cm, 5.6*cm, 6.1*cm], hdr_bg=TEAL), sp(6), PageBreak()]

# ── SECTION 4: STEP-BY-STEP HOW TO USE ───────────────────────────────────────
story += [GradientBanner("04  Step-by-Step: How to Use the Dashboard",
          "Complete walkthrough — no technical knowledge required",
          colors.HexColor("#7c3aed"), colors.HexColor("#4f46e5")), sp(8)]

steps = [
    (1, "Launch the Dashboard", TEAL,
     "Open PowerShell in the dashboard folder and run:\n"
     "  python launch_dashboard.py\n"
     "Browser opens automatically at http://localhost:5003/Sempra_CrossCycle_Summary_MASTER.html\n"
     "Two background services start — leave the PowerShell windows open."),
    (2, "Log In with Your Role", DM1C,
     "Login screen appears. Enter your username and select your role:\n"
     "  Admin → full access including automation   Manager → view + PDF\n"
     "  Analyst → upload + download CSV/Excel      Viewer → read-only\n"
     "Your session is saved — you stay logged in across page reloads."),
    (3, "Click ⚡ Auto-Sync All Cycles", DM2C,
     "One click reads all 5 Excel files from the C: drive, parses them in the browser,\n"
     "runs reconciliation for DM1, DM2, DM3 in parallel, and updates all three cycle cards.\n"
     "Rainbow button animation plays while running — completes in under 10 seconds.\n"
     "Spinning sync circles appear per cycle — show match % when done."),
    (4, "Read the Business View Results", DM3C,
     "Each cycle card shows:\n"
     "  • Animated match % gauge (0–100%)\n"
     "  • RAG badge: GREEN ≥95% · AMBER 80–94% · RED <80%\n"
     "  • Headline KPIs: total tables, matched, mismatched, missing\n"
     "  • Auto-generated insight boxes flagging key issues"),
    (5, "Switch to Technical View for Detail", AMBER,
     "Click the Technical View tab to see per-table breakdown:\n"
     "  Set 1 — Tables in REF with migration data (EXP vs IMP counts)\n"
     "  Set 2 — Tables NOT in Reference List (unexpected data)\n"
     "  Set 3 — Tables in REF with NO migration data (never migrated)\n"
     "  Set 4 — Tables where EXP count ≠ IMP count (data loss risk)"),
    (6, "Drill Down into Individual Cycles", colors.HexColor("#0369a1"),
     "Click DM1 / DM2 / DM3 navigation to open that cycle's detail page:\n"
     "  • Upload new Excel files via drag-and-drop anytime\n"
     "  • Search and filter the full table list\n"
     "  • Click any row for record-level drill-down with visual chart\n"
     "  • Download filtered subsets as CSV or Excel"),
    (7, "Export for Leadership", colors.HexColor("#be185d"),
     "Press Ctrl+P → Save as PDF for a clean leadership-ready report.\n"
     "Dashboard switches to white background with all colours preserved.\n"
     "Or download CSV/Excel from any analysis set using the export buttons.\n"
     "Full export (all cycles, all sets) available from the master dashboard."),
    (8, "Auto-Refresh Keeps Data Current", TEAL,
     "Dashboard auto-refreshes every 2 minutes — countdown shown in the toolbar.\n"
     "Red dot appears when refresh is <60 seconds away.\n"
     "Click Pause to freeze the view during a presentation.\n"
     "Data persists in localStorage — survives page reloads without re-syncing."),
]
for num, title, col, body in steps:
    story += [StepBox(num, title, body, colour=col, width=CONTENT_W), sp(5)]
story += [sp(4), PageBreak()]

# ── SECTION 5: FEATURE CATALOGUE ─────────────────────────────────────────────
story += [GradientBanner("05  Complete Feature Catalogue",
          "Everything the dashboard can do — at a glance",
          colors.HexColor("#0369a1"), colors.HexColor("#0284c7")), sp(8)]

feat_grid = [
    ("⚡", "Auto-Sync", DM1C,  "One click reads|all 5 Excel files|in < 10 seconds"),
    ("📊", "3 Views",   DM2C,  "Business · Technical|Performance|tabs"),
    ("🎯", "RAG Status",TEAL,  "Green/Amber/Red|per cycle|auto-calculated"),
    ("🔍", "Drill-Down",AMBER, "Click any row|record-level detail|+ visual chart"),
    ("🔄", "Auto Refresh",DM3C,"Every 2 minutes|pause/resume|countdown badge"),
    ("📥", "Exports",   colors.HexColor("#7c3aed"), "CSV · Excel · PDF|per set or full|browser-side"),
    ("🔐", "Role Login",colors.HexColor("#be185d"), "Admin/Manager/|Analyst/Viewer|access control"),
    ("🤖", "SAP Auto",  colors.HexColor("#0369a1"), "RFC to SAP source|+ target — batch|SE16N counts"),
]
fc_row1 = [FeatureCard(icon, title, desc, col, width=CONTENT_W/4-3) for icon, title, col, desc in feat_grid[:4]]
fc_row2 = [FeatureCard(icon, title, desc, col, width=CONTENT_W/4-3) for icon, title, col, desc in feat_grid[4:]]
fw = CONTENT_W/4-3
story += [
    Table([fc_row1], colWidths=[fw]*4, hAlign="LEFT",
          style=[("LEFTPADDING",(0,0),(-1,-1),2),("RIGHTPADDING",(0,0),(-1,-1),2)]),
    sp(5),
    Table([fc_row2], colWidths=[fw]*4, hAlign="LEFT",
          style=[("LEFTPADDING",(0,0),(-1,-1),2),("RIGHTPADDING",(0,0),(-1,-1),2)]),
    sp(10),
]
story += [tbl([
    ["Feature", "Where", "Benefit"],
    ["DISTINCT Deduplication",    "All 6 aggregation points",    "Prevents double-counting — EXP and IMP processed separately"],
    ["ETag 304 Caching",          "File Bridge (port 5002)",     "Zero re-read if files unchanged — instant response"],
    ["Gzip Compression",          "File Bridge transfers",       "60–70% smaller file transfers — faster dashboard load"],
    ["localStorage Persistence",  "All dashboards",             "Results survive page reloads — no need to re-sync"],
    ["Dynamic Bridge URL",        "JS: window.location.hostname","Works on any machine or IP — no hardcoded paths"],
    ["Print-optimised CSS",       "Ctrl+P on any page",         "Clean white output with colours preserved — leadership ready"],
    ["DM3 REF-Only Mode",         "DM3 dashboard",              "Gracefully handles no separate EXP/IMP — amber banner shown"],
    ["Bulk /files/all endpoint",  "Bridge API",                 "Manifest check before byte download — avoids wasted requests"],
], col_widths=[4.5*cm, 4*cm, 8*cm]), sp(6), PageBreak()]

# ── SECTION 6: DATA FLOW ─────────────────────────────────────────────────────
story += [GradientBanner("06  How Data Flows — Technical Overview",
          "Architecture and reconciliation logic for technical reviewers",
          colors.HexColor("#4f46e5"), colors.HexColor("#7c3aed")), sp(8)]
story += [p("The dashboard is a <b>three-layer local stack</b> — nothing is sent to any external server. "
            "All calculation happens in the browser using SheetJS. The Python bridge only serves "
            "raw Excel bytes — it never reads or interprets the data."), sp(6)]
story += [callout(
    "<b>Architecture:</b>  Browser (HTML+JS+SheetJS) ← gzip Excel bytes ← "
    "Flask Bridge :5002 ← Local .xlsx files on C: drive\n"
    "<b>Optional:</b>  Browser ← SAP counts ← Flask Bridge :5001 ← SAP RFC connection",
    bg="#eff6ff", border="#3b82f6", text_col="#1e40af"), sp(8)]

story += [h2("Reconciliation Steps — What Happens After You Click Sync")]
rec_steps = [
    ("FETCH",       "Browser requests /file?cycle=DM1&type=ref and /file?cycle=DM1&type=exp from the bridge. "
                    "Bridge returns gzip-compressed Excel bytes with ETag. If file unchanged, 304 Not Modified returned — zero disk read."),
    ("PARSE",       "SheetJS.read(arrayBuffer) converts raw bytes to a workbook in browser memory. "
                    "sheet_to_json() produces an array of row objects. Column names auto-detected from 20+ variants."),
    ("DEDUPLICATE", "EXP rows: DISTINCT(Type=EXP, TableName, RecordCount) then SUM.\n"
                    "IMP rows: DISTINCT(Type=IMP, TableName, RecordCount) then SUM.\n"
                    "EXP and IMP processed separately — prevents cross-type inflation."),
    ("RECONCILE",   "GREEN if EXP_count == IMP_count AND src_count == tgt_count.\n"
                    "AMBER if counts exist but do not match.\n"
                    "RED if EXP ≠ IMP or migration not started. GREY if no data found."),
    ("RENDER",      "SVG gauge animates to match %. KPI numbers update. RAG badge colours set. "
                    "Summary saved to localStorage. Sync circles hide after 5s."),
]
cols = [DM1C, DM2C, TEAL, AMBER, DM3C]
for i, (title, body) in enumerate(rec_steps):
    story += [StepBox(i+1, title, body, colour=cols[i], width=CONTENT_W), sp(5)]
story += [sp(4), PageBreak()]

# ── SECTION 7: SECURITY ───────────────────────────────────────────────────────
story += [GradientBanner("07  Security &amp; Data Privacy",
          "No cloud, no external calls — data stays on the Sempra laptop",
          colors.HexColor("#065f46"), TEAL), sp(8)]
story += [callout(
    "✅  <b>Security Statement:</b> No Sempra data ever leaves the local machine. All Excel files are "
    "served via a localhost-only Flask server (127.0.0.1 — not reachable from the network), "
    "parsed entirely in the browser, and results stored only in browser localStorage. "
    "There is no cloud API, no telemetry, no external network calls.",
    bg="#f0fdf4", border="#22c55e", text_col="#15803d"), sp(8)]
story += [tbl([
    ["Risk Vector", "Mitigation"],
    ["Data leaving the machine",  "All Flask servers bind to 127.0.0.1 only — not reachable from network"],
    ["External API calls",        "SheetJS is a one-time CDN fetch (library only) — no data sent outbound"],
    ["SAP credentials",           "Entered in-browser, passed to localhost only, never written to disk"],
    ["Network port exposure",     "Ports 5001/5002/5003 all loopback only — no firewall changes required"],
    ["Persistent data storage",   "Only reconciliation summary numbers in localStorage — no raw data"],
    ["File access control",       "Only config-listed files accessible — no directory traversal possible"],
], col_widths=[5.5*cm, 11*cm], hdr_bg=TEAL), sp(6)]

# ── SECTION 8: QUICK REFERENCE ───────────────────────────────────────────────
story += [GradientBanner("08  Quick Reference",
          "URLs, file locations, and contacts",
          colors.HexColor("#1e3a5f"), NAVY), sp(8)]
story += [h2("Dashboard URLs")]
story += [tbl([
    ["Page", "URL"],
    ["Executive Summary (MASTER)", "http://localhost:5003/Sempra_CrossCycle_Summary_MASTER.html"],
    ["DM1 Cycle Dashboard",        "http://localhost:5003/Sempra_DM1_Dashboard.html"],
    ["DM2 Cycle Dashboard",        "http://localhost:5003/Sempra_DM2_Dashboard.html"],
    ["DM3 Cycle Dashboard",        "http://localhost:5003/Sempra_DM3_Dashboard.html"],
    ["Bridge Health Check",        "http://localhost:5002/ping"],
    ["File Status (all cycles)",   "http://localhost:5002/paths"],
], col_widths=[5*cm, 11.5*cm]), sp(8)]

story += [h2("Current Data Files — C: Drive")]
story += [tbl([
    ["Cycle", "File Path", "Type"],
    ["DM1", r"C:\Users\KishorMarri\.bob\DM1\Reflist_m1.xlsx",                 "Reference List"],
    ["DM1", r"C:\Users\KishorMarri\.bob\DM1\DM1_ES2-SQ1 Export-Import.xlsx", "Export/Import"],
    ["DM2", r"C:\Users\KishorMarri\.bob\DM2\DM2 REF.xlsx",                   "Reference List"],
    ["DM2", r"C:\Users\KishorMarri\.bob\DM2\EXPORT IMPORT_DM2.xlsx",         "Export/Import"],
    ["DM3", r"C:\Users\KishorMarri\.bob\DM3\ref dm31.xlsx",                  "Reference List"],
    ["DM3", r"C:\Users\KishorMarri\.bob\DM3\DM3_EXPORT_IMPORT_LOG.xlsx",     "Export/Import"],
], col_widths=[1.5*cm, 12*cm, 3*cm]), sp(8)]

# Approval section
story += [h2("Sign-Off")]
story += [tbl([
    ["Role", "Name", "Signature", "Date"],
    ["Project Sponsor",       "", "", ""],
    ["Programme / IT Manager","", "", ""],
    ["Security / Compliance", "", "", ""],
], col_widths=[4*cm, 4.5*cm, 4.5*cm, 3.5*cm]), sp(10)]

story += [hr()]
story += [Paragraph(
    f"Sempra Data Migration Dashboard v1.0  ·  Odyssey Phase 1  ·  "
    f"Classification: Internal Use Only  ·  {datetime.date.today().strftime('%B %Y')}",
    S("ft", fontSize=7.5, leading=11, textColor=MUTED, fontName="Helvetica", alignment=TA_CENTER)
)]

# ── Build ─────────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(OUT, pagesize=A4,
      leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2.2*cm,
      title="Sempra DM Dashboard — Client Presentation",
      author="Kishor Marri — Sempra Migration Team")
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f"\nPDF created: {OUT}")
print(f"    Size: {round(__import__('os').path.getsize(OUT)/1024)} KB")
