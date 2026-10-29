"""
Business Partner (BP) Migration — ECC to S/4HANA
Premium PDF with real-world examples
Run: python generate_bp_migration_pdf.py
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, HRFlowable, PageBreak, KeepTogether)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.platypus.flowables import Flowable
import datetime

OUT = "BP_Migration_ECC_to_S4HANA.pdf"
W, H = A4
CONTENT_W = W - 4*cm

# ── Colours ──────────────────────────────────────────────────────────────────
NAVY    = colors.HexColor("#0a1628")
BLUE    = colors.HexColor("#1e3a5f")
TEAL    = colors.HexColor("#0f766e")
SKY     = colors.HexColor("#38bdf8")
CUSTC   = colors.HexColor("#3b82f6")
VENDC   = colors.HexColor("#a855f7")
BPC     = colors.HexColor("#22c55e")
AMBER   = colors.HexColor("#f59e0b")
RED_C   = colors.HexColor("#ef4444")
GREEN_C = colors.HexColor("#22c55e")
LTGREY  = colors.HexColor("#f7f8fa")
BORDER  = colors.HexColor("#e5e7eb")
MUTED   = colors.HexColor("#57606a")
DARK    = colors.HexColor("#1f2328")
WHITE   = colors.white
ORANGE  = colors.HexColor("#ea580c")

def S(name, **kw): return ParagraphStyle(name, **kw)

COVER_TITLE = S("ct", fontSize=28, leading=36, textColor=WHITE,   fontName="Helvetica-Bold")
COVER_SUB   = S("cs", fontSize=12, leading=17, textColor=colors.HexColor("#94a3b8"), fontName="Helvetica")
H1s  = S("H1", fontSize=17, leading=22, textColor=NAVY,  fontName="Helvetica-Bold", spaceBefore=20, spaceAfter=5)
H2s  = S("H2", fontSize=12, leading=16, textColor=BLUE,  fontName="Helvetica-Bold", spaceBefore=12, spaceAfter=4)
H3s  = S("H3", fontSize=10, leading=14, textColor=DARK,  fontName="Helvetica-Bold", spaceBefore=8,  spaceAfter=3)
BODY = S("BD", fontSize=9,  leading=14, textColor=DARK,  fontName="Helvetica",      spaceAfter=4, alignment=TA_JUSTIFY)
BUL  = S("BU", fontSize=9,  leading=13, textColor=DARK,  fontName="Helvetica",      leftIndent=14, spaceAfter=3)
CODE = S("CO", fontSize=8,  leading=12, textColor=colors.HexColor("#1e40af"),
         fontName="Courier", backColor=colors.HexColor("#eff6ff"), borderPad=5, spaceAfter=5)
CAPN = S("CA", fontSize=7.5,leading=11, textColor=MUTED, fontName="Helvetica-Oblique", alignment=TA_CENTER, spaceAfter=6)
NOTE = S("NT", fontSize=8,  leading=12, textColor=colors.HexColor("#92400e"),
         fontName="Helvetica", backColor=colors.HexColor("#fffbeb"), borderPad=5, spaceAfter=5)

def p(t, st=None):  return Paragraph(t, st or BODY)
def h1(t):          return Paragraph(t, H1s)
def h2(t):          return Paragraph(t, H2s)
def h3(t):          return Paragraph(t, H3s)
def sp(n=8):        return Spacer(1, n)
def bul(t):         return Paragraph(f"<bullet>&bull;</bullet> {t}", BUL)
def hr(c=BORDER):   return HRFlowable(width="100%", thickness=0.5, color=c, spaceAfter=5, spaceBefore=5)
def code(t):        return Paragraph(t, CODE)
def note(t):        return Paragraph(f"&#x26A0; {t}", NOTE)

# ── Custom Flowables ──────────────────────────────────────────────────────────

class GradientBanner(Flowable):
    def __init__(self, title, subtitle="", c1=NAVY, c2=BLUE, height=50):
        self.title=title; self.subtitle=subtitle
        self.c1=c1; self.c2=c2; self.height=height
    def wrap(self, w, h): self.w=w; return (w, self.height+6)
    def draw(self):
        c=self.canv; w=self.w; h=self.height
        c.saveState()
        steps=30
        for i in range(steps):
            t=i/steps
            r=self.c1.red  +t*(self.c2.red  -self.c1.red)
            g=self.c1.green+t*(self.c2.green-self.c1.green)
            b=self.c1.blue +t*(self.c2.blue -self.c1.blue)
            c.setFillColorRGB(r,g,b)
            c.rect(w*i/steps,0,w*(i+1)/steps-w*i/steps,h,stroke=0,fill=1)
        c.setFillColor(SKY); c.rect(0,h-3,w,3,stroke=0,fill=1)
        c.setFillColor(WHITE); c.setFont("Helvetica-Bold",13)
        c.drawString(14,h-24,self.title)
        if self.subtitle:
            c.setFillColor(colors.HexColor("#94a3b8")); c.setFont("Helvetica",8.5)
            c.drawString(14,h-36,self.subtitle)
        c.restoreState()

class MergeArrow(Flowable):
    """Visual showing Customer + Vendor merging into one BP"""
    def __init__(self, width=CONTENT_W):
        self.w=width; self.h=110
    def wrap(self,w,h): return (self.w, self.h)
    def draw(self):
        c=self.canv; w=self.w; h=self.h
        bw=(w-80)/2
        # Customer box
        c.setFillColor(colors.HexColor("#dbeafe")); c.setStrokeColor(CUSTC); c.setLineWidth(1.5)
        c.roundRect(0,h-70,bw,60,5,stroke=1,fill=1)
        c.setFillColor(CUSTC); c.setFont("Helvetica-Bold",9)
        c.drawCentredString(bw/2,h-22,"ECC CUSTOMER")
        c.setFont("Helvetica",7.5); c.setFillColor(DARK)
        for i,(lbl) in enumerate(["KNA1 — General","KNB1 — Co.Code","KNVV — Sales"]):
            c.drawCentredString(bw/2,h-36-i*10,lbl)
        # Vendor box
        x2=w-bw
        c.setFillColor(colors.HexColor("#f3e8ff")); c.setStrokeColor(VENDC); c.setLineWidth(1.5)
        c.roundRect(x2,h-70,bw,60,5,stroke=1,fill=1)
        c.setFillColor(VENDC); c.setFont("Helvetica-Bold",9)
        c.drawCentredString(x2+bw/2,h-22,"ECC VENDOR")
        c.setFont("Helvetica",7.5); c.setFillColor(DARK)
        for i,(lbl) in enumerate(["LFA1 — General","LFB1 — Co.Code","LFM1 — Purch."]):
            c.drawCentredString(x2+bw/2,h-36-i*10,lbl)
        # Arrows
        mx=w/2; my=h-40
        c.setStrokeColor(AMBER); c.setLineWidth(2)
        c.line(bw,my,mx-30,my); c.line(x2,my,mx+30,my)
        c.setFillColor(AMBER)
        p1=c.beginPath(); p1.moveTo(mx-30,my+5); p1.lineTo(mx-30,my-5); p1.lineTo(mx-10,my); p1.close(); c.drawPath(p1,stroke=0,fill=1)
        p2=c.beginPath(); p2.moveTo(mx+30,my+5); p2.lineTo(mx+30,my-5); p2.lineTo(mx+10,my); p2.close(); c.drawPath(p2,stroke=0,fill=1)
        # BP box
        c.setFillColor(colors.HexColor("#dcfce7")); c.setStrokeColor(GREEN_C); c.setLineWidth(2)
        c.roundRect(mx-38,4,76,50,6,stroke=1,fill=1)
        c.setFillColor(GREEN_C); c.setFont("Helvetica-Bold",9)
        c.drawCentredString(mx,46,"S/4 BUSINESS")
        c.drawCentredString(mx,35,"PARTNER")
        c.setFont("Helvetica",7); c.setFillColor(DARK)
        c.drawCentredString(mx,22,"BUT000")
        c.drawCentredString(mx,12,"One record")

def tbl(data, col_widths=None, hdr_bg=BLUE, fs=8):
    t=Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,0), hdr_bg),
        ("TEXTCOLOR",    (0,0),(-1,0), WHITE),
        ("FONTNAME",     (0,0),(-1,0), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0),(-1,-1),fs),
        ("TOPPADDING",   (0,0),(-1,-1),5),
        ("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",  (0,0),(-1,-1),7),
        ("RIGHTPADDING", (0,0),(-1,-1),7),
        ("FONTNAME",     (0,1),(-1,-1),"Helvetica"),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE,LTGREY]),
        ("GRID",         (0,0),(-1,-1),0.3,BORDER),
        ("VALIGN",       (0,0),(-1,-1),"MIDDLE"),
    ])); return t

def callout(text, bg="#eff6ff", border="#3b82f6", tc="#1e40af"):
    st=S("cb",fontSize=8.5,leading=13,fontName="Helvetica",textColor=colors.HexColor(tc))
    t=Table([[Paragraph(text,st)]],colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),colors.HexColor(bg)),
        ("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8),
        ("LEFTPADDING",(0,0),(-1,-1),12),("RIGHTPADDING",(0,0),(-1,-1),12),
        ("BOX",(0,0),(-1,-1),1,colors.HexColor(border)),
    ])); return t

def sidebox(left_content, right_content, lw=None, rw=None):
    lw = lw or CONTENT_W*0.48
    rw = rw or CONTENT_W*0.48
    t=Table([[left_content, right_content]], colWidths=[lw, rw])
    t.setStyle(TableStyle([
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("LEFTPADDING",(0,0),(-1,-1),4),
        ("RIGHTPADDING",(0,0),(-1,-1),4),
        ("TOPPADDING",(0,0),(-1,-1),0),
        ("BOTTOMPADDING",(0,0),(-1,-1),0),
    ])); return t

def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(MUTED); canvas.setFont("Helvetica",7)
    canvas.drawString(2*cm,1.2*cm,"Business Partner Migration — ECC to S/4HANA  ·  With Examples")
    canvas.drawRightString(W-2*cm,1.2*cm,f"Page {doc.page}")
    canvas.setStrokeColor(BORDER); canvas.setLineWidth(0.3)
    canvas.line(2*cm,1.5*cm,W-2*cm,1.5*cm)
    canvas.restoreState()

# ═══════════════════════════════════════════════════════════════════════════════
story = []

# ── COVER ────────────────────────────────────────────────────────────────────
cov=Table([[
    [
        p("&#x1F4CB;", S("ci",fontSize=38,leading=46,textColor=WHITE,fontName="Helvetica-Bold")),
        sp(8),
        p("Business Partner Migration", COVER_TITLE),
        p("ECC Customer &amp; Vendor → S/4HANA Business Partner", COVER_SUB),
        sp(14),
        tbl([["CUSTOMER","VENDOR","BUSINESS PARTNER"]],
            col_widths=[4*cm,4*cm,4*cm],
            hdr_bg=NAVY, fs=9),
        sp(14),
        p("Complete Guide with Real-World Examples  ·  Configuration &amp; Data Migration",
          S("x",fontSize=9,textColor=colors.HexColor("#475569"),fontName="Helvetica")),
        p(f"Prepared: {datetime.date.today().strftime('%B %Y')}  ·  Sempra Migration Team",
          S("x2",fontSize=9,textColor=colors.HexColor("#475569"),fontName="Helvetica")),
    ]
]],colWidths=[CONTENT_W])
cov.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,-1),NAVY),
    ("TOPPADDING",(0,0),(-1,-1),48),("BOTTOMPADDING",(0,0),(-1,-1),48),
    ("LEFTPADDING",(0,0),(-1,-1),38),("RIGHTPADDING",(0,0),(-1,-1),38),
]))
story += [cov, PageBreak()]

# ── SECTION 1: CONCEPT ───────────────────────────────────────────────────────
story += [GradientBanner("01  The Core Concept — What Changes and Why",
          "From two separate objects in ECC to one unified Business Partner in S/4HANA",NAVY,BLUE),sp(8)]

story += [p("In <b>ECC</b>, a Customer and a Vendor are completely separate master data objects — "
            "even if they represent the same real-world company. You can have <b>Siemens AG</b> as "
            "Customer 100045 <i>and</i> Vendor 200078 with no link between them. "
            "In <b>S/4HANA</b>, both collapse into a <b>single Business Partner (BP)</b> record "
            "with different roles attached."), sp(8)]

story += [MergeArrow(width=CONTENT_W), sp(4)]
story += [p("Figure 1 — ECC Customer + Vendor merge into one S/4HANA Business Partner",CAPN),sp(8)]

story += [tbl([
    ["Object","ECC Table","ECC Transaction","S/4HANA Table","S/4 Transaction"],
    ["Customer — General",  "KNA1","XD01 / XD03","BUT000","BP"],
    ["Customer — Co. Code", "KNB1","FD01 / FD03","KNBK via CVI","BP"],
    ["Customer — Sales",    "KNVV","VA01 / XD01","KNVV (kept)","BP + VA"],
    ["Vendor — General",    "LFA1","XK01 / XK03","BUT000","BP"],
    ["Vendor — Co. Code",   "LFB1","FK01 / FK03","LFB1 via CVI","BP"],
    ["Vendor — Purchasing", "LFM1","ME11 / XK01","LFM1 (kept)","BP + ME"],
],col_widths=[3.2*cm,2.2*cm,2.8*cm,2.8*cm,2.5*cm],hdr_bg=NAVY),sp(6),PageBreak()]

# ── SECTION 2: BP ROLES ───────────────────────────────────────────────────────
story += [GradientBanner("02  BP Roles — The Key Building Block",
          "Every BP has roles. Roles define what the BP can do in each module.",BLUE,CUSTC),sp(8)]

story += [p("A <b>BP Role</b> is assigned to the Business Partner and activates the relevant "
            "master data screen/fields for that context. One BP can hold multiple roles simultaneously."),sp(6)]

story += [tbl([
    ["BP Role","Role Name","ECC Equivalent","Activated By","Example"],
    ["FLCU00","Customer (General)",  "KNA1","CVI sync from Customer","Siemens AG — name, address, tax"],
    ["FLCU01","Customer (Co.Code)",  "KNB1","CVI sync from Customer","Recon acct 140000, pay term Z030"],
    ["FLVN00","Vendor (General)",    "LFA1","CVI sync from Vendor",  "Siemens AG — same address"],
    ["FLVN01","Vendor (Co.Code)",    "LFB1","CVI sync from Vendor",  "Recon acct 210000, pay meth T"],
    ["BUP001","Business Partner (Gen)","—", "Default on BP creation","Every BP gets this at minimum"],
    ["CVI_DEBITOR","FI Customer",    "Customer link","CVI mapping",  "Links BP 9000001 ↔ Customer 100045"],
    ["CVI_KREDITOR","FI Vendor",     "Vendor link",  "CVI mapping",  "Links BP 9000001 ↔ Vendor 200078"],
],col_widths=[2.2*cm,3.2*cm,2.8*cm,3.0*cm,5.3*cm],hdr_bg=BLUE),sp(8)]

story += [callout(
    "<b>Real Example:</b>  Siemens AG exists as Customer 100045 (pays us) AND Vendor 200078 "
    "(we pay them). In S/4HANA, they become ONE Business Partner — BP# 9000001 — "
    "with roles FLCU00, FLCU01, FLVN00, FLVN01 all assigned. "
    "A/R posts against Customer 100045, A/P posts against Vendor 200078 — "
    "both linked to BP 9000001 via CVI.",
    bg="#f0fdf4",border="#22c55e",tc="#15803d"),sp(6),PageBreak()]

# ── SECTION 3: CUSTOMER LEVELS ───────────────────────────────────────────────
story += [GradientBanner("03  Customer Migration — Level by Level with Examples",
          "Every data level, table, field and real example for Customer master",
          CUSTC,colors.HexColor("#1d4ed8")),sp(8)]

story += [h2("Level 1 — General Data (Client-Wide)")]
story += [p("General data exists <b>once per customer</b> — it is the same across all company codes "
            "and sales areas. This maps to <b>BUT000</b> in S/4HANA."),sp(4)]
story += [tbl([
    ["ECC Field","ECC Table","S/4 Table","Real Example Value","Notes"],
    ["Name 1",         "KNA1-NAME1","BUT000-NAME_ORG1","Siemens AG",          "Legal name"],
    ["Country",        "KNA1-LAND1","BUT020-COUNTRY",  "DE",                  "ISO country code"],
    ["Tax Number 1",   "KNA1-STCD1","BUT000-STCD1",    "DE123456789",         "VAT registration"],
    ["Language",       "KNA1-SPRAS","BUT000-LANGU",    "EN",                  "Correspondence lang"],
    ["Search Term",    "KNA1-SORTL","BUT000-BU_SORT1", "SIEMENS",             "Used in matchcode"],
    ["Account Group",  "KNA1-KTOKD","BP Grouping",     "CUST (External)",     "Drives number range"],
    ["Cust. Classif.", "KNA1-KUKLA","BUT000 custom",   "A (Top Customer)",    "Optional"],
],col_widths=[2.8*cm,2.5*cm,2.8*cm,3.5*cm,4.2*cm],hdr_bg=CUSTC),sp(6)]

story += [h2("Level 2 — Company Code Data")]
story += [p("Company code data is <b>per company code</b> — one record per customer per company code. "
            "Maps to role <b>FLCU01</b> in S/4HANA."),sp(4)]
story += [tbl([
    ["ECC Field","ECC Table","S/4 Equivalent","Real Example Value","Notes"],
    ["Reconciliation Acct","KNB1-AKONT","KNBK via CVI",   "140000",        "A/R recon account in G/L"],
    ["Payment Terms",      "KNB1-ZTERM","KNB1 retained",  "Z030 (30 days)","Due date calculation"],
    ["Dunning Procedure",  "KNB1-MAHNA","KNB1 retained",  "Z001",          "Dunning letters"],
    ["Payment Method",     "KNB1-ZWELS","KNB1 retained",  "T (Transfer)",  "Outgoing payment"],
    ["Tolerance Group",    "KNB1-TOGRU","KNB1 retained",  "GRP1",          "Posting tolerance"],
    ["Credit Limit",       "KNB1-KLIMK","KNB1 retained",  "500,000 USD",   "Credit management"],
    ["Sort Key",           "KNB1-ZUAWA","KNB1 retained",  "001 (Doc date)","Line item sort"],
],col_widths=[3.2*cm,2.5*cm,2.8*cm,3.2*cm,4.5*cm],hdr_bg=CUSTC),sp(6)]

story += [callout(
    "<b>Example — Siemens AG Co.Code 1000:</b>  KNB1 record has AKONT=140000 (A/R reconciliation), "
    "ZTERM=Z030 (net 30 days), MAHNA=Z001 (standard dunning), KLIMK=500000 USD credit limit. "
    "After migration, BP 9000001 with role FLCU01 in company code 1000 holds identical values.",
    bg="#dbeafe",border="#3b82f6",tc="#1e40af"),sp(4)]

story += [h2("Level 3 — Sales Area Data")]
story += [p("Sales area data is <b>per Sales Org / Distribution Channel / Division</b> combination. "
            "Table KNVV is retained in S/4HANA with minimal changes."),sp(4)]
story += [tbl([
    ["ECC Field","Table","Real Example","Notes"],
    ["Sales Org",        "KNVV-VKORG","1000 (US West)", "Organisational unit for sales"],
    ["Dist. Channel",    "KNVV-VTWEG","10 (Direct)",    "How goods reach customer"],
    ["Division",         "KNVV-SPART","01 (Pumps)",     "Product line grouping"],
    ["Customer Group",   "KNVV-KDGRP","01 (Industrial)","Pricing / statistics group"],
    ["Price Group",      "KNVV-KONDA","B2 (Large)",     "Condition master access"],
    ["Pricing Procedure","KNVV-KALKS","RVAA01",         "Determines condition types used"],
    ["Shipping Cond.",   "KNVV-VSBED","02 (Standard)",  "Delivery scheduling"],
    ["Incoterms",        "KNVV-INCO1","CIF",            "Risk / cost transfer point"],
],col_widths=[3.0*cm,2.8*cm,3.2*cm,6.5*cm],hdr_bg=CUSTC),sp(6)]

story += [h2("Level 4 — Partner Functions (KNVP)")]
story += [tbl([
    ["Partner Func.","Meaning","ECC Example","S/4 Behaviour"],
    ["SP — Sold-To",  "Who places the order",         "Siemens AG  100045","Retained in KNVP"],
    ["SH — Ship-To",  "Where goods are delivered",    "Siemens Plant Munich 100046","Retained"],
    ["BP — Bill-To",  "Who receives the invoice",     "Siemens Finance 100047","Retained"],
    ["PY — Payer",    "Who pays the invoice",         "Siemens Treasury 100048","Retained"],
],col_widths=[2.8*cm,3.5*cm,4.2*cm,5.0*cm],hdr_bg=CUSTC),sp(4),PageBreak()]

# ── SECTION 4: VENDOR LEVELS ─────────────────────────────────────────────────
story += [GradientBanner("04  Vendor Migration — Level by Level with Examples",
          "Every data level, table, field and real example for Vendor master",
          VENDC,colors.HexColor("#7c3aed")),sp(8)]

story += [h2("Level 1 — General Data (LFA1 → BUT000)")]
story += [tbl([
    ["ECC Field","ECC Table","S/4 Table","Real Example Value","Notes"],
    ["Name 1",       "LFA1-NAME1","BUT000-NAME_ORG1","SAP SE",             "Legal vendor name"],
    ["Country",      "LFA1-LAND1","BUT020-COUNTRY",  "DE",                 "ISO country"],
    ["Tax Number 1", "LFA1-STCD1","BUT000-STCD1",    "DE114103379",        "VAT number"],
    ["Language",     "LFA1-SPRAS","BUT000-LANGU",    "EN",                 "Correspondence"],
    ["Account Group","LFA1-KTOKK","BP Grouping",     "VEND",               "Number range driver"],
    ["GR-Based IV",  "LFA1-XGRED","LFB1 retained",   "X (Active)",         "3-way match required"],
    ["One-Time",     "LFA1-XCPDK","BUT000 flag",      "Blank (regular)",    "CPD = one-time vendor"],
],col_widths=[2.8*cm,2.5*cm,2.8*cm,3.5*cm,4.2*cm],hdr_bg=VENDC),sp(6)]

story += [h2("Level 2 — Company Code Data (LFB1 → FLVN01)")]
story += [tbl([
    ["ECC Field","ECC Table","S/4 Equivalent","Real Example","Notes"],
    ["Reconciliation Acct","LFB1-AKONT","LFB1 retained","210000",          "A/P recon acct in G/L"],
    ["Payment Terms",      "LFB1-ZTERM","LFB1 retained","Z014 (14 days)",  "Early pay discount"],
    ["Payment Method",     "LFB1-ZWELS","LFB1 retained","T (Bank transfer)","A/P payment run"],
    ["House Bank",         "LFB1-HBKID","LFB1 retained","MAIN",            "Bank for payments"],
    ["Chk Double Invoice", "LFB1-XDEZV","LFB1 retained","X (Active)",      "Duplicate check"],
    ["Withholding Tax",    "LFBW-WITHT","LFBW retained","W1 (1099-MISC)",  "US WHT type"],
    ["Tolerance Group",    "LFB1-TOGRU","LFB1 retained","GRP2",            "Posting tolerance"],
],col_widths=[3.2*cm,2.5*cm,2.8*cm,3.0*cm,4.8*cm],hdr_bg=VENDC),sp(4)]

story += [callout(
    "<b>Example — SAP SE Vendor Co.Code 1000:</b>  LFB1 has AKONT=210000 (A/P reconciliation), "
    "ZTERM=Z014 (14 days 2% discount), ZWELS=T (bank transfer), HBKID=MAIN. "
    "After migration → BP 9000002 role FLVN01 in company code 1000. "
    "Posting: DR Expense 400000 / CR Vendor 200 (posting key) → hits A/P recon 210000.",
    bg="#f3e8ff",border="#a855f7",tc="#6b21a8"),sp(6)]

story += [h2("Level 3 — Purchasing Org Data (LFM1)")]
story += [tbl([
    ["ECC Field","Table","Real Example","Notes"],
    ["Purchasing Org",   "LFM1-EKORG","1000 (Global Purch)","Org unit responsible for POs"],
    ["Order Currency",   "LFM1-WAERS","USD",               "Currency on POs"],
    ["Incoterms",        "LFM1-INCO1","FOB",               "Delivery responsibility"],
    ["Min. Order Value", "LFM1-MINBW","5,000 USD",         "Below this: no PO raised"],
    ["Payment Terms",    "LFM1-ZTERM","Z014",              "Can differ from FI terms"],
    ["Confirmation Ctrl","LFM1-BSTAE","0001 (Order Ack.)", "Vendor must confirm PO"],
    ["GR-Based IV",      "LFM1-XGRED","X",                 "3-way match on invoice"],
],col_widths=[3.0*cm,2.8*cm,3.2*cm,6.5*cm],hdr_bg=VENDC),sp(6)]

story += [h2("Level 4 — Bank Data (LFBK / KNBK → TIBAN)")]
story += [tbl([
    ["ECC Table","ECC Fields","S/4 Table","Real Example","Notes"],
    ["LFBK","BANKS, BANKL, BANKN","TIBAN + BNKA","DE89 3704 0044 0532 0130 00","IBAN mandatory in S/4"],
    ["KNBK","BANKS, BANKL, BANKN","TIBAN + BNKA","GB29 NWBK 6016 1331 9268 19","Customer bank for DD"],
],col_widths=[2.0*cm,3.5*cm,2.5*cm,4.5*cm,4.0*cm],hdr_bg=VENDC),sp(4)]
story += [note("Migration Alert: ECC stores bank data as Bank Key + Account Number. "
               "S/4HANA requires IBAN format. All bank records must be converted to IBAN "
               "before or during migration. Use program RFFMIBAN or LTMC migration object."),
          sp(4),PageBreak()]

# ── SECTION 5: CVI CONFIGURATION ─────────────────────────────────────────────
story += [GradientBanner("05  CVI Configuration — The Critical Link",
          "Customer-Vendor Integration setup in SPRO — step by step with settings",
          TEAL,colors.HexColor("#065f46")),sp(8)]

story += [p("CVI (Customer-Vendor Integration) is the <b>configuration backbone</b> of BP migration. "
            "It defines how ECC Customer/Vendor numbers map to BP numbers, which fields synchronise, "
            "and which BP roles are assigned automatically."),sp(6)]

story += [h2("SPRO Navigation Path")]
story += [code("SPRO → Cross-Application Components\n"
               "     → Master Data Synchronization\n"
               "       → Customer/Vendor Integration\n"
               "         → Business Partner Settings\n"
               "           → Settings for Customer Integration\n"
               "           → Settings for Vendor Integration")]

story += [h2("Step 1 — Define BP Role for Customer / Vendor")]
story += [tbl([
    ["Config Object","Value","Menu Path","Purpose"],
    ["BP Role Category for Cust.","FLCU","Assign roles to BP Cat.","Activates customer fields on BP screen"],
    ["BP Role Category for Vend.","FLVN","Assign roles to BP Cat.","Activates vendor fields on BP screen"],
    ["CVI Customer Role",  "CVI_DEBITOR", "Role assignment","Links FI customer posting to BP"],
    ["CVI Vendor Role",    "CVI_KREDITOR","Role assignment","Links FI vendor posting to BP"],
],col_widths=[4.0*cm,2.8*cm,4.0*cm,5.7*cm],hdr_bg=TEAL),sp(6)]

story += [h2("Step 2 — Number Range Synchronisation")]
story += [p("This is the most <b>critical configuration step</b>. ECC Customer and Vendor number ranges "
            "must be mapped to BP number ranges. Three modes are available:"),sp(4)]
story += [tbl([
    ["Mode","When to Use","Example Setup","Risk"],
    ["External = Internal\n(1:1 sync)","Customer# = BP#\nVendor# = BP#","Cust 100045 → BP 100045\nVend 200078 → BP 200078",
     "Overlap if cust & vendor share same number range"],
    ["Separate BP range\n(new numbers)","Cust# ≠ BP# — new BP#\nassigned from separate range",
     "Cust 100045 → BP 9100045\nVend 200078 → BP 9200078","Requires number mapping table"],
    ["Merge same company\n(manual)","Same company is both\ncustomer AND vendor",
     "Cust 100045 + Vend 200078\n→ Single BP 9000001","Complex — needs pre-analysis"],
],col_widths=[3.2*cm,3.5*cm,4.0*cm,4.8*cm],hdr_bg=TEAL),sp(4)]

story += [callout(
    "<b>Sempra Example:</b>  Southern California Gas has Customer range 1000000–1999999 and "
    "Vendor range 2000000–2999999 with NO overlap. Config: BP group CUST maps to external "
    "number range 1000000–1999999 (Customer# = BP#). BP group VEND maps to external range "
    "2000000–2999999 (Vendor# = BP#). Result: zero renumbering required.",
    bg="#f0fdf4",border="#22c55e",tc="#15803d"),sp(6)]

story += [h2("Step 3 — Field Mapping (KNA1/LFA1 → BUT000)")]
story += [tbl([
    ["Source Field","Source Table","Target Field","Target Table","Sync Direction"],
    ["NAME1",  "KNA1","NAME_ORG1","BUT000","Cust → BP  (and BP → Cust)"],
    ["LAND1",  "KNA1","COUNTRY",  "BUT020","Bidirectional"],
    ["STCD1",  "KNA1","STCD1",    "BUT000","Bidirectional"],
    ["SPRAS",  "KNA1","LANGU",    "BUT000","Bidirectional"],
    ["NAME1",  "LFA1","NAME_ORG1","BUT000","Vend → BP (shared with Cust)"],
    ["STCD1",  "LFA1","STCD1",    "BUT000","Bidirectional — must match Cust"],
],col_widths=[2.2*cm,2.5*cm,2.8*cm,2.5*cm,5.5*cm],hdr_bg=TEAL),sp(4),PageBreak()]

# ── SECTION 6: MIGRATION SCENARIOS ───────────────────────────────────────────
story += [GradientBanner("06  Real Migration Scenarios — End to End",
          "Four concrete examples: simple, dual-role, one-time, and blocked",
          colors.HexColor("#7c3aed"),colors.HexColor("#4f46e5")),sp(8)]

story += [h2("Scenario A — Simple Customer (Customer only, no vendor)")]
story += [tbl([
    ["Step","Action","ECC Data","S/4 Result"],
    ["1","Extract KNA1","NAME1=Pacific Gas\nKTOKD=KUNA\nLAND1=US","Source for BP general data"],
    ["2","Extract KNB1","AKONT=140000\nZTERM=Z030\nKLIMK=1,000,000","Source for FLCU01 role"],
    ["3","Extract KNVV","VKORG=3000\nVTWEG=10\nINCO1=CIF","Loaded to KNVV in S/4 unchanged"],
    ["4","Create BP","BP#=1001234 (=Cust#)","BUT000 created, FLCU00 + FLCU01 assigned"],
    ["5","Validate","CVI_CUST_LINK","Cust 1001234 ↔ BP 1001234 link confirmed"],
],col_widths=[0.8*cm,3.5*cm,4.5*cm,5.7*cm],hdr_bg=colors.HexColor("#7c3aed")),sp(6)]

story += [h2("Scenario B — Dual Role (Same company is Customer AND Vendor)")]
story += [p("<b>Challenge:</b> Siemens AG = Customer 100045 AND Vendor 200078. "
            "Must become ONE BP with both roles."),sp(4)]
story += [tbl([
    ["Step","Action","Data / Config","Result"],
    ["1","Identify duplicates","Match on TAX# (STCD1=DE123456789)\nor Name+Country","Found: Cust 100045 = Vend 200078"],
    ["2","Choose master BP#","Policy: use Customer# as BP#","BP# = 100045"],
    ["3","Create BP","Name, address from KNA1\n(or LFA1 if richer)","BUT000 BP 100045 created"],
    ["4","Assign FLCU roles","From KNA1 + KNB1 data","FLCU00 + FLCU01 assigned"],
    ["5","Assign FLVN roles","From LFA1 + LFB1 data","FLVN00 + FLVN01 assigned"],
    ["6","Link old Vendor#","CVI_VENDOR_LINK table","Vend 200078 → BP 100045"],
    ["7","Redirect postings","A/P still uses Vend 200078 key","S/4 routes via BP 100045"],
],col_widths=[0.8*cm,3.0*cm,4.5*cm,5.2*cm],hdr_bg=colors.HexColor("#7c3aed")),sp(4)]

story += [callout(
    "<b>Key Point:</b>  After migration, a single invoice from Siemens AG for $50,000 and a "
    "sales order TO Siemens AG for $30,000 are both visible on BP 100045. "
    "Treasury can see the net exposure ($20,000 net payable) in one place — impossible in ECC.",
    bg="#f3e8ff",border="#a855f7",tc="#6b21a8"),sp(6)]

story += [h2("Scenario C — One-Time / CPD Customer")]
story += [tbl([
    ["Field","ECC (KNA1)","S/4 (BUT000)","Example Value"],
    ["Account Group","CPDA (one-time)","BP Group = CPD","CPDA"],
    ["One-Time Flag","XCPDK = X","CPD indicator on BP","X = one-time"],
    ["Name","Entered at posting","Entered at posting","John Smith (at invoice)"],
    ["Address","Entered at posting","Entered at posting","123 Main St, LA CA"],
    ["BP#","Created once","Single BP for all CPD","CP000001"],
],col_widths=[2.8*cm,3.2*cm,3.2*cm,6.3*cm],hdr_bg=ORANGE),sp(4)]
story += [note("All one-time customers share ONE BP record (CP000001). "
               "The actual name/address is entered at the time of document posting — not on the master. "
               "Same behaviour as ECC — no functional change."),sp(6)]

story += [h2("Scenario D — Blocked Customer / Vendor")]
story += [tbl([
    ["Block Type","ECC Field/Table","S/4 Equivalent","Migration Action"],
    ["All company codes block","KNB1-SPERR = X","BP Central Block","Migrate block indicator"],
    ["Posting block (A/R)",    "KNB1-ZAHLS = X","BP Role FLCU01 block","Retain on KNB1"],
    ["Sales block",            "KNVV-AUFSD = Z1","KNVV retained","No change needed"],
    ["Vendor payment block",   "LFB1-ZAHLS = B","LFB1 retained","Retain on LFB1"],
    ["Purchasing block",       "LFM1-SPERM = X","LFM1 retained","Retain on LFM1"],
    ["Deletion flag",          "KNA1-LOEVM = X","BUT000-BU_DCIND","Map to BP deletion indicator"],
],col_widths=[3.5*cm,3.2*cm,3.2*cm,5.6*cm],hdr_bg=ORANGE),sp(4),PageBreak()]

# ── SECTION 7: MIGRATION TOOLS ────────────────────────────────────────────────
story += [GradientBanner("07  Migration Tools — Which One for What",
          "LTMC, LSMW, BAPI, SUM — when to use each tool",
          colors.HexColor("#0369a1"),colors.HexColor("#0284c7")),sp(8)]

story += [tbl([
    ["Tool","Full Name","Best For","Example Use Case"],
    ["LTMC","SAP Migration Cockpit","S/4 greenfield or\nselective migration","Load 50,000 new BPs\nfrom CSV template"],
    ["LSMW","Legacy System Mig. Workbench","ECC → ECC or\npre-S/4 migrations","Migrate vendor bank\ndata to new format"],
    ["BAPI","BAPI_BUPA_CREATE etc.","Custom code / large\nvolume automation","Python/ABAP script\nfor 500k+ BPs"],
    ["SUM + CVI","Software Update Manager","In-place ECC→S/4\nsystem conversion","Existing production\nsystem upgrade"],
    ["MDMGX","MDG for BP","Master data governance\npost-migration","Ongoing BP quality\nworkflow approvals"],
],col_widths=[1.8*cm,3.8*cm,3.5*cm,6.4*cm],hdr_bg=colors.HexColor("#0369a1")),sp(6)]

story += [h2("LTMC Migration Objects for BP")]
story += [tbl([
    ["LTMC Object","Migrates","Key Fields","Notes"],
    ["Business Partner","BP general data","NAME_ORG1, COUNTRY, STCD1","Must run before roles"],
    ["BP — Customer CoCode","FLCU01 role data","AKONT, ZTERM, KLIMK","Needs BP + CoCd to exist"],
    ["BP — Vendor CoCode",  "FLVN01 role data","AKONT, ZTERM, ZWELS","Needs BP + CoCd to exist"],
    ["BP — Customer Sales", "KNVV sales data", "VKORG, VTWEG, INCO1","Needs sales area config"],
    ["BP — Vendor Purch.",  "LFM1 purch. data","EKORG, WAERS, ZTERM","Needs purch org config"],
    ["BP Bank Details",     "TIBAN bank data", "IBAN, BANKS, BANKL",  "IBAN required — not BANKN"],
],col_widths=[3.5*cm,2.8*cm,3.5*cm,5.7*cm],hdr_bg=colors.HexColor("#0369a1")),sp(6),PageBreak()]

# ── SECTION 8: VALIDATION & ERRORS ───────────────────────────────────────────
story += [GradientBanner("08  Validation, Common Errors & Fixes",
          "Post-migration checks, error codes, and resolution steps",
          RED_C,ORANGE),sp(8)]

story += [h2("Post-Migration Validation Transactions")]
story += [tbl([
    ["Transaction","Purpose","What to Check"],
    ["BP",          "Display Business Partner","Confirm roles FLCU00/01, FLVN00/01 all visible"],
    ["BUPT",        "BP Consistency Check","Run for all migrated BPs — must show 0 errors"],
    ["CVI_CUST_LINK","Customer-BP Link Report","Every Customer# has a linked BP#"],
    ["CVI_VEND_LINK","Vendor-BP Link Report",  "Every Vendor# has a linked BP#"],
    ["FD03",        "Customer Display (still works)","Should open BP screen via CVI redirect"],
    ["XK03",        "Vendor Display (still works)", "Should open BP screen via CVI redirect"],
    ["MASS_BP",     "Mass BP Change",          "Post-migration mass updates if needed"],
],col_widths=[2.8*cm,4.0*cm,8.7*cm],hdr_bg=RED_C),sp(6)]

story += [h2("Common Migration Errors and Fixes")]
story += [tbl([
    ["Error Code / Message","Root Cause","Fix"],
    ["BP does not exist for\nCustomer 100045","CVI sync not run or\nnumber range gap","Run FLCU00/01 CVI sync;\ncheck BP number range config"],
    ["IBAN invalid for\nbank account","ECC BANKN not converted\nto IBAN","Run RFFMIBAN to convert;\nmanually correct outliers"],
    ["Duplicate BP name\nwarning","Same company migrated\ntwice (cust + vend)","Merge records; assign\nboth roles to one BP"],
    ["Tax number already\nexists on BP 9000045","Shared VAT# between\ntwo customers","Investigate — may be\nlegitimate parent/subsidiary"],
    ["Role FLCU01 missing\nin company code 2000","KNB1 record existed\nbut not migrated","Re-run LTMC object\n'BP Customer CoCode'"],
    ["Address data mismatch\nKNA1 vs BUT020","Field mapping config\nmissing for street/city","Check CVI field mapping\nfor STRAS, ORT01 fields"],
],col_widths=[4.0*cm,3.8*cm,7.7*cm],hdr_bg=RED_C),sp(6)]

story += [callout(
    "<b>Golden Rule for Validation:</b>  Run transaction BUPT (BP Consistency Check) for ALL "
    "migrated business partners before go-live. It checks role completeness, number range "
    "consistency, address data, bank data, and CVI links in one shot. Target = zero errors. "
    "Any error here will cause posting failures in FI/SD/MM on day one.",
    bg="#fff1f2",border="#ef4444",tc="#b91c1c"),sp(6),PageBreak()]

# ── SECTION 9: QUICK REFERENCE ───────────────────────────────────────────────
story += [GradientBanner("09  Quick Reference Card",
          "Tables, transactions, roles and number ranges at a glance",
          NAVY,BLUE),sp(8)]

story += [h2("Key Tables — ECC vs S/4HANA")]
story += [tbl([
    ["Area","ECC Table","S/4 Table","Retained?"],
    ["BP General",         "KNA1 / LFA1","BUT000","Replaced by BUT000"],
    ["BP Address",         "KNA1 (inline)","BUT020","New structure"],
    ["BP Bank",            "KNBK / LFBK", "TIBAN","IBAN replaces BANKN"],
    ["Cust Co.Code",       "KNB1",        "KNB1 (via CVI)","Retained + CVI link"],
    ["Cust Sales Area",    "KNVV",        "KNVV","Fully retained"],
    ["Cust Partner Func.", "KNVP",        "KNVP","Fully retained"],
    ["Vend Co.Code",       "LFB1",        "LFB1 (via CVI)","Retained + CVI link"],
    ["Vend Purch Org",     "LFM1",        "LFM1","Fully retained"],
    ["Vend WHT",           "LFBW",        "LFBW","Fully retained"],
    ["Contact Person",     "KNVK",        "BUT051/BUT052","New BP contact structure"],
    ["CVI Link (Cust)",    "—",           "CVI_CUST_LINK","New in S/4"],
    ["CVI Link (Vend)",    "—",           "CVI_VEND_LINK","New in S/4"],
],col_widths=[3.5*cm,3.2*cm,3.2*cm,5.6*cm],hdr_bg=NAVY),sp(6)]

story += [h2("Transaction Cross-Reference")]
story += [tbl([
    ["Action","ECC T-Code","S/4 T-Code","Notes"],
    ["Create Customer",   "XD01","BP (role FLCU00+01)","BP is the master screen now"],
    ["Create Vendor",     "XK01","BP (role FLVN00+01)","XK01 still works via CVI"],
    ["Mass Customer Chg", "XD99","MASS_BP","New transaction for mass BP"],
    ["Customer Credit",   "FD32","UKM_BP","New credit mgmt in S/4"],
    ["Vendor Evaluation", "ME61","ME61 (unchanged)","Purch still uses same screen"],
    ["BP Consistency",    "—",   "BUPT","Critical — run post-migration"],
    ["Sync Customer→BP",  "—",   "CVI_CUST_CENTRAL","Force resync if drift"],
    ["Sync Vendor→BP",    "—",   "CVI_VEND_CENTRAL","Force resync if drift"],
],col_widths=[3.5*cm,2.5*cm,3.0*cm,6.5*cm],hdr_bg=NAVY),sp(8)]

# ── SECTION 10: COMPLETE SPRO CONFIG TABLE ───────────────────────────────────
story += [PageBreak()]
story += [GradientBanner("10  Complete SPRO Configuration — All Nodes",
          "Every config step needed for BP migration — path, transaction, purpose",
          NAVY, TEAL), sp(8)]

story += [p("The table below covers <b>every SPRO node</b> that must be configured for a complete "
            "BP migration. Work through them top to bottom — each depends on the one above."), sp(6)]

story += [tbl([
    ["#","SPRO Node / Config Object","T-Code","Purpose / What to Set"],
    ["1",  "Define BP Number Ranges",
           "BUCF / SNRO",
           "Create internal + external number ranges for BP.\nExample: external 1000000–1999999 for customers, 2000000–2999999 for vendors"],
    ["2",  "Define BP Groupings",
           "BUCF",
           "Create groupings CUST, VEND, CPD, INTE.\nAssign number range to each grouping"],
    ["3",  "Define BP Roles",
           "BUCF",
           "Roles FLCU00, FLCU01, FLVN00, FLVN01 must exist.\nCheck standard roles delivered by SAP"],
    ["4",  "Assign BP Role to BP Role Category",
           "BUCF → BP Role Category",
           "FLCU = Customer category, FLVN = Vendor category.\nLinks role to screen layout"],
    ["5",  "Define BP Views (Screen Layout)",
           "BUCF → Field Grouping",
           "Set field status (required/optional/hidden) per role.\nExample: STCD1 = required for FLCU00"],
    ["6",  "Customer Account Groups",
           "OBD2",
           "Define KUNA (standard), CPD (one-time), KUNA_INT (internal).\nSet number range + field status per group"],
    ["7",  "Vendor Account Groups",
           "OBD3",
           "Define 0001 (domestic), 0002 (foreign), LIEF (standard vendor).\nSet number range + field status"],
    ["8",  "CVI — Assign Customer Roles",
           "SPRO → CVI → Customer Integration → Assign Roles",
           "Map account group to BP role.\nExample: KUNA → FLCU00 + FLCU01"],
    ["9",  "CVI — Assign Vendor Roles",
           "SPRO → CVI → Vendor Integration → Assign Roles",
           "Map account group to BP role.\nExample: 0001 → FLVN00 + FLVN01"],
    ["10", "CVI — Number Range Mapping",
           "SPRO → CVI → Number Range",
           "Sync customer number range to BP number range.\nChoose: external (keep cust#) or internal (new BP#)"],
    ["11", "CVI — Field Mapping Customer",
           "SPRO → CVI → Field Mapping → Customer",
           "Map KNA1 fields to BUT000.\nCritical: NAME1→NAME_ORG1, LAND1→COUNTRY, STCD1→STCD1"],
    ["12", "CVI — Field Mapping Vendor",
           "SPRO → CVI → Field Mapping → Vendor",
           "Map LFA1 fields to BUT000.\nSame fields as customer — conflicts resolved by priority rules"],
    ["13", "CVI — Activate Sync",
           "SPRO → CVI → Activate",
           "Switch on bidirectional sync.\nECC→BP and BP→ECC both active after go-live"],
    ["14", "Partner Determination (SD)",
           "SPRO → SD → Basic Functions → Partner Determination",
           "Ensure SP/SH/BP/PY partner functions work with BP.\nCheck procedure assigned to customer account group"],
    ["15", "Credit Management",
           "UKM_BP / SPRO → FSCM",
           "S/4 uses new Credit Management (FSCM).\nMigrate credit limits from FD32 → UKM_BP per BP"],
    ["16", "Output Tax / Tax Classification",
           "SPRO → SD → Basic Functions → Taxes",
           "Tax classification migrated from KNVI.\nMap ECC tax category to S/4 condition record"],
    ["17", "Dunning Configuration",
           "FBMP / SPRO → FI → AR → Dunning",
           "Dunning procedures same — ensure KNB1-MAHNA migrated correctly.\nTest dunning run on pilot BPs"],
    ["18", "Payment Program Config",
           "FBZP",
           "Vendor payment methods (LFB1-ZWELS) must match FBZP config.\nVerify T=transfer, C=cheque, B=bill active"],
    ["19", "GR-Based Invoice Verification",
           "SPRO → MM → LIV",
           "LFM1-XGRED flag must be migrated.\nControls 3-way match (PO + GR + Invoice)"],
    ["20", "Withholding Tax Config",
           "SPRO → FI → WHT",
           "LFBW (vendor WHT) and KNBK (customer WHT) data migrated.\nVerify WHT types and codes match S/4 config"],
], col_widths=[0.6*cm, 4.8*cm, 3.2*cm, 7.3*cm], hdr_bg=NAVY), sp(6)]

story += [callout(
    "<b>Config Sequence Rule:</b>  Always configure in order: Number Ranges → BP Groupings → "
    "BP Roles → Account Groups → CVI Mapping → Activate Sync. "
    "If you activate CVI before number ranges are aligned, the sync will create BPs with "
    "wrong numbers and you will need a full data cleanup.",
    bg="#fffbeb", border="#f59e0b", tc="#92400e"), sp(4), PageBreak()]

# ── SECTION 11: ALL S/4 BP TABLES ─────────────────────────────────────────────
story += [GradientBanner("11  All S/4HANA Business Partner Database Tables",
          "Complete table reference — what every table stores and how it links",
          BLUE, colors.HexColor("#0369a1")), sp(8)]

story += [h2("Core BP Tables (BUT*)")]
story += [tbl([
    ["Table","Description","Key Fields","Links To"],
    ["BUT000","BP Master (General)","PARTNER, BU_TYPE, NAME_ORG1, STCD1, LANGU","Central BP record — all roles point here"],
    ["BUT020","BP Address Assignment","PARTNER, ADDRNUMBER, DATE_FROM","ADRC for address detail"],
    ["BUT021_FS","BP Address Usage","PARTNER, ADDRESS_TYPE","Billing/shipping address types"],
    ["BUT050","BP Relationship","PARTNER1, PARTNER2, RELTYP","Relationships between BPs"],
    ["BUT051","BP Contact Person","PARTNER, CONTACT_PERSON","Links BP to contact person BP"],
    ["BUT052","BP Contact Person Address","PARTNER, CONTACT_PERSON","Address for contact persons"],
    ["BUT100","BP Role Assignment","PARTNER, RL_TYPE","Which roles each BP has"],
    ["BUT_HIER","BP Hierarchy",    "NODE_KEY, PARENT_NODE","Corporate hierarchy structure"],
    ["ADRC",   "Central Address",  "ADDRNUMBER, NAME1, STREET, CITY1","Shared across all address objects"],
    ["ADR6",   "Email Address",    "ADDRNUMBER, PERSNUMBER, SMTP_ADDR","Email per BP address"],
    ["TIBAN",  "IBAN Bank Details","IBAN, BANKS, BANKL, BANKN","Replaces KNBK/LFBK in S/4"],
], col_widths=[2.5*cm, 3.8*cm, 4.2*cm, 5.0*cm], hdr_bg=BLUE), sp(6)]

story += [h2("Customer-Specific Tables (retained / extended)")]
story += [tbl([
    ["Table","Description","Key Fields","Status in S/4"],
    ["KNA1", "Customer General",      "KUNNR, NAME1, LAND1, STCD1, KTOKD","Still exists — synced from BUT000 via CVI"],
    ["KNB1", "Customer Co.Code",      "KUNNR, BUKRS, AKONT, ZTERM, KLIMK","Retained — FLCU01 role writes here"],
    ["KNVV", "Customer Sales Area",   "KUNNR, VKORG, VTWEG, SPART, INCO1","Fully retained — no change"],
    ["KNVP", "Customer Partner Func.","KUNNR, PARVW, KUWE",               "Retained — SP/SH/BP/PY links"],
    ["KNVI", "Customer Tax Indicator","KUNNR, ALAND, TATYP, TAXKD",       "Retained — SD tax classification"],
    ["KNVK", "Customer Contact Person","KUNNR, PERNR, NAMEV, TELF1",      "Legacy — use BUT051 in new S/4"],
    ["KNBK", "Customer Bank Data",    "KUNNR, BANKS, BANKL, BANKN",       "Replaced by TIBAN for IBAN"],
    ["KNKA", "Customer Credit Mgmt",  "KUNNR, CTLPC, KLIMK",              "Replaced by UKM_* tables (FSCM)"],
    ["KNB5", "Customer Dunning Data", "KUNNR, BUKRS, MAHNA, MANSP",       "Retained — dunning procedure"],
    ["KNVS", "Customer Shipping",     "KUNNR, VSBED, LPRIO",              "Retained — shipping conditions"],
], col_widths=[2.0*cm, 3.5*cm, 4.5*cm, 5.5*cm], hdr_bg=CUSTC), sp(6)]

story += [h2("Vendor-Specific Tables (retained / extended)")]
story += [tbl([
    ["Table","Description","Key Fields","Status in S/4"],
    ["LFA1", "Vendor General",        "LIFNR, NAME1, LAND1, STCD1, KTOKK","Still exists — synced from BUT000 via CVI"],
    ["LFB1", "Vendor Co.Code",        "LIFNR, BUKRS, AKONT, ZTERM, ZWELS","Retained — FLVN01 role writes here"],
    ["LFM1", "Vendor Purch.Org",      "LIFNR, EKORG, WAERS, ZTERM, INCO1","Fully retained — no change"],
    ["LFM2", "Vendor Plant Data",     "LIFNR, EKORG, WERKS",              "Retained — plant-level purchasing"],
    ["LFBK", "Vendor Bank Data",      "LIFNR, BANKS, BANKL, BANKN",       "Replaced by TIBAN for IBAN"],
    ["LFBW", "Vendor WHT Data",       "LIFNR, BUKRS, WITHT, WT_WITHCD",   "Retained — withholding tax"],
    ["LFAS", "Vendor Tax Indicators", "LIFNR, ALAND, TATYP, TAXKZ",       "Retained — MM tax classification"],
    ["WYT3", "Vendor Partner Func.",  "LIFNR, EKORG, PARVW, LIFN2",       "Retained — ordering address etc."],
    ["LFB5", "Vendor Dunning",        "LIFNR, BUKRS, MAHNA",              "Retained — dunning procedure"],
    ["EORD", "Purchasing Source List","LIFNR, MATNR, WERKS, VDATU",       "Retained — preferred vendor list"],
], col_widths=[2.0*cm, 3.5*cm, 4.5*cm, 5.5*cm], hdr_bg=VENDC), sp(6)]

story += [h2("New CVI / Link Tables (S/4HANA only)")]
story += [tbl([
    ["Table","Description","Key Fields","Purpose"],
    ["CVI_CUST_LINK","Customer ↔ BP Link","CUSTOMER, PARTNER","Every customer must have one row here"],
    ["CVI_VEND_LINK","Vendor ↔ BP Link",  "VENDOR, PARTNER",  "Every vendor must have one row here"],
    ["BNKA",         "Bank Master",        "BANKS, BANKL, BANKA","Bank details (BIC, name) for TIBAN"],
    ["UKM_CASE",     "Credit Case (FSCM)", "CASE_GUID, PARTNER","Replaces old FD32 credit data"],
    ["UKM_BP_ATTR",  "BP Credit Attributes","PARTNER, BUKRS",  "Credit limit, score per BP/CoCode"],
], col_widths=[2.8*cm, 3.5*cm, 3.5*cm, 5.7*cm], hdr_bg=TEAL), sp(4), PageBreak()]

# ── SECTION 12: ACCOUNT GROUP CONFIG ─────────────────────────────────────────
story += [GradientBanner("12  Account Group Configuration",
          "Customer (OBD2) and Vendor (OBD3) account groups — fields and number ranges",
          colors.HexColor("#0369a1"), BLUE), sp(8)]

story += [p("Account Groups control the <b>field status</b> (required/optional/suppress) for each "
            "master data field and drive the <b>number range</b>. In S/4HANA they still exist but "
            "are subordinate to BP Groupings. Every account group must be mapped to a BP grouping "
            "in CVI config."), sp(6)]

story += [h2("Standard Customer Account Groups (OBD2)")]
story += [tbl([
    ["Acct Group","Description",     "Number Range","BP Grouping","Key Field Status"],
    ["KUNA",  "General Customer",    "Ext: 1000–1999999","CUST",  "Name=REQ, Country=REQ, Recon Acct=REQ"],
    ["CPD",   "One-Time Customer",   "Ext: 9000–9099999","CPD",   "Name=OPT (entered at posting)"],
    ["KUNA2", "Foreign Customer",    "Ext: 2000–2999999","CUST",  "Same as KUNA + VAT=REQ"],
    ["LEIS",  "Service Provider",    "Int: auto",        "CUST",  "Sales area optional"],
    ["INTE",  "Internal Customer",   "Int: auto",        "INTE",  "Intercompany — recon acct=REQ"],
    ["PROM",  "Prospect (CRM)",      "Ext or Int",       "CUST",  "No FI required fields"],
], col_widths=[1.8*cm, 3.2*cm, 3.0*cm, 2.5*cm, 6.0*cm], hdr_bg=CUSTC), sp(6)]

story += [h2("Standard Vendor Account Groups (OBD3)")]
story += [tbl([
    ["Acct Group","Description",     "Number Range","BP Grouping","Key Field Status"],
    ["0001",  "Domestic Vendor",     "Ext: 1–999999",    "VEND",  "Name=REQ, Recon Acct=REQ, Country=REQ"],
    ["0002",  "Foreign Vendor",      "Ext: 1–999999",    "VEND",  "VAT=REQ, IBAN encouraged"],
    ["LIEF",  "Standard Vendor",     "Ext: 1–999999",    "VEND",  "General purpose"],
    ["CPD",   "One-Time Vendor",     "Ext: 9100–9199999","CPD",   "Name/Address at posting"],
    ["0004",  "Employee (Expense)",  "Ext: HR-linked",   "VEND",  "Linked to HR Infotype 0009"],
    ["INTE",  "Intercompany Vendor", "Int: auto",        "INTE",  "Recon acct=REQ, no purch org"],
], col_widths=[1.8*cm, 3.2*cm, 3.0*cm, 2.5*cm, 6.0*cm], hdr_bg=VENDC), sp(6)]

story += [h2("Field Status Group — Key Fields per Account Group")]
story += [tbl([
    ["Field","Customer (KUNA)","Vendor (0001)","One-Time (CPD)","Internal"],
    ["Name 1 (NAME1)",         "Required","Required","Optional*","Required"],
    ["Country (LAND1)",        "Required","Required","Optional*","Required"],
    ["Tax Number (STCD1)",     "Required","Required","Suppress", "Suppress"],
    ["Recon. Account (AKONT)", "Required","Required","Optional", "Required"],
    ["Payment Terms (ZTERM)",  "Optional","Optional","Suppress", "Suppress"],
    ["Payment Method (ZWELS)", "Optional","Required","Suppress", "Suppress"],
    ["Sort Key (ZUAWA)",       "Optional","Optional","Suppress", "Optional"],
    ["Credit Limit (KLIMK)",   "Optional","Suppress","Suppress", "Suppress"],
    ["Sales Area Data",        "Optional","Suppress","Suppress", "Suppress"],
    ["Purchasing Org Data",    "Suppress","Optional","Suppress", "Suppress"],
    ["Bank Details (IBAN)",    "Optional","Required","Suppress", "Suppress"],
],col_widths=[4.2*cm,2.8*cm,2.5*cm,2.8*cm,2.8*cm],hdr_bg=NAVY),sp(4)]
story += [p("* One-Time: entered at document posting, not on master record.",CAPN),sp(4),PageBreak()]

# ── SECTION 13: NUMBER RANGE FULL SETUP ───────────────────────────────────────
story += [GradientBanner("13  Number Range Configuration — Full Setup Guide",
          "Internal vs external ranges, BP grouping assignment, overlap prevention",
          colors.HexColor("#7c3aed"), colors.HexColor("#4f46e5")), sp(8)]

story += [p("Number range configuration is the <b>most critical pre-migration step</b>. "
            "Wrong number ranges cause duplicate keys, failed CVI sync, and posting errors "
            "that are very hard to fix after go-live."), sp(4)]

story += [h2("Number Range Types")]
story += [tbl([
    ["Type","How Assigned","When to Use","Risk"],
    ["External (manual)","Assigned from outside — migrated records keep their ECC number",
     "Customer/Vendor migration where you want to keep existing numbers.\nExample: Cust 100045 → BP 100045",
     "Must ensure NO overlap between customer and vendor ranges"],
    ["Internal (auto)",  "SAP assigns the next available number automatically",
     "New BPs created in S/4 after go-live.\nExample: new vendor created → BP# auto from range",
     "Gaps possible if creation fails mid-sequence"],
],col_widths=[2.0*cm,4.5*cm,4.5*cm,4.5*cm],hdr_bg=colors.HexColor("#7c3aed")),sp(6)]

story += [h2("Recommended Number Range Design — Sempra Example")]
story += [tbl([
    ["Object","Range Type","From","To","BP Grouping","Used For"],
    ["Customer",       "External","1000000","1999999","CUST",  "Migrated customers — keep ECC number"],
    ["Vendor",         "External","2000000","2999999","VEND",  "Migrated vendors — keep ECC number"],
    ["One-Time Cust",  "External","9000000","9099999","CPD",   "CPD customers migrated"],
    ["One-Time Vend",  "External","9100000","9199999","CPD",   "CPD vendors migrated"],
    ["New BP (post go-live)","Internal","9200000","9999999","CUST/VEND","New BPs created in S/4"],
    ["Intercompany",   "Internal","8000000","8999999","INTE",  "Internal cross-company BPs"],
],col_widths=[3.2*cm,2.2*cm,2.0*cm,2.0*cm,2.2*cm,4.9*cm],hdr_bg=colors.HexColor("#7c3aed")),sp(4)]

story += [callout(
    "<b>Overlap Check — Run Before Go-Live:</b>  Execute SE16N on BUT000 grouped by PARTNER "
    "to check for number conflicts. Also run: SELECT PARTNER FROM BUT000 WHERE PARTNER IN "
    "(SELECT KUNNR FROM KNA1) AND PARTNER IN (SELECT LIFNR FROM LFA1) — any result means "
    "a customer and vendor share the same number and must be merged into one BP.",
    bg="#f3e8ff",border="#a855f7",tc="#6b21a8"),sp(4)]

story += [h2("SNRO / BUCF Config Steps")]
story += [tbl([
    ["Step","Transaction","Action","Example Value"],
    ["1","SNRO or BUCF → Number Ranges","Create number range object BP_PARTNER","Object: BP_PARTNER"],
    ["2","BUCF → Number Ranges → Assign to BP Group","Assign range 01 to grouping CUST","Group CUST → Range 01 (1000000–1999999)"],
    ["3","BUCF → Number Ranges → Assign to BP Group","Assign range 02 to grouping VEND","Group VEND → Range 02 (2000000–2999999)"],
    ["4","OBD2 → Customer Acct Group → Number Range","Link acct group KUNA to BP external range","KUNA → External, same range as CUST grouping"],
    ["5","OBD3 → Vendor Acct Group → Number Range",  "Link acct group 0001 to BP external range","0001 → External, same range as VEND grouping"],
    ["6","SPRO → CVI → Number Range Mapping",        "Map customer/vendor range to BP range",    "KUNNR range 1000000–1999999 ↔ BP range 01"],
],col_widths=[0.6*cm,3.2*cm,4.8*cm,6.9*cm],hdr_bg=colors.HexColor("#7c3aed")),sp(4),PageBreak()]

# ── SECTION 14: REQUIRED FIELDS ───────────────────────────────────────────────
story += [GradientBanner("14  Required Fields — What Must Be Present Before Migration",
          "Mandatory data per object level — missing these will fail validation",
          RED_C, ORANGE), sp(8)]

story += [p("These are the <b>minimum required fields</b> that must be populated in the source data "
            "before running migration. Missing mandatory fields cause LTMC errors, CVI sync failures, "
            "and rejected BPs. Enrich source data BEFORE loading."), sp(6)]

story += [h2("Customer — Mandatory Fields by Level")]
story += [tbl([
    ["Level","Table","Field","Description","Validate With"],
    ["General","KNA1","KUNNR","Customer Number",          "Must be unique, in number range"],
    ["General","KNA1","NAME1","Name 1",                   "Cannot be blank"],
    ["General","KNA1","LAND1","Country Key",               "Must exist in T005"],
    ["General","KNA1","KTOKD","Account Group",             "Must exist in OBD2 config"],
    ["General","KNA1","SPRAS","Language Key",              "Must exist in T002"],
    ["Co.Code","KNB1","KUNNR","Customer Number",           "Must match KNA1"],
    ["Co.Code","KNB1","BUKRS","Company Code",              "Must exist in T001"],
    ["Co.Code","KNB1","AKONT","Reconciliation Account",    "Must exist in SKA1, type D"],
    ["Sales",  "KNVV","VKORG","Sales Organisation",        "Must exist in TVKO"],
    ["Sales",  "KNVV","VTWEG","Distribution Channel",      "Must exist in TVTW"],
    ["Sales",  "KNVV","SPART","Division",                  "Must exist in TSPA"],
    ["Bank",   "TIBAN","IBAN", "IBAN Number",              "IBAN format validated (country-specific)"],
],col_widths=[1.8*cm,1.6*cm,2.0*cm,3.5*cm,6.6*cm],hdr_bg=CUSTC),sp(6)]

story += [h2("Vendor — Mandatory Fields by Level")]
story += [tbl([
    ["Level","Table","Field","Description","Validate With"],
    ["General","LFA1","LIFNR","Vendor Number",             "Must be unique, in number range"],
    ["General","LFA1","NAME1","Name 1",                    "Cannot be blank"],
    ["General","LFA1","LAND1","Country Key",                "Must exist in T005"],
    ["General","LFA1","KTOKK","Account Group",              "Must exist in OBD3 config"],
    ["Co.Code","LFB1","LIFNR","Vendor Number",              "Must match LFA1"],
    ["Co.Code","LFB1","BUKRS","Company Code",               "Must exist in T001"],
    ["Co.Code","LFB1","AKONT","Reconciliation Account",     "Must exist in SKA1, type K"],
    ["Co.Code","LFB1","ZWELS","Payment Methods",            "Must match FBZP config"],
    ["Purch",  "LFM1","EKORG","Purchasing Organisation",    "Must exist in T024E"],
    ["Purch",  "LFM1","WAERS","Order Currency",             "Must exist in TCURC"],
    ["Bank",   "TIBAN","IBAN", "IBAN Number",               "Required if ZWELS includes bank transfer"],
    ["WHT",    "LFBW","WITHT","Withholding Tax Type",       "Must match T059P config if WHT active"],
],col_widths=[1.8*cm,1.6*cm,2.0*cm,3.5*cm,6.6*cm],hdr_bg=VENDC),sp(6)]

story += [h2("Common Config/Reference Tables — Must Exist Before Migration")]
story += [tbl([
    ["Table","Description","Used By","How to Check"],
    ["T001",  "Company Codes",          "KNB1, LFB1 (BUKRS)",   "SE16N T001 — all company codes listed"],
    ["T005",  "Countries",              "KNA1, LFA1 (LAND1)",   "Must contain all source countries"],
    ["T002",  "Languages",              "KNA1, LFA1 (SPRAS)",   "EN, DE, FR etc. must be active"],
    ["TVKO",  "Sales Organisations",    "KNVV (VKORG)",         "All source sales orgs must exist"],
    ["T024E", "Purchasing Organisations","LFM1 (EKORG)",        "All source purch orgs must exist"],
    ["TCURC", "Currencies",             "LFM1 (WAERS)",         "All order currencies active"],
    ["SKA1",  "G/L Account Master",     "KNB1/LFB1 (AKONT)",   "Recon accounts type D (customer) / K (vendor)"],
    ["T059P", "WHT Types",              "LFBW (WITHT)",         "WHT types configured for company code"],
    ["BNKA",  "Bank Directory",         "TIBAN (BANKL)",        "All bank keys must exist with BIC"],
    ["TBSL",  "Posting Keys",           "FI posting",           "01=cust invoice, 31=vendor invoice active"],
    ["T052",  "Payment Terms",          "KNB1/LFB1 (ZTERM)",   "All ECC payment terms exist in S/4"],
    ["FBZP",  "Payment Methods",        "LFB1 (ZWELS)",         "T=transfer, C=cheque configured per CoCode"],
],col_widths=[1.8*cm,3.5*cm,3.5*cm,6.7*cm],hdr_bg=NAVY),sp(4),PageBreak()]

# ── SECTION 15: END-TO-END MIGRATION CHECKLIST ────────────────────────────────
story += [GradientBanner("15  End-to-End Migration Checklist",
          "Phase by phase — from preparation to go-live sign-off",
          TEAL, colors.HexColor("#065f46")), sp(8)]

story += [tbl([
    ["Phase","#","Task","Owner","Done?"],
    ["PREPARE","1", "Extract all KNA1 records — profile for blanks, duplicates, invalid country codes","Data Team","☐"],
    ["PREPARE","2", "Extract all LFA1 records — profile for blanks, duplicates, STCD1 conflicts","Data Team","☐"],
    ["PREPARE","3", "Identify Customer + Vendor same-company duplicates (match on STCD1 + NAME1)","Data Team","☐"],
    ["PREPARE","4", "Convert KNBK/LFBK bank accounts to IBAN format using RFFMIBAN or manual fix","Data Team","☐"],
    ["PREPARE","5", "Validate all reconciliation accounts (AKONT) exist in SKA1 with correct type","Config Team","☐"],
    ["CONFIG", "6", "Configure BP Number Ranges in BUCF / SNRO — no overlap between customer/vendor","Basis/Config","☐"],
    ["CONFIG", "7", "Configure BP Groupings (CUST, VEND, CPD, INTE) in BUCF","Config Team","☐"],
    ["CONFIG", "8", "Verify BP Roles FLCU00/01, FLVN00/01 exist and are assigned to correct category","Config Team","☐"],
    ["CONFIG", "9", "Configure CVI: Assign customer account groups to BP roles (OBD2 → FLCU)","Config Team","☐"],
    ["CONFIG", "10","Configure CVI: Assign vendor account groups to BP roles (OBD3 → FLVN)","Config Team","☐"],
    ["CONFIG", "11","Configure CVI number range mapping — external ranges for migrated records","Config Team","☐"],
    ["CONFIG", "12","Configure CVI field mapping KNA1/LFA1 → BUT000 — validate all critical fields","Config Team","☐"],
    ["MIGRATE","13","Run LTMC object 'Business Partner' — load BUT000 general data for all BPs","Migration Team","☐"],
    ["MIGRATE","14","Run LTMC 'BP Customer Company Code' — load FLCU01 data per company code","Migration Team","☐"],
    ["MIGRATE","15","Run LTMC 'BP Vendor Company Code' — load FLVN01 data per company code","Migration Team","☐"],
    ["MIGRATE","16","Run LTMC 'BP Customer Sales Area' — load KNVV data","Migration Team","☐"],
    ["MIGRATE","17","Run LTMC 'BP Vendor Purchasing Org' — load LFM1 data","Migration Team","☐"],
    ["MIGRATE","18","Run LTMC 'BP Bank Details' — load TIBAN data (IBAN format only)","Migration Team","☐"],
    ["VALIDATE","19","Run BUPT (BP Consistency Check) — target: 0 errors for all migrated BPs","QA Team","☐"],
    ["VALIDATE","20","Run CVI_CUST_LINK report — every customer must have exactly one BP link","QA Team","☐"],
    ["VALIDATE","21","Run CVI_VEND_LINK report — every vendor must have exactly one BP link","QA Team","☐"],
    ["VALIDATE","22","Post test customer invoice in FI — verify A/R hits recon account 140000","FI Team","☐"],
    ["VALIDATE","23","Post test vendor invoice in FI — verify A/P hits recon account 210000","FI Team","☐"],
    ["VALIDATE","24","Create test sales order in SD — verify partner functions SP/SH/BP/PY resolve","SD Team","☐"],
    ["VALIDATE","25","Create test purchase order in MM — verify vendor data resolves correctly","MM Team","☐"],
    ["GO-LIVE", "26","Activate CVI bidirectional sync — any BP change syncs to Customer/Vendor and back","Config Team","☐"],
    ["GO-LIVE", "27","Cutover sign-off — all workstream leads confirm validation passed","PM","☐"],
    ["GO-LIVE", "28","Hypercare: monitor BUPT daily for first 2 weeks post go-live","Support Team","☐"],
],col_widths=[1.8*cm,0.6*cm,7.5*cm,2.8*cm,1.0*cm],hdr_bg=TEAL,fs=7.5),sp(6)]

story += [callout(
    "<b>Go-Live Gate:</b>  Items 19–25 (validation) must ALL be green before proceeding to go-live. "
    "A single BUPT error on a reconciliation account or a failed test posting means the migration "
    "is NOT ready. No exceptions — fix and revalidate.",
    bg="#f0fdf4",border="#22c55e",tc="#15803d"),sp(8)]

story += [hr()]
story += [Paragraph(
    f"Business Partner Migration Guide — ECC to S/4HANA  ·  All Config, Tables & Examples  ·  "
    f"Classification: Internal  ·  {datetime.date.today().strftime('%B %Y')}",
    S("ft",fontSize=7.5,leading=11,textColor=MUTED,fontName="Helvetica",alignment=TA_CENTER)
)]

# ── BUILD ─────────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(OUT, pagesize=A4,
      leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2.2*cm,
      title="Business Partner Migration — ECC to S/4HANA",
      author="Sempra Migration Team")
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f"\nPDF created: {OUT}")
import os
print(f"    Size   : {round(os.path.getsize(OUT)/1024)} KB")
print(f"    Path   : {os.path.abspath(OUT)}")
