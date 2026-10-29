"""Shared house style for the SNP CrystalBridge PDFs (copied from generate_snp_crystalbridge_pdf.py)."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, HRFlowable, PageBreak, Preformatted,
                                KeepTogether, CondPageBreak)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus.flowables import Flowable
import datetime

W, H = A4
CONTENT_W = W - 4 * cm

# -- Colours -----------------------------------------------------------------
NAVY = colors.HexColor("#0a1628")
BLUE = colors.HexColor("#1e3a5f")
SKY = colors.HexColor("#38bdf8")
TEAL = colors.HexColor("#0f766e")
CUSTC = colors.HexColor("#3b82f6")
VIOLET = colors.HexColor("#7c5cd8")
AMBER = colors.HexColor("#f59e0b")
RED_C = colors.HexColor("#ef4444")
GREEN_C = colors.HexColor("#16a34a")
LTGREY = colors.HexColor("#f7f8fa")
BORDER = colors.HexColor("#e5e7eb")
MUTED = colors.HexColor("#57606a")
DARK = colors.HexColor("#1f2328")
WHITE = colors.white


def S(name, **kw):
    return ParagraphStyle(name, **kw)


COVER_TITLE = S("ct", fontSize=27, leading=34, textColor=WHITE, fontName="Helvetica-Bold")
COVER_SUB = S("cs", fontSize=12, leading=17, textColor=colors.HexColor("#94a3b8"), fontName="Helvetica")
H2s = S("H2", fontSize=12, leading=16, textColor=BLUE, fontName="Helvetica-Bold", spaceBefore=12, spaceAfter=4, keepWithNext=1)
H3s = S("H3", fontSize=10, leading=14, textColor=DARK, fontName="Helvetica-Bold", spaceBefore=8, spaceAfter=3)
BODY = S("BD", fontSize=9, leading=14, textColor=DARK, fontName="Helvetica", spaceAfter=4, alignment=TA_JUSTIFY)
BUL = S("BU", fontSize=9, leading=13, textColor=DARK, fontName="Helvetica", leftIndent=14, spaceAfter=3)
CAPN = S("CA", fontSize=7.5, leading=11, textColor=MUTED, fontName="Helvetica-Oblique", alignment=TA_CENTER, spaceAfter=6)
CELL = S("CL", fontSize=7.8, leading=10.5, textColor=DARK, fontName="Helvetica")
CELLH = S("CH", fontSize=7.8, leading=10.5, textColor=WHITE, fontName="Helvetica-Bold")
CODE_ST = S("CD", fontSize=6.8, leading=9, textColor=colors.HexColor("#1e40af"), fontName="Courier")


def p(t, st=None): return Paragraph(t, st or BODY)
def h2(t): return Paragraph(t, H2s)
def h3(t): return Paragraph(t, H3s)
def sp(n=8): return Spacer(1, n)
def bul(t): return Paragraph(f"<bullet>&bull;</bullet> {t}", BUL)
def mono(t): return f'<font name="Courier" size="7.6" color="#1e40af">{t}</font>'


def code(txt):
    t = Table([[Preformatted(txt, CODE_ST)]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#eff6ff")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#bfdbfe")),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    return [t, sp(6)]


# -- Flowables -----------------------------------------------------------------
class GradientBanner(Flowable):
    def __init__(self, title, subtitle="", c1=NAVY, c2=BLUE, height=50):
        super().__init__()
        self.title = title; self.subtitle = subtitle
        self.c1 = c1; self.c2 = c2; self.height = height

    def wrap(self, w, h):
        self.w = w
        return (w, self.height + 6)

    def draw(self):
        c = self.canv; w = self.w; h = self.height
        c.saveState()
        steps = 30
        for i in range(steps):
            t = i / steps
            c.setFillColorRGB(self.c1.red + t * (self.c2.red - self.c1.red),
                              self.c1.green + t * (self.c2.green - self.c1.green),
                              self.c1.blue + t * (self.c2.blue - self.c1.blue))
            c.rect(w * i / steps, 0, w / steps + 0.5, h, stroke=0, fill=1)
        c.setFillColor(SKY); c.rect(0, h - 3, w, 3, stroke=0, fill=1)
        c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 13)
        c.drawString(14, h - 24, self.title)
        if self.subtitle:
            c.setFillColor(colors.HexColor("#94a3b8")); c.setFont("Helvetica", 8.5)
            c.drawString(14, h - 37, self.subtitle)
        c.restoreState()


def _arrow(c, x1, y, x2, color=MUTED, width=1.5):
    c.setStrokeColor(color); c.setFillColor(color); c.setLineWidth(width)
    c.line(x1, y, x2 - 6, y)
    path = c.beginPath()
    path.moveTo(x2, y); path.lineTo(x2 - 7, y + 3.5); path.lineTo(x2 - 7, y - 3.5); path.close()
    c.drawPath(path, stroke=0, fill=1)


class FlowRow(Flowable):
    """Horizontal row of boxes joined by arrows. items = [(title, [lines], colour)]"""
    def __init__(self, items, height=78, width=CONTENT_W):
        super().__init__()
        self.items = items; self.h = height; self.w = width

    def wrap(self, w, h):
        return (self.w, self.h)

    def draw(self):
        c = self.canv; n = len(self.items); gap = 16
        bw = (self.w - gap * (n - 1)) / n
        for i, (title, lines, col) in enumerate(self.items):
            x = i * (bw + gap)
            c.setFillColor(colors.Color(col.red, col.green, col.blue, alpha=0.10))
            c.setStrokeColor(col); c.setLineWidth(1.3)
            c.roundRect(x, 0, bw, self.h, 5, stroke=1, fill=1)
            c.setFillColor(col); c.setFont("Helvetica-Bold", 8.5)
            c.drawCentredString(x + bw / 2, self.h - 16, title)
            c.setFillColor(DARK); c.setFont("Helvetica", 7)
            for j, ln in enumerate(lines):
                c.drawCentredString(x + bw / 2, self.h - 30 - j * 10, ln)
            if i < n - 1:
                _arrow(c, x + bw + 2, self.h / 2, x + bw + gap - 1)


class LandscapeDiagram(Flowable):
    """Control / Source / Target / File system landscape."""
    def __init__(self, width=CONTENT_W):
        super().__init__(); self.w = width; self.h = 215

    def wrap(self, w, h): return (self.w, self.h)

    def box(self, x, y, bw, bh, title, lines, col):
        c = self.canv
        c.setFillColor(colors.Color(col.red, col.green, col.blue, alpha=0.10))
        c.setStrokeColor(col); c.setLineWidth(1.4)
        c.roundRect(x, y, bw, bh, 6, stroke=1, fill=1)
        c.setFillColor(col); c.setFont("Helvetica-Bold", 9)
        c.drawCentredString(x + bw / 2, y + bh - 15, title)
        c.setFillColor(DARK); c.setFont("Helvetica", 7)
        for i, ln in enumerate(lines):
            c.drawCentredString(x + bw / 2, y + bh - 28 - i * 9.5, ln)

    def draw(self):
        c = self.canv; w = self.w
        cw = 250; cx = (w - cw) / 2
        self.box(cx, self.h - 85, cw, 80, "CONTROL SYSTEM (CENTRAL)",
                 ["Mission Control  /N/SNP/MC", "Transformation Cockpit  /N/SNP/TC",
                  "Rule base + Shadow DDIC + Scenarios", "TC Daemon  /SNP/TE01_DAEMON"], VIOLET)
        bw = 140; by = 0; bh = 92
        self.box(0, by, bw, bh, "SOURCE  (SAP ECC)",
                 ["Export programs generated", "Scout / Direct Reader", "RFC user: /SNP/XX_MIG_*_RFC",
                  "Data stays unchanged"], CUSTC)
        self.box(w - bw, by, bw, bh, "TARGET  (SAP S/4HANA)",
                 ["Import programs generated", "Mapping + rules applied", "Post-processing XPRA/XCLA/SDM",
                  "Number ranges (NRIV)"], GREEN_C)
        fx = (w - 120) / 2
        self.box(fx, by + 12, 120, 62, "FILE SYSTEM", ["Compressed export", "packages (staging)",
                                                       "never overwritten"], AMBER)
        _arrow(c, bw + 3, by + 43, fx - 2, AMBER)
        _arrow(c, fx + 122, by + 43, w - bw - 3, AMBER)
        c.setFont("Helvetica-Oblique", 6.5); c.setFillColor(MUTED)
        c.drawCentredString(bw + (fx - bw) / 2 + 1, by + 50, "EXPORT")
        c.drawCentredString(fx + 120 + (w - bw - fx - 120) / 2, by + 50, "IMPORT")
        # RFC dashed lines from control to source / target
        c.setStrokeColor(VIOLET); c.setLineWidth(1); c.setDash(4, 3)
        c.line(cx + 30, self.h - 85, bw / 2, by + bh)
        c.line(cx + cw - 30, self.h - 85, w - bw / 2, by + bh)
        c.setDash()
        c.setFont("Helvetica-Oblique", 6.5); c.setFillColor(VIOLET)
        c.drawString(bw / 2 + 28, by + bh + 38, "RFC / DIA")
        c.drawRightString(w - bw / 2 - 28, by + bh + 38, "RFC / DIA")


class NZDDiagram(Flowable):
    """Near-zero downtime timeline."""
    def __init__(self, width=CONTENT_W):
        super().__init__(); self.w = width; self.h = 120

    def wrap(self, w, h): return (self.w, self.h)

    def draw(self):
        c = self.canv; w = self.w
        base = 28
        segs = [("INITIAL LOAD", "source live", 0.34, CUSTC, 62),
                ("DELTA 1", "", 0.17, VIOLET, 42),
                ("DELTA 2", "", 0.11, VIOLET, 30),
                ("DELTA n", "", 0.07, VIOLET, 20),
                ("FINAL DELTA", "downtime", 0.07, RED_C, 20)]
        gap = 6; total = sum(s[2] for s in segs); avail = w - gap * (len(segs) - 1)
        x = 0
        for name, sub, frac, col, hh in segs:
            bw = avail * frac / total
            c.setFillColor(col); c.setStrokeColor(col)
            c.roundRect(x, base, bw, hh, 3, stroke=0, fill=1)
            c.setFillColor(DARK); c.setFont("Helvetica-Bold", 6.5)
            c.drawCentredString(x + bw / 2, base - 10, name)
            if sub:
                c.setFont("Helvetica", 6.3); c.setFillColor(MUTED)
                c.drawCentredString(x + bw / 2, base - 19, sub)
            x += bw + gap
        c.setStrokeColor(MUTED); c.setLineWidth(0.8)
        c.line(0, base - 1, w, base - 1)
        c.setFillColor(MUTED); c.setFont("Helvetica-Oblique", 7)
        c.drawString(0, self.h - 8, "Bar height = data volume transferred.  Each delta run shrinks the final cutover window.")

class McTcLinkDiagram(Flowable):
    """Mission Control <-> Transformation Cockpit interlink."""
    def __init__(self, width=CONTENT_W):
        super().__init__(); self.w = width; self.h = 190

    def wrap(self, w, h): return (self.w, self.h)

    def box(self, x, y, bw, bh, title, lines, col):
        c = self.canv
        c.setFillColor(colors.Color(col.red, col.green, col.blue, alpha=0.10))
        c.setStrokeColor(col); c.setLineWidth(1.3)
        c.roundRect(x, y, bw, bh, 5, stroke=1, fill=1)
        c.setFillColor(col); c.setFont("Helvetica-Bold", 8.5)
        c.drawCentredString(x + bw / 2, y + bh - 14, title)
        c.setFillColor(DARK); c.setFont("Helvetica", 6.8)
        for i, ln in enumerate(lines):
            c.drawCentredString(x + bw / 2, y + bh - 26 - i * 9, ln)

    def draw(self):
        c = self.canv; w = self.w; h = self.h
        bw = 150; gx = w - bw
        # Panel headers
        c.setFont("Helvetica-Bold", 8); c.setFillColor(VIOLET)
        c.drawString(0, h - 10, "MISSION CONTROL  /N/SNP/MC")
        c.setFillColor(TEAL)
        c.drawRightString(w, h - 10, "TRANSFORMATION COCKPIT  /N/SNP/TC")
        # left (MC) boxes
        self.box(0, h - 62, bw, 44, "Project / task", ["Task with automation XML", "R:CLASS = CN02_CL_TEX_REPORT"], VIOLET)
        self.box(0, h - 118, bw, 44, "Variables", ["TC_SCENARIO = scenario ID", "{M:GET_VARIABLE TC_SCENARIO}"], VIOLET)
        self.box(0, h - 174, bw, 44, "Tickets and status", ["Task Blocked / Closed", "progress %, log, documents"], VIOLET)
        # right (TC) boxes
        self.box(gx, h - 62, bw, 44, "API report", ["TE02_API_EXECUTE_BLOCKS", "P_SCEN, S_RUN, S_BLOCK"], TEAL)
        self.box(gx, h - 118, bw, 44, "Scenario", ["Selections, mappings, objects", "Runs and blocks"], TEAL)
        self.box(gx, h - 174, bw, 44, "Run / block status", ["Running, Completed, Crashed", "Records, errors, runtime"], TEAL)
        # arrows
        _arrow(c, bw + 3, h - 40, gx - 3, VIOLET)
        c.setFont("Helvetica-Oblique", 6.5); c.setFillColor(MUTED)
        c.drawCentredString(w / 2, h - 36, "starts")
        _arrow(c, bw + 3, h - 96, gx - 3, VIOLET)
        c.drawCentredString(w / 2, h - 92, "P_SCEN + proxy classes")
        _arrow(c, gx - 3, h - 152, bw + 3, TEAL)
        c.drawCentredString(w / 2, h - 148, "TE02_CL_TEX_TR_REFRESH")
        c.setFillColor(TEAL)
        c.drawCentredString(w / 2, h - 160, "status + auto tickets")


class ObjectFlowDiagram(Flowable):
    """One data object (sales orders VBAK/VBAP) from source to target."""
    def __init__(self, width=CONTENT_W):
        super().__init__(); self.w = width; self.h = 170

    def wrap(self, w, h): return (self.w, self.h)

    def box(self, x, y, bw, bh, title, lines, col):
        c = self.canv
        c.setFillColor(colors.Color(col.red, col.green, col.blue, alpha=0.10))
        c.setStrokeColor(col); c.setLineWidth(1.2)
        c.roundRect(x, y, bw, bh, 5, stroke=1, fill=1)
        c.setFillColor(col); c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(x + bw / 2, y + bh - 13, title)
        c.setFillColor(DARK); c.setFont("Helvetica", 6.8)
        for i, ln in enumerate(lines):
            c.drawCentredString(x + bw / 2, y + bh - 25 - i * 8.6, ln)

    def draw(self):
        c = self.canv; w = self.w; h = self.h
        bw = 112; gap = (w - 4 * bw) / 3
        xs = [i * (bw + gap) for i in range(4)]
        top = h - 78
        self.box(xs[0], top, bw, 74, "1  SOURCE TABLES", ["VBAK (start table)", "VBAP (dependent)", "BUKRS 1000 / 1100"], CUSTC)
        self.box(xs[1], top, bw, 74, "2  EXPORT BLOCK", ["Selection BUKRS", "Scout Reader on VBAP", "Export rules / events"], CUSTC)
        self.box(xs[2], top, bw, 74, "3  PACKAGES", ["Compressed files", "Raw source values", "Never overwritten"], AMBER)
        self.box(xs[3], top, bw, 74, "4  IMPORT BLOCK", ["MAP_BUKRS 1000,1100 > 2000", "Import rules, mode Insert", "Order: VBAK, then VBAP"], GREEN_C)
        for i in range(3):
            _arrow(c, xs[i] + bw + 2, top + 37, xs[i + 1] - 2, MUTED)
        low = 0
        self.box(xs[1], low, bw * 2 + gap, 56, "CONTROL FROM MISSION CONTROL",
                 ["Task 1: Export   Task 2: Import   Task 3: DCV + FK check",
                  "Refresh class returns progress and creates tickets"], VIOLET)
        self.box(xs[3], low, bw, 56, "5  TARGET + CHECK", ["VBAK / VBAP in S/4", "FK check, counts", "XPRA / SDM"], GREEN_C)
        c.setStrokeColor(VIOLET); c.setLineWidth(0.9); c.setDash(3, 3)
        c.line(xs[1] + bw / 2, low + 56, xs[1] + bw / 2, top)
        c.line(xs[3] - gap / 2, low + 28, xs[3] - 2, low + 28)
        c.setDash()
        c.setStrokeColor(GREEN_C); c.setLineWidth(1)
        c.line(xs[3] + bw / 2, top, xs[3] + bw / 2, low + 56)
        c.setFillColor(GREEN_C)
        p_ = c.beginPath(); cx_ = xs[3] + bw / 2; cy_ = low + 56
        p_.moveTo(cx_, cy_); p_.lineTo(cx_ - 3.5, cy_ + 7); p_.lineTo(cx_ + 3.5, cy_ + 7); p_.close()
        c.drawPath(p_, stroke=0, fill=1)




# -- Tables ---------------------------------------------------------------------
def tbl(data, col_widths, hdr_bg=BLUE, first_bold=False):
    rows = []
    for ri, row in enumerate(data):
        out = []
        for ci, v in enumerate(row):
            if isinstance(v, str):
                if ri == 0:
                    out.append(Paragraph(v, CELLH))
                elif first_bold and ci == 0:
                    out.append(Paragraph(f"<b>{v}</b>", CELL))
                else:
                    out.append(Paragraph(v, CELL))
            else:
                out.append(v)
        rows.append(out)
    t = Table(rows, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), hdr_bg),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LTGREY]),
        ("GRID", (0, 0), (-1, -1), 0.3, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return t


def callout(text, bg="#eff6ff", border="#3b82f6", tc="#1e40af"):
    st = S("cb", fontSize=8.5, leading=13, fontName="Helvetica", textColor=colors.HexColor(tc))
    t = Table([[Paragraph(text, st)]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(bg)),
        ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor(border)),
    ]))
    return t


def warn(t): return callout(t, bg="#fffbeb", border="#f59e0b", tc="#92400e")
def good(t): return callout(t, bg="#f0fdf4", border="#22c55e", tc="#15803d")


def banner(title, sub, c1=NAVY, c2=BLUE):
    return [GradientBanner(title, sub, c1, c2), sp(8)]


def make_on_page(footer):
    def on_page(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(MUTED); canvas.setFont("Helvetica", 7)
        canvas.drawString(2 * cm, 1.2 * cm, footer)
        canvas.drawRightString(W - 2 * cm, 1.2 * cm, f"Page {doc.page}")
        canvas.setStrokeColor(BORDER); canvas.setLineWidth(0.3)
        canvas.line(2 * cm, 1.5 * cm, W - 2 * cm, 1.5 * cm)
        canvas.restoreState()
    return on_page


TBC = '<font color="#b45309"><b>TBC</b></font>'
