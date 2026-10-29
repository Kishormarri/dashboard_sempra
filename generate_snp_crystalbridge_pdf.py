"""
SNP CrystalBridge - Data Migration SAP ECC to S/4HANA
Detailed reference document with System Snapshot.
Source: Kyano Mission Control Complete Reference Guide (SNP SE) - Mission Control,
        Transformation Cockpit (TC 19.03 training), CrystalBridge Analysis 20.07.
Run: python generate_snp_crystalbridge_pdf.py
"""
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

OUT = "SNP_CrystalBridge_Data_Migration_ECC_to_S4HANA.pdf"
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


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(MUTED); canvas.setFont("Helvetica", 7)
    canvas.drawString(2 * cm, 1.2 * cm, "SNP CrystalBridge Data Migration - SAP ECC to S/4HANA  |  Sempra Migration Team")
    canvas.drawRightString(W - 2 * cm, 1.2 * cm, f"Page {doc.page}")
    canvas.setStrokeColor(BORDER); canvas.setLineWidth(0.3)
    canvas.line(2 * cm, 1.5 * cm, W - 2 * cm, 1.5 * cm)
    canvas.restoreState()


TBC = '<font color="#b45309"><b>TBC</b></font>'

# ==============================================================================
story = []

# -- COVER ----------------------------------------------------------------------
cov = Table([[[
    p("SNP CrystalBridge", S("k", fontSize=11, leading=14, textColor=SKY, fontName="Helvetica-Bold")),
    sp(8),
    p("Data Migration<br/>SAP ECC to S/4HANA", COVER_TITLE),
    sp(6),
    p("Mission Control  |  Transformation Cockpit  |  Staging  |  Near-Zero Downtime  |  Validation", COVER_SUB),
    sp(18),
    tbl([["SCOPE", "SOURCE OF CONTENT", "SYSTEM SNAPSHOT"],
         ["SNP CrystalBridge data migration only", "Kyano MC Guide, User Guide 25.09, Module 5 v25.03, TC 19.03 decks", "Section 2 - landscape template"]],
        [5.0 * cm, 5.6 * cm, 4.6 * cm], hdr_bg=BLUE),
    sp(18),
    p(f"Prepared: {datetime.date.today().strftime('%B %Y')}  |  Sempra Migration Team  |  Version 1.0 (draft - more SNP documents to follow)",
      S("x", fontSize=9, textColor=colors.HexColor("#94a3b8"), fontName="Helvetica")),
]]], colWidths=[CONTENT_W])
cov.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), NAVY),
    ("TOPPADDING", (0, 0), (-1, -1), 26), ("BOTTOMPADDING", (0, 0), (-1, -1), 26),
    ("LEFTPADDING", (0, 0), (-1, -1), 34), ("RIGHTPADDING", (0, 0), (-1, -1), 34),
]))
story += [cov, sp(14)]
story += [callout(
    "<b>How to read this document.</b>  Everything marked as a product fact (roles, transactions, reports, parameters, "
    "defaults, workflow) is taken from the SNP guide. Values that depend on the Sempra landscape (SIDs, releases, "
    "client numbers, volumes, dates) are marked " + TBC + " and must be completed from the project-specific SNP "
    "documents. Nothing in the TBC fields has been assumed.")]
story += [sp(10), h2("Contents")]
toc = [["1", "Executive Overview", "What CrystalBridge does, components, migration approaches"],
       ["2", "System Snapshot", "Architecture, landscape template, components, RFC, run parameters"],
       ["3", "Migration Lifecycle", "Analyze, Create, Migrate, Validate and project phases"],
       ["4", "Transformation Cockpit Configuration", "Scenario, systems, selections, mapping, data objects, number ranges"],
       ["5", "Rules, Import Modes and Events", "Export/import rules, API calls, import modes"],
       ["6", "Executing the Transformation", "Runs, blocks, checklist, monitoring, restart"],
       ["7", "Mission Control Automation", "Tasks, XML config, API reports, tickets"],
       ["8", "Near-Zero Downtime and Delta Loads", "RBNZD phases, setup, best practice"],
       ["9", "Validation and S/4 Post-Processing", "DCV, balance comparison, XPRA/XCLA/SDM"],
       ["10", "End-to-End Workflow to Go-Live", "16-step sequence with owners"],
       ["11", "Roles and Authorizations", "Composite and single roles by system"],
       ["12", "Troubleshooting, Risks and Open Items", "Known issues, risk register, items to confirm"],
       ["13", "MC and TC Interlink, Options, Worked Object", "How MC drives TC, export / import options, one object end to end, when to use what"],
       ["14", "Advanced TC Techniques", "Data object design, own tables, events, number ranges, forerunners, execution control, analysis tools"]]
story += [tbl([["#", "Section", "Content"]] + toc, [1.0 * cm, 5.6 * cm, 10.4 * cm], hdr_bg=NAVY), PageBreak()]

# -- 1 EXECUTIVE OVERVIEW --------------------------------------------------------
story += banner("01  Executive Overview", "What SNP CrystalBridge does for an ECC to S/4HANA data migration")
story += [p("SNP <b>CrystalBridge</b> is a suite for planning, executing and validating SAP transformation projects. "
            "For a data migration it extracts data from the SAP ECC source, applies selections, mappings and rules, "
            "stores the result as compressed export packages and loads it into the S/4HANA target. The source data is "
            "<b>never modified</b>; all transformation is applied between export and import."),
          sp(4)]
story += [tbl([
    ["Component", "Code", "Role in the data migration"],
    ["CrystalBridge Analysis", "AN", "Pre-migration analysis: system scan, enterprise structure, data profiling, customizing, repository and interface analysis, S/4 simplification item check."],
    ["CrystalBridge Transformation (Transformation Cockpit)", "TF / TC", "Core migration engine: scenarios, selections, mappings, data objects, rules, export and import blocks, staging, number ranges."],
    ["Mission Control (Kyano)", "MC", "Project plan and orchestration layer: tasks, dependencies, automation of TC steps, tickets, monitoring, templates (units)."],
    ["Shell Creator", "SHC", "Creates the system shell (RESC) used as basis for the target in the Bluefield approach."],
    ["Data Consistency Verification", "DCV", "Post-load checks: record counts, foreign key checks, domain fixed values (/N/SNP/FKC)."],
    ["Rule-Based Near-Zero Downtime", "RBNZD", "Delta technique so the source stays live and only the last delta is moved at cutover."],
], [4.4 * cm, 1.6 * cm, 11.0 * cm], first_bold=True), sp(8)]

story += [h2("Migration approaches supported")]
story += [tbl([
    ["Approach", "Description", "Fit for ECC to S/4HANA"],
    ["Greenfield", "New S/4HANA implementation; processes redesigned; master data and open items only.", "Used when history is not required in the target."],
    ["Bluefield", "Selective data migration per entity into a (global) S/4HANA system; combination of Greenfield and Brownfield. SNP Transformation Backbone with SAP LT.", "Selective, harmonizing migration; source can stay live (RBNZD)."],
    ["Brownfield", "Upgrade of the current system to S/4HANA; keeps processes; changes limited to S/4 architecture.", "Conversion; target = converted source (no separate target system)."],
], [2.6 * cm, 8.2 * cm, 6.2 * cm], first_bold=True), sp(6)]
story += [callout(
    "<b>Bluefield unit - supported out of the box (Mission Control):</b> selection by company code; fiscal-year based selection; "
    "controlling area / credit control area / operating concern split; chart of accounts harmonization; switch from account to "
    "ledger approach, New GL and New Asset Accounting; custom data models 1:1 (Z*/Y*); business partner creation for each "
    "customer and vendor.<br/><b>Needs Professional Services:</b> business partner harmonization, mapping of org units or document "
    "types, document splitting, industry solutions, additional currencies, any other transformation requirement.",
    bg="#f0fdf4", border="#22c55e", tc="#15803d"), PageBreak()]

# -- 2 SYSTEM SNAPSHOT ------------------------------------------------------------
story += banner("02  System Snapshot", "Architecture, landscape, components, connectivity and run parameters", NAVY, VIOLET)
story += [h2("2.1  Reference architecture")]
story += [p("The <b>control system</b> hosts Mission Control and the Transformation Cockpit, the rule base and the shadow DDIC. "
            "It creates and monitors the export programs on the source and the import programs on the target. Data moves "
            "through a compressed file system, never directly between source and target."), sp(4)]
story += [LandscapeDiagram(), p("Figure 1 - Control, source, target and file system", CAPN)]

story += [h2("2.2  Supported system constellations")]
story += [tbl([
    ["Constellation", "Description", "Notes"],
    ["Migration, separate control", "Control + Source + Target connected via RFC / DIA.", "Recommended for large projects."],
    ["Conversion, separate control", "Control + Source via RFC / DIA; no separate target.", "Target = converted source."],
    ["No separate control", "Source or target acts as control system.", "Source recommended; TC slower under load; ruleset export/import needed on refresh (/SNP/TE02_SCENARIO_XML_EXPORT / _IMPORT)."],
    ["Multiple source systems", "Several sources feed one target via one scenario.", "Import block must be assigned manually per source; system alias required."],
], [4.0 * cm, 6.0 * cm, 7.0 * cm], first_bold=True), sp(6)]

story += [h2("2.3  Landscape snapshot (to be completed)")]
story += [p("Fill from the project documents. Each row is a fact the migration team must be able to state at any time.")]
story += [tbl([
    ["Attribute", "Source (ECC)", "Control system", "Target (S/4HANA)"],
    ["System ID (SID)", TBC, TBC, TBC],
    ["Client", TBC, TBC, TBC],
    ["SAP release / EHP / SP stack", TBC, TBC, TBC],
    ["SAP Basis release (drives /SNP/XX_MIG_751 / 755 roles)", TBC, TBC, TBC],
    ["Database system and size", TBC, TBC, TBC],
    ["Unicode", TBC, TBC, TBC],
    ["Host / IP (for RFC whitelist)", TBC, TBC, TBC],
    ["Role in scenario (SOURCE / TARGET / CENTRAL)", "SOURCE", "CENTRAL", "TARGET"],
    ["Max. process count (parallel jobs)", TBC, TBC, TBC],
    ["Export / import file path", TBC, TBC, TBC],
    ["SNP software component versions (AN / TF / MC)", TBC, TBC, TBC],
    ["SNP transports imported (date / request)", TBC, TBC, TBC],
    ["Approach (Greenfield / Bluefield / Brownfield)", TBC, TBC, TBC],
], [6.2 * cm, 3.6 * cm, 3.6 * cm, 3.6 * cm], first_bold=True), sp(8)]

story += [h2("2.4  Migration scope snapshot (to be completed)")]
story += [tbl([
    ["Item", "Value"],
    ["Company codes in scope (BUKRS)", TBC],
    ["Controlling area(s) (KOKRS) / Plants (WERKS) / Sales orgs (VKORG) / Purchasing orgs (EKORG)", TBC],
    ["Fiscal years in scope (GJAHR)", TBC],
    ["Modules in scope (FI / CO / MM / SD / PP / PM / HCM / other)", TBC],
    ["Target organizational structure (after mapping)", TBC],
    ["Custom (Z / Y) tables in scope - count and owner", TBC],
    ["Estimated data volume (GB) and largest tables", TBC],
    ["TC scenario ID(s) and type", TBC],
    ["Number of mock / test cycles planned", TBC],
    ["Cutover window and downtime target", TBC],
], [10.0 * cm, 7.0 * cm], first_bold=False), PageBreak()]

story += [h2("2.5  RFC connection and whitelist register")]
story += [p("All RFC connections used in the transformation must be entered in a whitelist on <b>all systems and all clients</b> "
            "(maintained in " + mono("/SNP/TCSYS") + "). One row per connection:")]
story += [tbl([
    ["Field", "Guide example", "Project value"],
    ["System-ID", "TRA / SRC / TAR", TBC],
    ["Client", "001 / 800 / 900", TBC],
    ["IP address", "123.45.678.901", TBC],
    ["RFC destination", "SNP_TB_TRA_001", TBC],
    ["Callback RFC destination", "SNP_TB_TRA_001", TBC],
    ["Dialog RFC destination", "SNP_TB_TRA_001_DIA", TBC],
], [5.0 * cm, 6.0 * cm, 6.0 * cm], first_bold=True), sp(4)]
story += [p("Connection checks: " + mono("Test Connection") + " in the Systems tab, or Mission Control API reports " +
            mono("/SNP/TE02_API_CHECK_SYS_CONS") + " and " + mono("/SNP/TE02_API_CHECK_FILE_PATHS") + ".")]

story += [h2("2.6  Run parameters - defaults and project values")]
story += [tbl([
    ["Parameter", "Default", "Meaning", "Project"],
    ["MAX_PACKAGE_SIZE_MB", "50 MB", "Max file size per package (override per table)", TBC],
    ["MAX_PACKAGE_SIZE_REC", "200,000", "Max records per package file", TBC],
    ["TASK_PROC_COUNT", "4", "Processes for other tasks (rule generation, syntax check)", TBC],
    ["TASK_PACKAGE_SIZE", "30", "Max objects per process for other tasks", TBC],
    ["EXEC_PROC_RETRY_CNT", "0", "Process restarts on rollback / deadlock failure", TBC],
    ["IN_MEMORY_GENERATION", "off", "Program generation up to 6x faster; programs not visible in SE38", TBC],
    ["MAX_IN_MEMORY_PROGRAMS", "5", "Programs held in memory (range 2-35)", TBC],
    ["LOG_MAX_ENTRIES", "100", "Max log entries per table / object", TBC],
    ["ENCRYPTION_PASS", "-", "Encrypt personal data; about 30% extra runtime; tables in /SNP/TE00TABENCR", TBC],
    ["EMAIL_NOTIFICATIONS / EMAIL_INTERVAL_MIN", "off / 60", "E-mail status dispatch (needs SAP SMTP)", TBC],
    ["GLOBAL_FUNCTION_EXPORT / _IMPORT", "X / X", "Generate global functions on source / target", TBC],
    ["NZD_ACTIVE", "off", "Enables Near-Zero Downtime delta identification", TBC],
], [5.0 * cm, 1.8 * cm, 8.0 * cm, 2.2 * cm], first_bold=True), sp(6),
    callout("<b>Prerequisite for any data object:</b> run the <b>Table Analysis</b> first. It collects DDIC and record-count "
            "information into table " + mono("/SNP/CE00TABINFO") + ". Refresh with report " + mono("/SNP/TE02_UPDATE_TABLE_INFO") +
            ". Data objects cannot be processed without it."), PageBreak()]

# -- 3 LIFECYCLE -------------------------------------------------------------------
story += banner("03  Migration Lifecycle", "SNP Bluefield approach and the project phases", BLUE, CUSTC)
story += [FlowRow([
    ("1  ANALYZE", ["System scan", "Interface scanner", "Customizing and", "repository analysis"], CUSTC),
    ("2  CREATE", ["S/4 customizing", "System shell (RESC)", "Upgrade / Unicode", "conversion"], VIOLET),
    ("3  MIGRATE", ["Export (selections", "and rules)", "Compressed files", "Import to target"], TEAL),
    ("4  VALIDATE", ["DCV", "Automated testing", "Transaction / random", "tests, FK checks"], GREEN_C),
], height=76), p("Figure 2 - SNP Bluefield approach", CAPN), sp(4)]

story += [tbl([
    ["Project phase", "Key activities"],
    ["Project Setup", "Present SNP procedure, determine system landscape, project planning, system scan, deliver Transformation Backbone, kick-off."],
    ["Analysis", "Detailed analysis in CrystalBridge, create data object list, analyze interfaces, customizing and repository analysis, scoping workshops."],
    ["Design", "Adjust data object list, rule set definition, create blueprint."],
    ["Implementation", "Rule-set implementation, maintain and check selections and mappings."],
    ["Test", "Individual tests with protocol, data validation, mass tests, transactional data check, DCV, automated testing."],
    ["Go-Live", "Go-live simulation, go-live, cutover, data validation, approval."],
    ["Hypercare", "Support by project team, post-migrations if necessary, lessons learned."],
], [3.2 * cm, 13.8 * cm], first_bold=True), sp(8)]

story += [h2("3.1  Analyze - pre-migration analysis tools (CrystalBridge Analysis)")]
story += [tbl([
    ["Tool", "Transaction / entry", "Output used by the migration"],
    ["System scan (extractor)", "/N/SNP/SC", "Standard scan (offer) or Extended scan (migration). Produces a .snp file (extension mandatory) loaded to the CrystalBridge platform. Role /SNP/SC required."],
    ["Enterprise structure and usage", "CrystalBridge platform", "Organizational structure, unused company codes / plants (carve-out candidates), usage matrix of data objects vs. domains, module usage."],
    ["Master data analysis", "/N/SNP/CW_MDA", "Compare master data across systems (EQ / NE / MS conflicts), golden-record rule bases, preselection for harmonization."],
    ["Customizing analysis", "/N/SNP/CW_CUST_COMP, /N/SNP/CW_TAB_MONITOR", "Compare customizing tables between systems; create SNP Analysis Cockpit project."],
    ["Repository analysis", "/N/SNP/BBRAP", "Checksum comparison of programs, classes, tables; finds custom code impact."],
    ["Interface analysis", "CrystalBridge platform", "RFC, web service, IDoc and DB connections by volume and frequency."],
    ["S/4 Simplification Item Check", "Part of system scan", "SAP relevance check for S/4HANA."],
    ["Master data preselection", "/N/SNP/CW_PRESELECTION", "Decides which record comes from which source system before export."],
], [3.8 * cm, 4.2 * cm, 9.0 * cm], first_bold=True), sp(4)]
story += [warn("Recommended temporary indexes for the scan (remove after success): COBK (MANDT, KOKRS), BKPF (MANDT, GJAHR), "
               "VBAK (MANDT, VBTYP), AUFK (MANDT, AUTYP)."), PageBreak()]

# -- 4 TC CONFIGURATION ---------------------------------------------------------
story += banner("04  Transformation Cockpit Configuration", "Transaction /N/SNP/TC on the control system", TEAL, BLUE)
story += [p("The cockpit is scenario based. A <b>scenario</b> is the complete migration blueprint: systems, selections, "
            "mappings, data objects, rules and runs. Requires role " + mono("/SNP/TF_TC_TC_700_DIA_ALL") +
            " (display: " + mono("..._DIA_DISP") + ").")]
story += [tbl([
    ["Layer", "Object", "Description"],
    ["1", "Scenario", "Top-level container; source / target systems, selections, mappings, data objects."],
    ["2", "Transformation run", "Named execution plan (Export, Import, Full Load, Delta, Validation, Rollback)."],
    ["3", "Transformation block", "Executable unit; processes a set of data objects. Types EXP, FOR, IMP, UPL."],
    ["4", "Data object", "Business entity at table level, including table hierarchy (e.g. FI documents, customer master)."],
], [1.4 * cm, 4.0 * cm, 11.6 * cm]), sp(6)]

story += [h2("4.1  Scenario types and handling")]
story += [tbl([
    ["Type", "Use"],
    ["Bluefield", "Selective migration; source stays live."],
    ["Greenfield", "Full migration to a new S/4HANA system."],
    ["Merge", "Consolidation of several systems into one target."],
    ["Carve-Out", "Extract a subset of entities to a new system."],
], [3.5 * cm, 13.5 * cm], first_bold=True), sp(4)]
story += [bul("Create: unique Scenario ID (up to 30 characters); the ID is the value of parameter " + mono("P_SCEN") + " in all Mission Control configs."),
          bul("Copy with options: selections, mapping values, data objects, runs and blocks. Delete is irreversible - download first."),
          bul("Download: zipped XML named ScenarioName_Date_Time.zip (about 30x size when unzipped). Upload can run in background. "
              "Delivery content must be uploaded manually at project start; links to global selections / rules are not validated on upload."),
          bul("Scenario variants can be saved locally with " + mono("/SNP/HC02_SCENARIO_XML_EXPORT") + " (ZIP: XML + rule base TXT).")]

story += [h2("4.2  Selections - scope of the migration")]
story += [tbl([
    ["Field", "Meaning", "Field", "Meaning"],
    ["BUKRS", "Company code", "VKORG", "Sales organization"],
    ["GJAHR", "Fiscal year", "EKORG", "Purchasing organization"],
    ["KOKRS", "Controlling area", "BWKEY", "Valuation area"],
    ["WERKS", "Plant", "PRCTR / GSBER", "Profit center / business area"],
    ["KUNNR", "Customer number", "LIFNR / MATNR", "Vendor / material number"],
], [2.4 * cm, 6.1 * cm, 2.8 * cm, 5.7 * cm], first_bold=True), sp(4)]
story += [p("Range notation (SIGN / OPTION / LOW / HIGH): " + mono("IEQ1000") + " include equal 1000; " + mono("ICP100*") +
            " include pattern; " + mono("IBT10002000") + " include between; " + mono("EEQ9999") + " exclude equal. "
            "Fill global selections from the blueprint with " + mono("/SNP/TE02_API_FILL_SEL_FROM_BP") +
            "; validate with " + mono("/SNP/TE02_VALIDATE_SELECTIONS") + ".")]
story += [tbl([
    ["Selection type", "Scope", "Reusable", "Mode"],
    ["Global selection", "All tables with a field of the assigned domain", "Yes", "Declarative (AND-linked) or SQL expert"],
    ["Field selection", "Single field in a single table", "No", "Declarative only"],
], [3.2 * cm, 7.0 * cm, 1.8 * cm, 5.0 * cm], first_bold=True), sp(2)]
story += [warn("Switching from SQL expert mode back to declarative mode loses all assigned selections. Cached Read (default) loads all "
               "values into memory; use Single Read only for memory problems with very large selections."), sp(6)]

story += [h2("4.3  Mapping - the transformation layer")]
story += [p("Mapping is applied between export and import, in the staging phase. Source data is never changed.")]
story += [FlowRow([
    ("SOURCE ECC", ["BUKRS 1000", "KUNNR 12345", "WAERS DEM"], CUSTC),
    ("STAGING", ["Raw export", "stored as", "packages"], AMBER),
    ("MAPPING ENGINE", ["Value / field map", "Derivation, default", "Hard-coded"], VIOLET),
    ("TARGET S/4", ["BUKRS 2000", "PARTNER 12345", "WAERS EUR"], GREEN_C),
], height=66), p("Figure 3 - Mapping applied between export and import", CAPN), sp(2)]

story += [tbl([
    ["Mapping type", "Source keys", "Target", "Example from guide"],
    ["1:1", "1 value", "1 value", "WERKS 1000 to 1001"],
    ["N:1", "Several values", "1 value", "WERKS 1000, 2000 to 2001"],
    ["1:N", "1 value", "Several values", "WERKS 1000 to 1001 and 2001 - causes an error, values shown in message"],
    ["X+N:1 (dependent)", "2 fields combined", "1 value", "WERKS + LGORT to LGORT"],
], [3.4 * cm, 3.4 * cm, 3.4 * cm, 6.8 * cm], first_bold=True), sp(4)]

story += [tbl([
    ["Mapping layer / method", "Description", "Example"],
    ["Global mapping", "Applies to all fields of the scope: domain, data element or table field. One rule covers all plant fields in all tables.", "BUKRS 1000 to 2000 everywhere"],
    ["Field mapping", "Specific table field only; overrides global; can be deactivated.", "BSEG-KOSTL custom logic"],
    ["Value mapping", "Known source value to known target value; wildcards and ranges; CSV bulk import (SOURCE_VALUE;TARGET_VALUE;DESCRIPTION).", "WAERS DEM to EUR"],
    ["Structural field mapping", "Source field content to a different target field when the data model differs.", "KNA1-KUNNR / LFA1-LIFNR to BUT000-PARTNER"],
    ["Derivation rule", "ABAP logic derives the target from one or more source fields.", "PRCTR from KOSTL via CEPC"],
    ["Hard-coded value", "Target always set to a fixed value.", "RLDNR = 0L, LOGSYS = target"],
    ["Default value", "Fills only if source field is initial.", "GSBER blank to 0001"],
    ["Concatenate / split / pad / conditional", "String and conditional operations.", "VKORG/VTWEG/SPART to key"],
], [4.0 * cm, 8.0 * cm, 5.0 * cm], first_bold=True), sp(6)]

story += [h3("Standard mapping objects")]
story += [tbl([
    ["Object", "Field", "Module", "Object", "Field", "Module"],
    ["MAP_BUKRS", "BUKRS", "All", "MAP_GSBER", "GSBER", "FI"],
    ["MAP_KOKRS", "KOKRS", "CO", "MAP_KOSTL", "KOSTL", "CO"],
    ["MAP_EKORG", "EKORG", "MM", "MAP_HKONT", "HKONT", "FI"],
    ["MAP_VKORG", "VKORG", "SD", "MAP_WAERS", "WAERS", "FI"],
    ["MAP_WERKS", "WERKS", "MM/PP", "MAP_KUNNR", "KUNNR", "SD"],
    ["MAP_LGORT", "LGORT", "MM/WM", "MAP_LIFNR", "LIFNR", "MM"],
    ["MAP_BWKEY", "BWKEY", "MM", "MAP_MATNR", "MATNR", "MM"],
    ["MAP_PRCTR", "PRCTR", "CO", "MAP_ANLN1 / MAP_BLART", "ANLN1 / BLART", "FI-AA / FI"],
    ["MAP_MWSKZ", "MWSKZ", "FI/MM", "MAP_ZTERM / MAP_SEGMT", "ZTERM / SEGMENT", "FI,SD,MM / FI(S4)"],
], [2.6 * cm, 1.8 * cm, 1.8 * cm, 4.0 * cm, 3.0 * cm, 3.8 * cm]), sp(6)]

story += [h3("Setting up mapping - steps")]
for s in ["Open the scenario, go to the Mapping tab (object catalog).",
          "Activate required mapping objects (e.g. MAP_BUKRS, MAP_HKONT, MAP_KUNNR).",
          "Edit values: source value, target value, description; wildcards (*) and ranges supported. More specific entries win over wildcards.",
          "Bulk upload via Import from File (semicolon CSV). Derivation rules on the Rules sub-tab; hard-coded and default values on their sub-tabs.",
          "Save, then run " + mono("/SNP/TE02_VALIDATE_MAPPINGS") + " to find gaps. Re-generate blocks (" + mono("/SNP/TE02_API_CREATE_BLOCKS") + ") after major changes."]:
    story.append(bul(s))
story += [sp(4), good("<b>Best practice:</b> start with org-unit mappings (BUKRS, KOKRS, WERKS, VKORG); use CSV for large GL account tables; "
                      "validate before every test run; document derivation rules; run in simulation first; store key target values as Mission Control "
                      "variables; obtain business sign-off on value mappings (role " + mono("/SNP/TF_TC_TC_700_DIA_BUSI") + ")."),
          PageBreak()]

story += [h2("4.4  Data objects")]
story += [p("A data object represents business data at table level, including table hierarchy and dependencies. "
            "Add from the catalog (Data Objects tab, Adopt). Custom Z-tables are covered by the <b>Data Object Builder</b> "
            "(role " + mono("/SNP/TF_CO_DOB_700_DIA_ALL") + ").")]
story += [tbl([
    ["Module", "Examples of data objects"],
    ["FI", "G/L account master, open items AR/AP, G/L balances, asset master (FI-AA), down payments, recurring entries"],
    ["CO", "Cost center master and actuals, internal orders, profit center master, CO-PA"],
    ["MM", "Material master, purchase orders, scheduling agreements, goods receipts, inventory, info records"],
    ["SD", "Customer master, sales orders, deliveries, billing documents, pricing conditions, credit management"],
    ["PP / PM / CS / WM", "Production orders, BOMs, routings, work centers; functional locations, equipment, maintenance orders; warehouse structures"],
    ["HCM / ISU / Basis", "Employee and payroll; contracts, devices, installations; number ranges, custom Z-tables, application log"],
], [3.2 * cm, 13.8 * cm], first_bold=True), sp(4)]
story += [tbl([
    ["Table property", "Options / meaning"],
    ["Export method", "SR Scout Reader (FOR ALL ENTRIES, uses last export of selection table) or DR Direct Reader (INNER JOIN, independent)."],
    ["DKP - duplicate key prevention", "Auto-activated when selection table has more key fields than used for the dependent table; slow (no parallelization). Use Direct Reader or adapt structure."],
    ["Selection mode", "F field selection (declarative) or S free selection (SQL expert)."],
    ["Package / FAE size / Blocking factor", "Override scenario package size for large tables; sub-package segmentation."],
    ["Import mode per table", "FROM_BLOCK, INSERT, UPDATE, MODIFY, DELETE, NO_IMPORT, FROM_TABLE."],
], [5.0 * cm, 12.0 * cm], first_bold=True), sp(4)]
story += [p("Validate objects with " + mono("/SNP/TE02_VALIDATE_OBJECTS") + ", find missing DDIC with " + mono("/SNP/TE02_FIND_MISSING_DDIC") +
            ", syntax check with " + mono("/SNP/TE02_API_EXEC_SYNTAX_CHK") + ". Export the object table list to CSV with " + mono("/SNP/TE02_TABLES_TO_CSV") +
            ". <b>Address object</b> (domains ADRNR, AD_ADDRNUM, AD_PERSNUM, AD_SO_KEY, CADRNR): export <b>last</b>, import <b>first</b>; "
            "address numbers are collected in global selection SEL_ADRNR.")]

story += [h2("4.5  Number ranges (NRIV)")]
story += [tbl([
    ["Strategy", "Use case"],
    ["Increment", "Internal number ranges in target - shift existing range upward."],
    ["Difference calculation", "Internal number ranges - calculate gap between source and target."],
    ["1:1", "Internal number ranges - copy as-is."],
    ["Inactive (adopt 1:1)", "External number ranges in target."],
], [4.5 * cm, 12.5 * cm], first_bold=True), sp(2)]
story += [p("Functions: Save NRIV, Check NRIV, Update NRIV, Mass Maintenance. Lock number ranges on the target before delta imports and unlock afterwards."), PageBreak()]

# -- 5 RULES ---------------------------------------------------------------------
story += banner("05  Rules, Import Modes and Events", "Export rules (consultant) and import rules (migration specialist)", VIOLET, BLUE)
story += [h2("5.1  Import modes")]
story += [tbl([
    ["Mode", "Existing key", "New key"],
    ["Insert", "Terminates with duplicate key error", "Inserts record"],
    ["Insert ADK", "Skips record (no error)", "Inserts record"],
    ["Update", "Updates non-key fields", "Nothing imported"],
    ["Modify", "Updates non-key fields", "Inserts record"],
    ["Delete", "Removes record by key", "Nothing done"],
], [3.5 * cm, 7.0 * cm, 6.5 * cm], first_bold=True), sp(2)]
story += [warn("Special care for Insert ADK, Modify, Update and Delete: agree with the customer which records are retained. "
               "A field without an import rule is transferred 1:1.")]

story += [h2("5.2  Export event sequence")]
story += [p("Before data object export; process initialization; before table processing; before package processing; before data record "
            "(EV_SKIP = 'X' skips a record); global export rule; after data record; after package; global event after package; "
            "after table; after data object export. Changes in an earlier event are effective in all later events of the same cycle.")]

story += [h2("5.3  Rule interfaces")]
story += [tbl([
    ["Rule type", "Key parameters"],
    ["Global import rule", "IV_VALUE (incoming), EV_VALUE (outgoing), EV_SKIP"],
    ["Field rule", "IS_<TABLE> (source record), CV_<FIELD> (target field), EV_SKIP"],
    ["After data record", "IS_<TABLE> original, CS_<TABLE> target changeable, EV_SKIP"],
    ["After package", "CT_<TABLE> package table changeable"],
    ["Parameter prefixes", "I importing, C changing, E exporting; V value, S structure, T table"],
], [4.5 * cm, 12.5 * cm], first_bold=True), sp(4)]

story += [h2("5.4  API calls available in rules")]
story += [tbl([
    ["Function", "Purpose"],
    ["API_MAPPING_ADD / _SET / _GET / _CLEAR", "Add (dump if exists) / add or overwrite / read (sy-subrc 4 = 1:1 passthrough) / clear auto-added entries."],
    ["API_SELECTION_ADD / _GET / _EXISTS / _CLEAR", "Maintain global selections during export (visible on source only; selection must exist and be generated)."],
    ["API_MESSAGE_ADD", "Log message S/E/W/I/A/X; types X and A always written."],
    ["API_LOCK / API_UNLOCK", "Named lock between parallel processes (visible in SM12)."],
], [6.0 * cm, 11.0 * cm], first_bold=True), sp(4)]
story += code("""* Global export rule - collect values across packages
* Process initialization
PERFORM api_selection_get USING 'PRCTR' CHANGING lt_prctr.
* Before table processing
SELECT vbeln posnr FROM vbap INTO TABLE lt_vbeln WHERE vbap-prctr IN lt_prctr.
* After package processing
PERFORM api_selection_clear USING 'SEL_VBELN_PRCTR'.
PERFORM api_selection_add   USING 'SEL_VBELN_PRCTR' lw_vbfk-vbeln.""")
story += [p("Tools: sample feature (F4) generates template code; CTRL+Space auto-completion; version management (compare two versions). "
            "Syntax check runs against the shadow DDIC in dialog or background and executes automatically when export or import starts - "
            "the transformation terminates on a syntax error. Debugging works in dialog mode only; stop parallel processes first."), sp(10)]

# -- 6 EXECUTION -----------------------------------------------------------------
story += banner("06  Executing the Transformation", "Runs, blocks, pre-execution checklist, monitoring", TEAL, BLUE)
story += [FlowRow([
    ("EXPORT block", ["Runs on SOURCE", "Extracts and", "writes packages"], CUSTC),
    ("FORERUNNER", ["Reads + transforms", "No import; creates", "conversion table"], AMBER),
    ("IMPORT block", ["Runs on TARGET", "Reads packages,", "applies rules"], GREEN_C),
    ("POST-PROCESS", ["XPRA / XCLA / SDM", "on target after", "import"], VIOLET),
], height=66), p("Figure 4 - Block types in a run", CAPN), sp(2)]

story += [h2("6.1  Block configuration")]
story += [tbl([
    ["Option", "Description"],
    ["Package size", "Records per commit (default 10,000 at block level). Larger = faster but more memory."],
    ["Parallel processes", "Concurrent jobs; limited by Max. process count of the system."],
    ["Restart capability", "Restart from last successfully processed package."],
    ["Sequence / dependencies", "Execution order within the run."],
    ["Index suspension", "Suspend indexes during import for performance; rebuild afterwards."],
    ["Without rule base", "Bypass all transformation rules."],
    ["Block / table mode", "INSERT, INSERT_ADK, UPDATE, MODIFY, DELETE; table level also FROM_BLOCK, NO_IMPORT, FROM_TABLE."],
    ["Alias of the system", "Required when two or more source systems are assigned."],
], [4.5 * cm, 12.5 * cm], first_bold=True), sp(6)]
story += [p("Create blocks automatically with " + mono("/SNP/TE02_API_CREATE_BLOCKS") + "; copy runs with " + mono("/SNP/TE02_API_COPY_RUNS_BLOCKS") +
            " when starting a new cycle. Export files are created per run and never overwritten; deleting a block deletes its files; import uses the "
            "last export by default (re-assign via context menu).")]

story += [h2("6.2  Pre-execution checklist")]
story += [tbl([
    ["#", "Check", "Report / action"],
    ["1", "Systems connected, RFC destinations working", "/SNP/TE02_API_CHECK_SYS_CONS"],
    ["2", "Selections complete and valid", "/SNP/TE02_VALIDATE_SELECTIONS"],
    ["3", "Mappings complete and valid", "/SNP/TE02_VALIDATE_MAPPINGS"],
    ["4", "Data objects valid", "/SNP/TE02_VALIDATE_OBJECTS"],
    ["5", "DDIC analysis executed", "/SNP/TE02_API_REMOTE_DDIC_ANA"],
    ["6", "Syntax check executed", "/SNP/TE02_API_EXEC_SYNTAX_CHK"],
    ["7", "Violation check passed", "/SNP/TE02_API_VIOLATION_CHECK"],
    ["8", "Target user authorizations sufficient", "Roles per section 11"],
    ["9", "Number ranges locked on target (if required)", "NRIV area / control block"],
], [0.9 * cm, 8.6 * cm, 7.5 * cm]), sp(6)]

story += [h2("6.3  Execution options")]
story += [tbl([
    ["Option", "Use"],
    ["Background mode", "Recommended for production; dialog only for testing / debugging."],
    ["Simulation", "Validates extraction and transformation logic without writing to the database."],
    ["Restart", "Resume a failed block from the last successful commit package."],
    ["Reset", "Reset status and delete intermediate results before re-executing."],
    ["Schedule / start immediately", "Job priority A/B/C; schedule for a future time."],
], [4.5 * cm, 12.5 * cm], first_bold=True), sp(4)]

story += [h2("6.4  Monitoring")]
story += [tbl([
    ["Tool", "Content"],
    ["Log tab / /SNP/TCPROT", "Start / end, records per object, written to target, errors with table references, records per second; filter options."],
    ["Not migrated tables", "Exported-versus-imported status per table."],
    ["TC Daemon /SNP/TE01_DAEMON", "Background SLEEP process (cycle up to 5 s); updates display and drives dependency-based starts."],
    ["System Monitor", "Remote file system, lock entries, logged-on users, process overview with scenario / run / block, system log."],
    ["Remote SE16 /SNP/CN_SE16", "View source or target table content without logon."],
    ["Run steering", "Reset, Refresh, Stop, Restart, Duplicate at run, block, object and table level."],
], [5.0 * cm, 12.0 * cm], first_bold=True), PageBreak()]

# -- 7 MISSION CONTROL -------------------------------------------------------------
story += banner("07  Mission Control Automation", "Plan, orchestrate, execute and monitor the migration project (/N/SNP/MC)", BLUE, VIOLET)
story += [p("Mission Control runs on the central system; no additional transports or RFC settings are needed (unlike the cockpit). "
            "A project is created from a <b>unit</b> (template), must be <b>licensed</b> before tasks can run (download license file, "
            "support ticket at support.snpgroup.com, upload returned file).")]
story += [tbl([
    ["Task type", "Description"],
    ["Manual activity", "Executed by a person; status reported manually."],
    ["Report call in dialog", "Report on a defined system in dialog; status reported manually."],
    ["Report call in background", "Background job; status derived automatically."],
    ["Summary task", "Non-executable structure element; variables for all sub-tasks."],
], [5.0 * cm, 12.0 * cm], first_bold=True), sp(6)]

story += [h2("7.1  Typical automation configurations")]
story += [p("<b>Execute TC export blocks (central system, with automatic ticket creation on error):</b>")]
story += code("""<config R:CLASS="/SNP/CN02_CL_TEX_REPORT"
        R:REFRESH_CLASS="/SNP/TE02_CL_TEX_TR_REFRESH"
        R:REMOTE_CALLTYPE="LA" R:IV_REPORT="/SNP/TE02_API_EXECUTE_BLOCKS"
        P_SCEN="{M:GET_VARIABLE TC_SCENARIO}" S_RUN="Export" S_BLOCK="BLK_*">
  <R:COMMAND CLASS="/SNP/TE02_CL_CMD_API_GOTO_TC"
             SCENARIO="{M:GET_VARIABLE TC_SCENARIO}" RUN_NAME="Export"/>
</config>""")
story += [p("<b>Open a selection in the cockpit:</b>")]
story += code("""<config R:CLASS="/SNP/CN02_CL_TEX_REPORT" R:REMOTE_CALLTYPE="LS"
        R:IV_REPORT="/SNP/TE02_SCENARIO_GOTO"
        P_SCEN="{M:GET_VARIABLE TC_SCENARIO}" P_G_SEL="X" P_ID="BUKRS" P_N_MODE="X"/>""")
story += [p("<b>Remote SE16 on the source system:</b>")]
story += code("""<config R:CLASS="/SNP/CN02_CL_TEX_REPORT" R:REMOTE_CALLTYPE="LS"
        R:IV_REPORT="/SNP/CN02_SE16" P_TAB="T001"
        P_RFC="{M:GET_SYSTEM_RFC SOURCE}" R:IV_SHOW_SELECTION_SCREEN="X"/>""")

story += [h2("7.2  Transformation Cockpit API reports used from Mission Control")]
story += [tbl([
    ["Group", "Report / class", "Purpose"],
    ["Scenario", "/SNP/TE02_API_SCEN_FROM_MC", "Create TC scenario from Mission Control (P_FILE or P_R_SCEN)."],
    ["Scenario", "/SNP/TE02_API_IMPORT_SCEN_MC", "Extend existing scenario with another TC scenario."],
    ["Systems", "/SNP/TE02_API_SYNC_SYSTEMS", "Assign systems to TC scenarios (errors become tickets)."],
    ["Preparation", "/SNP/TE02_API_REMOTE_DDIC_ANA", "Remote DDIC analysis."],
    ["Preparation", "/SNP/TE02_API_FILL_SEL_FROM_BP", "Fill global selections from blueprint."],
    ["Validation", "/SNP/TE02_VALIDATE_SELECTIONS / _MAPPINGS / _OBJECTS", "Check selections, mappings, data objects."],
    ["Blocks", "/SNP/TE02_API_CREATE_BLOCKS / _COPY_RUNS_BLOCKS / _EXECUTE_BLOCKS", "Create, copy, execute (P_SCEN, S_RUN, S_BLOCK)."],
    ["Logging", "/SNP/TE02_API_REP_TRANS_PROT / _PROT_FINDINGS", "Show migration log; filter log contents."],
    ["Proxy", "/SNP/TE01_CL_API_TDEF_PROXY", "Sync selections and mappings between MC variables and TC."],
    ["Proxy", "/SNP/TE01_CL_API_MAP_VAL_PROXY / _SCE_PAR_PROXY", "Read target mapping values; scenario parameters."],
    ["Sync", "/SNP/CN02_API_CB_SYNC_PROJECT", "Synchronize scenario from blueprint."],
], [2.2 * cm, 7.4 * cm, 7.4 * cm], first_bold=True), sp(6)]

story += [h2("7.3  Tickets and forced actions")]
story += [bul("Warnings and errors become <b>tickets</b>; the task stays <b>Blocked</b> until tickets are resolved. Close tickets as FIXED / NO_CHANGE / IGNORE with comment."),
          bul("Closing a ticket as 'ignored' sets status Erroneous and may cause issues in later tasks."),
          bul("Forced close / reset / execute must be enabled in Project settings (ALLOW_FORCED_CLOSING, Allow forced reset, Force execution); use with caution."),
          bul("Task daemon job " + mono("/SNP/CN01_TASK_DAEMON") + " updates asynchronous tasks; process count in registry MC.TASK_DAEMON.PROCESS_COUNT (default 2)."),
          bul("Projects can be downloaded / uploaded as ZIP (software version must match exactly) and saved as new unit versions.")]
story += [PageBreak()]

# -- 8 NZD ----------------------------------------------------------------------
story += banner("08  Near-Zero Downtime and Delta Loads", "Rule-Based Near-Zero Downtime (RBNZD)", RED_C, BLUE)
story += [p("RBNZD lets the source stay live while the bulk of the data is migrated in advance. Only the final delta "
            "(changes since the last run) is moved during the cutover window."), sp(2)]
story += [NZDDiagram(), p("Figure 5 - RBNZD load sequence", CAPN)]
story += [tbl([
    ["Phase", "Description"],
    ["1 Initial load", "Full extraction and import while source is live."],
    ["2 Delta sync", "Multiple delta runs; repeat to shrink the final delta."],
    ["3 Final delta", "Short downtime: source locked, final sync, target go-live."],
], [3.5 * cm, 13.5 * cm], first_bold=True), sp(6)]

story += [h2("8.1  Setting up RBNZD")]
for s in ["Assign role " + mono("/SNP/TF_DO_RBNZD_700_DIA_ALL") + "; set run parameter NZD_ACTIVE.",
          "Create the scenario with " + mono("/SNP/ZD02_TC_CREATE_SCENARIO") + "; open the hub with " + mono("/SNP/ZD02_SCENARIO_GOTO") + ".",
          "Configure delta detection rules per data object.",
          "Execute the initial load through the standard TC blocks.",
          "Create delta loads with " + mono("/SNP/ZD02_MC_CREATE_DELTA_LOAD") + ".",
          "Execute with class " + mono("/SNP/ZD01_CL_MC_EXECUTE_TASK") + " from Mission Control; monitor via " + mono("/SNP/ZD02_CL_CMD_SCENARIO_GOTO") + " and refresh class " + mono("/SNP/TE02_CL_TEX_TR_REFRESH") + ".",
          "Delete a scenario or part of it with " + mono("/SNP/ZD02_DELETE_SCENARIO") + " (errors become tickets)."]:
    story.append(bul(s))

story += [h2("8.2  Delta process rules")]
story += [bul("An initial full load must be completed first; a <b>delta timestamp</b> is recorded after each successful export."),
          bul("Next delta extracts only records created or changed after the timestamp; import applies in update mode on top of existing data."),
          bul("Run deltas frequently (daily or more); validate each delta with DCV before the next."),
          bul("Lock number ranges on the target before each delta import and unlock after."),
          bul("Track timestamps to avoid overlap or gaps; test the full delta process including rollback in QA before production.")]
story += [PageBreak()]

# -- 9 VALIDATION ---------------------------------------------------------------
story += banner("09  Validation and S/4 Post-Processing", "Prove completeness and finalize the S/4HANA data model", GREEN_C, BLUE)
story += [tbl([
    ["Check", "Tool", "What it proves"],
    ["Compare export to target", "Transformation area", "Key fields identical; changed non-key fields (mapped values) shown as expected differences."],
    ["Data Consistency Verification", "/N/SNP/FKC on target; /SNP/FK02_SUMMARY", "Domain fixed values (DD07L), foreign key and value-table checks. Supports ECC, HCM, S/4HANA. Results by check, table, domain; before / after comparison."],
    ["Balance sheet comparison", "RFBILA00 + /SNP/CW02_VR_API_BALANCE_CMP", "Financial balances equal between systems; variable VR_IS_MAP_ACTIVE (XFELD) activates TC mapping in comparison."],
    ["Parametric transaction comparison", "/SNP/CW02_VR_PARAMETRIC_TRX", "Same SAP transaction run on both systems; spool outputs compared. Field mapping in variable VR_FIELDS_MAP."],
    ["Violation check", "/SNP/TE02_API_VIOLATION_CHECK", "Referential integrity and mandatory fields."],
    ["Automated testing", "Role /SNP/TF_AT_700_ALL", "Application-level tests via SAP GUI in read and change mode on selected / random test data."],
    ["Test units", "Cockpit to target", "Stored SAP reports and transactions launched from the transformation."],
    ["Business Object Detail Analysis", "/N/SNP/CW_BODA", "HTML report per system for business objects of a TC scenario."],
], [4.2 * cm, 4.8 * cm, 8.0 * cm], first_bold=True), sp(8)]

story += [h2("9.1  S/4HANA post-processing")]
story += [tbl([
    ["Program", "Purpose"],
    ["XPRA", "Post-processing routines adjusting migrated data to the S/4HANA data model."],
    ["XCLA", "Classification and characteristic value assignments."],
    ["SDM (Selective Data Migration)", "S/4-specific programs for Finance, Logistics etc.; role /SNP/TF_TC_PP_SAT_754_ALL."],
], [5.0 * cm, 12.0 * cm], first_bold=True), sp(4)]
story += [p("Authorization for post-processing: " + mono("/SNP/TF_TC_PP_700_ALL") + ". Performance optimization role: " + mono("/SNP/TF_PF_700_ALL") + ". "
            "The S/4HANA Cockpit uses " + mono("/SNP/TF_TC_S4_SAT_751_ALL") + ".")]
story += [warn("Business partner creation: ECC customers and vendors are created as business partners in the target. BAPI-based migrations "
               "(e.g. business partners) need the additional role /SNP/XX_MIG_BAPI_SAT_700/751/754_ALL on the target. "
               "Business partner harmonization is a Professional Services item."), PageBreak()]

# -- 10 WORKFLOW -----------------------------------------------------------------
story += banner("10  End-to-End Workflow to Go-Live", "Scenario creation to post-processing (16 steps from the guide)", NAVY, TEAL)
wf = [["#", "Action", "Tool / transaction", "Owner", "Status"],
      ["1", "Create scenario", "/N/SNP/TC", "Migration lead", TBC],
      ["2", "Assign systems, test connections", "Systems tab; /SNP/TE02_API_CHECK_SYS_CONS", "Basis", TBC],
      ["3", "Define selections (company code, fiscal year ...)", "Selections tab", "Functional", TBC],
      ["4", "Configure mapping", "Mapping tab", "Functional + business", TBC],
      ["5", "Add data objects", "Data Objects tab", "Migration lead", TBC],
      ["6", "Validate setup", "/SNP/TE02_VALIDATE_SELECTIONS / _MAPPINGS / _OBJECTS", "Migration lead", TBC],
      ["7", "DDIC analysis", "/SNP/TE02_API_REMOTE_DDIC_ANA", "Technical", TBC],
      ["8", "Syntax check", "/SNP/TE02_API_EXEC_SYNTAX_CHK", "Technical", TBC],
      ["9", "Create blocks", "/SNP/TE02_API_CREATE_BLOCKS", "Technical", TBC],
      ["10", "Test execution (simulation)", "Execute blocks in simulation mode", "Technical", TBC],
      ["11", "Test migration (QA)", "Full load into QA target", "Migration team", TBC],
      ["12", "Validate results", "/SNP/FK02_SUMMARY; /SNP/CW02_VR_API_BALANCE_CMP", "Functional", TBC],
      ["13", "Production initial load", "Export + Import blocks in background", "Migration team", TBC],
      ["14", "Delta runs (RBNZD)", "/SNP/ZD01_CL_MC_EXECUTE_TASK (repeat)", "Migration team", TBC],
      ["15", "Final cutover delta", "Lock source, final delta, validate, go-live", "Cutover manager", TBC],
      ["16", "Post-processing", "XPRA / XCLA / SDM", "Technical", TBC]]
story += [tbl(wf, [0.8 * cm, 5.2 * cm, 6.0 * cm, 3.2 * cm, 1.8 * cm]), sp(8)]
story += [callout("Owners shown are proposed role types, not names from the SNP guide; confirm against the Sempra RACI. "
                  "Status column is for use during the project.")]
story += [PageBreak()]

# -- 11 ROLES --------------------------------------------------------------------
story += banner("11  Roles and Authorizations", "Composite and single roles for dialog and RFC users", BLUE, CUSTC)
story += [p("Composite roles reduce effort. They do <b>not</b> contain roles delivered separately, such as " +
            mono("/SNP/XX_MIG_755_RFC") + " or " + mono("/SNP/TF_TC_PP_SAT_754_ALL") + ", which must be installed and assigned separately.")]
story += [tbl([
    ["Role", "Purpose", "System"],
    ["/SNP/TF_DIA_ALL", "Composite - dialog users for TF and AN", "Control + satellites"],
    ["/SNP/TF_RFC", "Composite - RFC users for TF and AN", "Control + satellites"],
    ["/SNP/TF_TC_TC_700_DIA_ALL", "Transformation Cockpit (full)", "Control"],
    ["/SNP/TF_TC_TC_700_DIA_BUSI", "Business users maintain selections and mapping values", "Control"],
    ["/SNP/TF_TC_TC_700_DIA_DISP", "Read access to scenarios", "Control"],
    ["/SNP/MC_700_DIA_ALL", "Mission Control", "Control"],
    ["/SNP/AN_700_DIA_ALL", "CrystalBridge Analysis", "Control"],
    ["/SNP/XX_MIG_700_RFC (+751, 755)", "Cross-component RFC user; 755 for generating tables on Basis 7.55 (or auth object S_ABPLNGVS ABP_LNG_VS='', ACTVT 40)", "Source, target"],
    ["/SNP/XX_MIG_BAPI_SAT_700/751/754_ALL", "Migrations using BAPIs (e.g. business partners)", "Target"],
    ["/SNP/TF_TC_SG_700_DIA_ALL / _DISP / _RFC", "Staging framework (use / review logs / cross-system RFC)", "Control, satellites"],
    ["/SNP/TF_DC_DCV_700_DIA_ALL / _DISP / _RFC", "Data Consistency Verification (use / display results / RFC)", "Control, satellites"],
    ["/SNP/TF_DC_DCV_751_DIA_ALL", "DCV - Foreign Key Finder", "Control"],
    ["/SNP/TF_DO_RBNZD_700_DIA_ALL", "Rule-Based Near-Zero Downtime", "Control"],
    ["/SNP/TF_TC_S4_SAT_751_ALL", "SNP S/4HANA Cockpit", "Target"],
    ["/SNP/TF_TC_PP_700_ALL", "S/4 post-processing (XPRA, XCLA, SDM)", "Control, target"],
    ["/SNP/TF_TC_PP_SAT_754_ALL", "S/4 post-processing, SDM-specific (separate install)", "Target"],
    ["/SNP/TF_PF_700_ALL", "Performance optimizations", "Control, satellites"],
    ["/SNP/TF_CO_DOB_700_DIA_ALL", "Data Object Builder", "Control"],
    ["/SNP/TF_AT_700_ALL", "Automated Testing", "All"],
    ["/SNP/TF_TC_AM", "Archive Migration", "Target"],
    ["/SNP/SC", "CrystalBridge Analysis extractor (system scan)", "Scanned system"],
], [6.0 * cm, 8.2 * cm, 2.8 * cm], first_bold=False), sp(6)]
story += [tbl([
    ["Authorization profile", "Description"],
    ["/SNP/ADMINISTRATION", "Full authorization in all cockpits"],
    ["/SNP/CE_ADMIN", "Full authorization in the Transformation Cockpit"],
    ["/SNP/CE_SCENARIO_IMPL", "Maintain rules"],
    ["/SNP/USER, /SNP/PROJECTMANAGER", "Standard user / project manager"],
    ["/SNP/CW_DEVELOPER, /SNP/CW_DISPATCHER", "SNP Analysis Cockpit developer / dispatcher"],
], [6.0 * cm, 11.0 * cm], first_bold=True), PageBreak()]

# -- 12 TROUBLESHOOTING ------------------------------------------------------------
story += banner("12  Troubleshooting, Risks and Open Items", "Known issues from the guide and items to confirm", RED_C, NAVY)
story += [h2("12.1  Known issues and resolutions")]
story += [tbl([
    ["Issue", "Symptom", "Resolution"],
    ["Unmapped source value", "Import fails: no target value found for BUKRS=1200", "Add entry to MAP_BUKRS; run /SNP/TE02_VALIDATE_MAPPINGS to find all gaps."],
    ["Mapping not applied", "Source value unchanged in target", "Check object is activated and block includes the relevant tables."],
    ["Stale mapping cache", "New entries not in test run", "Re-generate blocks via /SNP/TE02_API_CREATE_BLOCKS."],
    ["Wildcard conflict", "Wrong value mapped", "More specific entries win; review mapping table sequence."],
    ["Case sensitivity", "EUR does not match eur", "Values are case-sensitive; use consistent casing."],
    ["Circular mapping", "Endless loop in transformation", "Check derivation classes for recursion; run syntax check."],
    ["Data object not processable", "Processing refused", "Run Table Analysis (/SNP/TE02_UPDATE_TABLE_INFO)."],
    ["Slow export with DKP", "Low throughput", "Use Direct Reader or adapt object structure."],
    ["Block failed", "Status Crashed / Canceled", "Review log; Restart from last good package; Reset only if re-extraction is intended."],
    ["Task blocked", "Task cannot be closed", "Resolve or properly close tickets in Mission Control."],
    ["Debugging parallel runs", "Debugger does not stop", "Debug in dialog with one process; stop parallel processes."],
], [3.6 * cm, 5.0 * cm, 8.4 * cm], first_bold=True), sp(8)]

story += [h2("12.2  Risk register (derived from guide behaviour)")]
story += [tbl([
    ["Risk", "Impact", "Mitigation"],
    ["Incomplete value mappings", "Import errors, rework in cutover", "Validate mappings before every cycle; business sign-off."],
    ["Import modes Modify / Update / Delete misused", "Unintended overwrite or loss in target", "Agree retained records; restrict to named blocks."],
    ["Delta timestamp gaps or overlaps", "Missing or duplicated records", "Track timestamps; DCV after each delta."],
    ["Number range clashes", "Duplicate keys, wrong ranges", "NRIV strategy per object; lock before delta."],
    ["RFC whitelist incomplete", "Connection failures at execution", "Maintain /SNP/TCSYS on all systems and clients; test connection."],
    ["Role gaps (755 / BAPI / PP SAT)", "Generation or import failures", "Install separately delivered roles; check section 11."],
    ["Software version mismatch on project upload", "Project cannot be loaded", "Align SNP versions between systems."],
    ["No license on new MC project", "Tasks cannot be executed", "Request license via SNP support before first execution."],
], [5.0 * cm, 5.0 * cm, 7.0 * cm], first_bold=True), sp(8)]

story += [h2("12.3  Open items - to be filled from the next SNP documents")]
story += [tbl([
    ["#", "Open item", "Needed from", "Status"],
    ["1", "Landscape snapshot values (section 2.3)", "SNP system documentation", TBC],
    ["2", "Scope: company codes, plants, fiscal years, modules (section 2.4)", "Blueprint / scoping", TBC],
    ["3", "Scenario IDs and run / block naming convention", "TC scenario export", TBC],
    ["4", "Mapping specification (org units, GL accounts, document types)", "Functional design", TBC],
    ["5", "Cycle plan: mock loads, volumes, durations", "Project plan", TBC],
    ["6", "Cutover schedule and downtime target", "Cutover plan", TBC],
    ["7", "Business partner approach (CVI / harmonization)", "Data design", TBC],
    ["8", "RACI and named owners for workflow steps", "Project governance", TBC],
    ["9", "Reconciliation tolerances and sign-off criteria", "Finance / business", TBC],
], [0.9 * cm, 8.6 * cm, 4.8 * cm, 2.7 * cm]), sp(10)]

# -- 13 MC-TC INTERLINK, OPTIONS, WORKED OBJECT ----------------------------------
story += [sp(14)]
story += banner("13  MC / TC Interlink and Options", "How Mission Control drives the cockpit, export / import options, one object end to end", TEAL, VIOLET)
story += [h2("13.1  How Mission Control and the Transformation Cockpit are interlinked")]
story += [p("Mission Control (" + mono("/N/SNP/MC") + ") plans and orchestrates; the Transformation Cockpit (" + mono("/N/SNP/TC") + ") holds the "
            "scenario and moves the data. They run on the same control system and are coupled by <b>configuration</b>, not by a shared "
            "table: an MC task carries an automation XML that calls a TC API report, and the scenario ID is passed through the "
            "project variable " + mono("TC_SCENARIO") + " (report parameter " + mono("P_SCEN") + ").")]
story += [McTcLinkDiagram(), p("Figure 6 - Mission Control to Transformation Cockpit interlink", CAPN)]
story += [tbl([
    ["Link point", "How it works", "Where it is configured"],
    ["Scenario ID", "Variable TC_SCENARIO holds the scenario ID and is read in every task with {M:GET_VARIABLE TC_SCENARIO}.", "MC project / summary task variables"],
    ["Start", "Report class CN02_CL_TEX_REPORT calls API report TE02_API_EXECUTE_BLOCKS with P_SCEN, S_RUN and S_BLOCK.", "Task automation XML"],
    ["Status back", "Refresh class TE02_CL_TEX_TR_REFRESH reads run / block status into the task: progress, log, auto ticket on error.", "Task automation XML"],
    ["Navigation", "Command class TE02_CL_CMD_API_GOTO_TC and report TE02_SCENARIO_GOTO open the cockpit on the right scenario or selection.", "Task automation XML"],
    ["Remote checks", "CN02_SE16 and similar reports let the task read source or target tables via the RFC of the system alias.", "Task automation XML"],
], [3.0 * cm, 9.5 * cm, 4.5 * cm], first_bold=True), sp(6)]
story += [h3("Backend tables involved")]
story += [tbl([
    ["Table", "Area", "Purpose (from the SNP guides)"],
    ["/SNP/CN01DAEMLOG", "MC", "Daemon log of Mission Control background processing."],
    ["/SNP/CN00REGUV", "MC / TC", "Registry parameter table (for example the TE.DAEMON.* settings)."],
    ["/SNP/CE00TABINFO", "Analysis", "Output of the table analysis (size, growth)."],
    ["/SNP/TE00TRPROT", "TC", "Transformation protocol; can be rebuilt with /SNP/TE02_REBUILD_TRANS_PROT."],
    ["/SNP/TE00NRIV", "TC", "Saved number-range levels on the target (SCEN_ID, OBJECT, NRRANGENR, FROMNUMBER, TONUMBER, NRLEVEL)."],
    ["/SNP/TE00TABREFT", "TC", "Table statistics, refreshed by the daemon (interval TE.DAEMON.TAB_STAT_REF_INTERVAL_IN_MIN, default 30 min)."],
    ["/SNP/TE00TABENCR", "TC", "List of encrypted tables (HR tables encrypted by default under scenario *)."],
    ["/SNP/TE05DKP, TE05ESEL, TE05ESELC", "TC", "Duplicate-key prevention and extended selection tables; cleaned by /SNP/TE05_CLEANUP."],
    ["/SNP/FK01FKEYDEF", "DCV", "Customizing of additional foreign keys for the foreign key check."],
    ["/SNP/CW00TABCMP, /SNP/CW00VRCFG*", "Validation", "Table comparison results and validation report configuration."],
    ["/SNP/PE01STGHEAD, PE01STGREG, SG05DDTSTAT, SG05DDDET", "Staging", "Posting Engine / staging header, registry and status."],
    ["/SNP/US00STAT", "Support", "Usage statistics."],
], [5.2 * cm, 2.2 * cm, 9.6 * cm], first_bold=True), sp(4)]
story += [warn("<b>No table that links an MC task to a TC scenario is named in the SNP documents.</b> The link is the scenario-ID variable plus the "
               "API report parameters. To see the stored task configuration, search the control system with SE11 / SE16N for " +
               mono("/SNP/CN0*") + ", " + mono("/SNP/CE0*") + " and " + mono("/SNP/TE0*") + "."), PageBreak()]

story += [h2("13.2  Export and import inside the Transformation Cockpit")]
story += [FlowRow([
    ("EXPORT BLOCK (EXP)", ["Selection of source", "data, export rules", "and events"], CUSTC),
    ("FILES", ["Compressed packages", "[share]/Scenario/", "Block/Table"], AMBER),
    ("FORERUNNER (FOR)", ["Optional: adjust", "exported data before", "import (on target)"], VIOLET),
    ("IMPORT BLOCK (IMP)", ["Mapping, import rules", "block / table mode", "write to target"], GREEN_C),
], height=76), p("Figure 9 - Block types in a TC run (an upload block UPL loads a CSV file into a table)", CAPN), sp(4)]

story += [h3("Export options")]
story += [tbl([
    ["Option", "Behaviour", "When to use"],
    ["Scout Reader (SR) - default", "FOR ALL ENTRIES. Max 1 process per table; dependent tables run after the selection table using its last export. Restart resets the whole table.", "Standard choice for object hierarchies."],
    ["Direct Reader (DR)", "INNER JOIN. DR tables are start tables, run with exactly 1 process, restart means full re-export. Not usable with concatenated field connections; export code changing join fields is ignored.", "Very large dependent tables where the join is cheaper than FAE."],
    ["Duplicate key prevention (DKP)", "Active when not all key fields of the selection table are used in the connection; forces 1 process per table. A unique selection on the missing key field (for example WERKS = 1000 on MARC / MARA) deactivates it.", "Leave on by default; deactivate only with a unique selection."],
    ["Selection mode F / S / N", "F = field selection; S = free SQL; N = native SQL (set manually).", "F for normal scope; S / N for complex conditions."],
    ["Blocking factor (FAE)", "Default 10 for transparent tables and 5 for pool / cluster tables; FAE package size is separate.", "Tune when FAE statements are slow."],
    ["Package size", "In records or MB; 0 puts all records into one package.", "Small packages for restartability; large for fewer files."],
    ["Parallel hint (Oracle)", "Default 4; applies to start tables and DR tables only.", "Oracle sources only."],
    ["Stick to same process / Ignore redirect", "Keeps a table on one process; ignore redirect generates a proxy table.", "Special cases only."],
    ["Field vs. global selection", "A field selection with no value exports the whole table; a global selection with no value transfers no records.", "Check empty selections before every export."],
], [3.6 * cm, 9.0 * cm, 4.4 * cm], first_bold=True), sp(4)]
story += [p("Export files are stored at " + mono("[share]/ScenarioID/Block PO ID/Table PO ID/") + " and are never overwritten. A restart exports only failed tables; "
            "child tables of a failed parent are not processed. Related tools: " + mono("/SNP/TE02_CHECK_EXPORT_FILES") + ", browse / download export files, display number of entries.")]

story += [h3("Import options")]
story += [tbl([
    ["Option", "Behaviour", "When to use"],
    ["Block mode", "INSERT, INSERT_ADK, UPDATE, MODIFY, DELETE. MODIFY or DELETE at block level override the table settings.", "INSERT for a clean load; others only by agreement."],
    ["Table mode", "FROM_BLOCK, INSERT, UPDATE, MODIFY, INSERT_ADK, DELETE, NO_IMPORT.", "Exceptions per table, NO_IMPORT to skip a table."],
    ["Several import modes", "Adds field TE_IMPORT_MODE that rules can set per record, for example cs_mara-te__import_mode = 'MODIFY'.", "Mixed new / existing records in one table."],
    ["Import option APPEND / SUM", "SUM works only with the rule base and numeric non-key fields.", "Merging balances into existing records."],
    ["With / without rule base", "Applies import rules or loads the exported data as is.", "Without rule base for pure copies."],
    ["Import sequence", "1-9999, default 10; lower numbers first.", "Header before item tables."],
    ["Select export", "If none is selected, the last successful export is used.", "Pick an older export to reload."],
    ["Differing target table", "Imports into a table with another name.", "Staging or redirect targets."],
    ["Simulation mode", "Writes no data; checks duplicates within the package and keys already in the DB; max 100 errors per table and process; not possible once a real import has started.", "Before the first real import of a block."],
    ["Deletion block", "Can be created for an incomplete import block.", "Clean-up after a failed import."],
], [3.6 * cm, 9.0 * cm, 4.4 * cm], first_bold=True), sp(4)]
story += [p("Import process distribution avoids lock problems; tables with table locks get priority, and a duplicate-key check runs within each package.")]

story += [h3("Event order")]
story += [tbl([
    ["Run", "Order of events"],
    ["Export", "Before object, process init, before table, before package, before record, global export rules, after record, after package, global event after package, after table, after object."],
    ["Import", "Process init, before table, before package, before record, field rule (overrides the global rule), global import rules / offsets, after record, after package, global event, after table."],
], [2.4 * cm, 14.6 * cm], first_bold=True), sp(4)]
story += [p("Setting " + mono("ev_skip = abap_true") + " skips a record. Global rules are scoped by domain, data element or table field and take up to 20 parameters; offsets handle concatenated fields."), PageBreak()]

story += [h2("13.3  One object end to end - sales documents (illustrative)")]
story += [warn("Illustrative example. The tables, values and names below are chosen to show the mechanics; they are not Sempra values and not taken "
               "from a Sempra scenario. Real selection fields come from the SNP data object definition (" + TBC + ").")]
story += [ObjectFlowDiagram(), p("Figure 8 - Sales document object from source to target, controlled from Mission Control", CAPN), sp(4)]
story += [tbl([
    ["#", "System", "Action", "Backend / API"],
    ["1", "MC", "Project from the S4B template; variable TC_SCENARIO set to the scenario ID.", "MC project, variables"],
    ["2", "TC", "Scenario created, via the Scenario Configurator from an SNP_MIG* template.", "/SNP/TE02_SCEN_CONFIGURATOR"],
    ["3", "TC", "Global selection on organizational units (example: company codes 1000, 1100).", "Selections"],
    ["4", "TC", "Mapping MAP_BUKRS: 1000 and 1100 to 2000 (example values).", "Mapping objects"],
    ["5", "TC", "Data object for sales documents assigned to an export block; start table VBAK, dependent VBAP.", "Data object, block"],
    ["6", "TC", "Import block created: mode INSERT, import sequence VBAK before VBAP.", "Import block"],
    ["7", "TC", "Validate objects and syntax check of rules.", "/SNP/TE02_VALIDATE_OBJECTS"],
    ["8", "MC", "Task 1 starts the export (S_RUN = Export).", "TE02_API_EXECUTE_BLOCKS"],
    ["9", "TC", "Scout Reader selects VBAK, then VBAP via FOR ALL ENTRIES on the VBAK export.", "Export block"],
    ["10", "Files", "Compressed packages written; raw source values, never overwritten.", "[share]/Scenario/Block/Table"],
    ["11", "MC", "Refresh class returns progress; an error creates a ticket and blocks the task.", "TE02_CL_TEX_TR_REFRESH"],
    ["12", "MC", "Task 2 starts the import (S_RUN = Import).", "TE02_API_EXECUTE_BLOCKS"],
    ["13", "TC", "Mapping applied between export and import; import rules run; VBAK then VBAP written.", "Import block"],
    ["14", "TC", "Number ranges saved / checked on the target.", "/SNP/TE00NRIV"],
    ["15", "MC", "Task 3 runs DCV and the foreign key check; results close the task.", "DCV, /SNP/FK01FKEYDEF"],
], [0.8 * cm, 1.7 * cm, 9.9 * cm, 4.6 * cm]), sp(4)]
story += [p("<b>Task 1 as automation XML</b> (same pattern as section 7.1; the export block name is illustrative):")]
story += code("""<config R:CLASS="/SNP/CN02_CL_TEX_REPORT"
        R:REFRESH_CLASS="/SNP/TE02_CL_TEX_TR_REFRESH"
        R:REMOTE_CALLTYPE="LA" R:IV_REPORT="/SNP/TE02_API_EXECUTE_BLOCKS"
        P_SCEN="{M:GET_VARIABLE TC_SCENARIO}" S_RUN="Export" S_BLOCK="BLK_SALES_EXP"/>""")

story += [h2("13.4  When to use what")]
story += [tbl([
    ["Situation", "Use", "Reason"],
    ["Normal parent / child object", "Scout Reader, mode INSERT", "Default behaviour, restartable per table."],
    ["Huge dependent table, join is cheaper", "Direct Reader", "INNER JOIN; accepts 1 process and full re-export on restart."],
    ["Fix exported data before import", "Forerunner block", "Adjusts exported data on the target without re-export."],
    ["Load a list from Excel / CSV", "Upload block", "CSV template is downloadable."],
    ["Test an import safely", "Simulation mode", "No data written; duplicate and key checks."],
    ["Changed values per record", "Several import modes", "Rule sets TE_IMPORT_MODE per record."],
    ["Large volume, short downtime", "RBNZD delta loads", "Triggers and collector tables capture changes; see section 8."],
    ["Check data without writing to the target", "Staging manager", "Type D (DDIC, constant runtime) or C (client, linear runtime)."],
], [5.4 * cm, 4.6 * cm, 7.0 * cm], first_bold=True), sp(6)]

story += [h2("13.5  Additional detail from the Transformation User Guide (25.09)")]
story += [tbl([
    ["Topic", "Fact"],
    ["Setup", "System maintenance /N/SNP/TCSYS; RFC whitelist /N/SNP/PXRFCWL per client on all systems (use * for the namespace). Template runs must be converted to executable runs."],
    ["Scenario Configurator", "5 steps: add file, scoping, target system, import preview, cleanup. Parameters include TGT_SYS_CREA_TYPE_TC (N, O, S), SCENARIO_TYPE, TGT_SAP_APPL_VERSN, TGT_S4CORE_VERSN, SC_MANDATORY."],
    ["Forerunner (FOR)", "Runs on the target, uses only successfully exported FOR-type objects, writes to the target."],
    ["Staging", "Manager type D (DDIC): shadow tables switched by renaming; pool / cluster tables become transparent. Type C (client): clients AAA-ZZZ. Use cases: downtime minimization, recycle bin, FK check without writing, transformation log with undo."],
    ["RBNZD internals", "DB triggers write to trigger tables; collector tables and collector programs are generated per root table. Delta loads use the collector tables as additional selection with the same rule base (delete / insert principle). Triggers must be on before the initial load; only TC is supported as engine; non-compliant objects go to the final delta or initial load."],
    ["Validation in MC", "Tasks: define parameters, set SNP layout as default, run report in source and target, compare (auto or manual), set customer layout as default. The S4B unit template contains them."],
], [3.4 * cm, 13.6 * cm], first_bold=True), sp(10)]


# -- 14 ADVANCED TECHNIQUES FROM TRAINING MATERIAL -------------------------------
story += [PageBreak()]
story += banner("14  Advanced TC Techniques", "Additional detail from Module 5 (v25.03), SNP2[TC] and SNP3[TC] (TC 19.03)", VIOLET, TEAL)
story += [p("This section adds what the SNP training decks contain beyond the reference guides. Source tags: <b>M5</b> = Module 5 Transformation Advanced "
            "Carve-Out v25.03; <b>SNP2</b> = SNP2[TC] Transformation Cockpit 19.03 SP00; <b>SNP3</b> = SNP3[TC] Advanced Learners 19.03 SP00. "
            "The 19.03 decks are older than the 25.09 user guide, so check a point against the 25.09 guide before relying on it for release-specific behaviour.")]

story += [h2("14.1  Technical process and scenario handling")]
story += [tbl([
    ["Topic", "Fact", "Source"],
    ["Technical process", "The controller on the control system creates and monitors worklists. Export programs on the source read the DB and write files; import programs on the target read the files and write the DB. Both are generated from the rule base and the shadow DDIC. A scenario can be switched from TC to the SAP LT migration workbench (MWB) at scenario level.", "SNP2"],
    ["Skills needed", "ABAP, SQL and module experience.", "SNP2"],
    ["Test vs. productive runs", "Satellite systems are typically system copies; the file system sits between source and target.", "SNP2"],
    ["Scenario content", "Delivery content must be uploaded manually at project start. Scenarios can be created, copied, downloaded (zipped XML named Scenario_Date_Time) and uploaded. When single objects are uploaded, links to global selections, rules, offsets and functions are not validated.", "SNP2"],
    ["Table analysis", "Collects DDIC and record counts from source and target into the control system (spool and /SNP/CE00TABINFO). Data objects cannot be processed without it. Refresh with /SNP/TE02_UPDATE_TABLE_INFO.", "SNP2"],
    ["Active tables to CSV", "Report /SNP/TE02_TABLES_TO_CSV exports all active tables of a data object.", "SNP2"],
    ["In-memory generation", "Programs/source texts are kept in /SNP/PX0XMEMREP and loaded at run time: generation can be parallelized (up to 1/6 of the time) but programs cannot be seen in SE38. Standard version creates reports on the satellite (visible and debuggable, only partly parallel).", "SNP2"],
    ["Training scenario caution", "The training project differs from typical project content and procedure.", "M5"],
], [3.2 * cm, 12.0 * cm, 1.8 * cm], first_bold=True), sp(6)]

story += [h2("14.2  Data object design")]
story += [p("Mass maintenance of a data object shows these columns per table: number, table name, alias, number of selection table, selection tables "
            "(generated path), differing target, status (active / inactive), export predecessor, export method (SR / DR), import sequence (10, 15, 20 ...), "
            "mode, import option (APPEND / SUM), sum fields, restrictions and categories (to enable or disable tables). Aliases are needed when a table is "
            "used more than once in an object and must be unique inside the object. Inactive tables are ignored in export and import. (M5, SNP2)")]
story += [tbl([
    ["Technique", "How it works / when to use", "Source"],
    ["Selection vs. dependent table", "Header tables drive the records exported; dependent tables hold the details (for example VBAK to VBAP, KNB1 to KNA1). A right-click unlinks a dependent table back to a selection table.", "M5"],
    ["Table connection by key fields", "Connect on key fields or on parts of a field (offset and length, for example OBJNR(2)). Free selection mode S allows SQL such as KNA1~KUNNR = {seltab:KUNNR}.", "M5, SNP2"],
    ["Concatenated fields", "One field built from several (for example STXH-TDNAME = MATNR + VKORG + VTWEG with TDOBJECT = 'MVKE'). A table extension is filled from the header table; in SQL expert mode the user must set up and fill the extension.", "M5, SNP2"],
    ["Avoiding DKP", "Three options: use the Direct Reader, adapt the object structure (table hierarchy, collecting values into a global selection and using it with an export predecessor), or complete the table connection. DKP is slow because it cannot run in parallel and logs every exported key.", "M5, SNP2"],
    ["Copy data objects", "Duplicate (1:1 in the same scenario) or copy tables from another object / scenario. Cross-scenario copy transfers global selections and existing rules are not overwritten.", "M5, SNP2"],
    ["Domain usage", "Finds table fields using a chosen domain and shows whether the table is already in the scenario (missing, inactive, active); can create a new object. Domain usage with content also checks real values and cross-client tables.", "M5, SNP2"],
    ["Deactivate empty tables", "Deactivates tables with no records; must be repeated for each test because contents change. No longer works with multiple source systems (only default systems are checked).", "M5, SNP2"],
    ["View as source", "A DB view can be used like a table. Without a differing target table only import mode NO_IMPORT is allowed; with a differing target (for example an own table modelled on the view) data can be imported.", "SNP3"],
    ["CSV upload", "Template CSV downloaded, filled by the customer, uploaded. Export methods: upload into an available SAP table, or into a virtual $ table that takes the CSV format.", "SNP3"],
    ["Differing target table", "Must exist in the target DDIC. Same-named fields are assigned automatically; unassigned field contents are lost. Fields can be filled with MOVE or by coding; data consistency is the consultant's responsibility.", "SNP3"],
    ["Objects without DDIC reference", "A check lists exceptions per system; the affected object can be deactivated.", "SNP3"],
], [3.4 * cm, 11.8 * cm, 1.8 * cm], first_bold=True), sp(6)]

story += [CondPageBreak(5 * cm), Paragraph("14.3  Selections, own tables, events and functions", ParagraphStyle("H2n", parent=H2s, keepWithNext=0))]
story += [tbl([
    ["Topic", "Fact", "Source"],
    ["Selection modes", "Field selection (declarative, default, recommended): connection AND field selection AND global selections, always with AND. Free selection (imperative, SQL expert mode): OR / NOT and other combinations in Open SQL. Switching back to declarative loses the assigned selections.", "M5, SNP2"],
    ["Read modes", "Cached read (default): all values loaded on first read, fast but can run out of memory on large tables. Single read: values read individually, slow, no complex selections; use when memory is a problem.", "SNP2"],
    ["Global selections", "Reusable for every field of the assigned domain (or same type if functionally correct). Values in database format incl. leading zeros. Created centrally in Global or on the table; mass assignment via Functions - Apply global selections (not possible if a selection is already assigned). Deleting a global selection deletes its links. Overview: /SNP/TE02_SELECTION_OVERVIEW.", "M5, SNP2"],
    ["Runtime-filled selections", "Initialize with API_SELECTION_CLEAR (event before object export), collect with API_SELECTION_ADD, test with API_SELECTION_EXISTS. API_SELECTION_CLEAR_SCOPED limits clearing to objects and tables. Global selections are generated as sub-selects, not INNER JOINs. Entries are added with MODIFY, are visible on the source only and are shown via the table in source system (remote SE16).", "M5, SNP3"],
    ["Own tables", "Namespace /SNP/TE_*; created for source and/or target; any structure; usable like DDIC tables in objects (also as header table in front of the original header). Fill with INSERT ... ACCEPTING DUPLICATE KEYS per package. Use NO_IMPORT for selection-only tables and generate for the source only; generate for source and target to migrate 1:1. Structural changes are detected when a run starts and trigger regeneration.", "M5, SNP3"],
    ["Global selection vs. own table", "Global selection: one column, simple, list upload. Own table: dependent values, flexible, global rules apply, can be placed in the tree, documentable, works across scenarios, needs planning.", "M5, SNP3"],
    ["Global events", "Effective for all tables unless the scope is limited to modules, objects or tables (Maintain Scope). Example: write company codes with object and table names into an own table. Another example calls SAVE_DATA_FOR_AT in the import event after package processing for Automated Testing.", "SNP3"],
    ["Global functions", "Called with PERFORM from rules; must be activated for export and/or import (run parameters GLOBAL_FUNCTION_EXPORT / _IMPORT); interface of importing and changing parameters. Example: UMSCHL_NUMBER_GET_NEXT_CHAR calls DO_NRIV which calls NUMBER_GET_NEXT and maps its sy-subrc values to API_MESSAGE_ADD.", "SNP3"],
    ["Standard global import rules", "MANDT (client changed to target), LOGSYS (source logical system to target logical system, abort message if either is missing) and ADRNR (address numbers via global function).", "SNP3"],
    ["Offsets", "Segment concatenated fields such as VAKEY by parameters (for example KVEWE, KOTABNR) and a segmentation string such as LIFNR(0,10),MATNR(10,18),EKORG(28,4),WERKS(32,4) for table A017. Relative position is typically 0 with no gaps; adjust when domain lengths change in a higher release (for example MATNR in S/4HANA).", "SNP3"],
    ["Mapping details", "Generated mapping tables are /SNP/TE_<hash>; 1:1 entries are added automatically by API call. Standard content builds mappings as dependent mappings with the system alias as first source field. Pattern: API_MAPPING_GET first, ADD only if sy-subrc is not 0. Mapping vs. own table: a mapping has source and target values and is read by rule. Field rules override global rules and can read the whole record but change only their own field. Check CHECK NOT iv_value IS INITIAL first to save runtime.", "M5, SNP2"],
    ["Mapping tools", "Bulk upload / download of mappings; validate values under Functions - Data Quality Mappings; report /SNP/TE05_OVERVIEW_TDEF_TABS lists generated tables. API_MAPPING_ADD dumps when the key exists, _SET overwrites, _CLEAR removes automatically added entries only.", "M5, SNP2"],
    ["Debugging", "Dialog only, one process. Set BREAK-POINT or break user in the coding; step keys F5 into, F6 over, F7 out, F8 execute. Predefined debugging points exist for export and import events.", "M5, SNP2"],
], [3.4 * cm, 11.8 * cm, 1.8 * cm], first_bold=True), sp(4)]
story += code("""* Own table fill pattern (export) - /SNP/TE_AUFNR example from the training
* Data definition:         DATA: lt_te_aufnr TYPE TABLE OF /snp/te_aufnr, ls_te_aufnr TYPE /snp/te_aufnr.
* Before table processing: DELETE FROM /snp/te_aufnr WHERE scen_id = te-scen_id
*                            AND source = te-source_system_alias AND object_id = te-object_id
*                            AND table_id = te-table_alias.
* After data record:       ls_te_aufnr-aufnr = cs_aufk-aufnr.  APPEND ls_te_aufnr TO lt_te_aufnr.
* After package:           INSERT /snp/te_aufnr FROM TABLE lt_te_aufnr.""")
story += [sp(4)]

story += [h2("14.4  Number ranges and forerunners")]
story += [tbl([
    ["Strategy", "Behaviour", "Needs"],
    ["Increment (internal ranges in target)", "Numbers are re-incremented in the target with NUMBER_GET_NEXT; mappings document old and new numbers.", "Forerunners for a smooth run"],
    ["Difference calculation (internal ranges)", "New number = old number plus an NRIV offset; much faster, no forerunner or mapping. If no reserved number exists, NUMBER_GET_NEXT is used as fallback.", "Save NRIV (several times for RBNZD), assign source systems, Update NRIV before import, buffer % and fixed buffer for RBNZD"],
    ["1:1 (internal ranges)", "Numbers adopted unchanged; number statuses updated in target.", "-"],
    ["Inactive, adopt 1:1 (external ranges)", "External numbers adopted unchanged.", "-"],
], [4.6 * cm, 7.6 * cm, 4.8 * cm], first_bold=True), sp(4)]
story += [bul("<b>Forerunner</b> (a special data object, block type FOR): contains table references of existing objects, runs after the export and before the import, builds the mapping for key domains, has no export of its own and imports in simulation mode with one process per file. Only the mapping is created; nothing is written to the data tables. The linked objects must have been exported successfully. (M5, SNP3)"),
        bul("<b>Why use it:</b> adjust exported data to the target (mappings for domains with internal number ranges), improve parallelization of the main import, and find errors early. Typical flow: export linked objects, import forerunner in simulation, then import the normal objects which read the built mapping. (M5, SNP3)"),
        bul("<b>API_NUMBER_GET_NEXT</b> returns sy-subrc 0 when the value was calculated from the NRIV offset and 4 when it was generated with NUMBER_GET_NEXT; the strategy is returned too. After Update NRIV, the offsets are added to the old source numbers during import. (SNP3)"),
        bul("<b>Simulation mode</b> runs the import without writing to the database and can be repeated as often as needed. (M5)"), sp(6)]

story += [h2("14.5  Execution control")]
story += [FlowRow([
    ("PRE-RUNNER", ["Build global", "selections and", "own tables"], VIOLET),
    ("EXPORT", ["All objects", "from source"], CUSTC),
    ("EXPORT ADR", ["Addresses last,", "after collection"], AMBER),
    ("FORERUNNER", ["Build mapping", "tables"], TEAL),
    ("IMPORT ADR", ["Addresses", "imported first"], AMBER),
    ("IMPORT", ["All other", "objects"], GREEN_C),
], height=62), p("Figure 9 - Recommended block order when addresses are involved (M5, SNP2)", CAPN), sp(4)]
story += [tbl([
    ["Topic", "Fact", "Source"],
    ["Block types", "EXP, FOR, IMP, UPL and DEL. Import blocks can be created from export / upload blocks; deletion blocks from import blocks after successful execution. Only active objects can be assigned; tables can be removed from an object inside a block without changing the object.", "M5, SNP2"],
    ["Address object", "Address numbers are collected by global export rules for the domains ADRNR, AD_ADDRNUM, AD_PERSNUM, AD_SO_KEY and CADRNR. Export object ADR last and import it first.", "SNP2"],
    ["Dependencies", "Predecessors order blocks and objects; missing dependencies cause problems or terminations. Multiple predecessors are allowed.", "SNP2"],
    ["Process control", "Distributes processes by parameters such as table size. Max. processes above 0 on a block limits it and can prevent optimal control. For single executions 1 or 2 processes are recommended.", "M5, SNP2"],
    ["User priority", "MIN runs at the end (1/10 of processes); empty = calculated or inherited (1/10); MEDIUM = calculated x50 (1/10); HIGH = calculated x100 (1/5); MAX runs first (1/2). Settable at block, object and table level and changeable during the transformation.", "M5"],
    ["Table locks", "Lock set for cluster tables and tables with option Summarize (needed only for n:1 mapping); not set in DELETE mode. Switching the block mode adjusts locks on later tables. Disabling cluster locks saves runtime but is risky: with BSEG, several processes may write the same record into cluster RFBLG and cause a deadlock.", "SNP3"],
    ["Select export", "Right-click the import block to assign exports manually, also from other systems of the scenario; with several source systems this is mandatory. Cross-system assignment can make target data inconsistent; tables that were not exported cannot be assigned.", "SNP3, SNP2"],
    ["Multiple satellite systems", "Each system needs a unique alias (do not change it after global selections are maintained); a standard system is used where no system can be chosen (DDIC value help, syntax check). Global selection values are maintained per alias. Use environment variable te-source_system_alias in import coding for source-dependent mapping. Mappings added by API on one system are not transferred between systems. The system alias is set at block level.", "SNP3"],
    ["No shared file share", "Report /SNP/TE02_FILE_TRANSFER moves export files from source share to target share via RFC through the control system; files are transferred only once, otherwise import ends with files-not-found. Transfer all files of a scenario together.", "SNP3"],
    ["Export-based customizing analysis", "Analyzes customizing tables from an export. Green = filled identically, yellow = missing in source or target, red = filled with deviations in the target. Run it with all relevant objects and largely maintained organizational-unit selections, if needed in a separate scenario.", "SNP3"],
    ["RET scenario (save and restore)", "Source = target. Save: export complete tables without selections or rules (the files are the backup). Reset: deletion object plus import block in mode DELETE. Restore: import the saved tables in mode INSERT without rule base, then repeat the original import with the corrected rule base.", "SNP3"],
    ["Deletion", "Used for deletion projects (source and target at once) and for import correction. After deleting, clean up runs carefully because the transformation tree is the transformation history.", "M5"],
    ["Table statistics", "Refresh in Systems after export programs are generated, after export forerunners and for filled own tables; the daemon refreshes SNP tables automatically (default interval 30 min).", "SNP3"],
], [3.4 * cm, 11.8 * cm, 1.8 * cm], first_bold=True), sp(6)]

story += [h2("14.6  Validation and analysis tools")]
story += [tbl([
    ["Tool", "Fact", "Source"],
    ["Compare export to target", "After import, compares the export file with the target table; key fields must be identical. Fields changed by rules (mapped, incremented) are expected differences.", "SNP2"],
    ["Test units", "Stored reports and transactions called from the transformation in the target system.", "SNP2"],
    ["DCV prerequisites", "Migration finished and check tables filled. Fields can be given a status to exclude irrelevant checks; tables a context (priority, responsibility, owner). Two checks from different times can be compared, for example before / after conversion or source / target.", "SNP2"],
    ["Automated Testing", "Tests on application level (read mode, change mode) with random or selected data. With SAVE_DATA_FOR_AT the TC passes migrated data to /n/SNP/AT_mig_check on the target (requires the Migration CHECK add-on); the number tested can differ from the header table count.", "SNP2, SNP3"],
    ["Compare transformations", "Compare runs of one or several scenarios by table (records and runtime) or by object (runtime); one leading run is the basis; CSV up and download.", "M5, SNP2"],
    ["Transformation log", "/SNP/TCPROT; archived when tables are deleted or reset; Notes column for comments; progress shown as a percentage after each log refresh; duplicate keys shown during import or simulation, limited by LOG_MAX_ENTRIES.", "M5, SNP2"],
    ["Analyze DB indexes", "In Data Objects - Functions, shows the secondary indexes with the best coverage of the selection fields (60% in the example) to help choose selections.", "SNP3"],
    ["PO Query", "/n/SNP/CN_PO_QUERY queries cockpit persistent objects (classes /SNP/TE01_CL_SCENARIO, _MODULE, _OBJECT, _TABLE); can show change information and history. Start simple and refine; default maximum 500 records.", "SNP3"],
    ["Change history", "Technical log of changes in data objects, global and systems, with user and time. SAP menu - Information - Change history.", "M5"],
    ["Back in Mission Control", "Final training steps: copy template runs to executable runs, execute and verify runs, run the final syntax check, check that the runs exist in TC.", "M5"],
], [3.4 * cm, 11.8 * cm, 1.8 * cm], first_bold=True), sp(10)]


story += [callout("<b>Reference:</b> Kyano Mission Control Complete Reference Guide - chapters 1-7 Mission Control, 10 Transformation Cockpit, "
                  "11 Transformation Cockpit Training Guide (v19.03), 12 CrystalBridge Analysis (release 20.07); CrystalBridge Transformation User Guide 25.09 SP00; "
                  "Module 5 Transformation Advanced (v25.03); Transformation Cockpit SNP2 and Advanced SNP3 training decks (19.03 SP00). SNP Support: "
                  "support.snpgroup.com, support-tc@snpgroup.com. Document generated with IBM Bob.")]

# ==============================================================================
doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm,
                        topMargin=1.8 * cm, bottomMargin=2.0 * cm,
                        title="SNP CrystalBridge Data Migration - ECC to S/4HANA",
                        author="Sempra Migration Team")
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f"Created {OUT}")
