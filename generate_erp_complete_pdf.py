"""
Complete ERP Model — ECC to S/4HANA
All Modules · Config Tables · Real Examples · How ERP is Built
Run: python generate_erp_complete_pdf.py
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, HRFlowable, PageBreak, KeepTogether)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus.flowables import Flowable
import datetime

OUT = "ERP_Complete_ECC_to_S4HANA.pdf"
W, H = A4
CONTENT_W = W - 4*cm

NAVY  = colors.HexColor("#0a1628"); BLUE  = colors.HexColor("#1e3a5f")
TEAL  = colors.HexColor("#0f766e"); SKY   = colors.HexColor("#38bdf8")
FIC   = colors.HexColor("#1d4ed8"); MMC   = colors.HexColor("#0369a1")
SDC   = colors.HexColor("#7c3aed"); PPC   = colors.HexColor("#059669")
COC   = colors.HexColor("#b45309"); PMC   = colors.HexColor("#0e7490")
HRC   = colors.HexColor("#be185d"); QMC   = colors.HexColor("#65a30d")
AMBER = colors.HexColor("#f59e0b"); RED_C = colors.HexColor("#ef4444")
GREEN_C=colors.HexColor("#22c55e"); ORANGE=colors.HexColor("#ea580c")
LTGREY=colors.HexColor("#f7f8fa"); BORDER=colors.HexColor("#e5e7eb")
MUTED =colors.HexColor("#57606a"); DARK  =colors.HexColor("#1f2328")
WHITE =colors.white

def S(n,**k): return ParagraphStyle(n,**k)
CT=S("ct",fontSize=26,leading=34,textColor=WHITE,fontName="Helvetica-Bold")
CS=S("cs",fontSize=11,leading=16,textColor=colors.HexColor("#94a3b8"),fontName="Helvetica")
H1s=S("H1",fontSize=15,leading=20,textColor=NAVY,fontName="Helvetica-Bold",spaceBefore=18,spaceAfter=5)
H2s=S("H2",fontSize=11,leading=15,textColor=BLUE,fontName="Helvetica-Bold",spaceBefore=10,spaceAfter=3)
H3s=S("H3",fontSize=9, leading=13,textColor=DARK,fontName="Helvetica-Bold",spaceBefore=6,spaceAfter=2)
BODY=S("BD",fontSize=8.5,leading=13,textColor=DARK,fontName="Helvetica",spaceAfter=3,alignment=TA_JUSTIFY)
BUL =S("BU",fontSize=8.5,leading=12,textColor=DARK,fontName="Helvetica",leftIndent=12,spaceAfter=2)
CODE=S("CO",fontSize=7.5,leading=11,textColor=colors.HexColor("#1e40af"),fontName="Courier",backColor=colors.HexColor("#eff6ff"),borderPad=4,spaceAfter=4)
CAPN=S("CA",fontSize=7,leading=10,textColor=MUTED,fontName="Helvetica-Oblique",alignment=TA_CENTER,spaceAfter=5)
NOTE=S("NT",fontSize=8,leading=12,textColor=colors.HexColor("#92400e"),fontName="Helvetica",backColor=colors.HexColor("#fffbeb"),borderPad=4,spaceAfter=4)

def p(t,st=None): return Paragraph(t,st or BODY)
def h1(t): return Paragraph(t,H1s)
def h2(t): return Paragraph(t,H2s)
def h3(t): return Paragraph(t,H3s)
def sp(n=6): return Spacer(1,n)
def bul(t): return Paragraph(f"<bullet>&bull;</bullet> {t}",BUL)
def hr(c=BORDER): return HRFlowable(width="100%",thickness=0.5,color=c,spaceAfter=4,spaceBefore=4)
def code(t): return Paragraph(t,CODE)
def note(t): return Paragraph(f"&#x26A0; {t}",NOTE)

class GradientBanner(Flowable):
    def __init__(self,title,subtitle="",c1=NAVY,c2=BLUE,height=48):
        self.title=title;self.subtitle=subtitle;self.c1=c1;self.c2=c2;self.height=height
    def wrap(self,w,h): self.w=w; return (w,self.height+4)
    def draw(self):
        c=self.canv;w=self.w;h=self.height
        c.saveState()
        for i in range(30):
            t=i/30
            r=self.c1.red+t*(self.c2.red-self.c1.red)
            g=self.c1.green+t*(self.c2.green-self.c1.green)
            b=self.c1.blue+t*(self.c2.blue-self.c1.blue)
            c.setFillColorRGB(r,g,b)
            c.rect(w*i/30,0,w*(i+1)/30-w*i/30,h,stroke=0,fill=1)
        c.setFillColor(SKY);c.rect(0,h-3,w,3,stroke=0,fill=1)
        c.setFillColor(WHITE);c.setFont("Helvetica-Bold",12)
        c.drawString(12,h-22,self.title)
        if self.subtitle:
            c.setFillColor(colors.HexColor("#94a3b8"));c.setFont("Helvetica",8)
            c.drawString(12,h-33,self.subtitle)
        c.restoreState()

class LayerBox(Flowable):
    def __init__(self,layers,width=CONTENT_W):
        self.layers=layers;self.w=width;self.h=len(layers)*32+10
    def wrap(self,w,h): return (self.w,self.h)
    def draw(self):
        c=self.canv;w=self.w;y=self.h-10
        cols=[NAVY,FIC,MMC,SDC,PPC,COC,PMC,HRC]
        for i,(num,label,detail) in enumerate(self.layers):
            col=cols[i%len(cols)]
            c.setFillColor(col);c.roundRect(0,y-22,w,24,4,stroke=0,fill=1)
            c.setFillColor(WHITE);c.setFont("Helvetica-Bold",9)
            c.drawString(10,y-13,f"LAYER {num}  —  {label}")
            c.setFont("Helvetica",7.5)
            c.drawRightString(w-10,y-13,detail)
            y-=32

class ModuleCard(Flowable):
    def __init__(self,code,name,colour,changes,width=CONTENT_W/3-4):
        self.code=code;self.name=name;self.colour=colour
        self.changes=changes;self.width=width;self.height=80
    def wrap(self,w,h): return (self.width,self.height)
    def draw(self):
        c=self.canv;w=self.width;h=self.height
        c.setFillColor(LTGREY);c.setStrokeColor(self.colour);c.setLineWidth(1.5)
        c.roundRect(0,0,w,h,5,stroke=1,fill=1)
        c.setFillColor(self.colour);c.roundRect(0,h-4,w,4,2,stroke=0,fill=1)
        c.setFillColor(self.colour);c.setFont("Helvetica-Bold",11)
        c.drawCentredString(w/2,h-18,self.code)
        c.setFillColor(DARK);c.setFont("Helvetica-Bold",7.5)
        c.drawCentredString(w/2,h-28,self.name)
        c.setFillColor(MUTED);c.setFont("Helvetica",6.5)
        y=h-40
        for ch in self.changes:
            c.drawCentredString(w/2,y,ch);y-=9

def tbl(data,col_widths=None,hdr_bg=BLUE,fs=7.5):
    t=Table(data,colWidths=col_widths,repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),hdr_bg),("TEXTCOLOR",(0,0),(-1,0),WHITE),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,-1),fs),
        ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
        ("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),
        ("FONTNAME",(0,1),(-1,-1),"Helvetica"),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE,LTGREY]),
        ("GRID",(0,0),(-1,-1),0.3,BORDER),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ])); return t

def callout(text,bg="#eff6ff",border="#3b82f6",tc="#1e40af"):
    st=S("cb",fontSize=8,leading=12,fontName="Helvetica",textColor=colors.HexColor(tc))
    t=Table([[Paragraph(text,st)]],colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),colors.HexColor(bg)),
        ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7),
        ("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10),
        ("BOX",(0,0),(-1,-1),1,colors.HexColor(border)),
    ])); return t

def on_page(canvas,doc):
    canvas.saveState()
    canvas.setFillColor(MUTED);canvas.setFont("Helvetica",7)
    canvas.drawString(2*cm,1.2*cm,"Complete ERP Model — ECC to S/4HANA  ·  All Modules · Config · Tables · Examples")
    canvas.drawRightString(W-2*cm,1.2*cm,f"Page {doc.page}")
    canvas.setStrokeColor(BORDER);canvas.setLineWidth(0.3)
    canvas.line(2*cm,1.5*cm,W-2*cm,1.5*cm)
    canvas.restoreState()

# ═══════════════════════════════════════════════════════════════════════════════
story=[]

# ── COVER ─────────────────────────────────────────────────────────────────────
cov=Table([[[ p("&#x1F3DB;",S("ci",fontSize=36,leading=44,textColor=WHITE,fontName="Helvetica-Bold")),
    sp(6), p("Complete ERP Model",CT),
    p("ECC to S/4HANA — All Modules · Config Tables · Real Examples",CS), sp(10),
    tbl([["FI","CO","MM","SD","PP","PM","QM","HR","AA","TR"]],
        col_widths=[CONTENT_W/10]*10,hdr_bg=NAVY,fs=8),
    sp(10),
    p("How the ERP is Built · Layer by Layer · Integration · Migration Impact",
      S("x",fontSize=9,textColor=colors.HexColor("#475569"),fontName="Helvetica")),
    p(f"Prepared: {datetime.date.today().strftime('%B %Y')}  ·  Sempra Migration Team",
      S("x2",fontSize=9,textColor=colors.HexColor("#475569"),fontName="Helvetica")),
]]],colWidths=[CONTENT_W])
cov.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),NAVY),
    ("TOPPADDING",(0,0),(-1,-1),46),("BOTTOMPADDING",(0,0),(-1,-1),46),
    ("LEFTPADDING",(0,0),(-1,-1),36),("RIGHTPADDING",(0,0),(-1,-1),36)]))
story+=[cov,PageBreak()]

# ── TOC ───────────────────────────────────────────────────────────────────────
story+=[GradientBanner("Table of Contents","What is in this document",NAVY,BLUE),sp(6)]
toc_data=[["Section","Title","Key Coverage"],
    ["01","How an ERP is Built — The 7 Layers","Foundation → Transactions, build sequence"],
    ["02","Layer 1 — Client & System Settings","T000, T005, T002, TCURC, T006"],
    ["03","Layer 2 — Financial Foundation (FI)","CoA, Company Code, Ledgers, ACDOCA"],
    ["04","Layer 3 — Enterprise Structure","Plants, Sales Orgs, Controlling Area"],
    ["05","FI — Accounts Receivable Config","OBD2, T052, FBMP, UKM_BP"],
    ["06","FI — Accounts Payable Config","OBD3, FBZP, T042, WHT"],
    ["07","FI — Asset Accounting (New AA)","T090, TAFA, ACDOCA, depreciation engine"],
    ["08","MM — Materials Management","OBYC, T030, T134, OMX1, MATDOC"],
    ["09","SD — Sales & Distribution","TVAK, T683, PRCD_ELEMENTS, VKOA"],
    ["10","PP — Production Planning","STKO, PLKO, T438M, MRP Live"],
    ["11","CO — Controlling","TKA01, CSKS, CEPC, ACDOCA, COPA"],
    ["12","QM — Quality Management","QPCA, QMEL, inspection types"],
    ["13","PM — Plant Maintenance","IFLOT, EQUI, T003P, integration"],
    ["14","HR/HCM — Human Resources","PA tables, payroll, FI integration"],
    ["15","TR — Treasury","TIBAN, T012, F110, cash management"],
    ["16","Module Integration Map","How all modules talk to each other"],
    ["17","ACDOCA — Universal Journal","Every field, every module, one table"],
    ["18","Complete Table Reference","ECC vs S/4 — what changed, what stayed"],
    ["19","Migration Impact by Module","Complexity, key changes, what to do"],
    ["20","End-to-End Build Sequence","Month by month implementation order"],
]
story+=[tbl(toc_data,col_widths=[1.2*cm,4.5*cm,9.8*cm],hdr_bg=NAVY),sp(4),PageBreak()]

# ── SECTION 01: 7 LAYERS ──────────────────────────────────────────────────────
story+=[GradientBanner("01  How an ERP is Built — The 7 Layers",
    "Every SAP system is built bottom to top — you cannot skip a layer",NAVY,BLUE),sp(6)]
story+=[p("Before any user can raise a purchase order or post an invoice, SAP must be <b>built layer by layer</b>. "
    "Think of it like constructing a building — the foundation must be solid before you add floors. "
    "Each layer depends on the one below it."),sp(6)]
story+=[LayerBox([
    ("7","TRANSACTIONS","VA01 sales order · ME21N purchase order · FB60 vendor invoice · MIGO goods receipt"),
    ("6","MASTER DATA","Material Master · Business Partner (Customer/Vendor) · Assets · Cost Centres"),
    ("5","INTEGRATION CONFIG","CVI · Account Determination · Partner Det. · Revenue Acct Det."),
    ("4","MODULE CONFIG","MRP types · Payment terms · Pricing procedures · Depreciation keys"),
    ("3","ENTERPRISE STRUCTURE","Plants · Sales Orgs · Purchasing Orgs · Controlling Area · Company Codes"),
    ("2","FINANCIAL FOUNDATION","Chart of Accounts · Fiscal Year · Ledgers · Document types · Posting keys"),
    ("1","CLIENT / SYSTEM","Client 100 · Languages · Currencies · Countries · Units of Measure"),
],width=CONTENT_W),sp(8)]
story+=[callout("<b>Golden Rule:</b> Always configure bottom to top. Cannot create a Plant (Layer 3) before "
    "Company Code (Layer 2). Cannot create Material Master (Layer 6) before Plant (Layer 3). "
    "Cannot post a transaction (Layer 7) before master data (Layer 6) exists.",
    bg="#fffbeb",border="#f59e0b",tc="#92400e"),sp(4),PageBreak()]

# ── SECTION 02: LAYER 1 CLIENT ────────────────────────────────────────────────
story+=[GradientBanner("02  Layer 1 — Client & System Settings",
    "The lowest building block — everything in SAP lives inside a client",NAVY,BLUE),sp(6)]
story+=[p("A <b>Client</b> is the highest-level container in SAP. All config, master data and transactions "
    "live inside it. Most companies use: Client 100=Production, 200=Quality/Test, 300=Development."),sp(4)]
story+=[tbl([["Config Object","Transaction","Table","ECC","S/4","Example"],
    ["Define Client","SCC4","T000","✅","✅","Client 100 — Sempra Production"],
    ["Countries","SPRO","T005","✅","✅","US, DE, MX, CA, GB"],
    ["Country Descriptions","OY01","T005T","✅","✅","US = United States"],
    ["Languages","SPRO","T002","✅","✅","EN, DE, ES, FR"],
    ["Currencies","OY03","TCURC","✅","✅","USD, EUR, MXN, CAD"],
    ["Exchange Rate Types","OB07","TCURV","✅","✅","M=average, B=bank buying rate"],
    ["Exchange Rates","OB08","TCURR","✅","✅","USD/EUR = 0.92 (daily updated)"],
    ["Units of Measure","CUNI","T006","✅","✅","EA, KG, L, M3, HR, PC, SET"],
    ["Factory Calendar","SCAL","TFACD","✅","✅","US = USA working days"],
    ["Time Zones","SPRO","TTZZ","✅","✅","America/Los_Angeles"],
    ["Number Range Objects","SNRO","NRIV","✅","✅","All doc/object number ranges"],
],col_widths=[3.5*cm,2.0*cm,2.0*cm,1.0*cm,1.0*cm,5.5*cm],hdr_bg=NAVY),sp(4),PageBreak()]

# ── SECTION 03: LAYER 2 FINANCIAL FOUNDATION ──────────────────────────────────
story+=[GradientBanner("03  Layer 2 — Financial Foundation (FI)",
    "Chart of Accounts, Company Code, Ledgers, ACDOCA — the accounting backbone",FIC,BLUE),sp(6)]
story+=[h2("Chart of Accounts — The Master G/L Account List")]
story+=[p("The <b>Chart of Accounts (CoA)</b> is the master list of all G/L accounts. "
    "In S/4HANA, EVERY G/L account is automatically a cost element (CO). "
    "In ECC they were separate objects — a common source of errors."),sp(4)]
story+=[tbl([["Account Range","Category","Example Accounts","Notes"],
    ["1xxxxx","Assets","100000=Cash, 113100=Bank, 140000=AR Recon, 191100=GR/IR, 310000=FG Inventory","Balance sheet — debit normal"],
    ["2xxxxx","Liabilities","210000=AP Recon, 220000=Accruals, 280000=Long-Term Debt","Balance sheet — credit normal"],
    ["3xxxxx","Equity","300000=Retained Earnings, 310000=Share Capital","Balance sheet"],
    ["4xxxxx","Revenue","400000=Product Revenue, 410000=Service Revenue","P&L — credit normal"],
    ["5xxxxx","COGS","500000=Labour, 600000=Overhead, 893000=Cost of Goods Sold","P&L — debit normal"],
    ["8xxxxx","Other Costs","800000=Admin, 810000=Selling, 850000=Depreciation","P&L"],
],col_widths=[2.2*cm,2.0*cm,7.0*cm,4.3*cm],hdr_bg=FIC),sp(4)]
story+=[tbl([["Config Object","Transaction","Table","ECC","S/4","Example / Notes"],
    ["Create Chart of Accounts","OB13","T004","✅","✅","USCA=US Sempra, INT=International"],
    ["G/L Account Master (CoA level)","FS00","SKA1","✅","✅","Account type, short text, P&L/BS"],
    ["G/L Account Master (CoCode level)","FS00","SKB1","✅","✅","Open item mgmt, sort key, field status"],
    ["Account Groups (G/L)","OBD4","T077S","✅","✅","Assets, Liabilities, Revenue, Costs"],
    ["Field Status Groups","OBC4","T004F","✅","✅","Which fields req/opt per account"],
    ["Fiscal Year Variant","OB29","T009","✅","✅","K4=Jan-Dec (12 periods), V3=Apr-Mar"],
    ["Assign FY to Company Code","OB37","T001","✅","✅","CoCode 1000 → Variant K4"],
    ["Posting Periods","OB52","T010O","✅","✅","Period 1=Jan open, 13=special period"],
    ["Document Types","OBA7","T003","✅","✅","SA=G/L, KR=Vendor inv, DR=Cust inv, AA=Asset"],
    ["Document Number Ranges","FBN1","NRIV","✅","✅","Doc type SA → internal range 01"],
    ["Posting Keys","OB41","TBSL","✅","✅","01=Cust Debit, 31=Vend Credit, 40=G/L Dr"],
    ["Tolerance Groups (FI)","OBA3","T043T","✅","✅","Max posting difference: $5 or 0.5%"],
    ["New G/L — Ledgers","FINSC_LEDGER","FINSC_LEDGER","Opt","<b>MAND</b>","0L=IFRS leading, 2L=local GAAP"],
    ["Document Splitting","FAGL_SPLITTING","FAGL_SPLINFO","Opt","<b>MAND</b>","Split by Profit Centre per line"],
    ["Parallel Ledgers","FINSC_LEDGER","FAGL_SEGM","Opt","<b>MAND</b>","IFRS+US GAAP simultaneously"],
],col_widths=[3.5*cm,2.2*cm,2.5*cm,0.9*cm,0.9*cm,5.5*cm],hdr_bg=FIC),sp(4)]
story+=[callout("<b>S/4 Key Change — ACDOCA Universal Journal:</b>  In ECC, FI posted to BKPF+BSEG and CO "
    "posted to COEP — two separate tables that needed monthly reconciliation. In S/4HANA both post "
    "to ONE table: ACDOCA. Every line item carries ALL dimensions: G/L account, cost centre, profit "
    "centre, segment, material, plant, customer, vendor — simultaneously. Real-time P&L, no batch jobs.",
    bg="#dbeafe",border="#3b82f6",tc="#1e40af"),sp(4),PageBreak()]

# ── SECTION 04: LAYER 3 ENTERPRISE STRUCTURE ─────────────────────────────────
story+=[GradientBanner("04  Layer 3 — Enterprise Structure",
    "The organisational skeleton — plants, sales orgs, purchasing orgs, controlling area",BLUE,NAVY),sp(6)]
story+=[p("Enterprise structure is the <b>framework everything else hangs from</b>. "
    "Get this wrong and every subsequent config and master data load has to be redone. "
    "Define this in week 1 of the project and lock it down."),sp(4)]
story+=[code(
    "CLIENT 100\n"
    "├── CONTROLLING AREA: 1000 (North America)  →  table TKA01\n"
    "│   └── Links to Company Codes 1000, 2000\n"
    "│\n"
    "├── COMPANY CODE: 1000 (SoCal Gas)  →  table T001\n"
    "│   ├── Chart of Accounts: USCA\n"
    "│   ├── Fiscal Year: K4 (Jan–Dec)\n"
    "│   ├── Currency: USD\n"
    "│   ├── PLANT: 1000 (Los Angeles)  →  table T001W\n"
    "│   │   ├── Storage Location: 0001 Main Warehouse  →  table T001L\n"
    "│   │   └── Storage Location: 0002 Spare Parts\n"
    "│   ├── PLANT: 2000 (San Diego)\n"
    "│   └── PURCHASING ORG: 1000 (Global)  →  table T024E\n"
    "│       └── Purchasing Group: 001 Pumps, 002 Electronics  →  T024\n"
    "│\n"
    "├── SALES ORG: 1000 (US West)  →  table TVKO\n"
    "│   ├── Distribution Channel: 10 Direct, 20 Wholesale  →  TVTW\n"
    "│   └── Division: 01 Pumps, 02 Motors  →  TSPA\n"
    "│       SALES AREA = SalesOrg 1000 + Channel 10 + Division 01\n"
    "│\n"
    "└── CREDIT CONTROL AREA: 1000  →  table T014"
)]
story+=[tbl([["Config Object","Transaction","Table","ECC","S/4","Example"],
    ["Define Company","OX15","T880","✅","✅","SEMP = Sempra Energy (holding)"],
    ["Define Company Code","OX02","T001","✅","✅","1000 = Southern California Gas"],
    ["Assign CoA to CoCode","OB62","T001","✅","✅","CoCode 1000 → USCA"],
    ["Define Controlling Area","OKKP","TKA01","✅","✅","1000 = North America CO Area"],
    ["Assign CoCode to CoArea","OX19","TKA02","✅","✅","CoCode 1000 → CoArea 1000"],
    ["Define Plant","OX10","T001W","✅","✅","1000=Los Angeles, 2000=San Diego"],
    ["Define Storage Location","OX09","T001L","✅","✅","0001=Main WH, 0002=Spare Parts"],
    ["Assign Plant to CoCode","OX18","T001W","✅","✅","Plant 1000 → CoCode 1000"],
    ["Define Purchasing Org","OX08","T024E","✅","✅","1000 = Global Procurement"],
    ["Assign POrg to Plant","OX17","T024W","✅","✅","POrg 1000 → Plant 1000, 2000"],
    ["Define Purchasing Group","OME4","T024","✅","✅","001=Pumps buyers, 002=Electronics"],
    ["Define Sales Organisation","OVX5","TVKO","✅","✅","1000=US West, 2000=US East"],
    ["Define Distribution Channel","OVXI","TVTW","✅","✅","10=Direct, 20=Wholesale"],
    ["Define Division","OVXB","TSPA","✅","✅","01=Pumps, 02=Motors, 03=Services"],
    ["Assign Sales Org to CoCode","OVX3","TVKO","✅","✅","SOrg 1000 → CoCode 1000"],
    ["Assign Plant to Sales Org","OVX6","TVKWZ","✅","✅","Plant 1000 → SOrg 1000"],
    ["Define Valuation Area","OMWM","T001K","✅","✅","= Plant in standard setup"],
    ["Define Warehouse Number","OMB1","T300","✅","✅","001=LA Main Warehouse"],
    ["Assign WH to Plant/SLoc","OMB2","T320","✅","✅","WH001 → Plant 1000, SLoc 0001"],
    ["Credit Control Area","OB45","T014","✅","✅","1000=US Credit Control Area"],
],col_widths=[3.5*cm,2.0*cm,2.0*cm,0.9*cm,0.9*cm,6.2*cm],hdr_bg=BLUE),sp(4),PageBreak()]

# ── SECTION 05: AR CONFIG ─────────────────────────────────────────────────────
story+=[GradientBanner("05  FI — Accounts Receivable Configuration",
    "Customer groups, payment terms, dunning, credit management",FIC,colors.HexColor("#1e40af")),sp(6)]
story+=[tbl([["Config Object","Transaction","Table","ECC","S/4","Example"],
    ["Customer Account Groups","OBD2","T077D","✅","✅","KUNA=general, CPD=one-time, INTE=internal"],
    ["Customer Number Ranges","XDN1","NRIV","✅","✅","External 1000000–1999999"],
    ["BP Number Ranges","BUCF","SNRO","❌","✅","BP group CUST → range 1000000–1999999"],
    ["BP Groupings","BUCF","BU_PARTNERGR","❌","✅","CUST, VEND, CPD, INTE"],
    ["BP Roles","BUCF","BUT_ROLES","❌","✅","FLCU00=Cust General, FLCU01=Cust CoCode"],
    ["CVI: Assign Cust Roles","SPRO→CVI","CVI_CUST_LINK_DEF","❌","✅","KUNA → FLCU00+FLCU01"],
    ["Payment Terms","OBB8","T052","✅","✅","Z030=Net 30, Z014=14 days 2% discount"],
    ["Dunning Procedures","FBMP","T047","✅","✅","Z001=3-level dunning"],
    ["Dunning Levels","FBMP","T047S","✅","✅","Level 1=7d, 2=14d, 3=30d past due"],
    ["Dunning Texts","FBMP","T047T","✅","✅","Letter text per dunning level"],
    ["Interest Calculation","OB46","T056","✅","✅","8% annual on overdue items"],
    ["Reconciliation Account","FS00","SKB1","✅","✅","G/L 140000 = A/R Recon (type D)"],
    ["Tolerance Groups (Cust.)","OBA3","T043T","✅","✅","Max diff: $5 or 0.5% (whichever less)"],
    ["Credit Control Area","OB45","T014","✅","✅","1000 = US Credit Control"],
    ["Credit Mgmt (ECC)","FD32","KNKK","✅","❌","Per-customer credit limit (old)"],
    ["Credit Mgmt (S/4 FSCM)","UKM_BP","UKM_BP_ATTR","❌","✅","Score-based, real-time, per BP"],
    ["Output (Invoice PDF)","V/40","TNAPR","✅","✅","RD00=invoice output via email/print"],
],col_widths=[3.5*cm,2.2*cm,2.8*cm,0.8*cm,0.8*cm,5.4*cm],hdr_bg=FIC),sp(4)]
story+=[callout("<b>Example — Payment Terms Z030:</b>  Customer Siemens AG orders $10,000 of pumps. "
    "Invoice FB70 raised. Payment term Z030 = Net 30 days. Due date = invoice date + 30 days. "
    "If unpaid → dunning level 1 letter at day 37 → level 2 at day 44 → level 3 (legal) at day 60. "
    "In S/4: credit check via UKM_BP blocks new orders if Siemens exceeds $500,000 credit limit.",
    bg="#dbeafe",border="#3b82f6",tc="#1e40af"),sp(4),PageBreak()]

# ── SECTION 06: AP CONFIG ─────────────────────────────────────────────────────
story+=[GradientBanner("06  FI — Accounts Payable Configuration",
    "Vendor groups, payment program, house banks, withholding tax",FIC,colors.HexColor("#1e40af")),sp(6)]
story+=[tbl([["Config Object","Transaction","Table","ECC","S/4","Example"],
    ["Vendor Account Groups","OBD3","T077K","✅","✅","0001=domestic, 0002=foreign, CPD=one-time"],
    ["Vendor Number Ranges","XKN1","NRIV","✅","✅","External 2000000–2999999"],
    ["BP Roles (Vendor)","BUCF","BUT_ROLES","❌","✅","FLVN00=Vend General, FLVN01=Vend CoCode"],
    ["CVI: Assign Vend Roles","SPRO→CVI","CVI_VEND_LINK_DEF","❌","✅","0001 → FLVN00+FLVN01"],
    ["Payment Terms","OBB8","T052","✅","✅","Z014=14 days 2% discount, Z000=immediate"],
    ["Payment Methods","FBZP","T042Z","✅","✅","T=Bank transfer, C=Cheque, B=Bill"],
    ["House Banks","FI12","T012","✅","✅","MAIN=Citibank LA, WEST=WellsFargo"],
    ["Bank Accounts","FI12","T012K","✅","✅","113100=Citibank checking account"],
    ["Bank Master (IBAN)","FI01","BNKA","✅","✅","Bank BIC, name, address"],
    ["Vendor Bank (S/4)","BP→IBAN","TIBAN","❌","✅","IBAN replaces LFBK account number"],
    ["Payment Program","FBZP","T042","✅","✅","F110 run: propose → display → pay"],
    ["Paying Company Codes","FBZP","T042B","✅","✅","CoCode 1000 pays for CoCode 2000 too"],
    ["Payment Run (F110)","F110","REGUH/REGUP","✅","✅","Batch: select due items → create pmts"],
    ["WHT Types","SPRO→FI→WHT","T059P","✅","✅","W1=1099-MISC, W9=1099-DIV"],
    ["WHT Codes","SPRO","T059Z","✅","✅","W1-01=backup WHT 24%, W1-02=standard 0%"],
    ["Reconciliation Account","FS00","SKB1","✅","✅","G/L 210000 = A/P Recon (type K)"],
    ["Check Double Invoice","SPRO","T001","✅","✅","XDEZV=X: block duplicate ref+vendor+amt"],
],col_widths=[3.5*cm,2.0*cm,2.8*cm,0.8*cm,0.8*cm,5.6*cm],hdr_bg=FIC),sp(4)]
story+=[callout("<b>Example — F110 Payment Run:</b>  Vendor SAP SE invoice $45,000, due in 14 days, "
    "payment method T (transfer), house bank MAIN. F110 run: identifies all due items → creates "
    "payment proposal → accounting posts DR Vendor 210000 $45,000 / CR Bank 113100 $45,000 → "
    "ACDOCA entry created → DME file sent to Citibank → IBAN DE89 3704 0044 debited.",
    bg="#f3e8ff",border="#a855f7",tc="#6b21a8"),sp(4),PageBreak()]

# ── SECTION 07: ASSET ACCOUNTING ─────────────────────────────────────────────
story+=[GradientBanner("07  FI — Asset Accounting (New AA in S/4HANA)",
    "Chart of depreciation, asset classes, depreciation keys, new engine",FIC,NAVY),sp(6)]
story+=[p("S/4HANA introduces <b>New Asset Accounting (New AA)</b>. The biggest change: depreciation "
    "is no longer a batch job (AFAB) — it is calculated <b>on-the-fly per posting</b> and stored "
    "directly in ACDOCA. Parallel depreciation for IFRS, US GAAP and Tax simultaneously."),sp(4)]
story+=[tbl([["Config Object","Transaction","Table","ECC","S/4","Example"],
    ["Chart of Depreciation","EC08","T090","✅","✅","US00=US GAAP, IAS=IFRS, DE=German HGB"],
    ["Asset Classes","OAOA","ANKA","✅","✅","1000=Land, 2000=Buildings, 3000=Machinery"],
    ["Asset Class Number Ranges","AS08","NRIV","✅","✅","Class 3000 → assets 3000000–3999999"],
    ["Depreciation Areas","OADB","T090R","✅","✅","01=Book (IFRS), 15=Tax, 32=Local GAAP"],
    ["Depreciation Keys","AFAMA","TAFA","✅","✅","LINR=straight line, DG10=10% declining bal"],
    ["Useful Life per Asset Class","OAYZ","T090N","✅","✅","Class 3000 → 10 years useful life"],
    ["G/L Account Assignment","AO90","FIAA_ACCOUNT","✅","✅","Asset class 3000 → Depr exp 850000"],
    ["Screen Layout (Asset)","AO73","T015","✅","✅","Which fields required per asset class"],
    ["Transaction Types","OAYA","TTTYP","✅","✅","100=acquisition, 200=retirement, 600=depr"],
    ["New Depreciation Engine","SPRO","FAAT_DOC_TYPE","❌","✅","S/4: calculates from asset value date"],
    ["Asset Values in ACDOCA","Auto","ACDOCA","❌","✅","All asset postings in universal journal"],
    ["Parallel Ledger Depr.","OADB","T090R","Opt","✅","IFRS area 01 + Tax area 15 simultaneously"],
],col_widths=[3.5*cm,2.0*cm,2.8*cm,0.8*cm,0.8*cm,5.6*cm],hdr_bg=FIC),sp(4)]
story+=[callout("<b>Example — Asset Pump-Station-001 (class 3000, LINR):</b>\n"
    "Acquired 01.01.2026 for $120,000. Useful life = 10 years. Annual depreciation = $12,000.\n"
    "ECC: AFAB batch job runs monthly → posts $1,000/month.\n"
    "S/4 New AA: depreciation calculated at time of posting → ACDOCA: DR Depr Exp 850000 $1,000 "
    "/ CR Accum Depr 175000 $1,000 — automatically for IFRS area AND Tax area simultaneously.",
    bg="#dbeafe",border="#3b82f6",tc="#1e40af"),sp(4),PageBreak()]

# ── SECTION 08: MM CONFIG ─────────────────────────────────────────────────────
story+=[GradientBanner("08  MM — Materials Management Configuration",
    "Account determination, material types, movement types, Material Ledger",MMC,BLUE),sp(6)]
story+=[h2("Account Determination — How Stock Movements Post to G/L")]
story+=[p("This is the most critical MM config. Transaction <b>OBYC</b> maps: "
    "movement type + valuation class → G/L account automatically. No manual G/L entry needed."),sp(3)]
story+=[tbl([["Transaction Key","Meaning","Dr Account","Cr Account","Example"],
    ["BSX","Inventory posting","300000 Raw Mat / 310000 FG","—","GR: DR Inventory"],
    ["WRX","GR/IR clearing","—","191100 GR/IR","GR: CR GR/IR"],
    ["GBB+VAX","Goods issue (sales)","893000 COGS","—","Delivery: DR COGS"],
    ["GBB+VBR","GI to cost centre","400000 Expense","—","Maintenance issue"],
    ["GBB+AUF","GI to prod order","WIP account","—","Issue components"],
    ["PRD","Price difference","281000 Variance","—","MAP recalculation"],
    ["AUM","Stock transfer","Dest inventory","Src inventory","Inter-plant transfer"],
    ["KBS","GR to cost centre","Cost ctr expense","—","Non-stock PO receipt"],
],col_widths=[2.5*cm,3.0*cm,3.2*cm,2.8*cm,4.0*cm],hdr_bg=MMC),sp(4)]
story+=[tbl([["Config Object","Transaction","Table","ECC","S/4","Notes"],
    ["Valuation Classes","OMSK","T025, T025T","✅","✅","7920=FG, 3000=RM, 7900=HALB"],
    ["Account Category Reference","OMSK","T025B","✅","✅","Links mat type to val class group"],
    ["Account Determination","OBYC","T030","✅","✅","BSX+7920 → G/L 310000"],
    ["Material Types","OMS2","T134, T134M","✅","✅","FERT, ROH, HALB, HAWA, DIEN"],
    ["Material Groups","OMSF","T023, T023T","✅","✅","001=Pumps, 002=Motors"],
    ["Movement Types","OMJJ","T156, T156T","✅","✅","101=GR PO, 601=GI delivery"],
    ["Material Number Ranges","MMNR","NRIV","✅","✅","External 1–999999, Internal auto"],
    ["Purchasing Value Keys","SPRO","T068","✅","✅","Default tolerances for materials"],
    ["Tolerance Keys","SPRO","T169G","✅","✅","B1=order price, B2=delivery cost"],
    ["Source List","ME01","EORD","✅","✅","Preferred vendor for material/plant"],
    ["Info Records","ME11","EINA, EINE","✅","✅","Agreed price: vendor X, mat Y=$450"],
    ["Activate Material Ledger","OMX1","CKMLMVOBJ","Opt","<b>MAND</b>","All plants — mandatory in S/4"],
    ["ML Actual Costing","CKMVFM","CKMLHD","Opt","<b>MAND</b>","Period-end actual cost calc"],
    ["Material Document","Auto","MATDOC","❌","✅","Replaces MKPF+MSEG in S/4"],
    ["Batch Management","SPRO","T001W","✅","✅","Per plant — cannot reverse once stock exists"],
    ["Serial Number Profiles","SPRO","SERP","✅","✅","Track each unit individually"],
],col_widths=[3.5*cm,2.0*cm,2.5*cm,0.8*cm,0.8*cm,5.9*cm],hdr_bg=MMC),sp(4)]
story+=[callout("<b>Key Movement Types with Accounting:</b>\n"
    "101 GR vs PO: DR Inventory 310000 / CR GR/IR 191100 (vendor goods arrive)\n"
    "261 GI to Production: DR WIP / CR Inventory 310000 (components issued to order)\n"
    "601 GI for Delivery: DR COGS 893000 / CR Inventory 310000 (pump shipped to customer)\n"
    "In S/4: all post to ACDOCA with material, plant, profit centre stamped on every line.",
    bg="#e0f2fe",border="#0369a1",tc="#0c4a6e"),sp(4),PageBreak()]

# ── SECTION 09: SD CONFIG ─────────────────────────────────────────────────────
story+=[GradientBanner("09  SD — Sales & Distribution Configuration",
    "Sales doc types, pricing, output, partner determination, revenue account",SDC,NAVY),sp(6)]
story+=[h2("Pricing — How a Customer Price is Calculated")]
story+=[code("Customer orders PUMP-100, Sales Org 1000, Channel 10:\n"
    "Pricing Procedure RVAA01 runs — condition types in sequence:\n"
    "  Step 10  PR00  List Price         +$500.00  (from material price list)\n"
    "  Step 20  K007  Customer Discount  -$25.00   (5% for key account)\n"
    "  Step 30  K029  Material Discount  -$10.00   (2% special promotion)\n"
    "  Step 40  MWST  Output Tax         +$37.35   (8.09% California)\n"
    "  ──────────────────────────────────────────\n"
    "  Net to customer: $502.35  |  Tax: $37.35  |  Invoice total: $539.70")]
story+=[tbl([["Config Object","Transaction","Table","ECC","S/4","Example"],
    ["Sales Document Types","VOV8","TVAK","✅","✅","OR=order, RE=return, CR=credit memo"],
    ["Item Category Groups","OVH3","T171","✅","✅","NORM=standard item, DIEN=service"],
    ["Item Categories","VOV7","TVAP","✅","✅","TAN=standard, TATX=text, TANN=free"],
    ["Schedule Line Categories","VOV6","TVEP","✅","✅","CP=MRP relevant, CB=no MRP"],
    ["Delivery Document Types","OVL2","TVSM","✅","✅","LF=outbound, LR=returns delivery"],
    ["Billing Document Types","VOFA","TVFK","✅","✅","F2=invoice, G2=credit, L2=debit"],
    ["Pricing Procedure","M/08","T683","✅","✅","RVAA01=standard sales pricing"],
    ["Condition Types","V/06","T685","✅","✅","PR00=price, K007=cust disc, MWST=tax"],
    ["Pricing Conditions (ECC)","VK11","KONV","✅","❌","Old condition table — gone in S/4"],
    ["Pricing Conditions (S/4)","VK11","PRCD_ELEMENTS","❌","✅","New table — faster queries"],
    ["Partner Determination","VOPA","TPAER","✅","✅","SP=sold-to, SH=ship-to, PY=payer"],
    ["Availability Check","OVZ2","T441","✅","✅","Checking rule 02=ATP check"],
    ["Transfer of Requirements","OVZG","T441A","✅","✅","SD demand flows to MRP in PP/MM"],
    ["Revenue Account Determ.","VKOA","T030","✅","✅","Revenue class → G/L 400000"],
    ["Output Determination","V/40","TNAPR","✅","✅","RD00=invoice PDF to customer email"],
    ["Credit Check (S/4)","SPRO→FSCM","UKM_PROF","❌","✅","Real-time credit score + limit check"],
    ["Shipping Points","OVXD","TVSST","✅","✅","SP01=LA dock, SP02=San Diego dock"],
    ["Shipping Conditions","OVST","TVSB","✅","✅","01=standard, 02=express, 03=overnight"],
],col_widths=[3.5*cm,2.0*cm,2.8*cm,0.8*cm,0.8*cm,5.6*cm],hdr_bg=SDC),sp(4),PageBreak()]

# ── SECTION 10: PP CONFIG ─────────────────────────────────────────────────────
story+=[GradientBanner("10  PP — Production Planning Configuration",
    "BOM, routings, work centres, MRP, production orders",PPC,NAVY),sp(6)]
story+=[h2("BOM + Routing + Work Centre = Standard Cost Estimate")]
story+=[code("PUMP-100 Standard Cost Estimate:\n\n"
    "Bill of Materials (CS01 → STKO/STPO):    Routing (CA01 → PLKO/PLPO):\n"
    "  SHAFT-01   1 EA × $80  = $80             Op 0010 Cut    WC:LATHE-01  0.5 HR\n"
    "  BODY-01    1 EA × $120 = $120             Op 0020 Weld   WC:WELD-01   1.0 HR\n"
    "  SEAL-KIT   1 SET× $35  = $35              Op 0030 Test   WC:TEST-01   0.5 HR\n"
    "  PAINT-01   2 L  × $5   = $10\n"
    "  Material Cost:          $245             Labour  2HR × $40 = $80\n"
    "                                           Machine 2HR × $25 = $50\n"
    "                                           Overhead 25% on labour = $20\n"
    "                                           Total Standard Cost: $245+$150 = $395\n"
    "                                           MBEW-STPRS = $395/EA")]
story+=[tbl([["Config Object","Transaction","Table","ECC","S/4","Example"],
    ["Work Centres","CR01","CRHD, CRCA","✅","✅","LATHE-01=turning, WELD-01=welding"],
    ["Capacity Categories","OPJK","CR tables","✅","✅","Machine hrs, Labour hrs, Tool"],
    ["Routings","CA01","PLKO, PLPO","✅","✅","PUMP-100: cut→weld→test operations"],
    ["Bill of Materials","CS01","STKO, STPO","✅","✅","PUMP-100 = SHAFT+BODY+SEAL+PAINT"],
    ["BOM Usage","SPRO","STZU","✅","✅","1=production, 5=sales, 3=universal"],
    ["MRP Types","OMDT","T438M","✅","✅","PD=MRP, VB=reorder point, ND=no plan"],
    ["Lot Sizes","OMI4","T438D","✅","✅","EX=exact, FX=fixed 100, HB=replenish max"],
    ["Scheduling Parameters","OPUZ","T490","✅","✅","Backward scheduling, float times"],
    ["Production Order Types","OPL8","T003O","✅","✅","PP01=standard, PP02=rework order"],
    ["Costing Variants","OKKN","TKK4V","✅","✅","PPC1=planned cost, PPP1=actual cost"],
    ["Results Analysis Keys","SPRO","TKKAV","✅","✅","WIP calculation method at month end"],
    ["Variance Keys","OKV1","TKKVS","✅","✅","000001=full variance calculation"],
    ["Overhead Cost Sheet","KZS2","TKKOS","✅","✅","25% overhead surcharge on labour"],
    ["Production Versions","SPRO","MKAL","✅","✅","0001=BOM alt 1+Routing 1"],
    ["MRP Live (S/4)","SPRO","PPH_* tables","❌","✅","Real-time MRP — no overnight batch"],
    ["Demand Management","MD61","PBIM","✅","✅","Planned independent requirements"],
],col_widths=[3.5*cm,2.0*cm,2.5*cm,0.8*cm,0.8*cm,5.9*cm],hdr_bg=PPC),sp(4),PageBreak()]

# ── SECTION 11: CO CONFIG ─────────────────────────────────────────────────────
story+=[GradientBanner("11  CO — Controlling Configuration",
    "Cost centres, profit centres, COPA, internal orders, ACDOCA merger",COC,NAVY),sp(6)]
story+=[p("In S/4HANA, <b>CO is no longer separate from FI</b>. Both post to ACDOCA. "
    "The old reconciliation between FI and CO (transaction KALC) is no longer needed. "
    "Also: Cost Elements are gone as a separate object — every G/L account IS a cost element."),sp(4)]
story+=[tbl([["Config Object","Transaction","Table","ECC","S/4","Example / Change"],
    ["Controlling Area","OKKP","TKA01","✅","✅","1000=North America, currency USD"],
    ["Cost Element Types (ECC)","KA01","CSKU","✅","❌","ECC only — separate object, now gone"],
    ["Cost Elements = G/L (S/4)","FS00","SKA1","❌","✅","Every G/L is auto a cost element"],
    ["Cost Centre Types","OKA2","TKA04","✅","✅","A=production, B=admin, C=service"],
    ["Cost Centres","KS01","CSKS, CSKT","✅","✅","1000=Pumps Prod, 2000=Finance"],
    ["Cost Centre Hierarchy","OKEON","SETHEADER","✅","✅","Standard hierarchy for reporting"],
    ["Profit Centres","KE51","CEPC, CEPCT","✅","✅","PC_PUMPS, PC_MOTORS, PC_SERVICES"],
    ["Profit Centre Hierarchy","KCH1","SETHEADER","✅","✅","All PCs under one root node"],
    ["Internal Orders","KO01","AUFK","✅","✅","Marketing campaign, R&D project"],
    ["Order Types (CO)","KOT2","T003O","✅","✅","0100=overhead order, 0200=invest"],
    ["Activity Types","KL01","CSLA","✅","✅","LABOUR=machine hours, SETUP=setup hrs"],
    ["Statistical Key Figures","KK01","CSKF","✅","✅","HEADCNT=headcount, SQMETR=floor space"],
    ["Assessment Cycles","KSU1","RKCT_* tables","✅","✅","IT cost → all plants by headcount"],
    ["Distribution Cycles","KSV1","RKCA_* tables","✅","✅","HR cost → departments by headcount"],
    ["COPA (Costing-based)","KEA0","CE4xxxx","✅","Deprc","Old COPA — phased out in S/4"],
    ["COPA (Account-based)","KEA0","ACDOCA","Opt","✅","Preferred: same table as FI — no recon"],
    ["Material Ledger","OMX1","CKMLHD","Opt","<b>MAND</b>","Actual cost per period, mandatory S/4"],
    ["Plan/Actual Comparison","KSBL","COSS/COSP(ECC)","✅","ACDOCA","Plan vs actual in ACDOCA in S/4"],
],col_widths=[3.5*cm,2.0*cm,2.8*cm,0.8*cm,0.8*cm,5.6*cm],hdr_bg=COC),sp(4)]
story+=[callout("<b>COPA Example — Account-Based (S/4 preferred):</b>\n"
    "Sale of PUMP-100 to Siemens AG, $502.35, COGS $395:\n"
    "ACDOCA lines: Revenue $502.35 → Profit Centre PC_PUMPS, Segment SEG_INDUSTRIAL, "
    "Customer 100045, Material PUMP-100, Plant 1000\n"
    "COGS $395 → same dimensions.\n"
    "Gross Margin = $107.35 visible in REAL-TIME — no month-end COPA transfer needed.",
    bg="#fef9c3",border="#d97706",tc="#78350f"),sp(4),PageBreak()]

# ── SECTION 12: QM ────────────────────────────────────────────────────────────
story+=[GradientBanner("12  QM — Quality Management Configuration",
    "Inspection types, sampling, results recording, usage decisions",QMC,NAVY),sp(6)]
story+=[tbl([["Config Object","Transaction","Table","Example"],
    ["Inspection Types","SPRO","QPCA","01=GR, 04=production, 06=delivery, 10=audit"],
    ["Sampling Procedures","QDV1","QDSV","100% check, AQL 0.65, fixed sample 10"],
    ["Inspection Methods","QS21","QPMK","Dimensional check, visual inspection, lab test"],
    ["Inspection Characteristics","QS21","QPMK","LENGTH 450mm±2mm, PRESSURE 16BAR"],
    ["Defect Codes","QS41","QPCD","DENT=surface dent, CRACK=hairline crack"],
    ["Catalogs","QS61","Q* tables","Usage decisions: A=accept, R=reject, I=block"],
    ["Notification Types","SPRO","QMIH","Q1=internal, Q2=customer complaint, Q3=vendor"],
    ["Quality Info Record","QI01","QINF","Vendor X certified for PUMP-100, skip lot 1/10"],
    ["Inspection Lot (auto created)","MIGO/auto","QMEL","Created on GR if MARC-INSMK=1"],
    ["Results Recording","QE01","QMRS","Inspector records measured values vs specs"],
    ["Usage Decision","QA11","QMUR","A=accept → move 321 to unrestricted stock"],
],col_widths=[3.5*cm,1.8*cm,2.2*cm,8.0*cm],hdr_bg=QMC),sp(4)]
story+=[code("QM Flow Example:\n"
    "GR for PUMP-100 (MARC-INSMK=1) → stock to QI automatically\n"
    "Inspector: QE01 records LENGTH=449mm (spec 450±2mm) → PASS\n"
    "Inspector: QA11 usage decision A=Accept → Movement 321 → stock to unrestricted\n"
    "If REJECT: Movement 344 → blocked stock → Q2 notification → vendor return Movement 122"),sp(4),PageBreak()]

# ── SECTION 13: PM ────────────────────────────────────────────────────────────
story+=[GradientBanner("13  PM — Plant Maintenance Configuration",
    "Equipment, functional locations, maintenance orders, integration",PMC,NAVY),sp(6)]
story+=[tbl([["Config Object","Transaction","Table","Example"],
    ["Functional Locations","IL01","IFLOT","SEP-LA-PUMP-001 = Pump station Los Angeles"],
    ["Equipment Master","IE01","EQUI","PUMP-001 S/N A12345 installed at SEP-LA-PUMP-001"],
    ["Maintenance Plant","SPRO","T001W","1000 = Los Angeles maintenance plant"],
    ["Order Types","OIOA","T003P","PM01=corrective, PM02=preventive, PM03=inspection"],
    ["Work Centre (PM)","IR01","CRHD","MECH-01=Mechanics, ELEC-01=Electrical"],
    ["Catalog (PM)","QS41","QPCD","Breakdown codes: ELEC=electrical, MECH=mechanical"],
    ["Maintenance Strategies","IP11","MMPT","Annual service, Quarterly check, 5000hr service"],
    ["Task Lists (PM)","IA05","PLKO","Standard ops: inspect bearings, change oil, test"],
    ["Planner Groups","SPRO","T024I","001=Mechanical, 002=Electrical, 003=Civil"],
    ["Notification Types","SPRO","QMIH","M1=malfunction, M2=maintenance request"],
    ["Settlement Rules","SPRO","TKA3A","PM Order cost → Cost Centre or Asset"],
],col_widths=[3.5*cm,1.8*cm,2.0*cm,8.2*cm],hdr_bg=PMC),sp(4)]
story+=[code("PM Integration Flow:\n"
    "Equipment PUMP-001 breaks → IW21 Notification M1 (malfunction)\n"
    "→ IW31 PM Order PM01 created (corrective)\n"
    "→ Spare parts reserved (MM: SEAL-KIT-01 from SLoc 0002)\n"
    "→ Labour assigned: MECH-01 work centre, 4 hours\n"
    "→ Parts issued: MVT 261 → ACDOCA: DR PM Order / CR Inventory 200000\n"
    "→ Labour confirmed: CO → ACDOCA: DR PM Order / CR Cost Centre MECH\n"
    "→ Order settlement: total cost $850 → Cost Centre 1000 (ACDOCA)\n"
    "→ If capital repair > threshold: capitalise to Asset → FI-AA depreciation"),sp(4),PageBreak()]

# ── SECTION 14: HR ────────────────────────────────────────────────────────────
story+=[GradientBanner("14  HR/HCM — Human Resources Configuration",
    "Org structure, payroll, infotypes, FI integration",HRC,NAVY),sp(6)]
story+=[tbl([["Config Object","Transaction","Table","Example"],
    ["Personnel Areas","SPRO","T500P","1000=Los Angeles, 2000=San Diego"],
    ["Personnel Subareas","SPRO","T503","0001=Office staff, 0002=Plant workers"],
    ["Employee Groups","SPRO","T501","1=Active, 2=Retired, 3=Contractor"],
    ["Employee Subgroups","SPRO","T503K","D1=Hourly, D2=Salaried, D3=Executive"],
    ["Pay Scale Types","SPRO","T510A","US01=US hourly, US02=US salaried"],
    ["Pay Scale Levels","SPRO","T510","Level 1-10 per pay scale type"],
    ["Wage Types","SPRO","T512T","/001=basic pay, /006=overtime 1.5x, /550=bonus"],
    ["Payroll Areas","SPRO","T549A","US=US monthly, BI=biweekly"],
    ["Payroll Schema","PE01","T52C0","US schema: gross→tax→deductions→net pay"],
    ["Cost Centre Assignment","PP01","HRP1001","Employee 10001 → Cost Centre 1000"],
    ["Infotype 0001 (Org)","PA30","PA0001","Employee, position, org unit, cost centre"],
    ["Infotype 0002 (Personal)","PA30","PA0002","Name, DOB, nationality, ID"],
    ["Infotype 0008 (Basic Pay)","PA30","PA0008","Salary $85,000/year, pay scale D2-L5"],
    ["Infotype 0009 (Bank)","PA30","PA0009","Employee IBAN for salary payment"],
    ["Infotype 0071 (Pension)","PA30","PA0071","401k: employee 6%, employer match 3%"],
],col_widths=[3.5*cm,1.8*cm,2.5*cm,7.7*cm],hdr_bg=HRC),sp(4)]
story+=[code("Payroll → FI Integration:\n"
    "Monthly payroll run (PC00_M99_CIPE) for 500 employees:\n"
    "ACDOCA posting:\n"
    "  DR Labour Cost 500000     $2,500,000  (reads IT0001 cost centre per employee)\n"
    "  CR Federal Tax Payable    $  500,000  (reads IT0071 tax data)\n"
    "  CR Social Security Pay.   $  190,000\n"
    "  CR Payroll Clearing       $1,810,000  (net pay to employees)\n"
    "Next step: F110 payment run → IBAN per employee (IT0009) → bank transfer"),sp(4),PageBreak()]

# ── SECTION 15: TREASURY ─────────────────────────────────────────────────────
story+=[GradientBanner("15  TR — Treasury Configuration",
    "House banks, IBAN, payment factory, cash management",colors.HexColor("#0c4a6e"),NAVY),sp(6)]
story+=[tbl([["Config Object","Transaction","Table","ECC","S/4","Example"],
    ["House Banks","FI12","T012","✅","✅","MAIN=Citibank LA, WEST=WellsFargo Phoenix"],
    ["Bank Accounts","FI12","T012K","✅","✅","MAIN-CHK=checking 113100, MAIN-SAV=savings"],
    ["Bank Master","FI01","BNKA","✅","✅","Bank BIC CITIUS33, name, address"],
    ["Vendor IBAN (S/4)","BP","TIBAN","❌","✅","DE89 3704 0044 0532 0130 00"],
    ["Customer IBAN (S/4)","BP","TIBAN","❌","✅","GB29 NWBK 6016 1331 9268 19"],
    ["Bank Communication Mgmt","BCM","BCM tables","Opt","✅","SWIFT MT100, XML PAIN.001"],
    ["Cash Journal","FBCJ","CSKS","✅","✅","Petty cash transactions, daily balance"],
    ["Cash Management (ECC)","FF7A","FDFD","✅","❌","Separate transaction — legacy"],
    ["Cash Mgmt (S/4 embedded)","FF7A","ACDOCA","❌","✅","Real-time cash position from ACDOCA"],
    ["Electronic Bank Statement","FF_5","FEBEP","✅","✅","MT940 bank statement auto-reconcile"],
    ["Liquidity Planner","LQ01","FLQMG","Opt","✅","30-day forward cash forecast"],
    ["Payment Factory","FBZP","T042","✅","✅","Central payments for all group entities"],
],col_widths=[3.5*cm,1.8*cm,2.2*cm,0.8*cm,0.8*cm,6.4*cm],hdr_bg=colors.HexColor("#0c4a6e")),sp(4),PageBreak()]

# ── SECTION 16: INTEGRATION MAP ───────────────────────────────────────────────
story+=[GradientBanner("16  Module Integration Map — How Everything Talks",
    "Every module connection, trigger, and ACDOCA posting",NAVY,BLUE),sp(6)]
story+=[tbl([["From Module","Event / Trigger","To Module","Result / ACDOCA Posting"],
    ["MM / MRP","Stock below reorder point or sales order demand","PP","Planned Order created → Production Order"],
    ["MM","Goods Receipt against PO (MVT 101)","FI","DR Inventory 310000 / CR GR/IR 191100 (ACDOCA)"],
    ["MM","Invoice Verification (MIRO)","FI","DR GR/IR 191100 / CR Vendor 210000 (ACDOCA)"],
    ["MM","Goods Issue to Production (MVT 261)","FI+CO","DR WIP / CR Inventory; cost on PP Order (ACDOCA)"],
    ["MM","Goods Issue for Delivery (MVT 601)","FI+CO","DR COGS 893000 / CR Inventory 310000 (ACDOCA)"],
    ["SD","Sales Order created (VA01)","MM+PP","ATP check vs MARD; MRP demand if insufficient"],
    ["SD","Billing document (VF01)","FI","DR Customer 140000 / CR Revenue 400000 (ACDOCA)"],
    ["SD","Credit check on order","TR/FI","UKM_BP checks BP credit score → block if over limit"],
    ["PP","Production Order GR (MVT 101)","MM+FI","Finished goods added to MARD; ACDOCA: DR FG / CR WIP"],
    ["PP","Production Order settlement","CO+FI","Variance: DR/CR ACDOCA; cost to Profit Centre"],
    ["PM","Spare parts issued to maint. order","MM+FI","MVT 261: DR PM Order / CR Inventory (ACDOCA)"],
    ["PM","Order settlement","CO+FI","Maintenance cost → Cost Centre or Asset (ACDOCA)"],
    ["HR","Payroll posting","FI+CO","DR Labour (per cost centre) / CR Payroll Clearing (ACDOCA)"],
    ["AA","Depreciation posting (New AA)","FI","DR Depr Expense 850000 / CR Accum Depr 175000 (ACDOCA)"],
    ["AA","Asset acquisition (capitalise)","FI+CO","DR Asset / CR Clearing or Vendor (ACDOCA)"],
    ["QM","Usage decision REJECT (MVT 344)","MM+SD","Stock blocked; Q2 notification; vendor return MVT 122"],
    ["CO","Period-end allocation (assessment)","FI+CO","IT cost → plants by headcount (ACDOCA reposting)"],
    ["ML (CO)","Period-end actual cost calc","FI+CO+MM","Revalue inventory + COGS to actual (ACDOCA)"],
],col_widths=[2.0*cm,4.5*cm,2.0*cm,7.0*cm],hdr_bg=NAVY),sp(4),PageBreak()]

# ── SECTION 17: ACDOCA ────────────────────────────────────────────────────────
story+=[GradientBanner("17  ACDOCA — The Universal Journal (S/4HANA Only)",
    "Every financial posting lands here — FI, CO, MM, SD, AA, ML all in one table",FIC,NAVY),sp(6)]
story+=[p("ACDOCA = <b>AC</b>counting <b>DOC</b>ument <b>A</b>ctual. "
    "This is the single most important table in S/4HANA. In ECC you needed BKPF+BSEG (FI) "
    "+ COEP (CO) + ANLC (AA) + CE4x (COPA) — 5+ tables, all needing reconciliation. "
    "In S/4HANA: <b>one table, always reconciled, real-time.</b>"),sp(4)]
story+=[tbl([["ACDOCA Field Group","Field","Description","Example Value"],
    ["Identity","RCLNT / RBUKRS","Client / Company Code","100 / 1000"],
    ["Identity","GJAHR / BELNR","Fiscal Year / Document Number","2026 / 5000012345"],
    ["Identity","DOCLN / BLDAT","Line Number / Document Date","001 / 15.10.2026"],
    ["G/L","RACCT","G/L Account","310000 (FG Inventory)"],
    ["G/L","DRCRK / HSL","Dr/Cr Indicator / Amount Local","S (Debit) / 45,000.00"],
    ["G/L","WSL / TSL","Transact. Currency / 2nd Local","45,000.00 USD / 41,400.00 EUR"],
    ["Controlling","RCNTR","Cost Centre","1000 (Pumps Production)"],
    ["Controlling","PRCTR","Profit Centre","PC_PUMPS"],
    ["Controlling","SEGMENT","Segment","SEG_INDUSTRIAL"],
    ["Controlling","RFAREA","Functional Area","PRODUCTION"],
    ["Logistics","MATNR / WERKS","Material / Plant","PUMP-100 / 1000"],
    ["Logistics","KUNNR","Customer","100045 (Siemens AG)"],
    ["Logistics","LIFNR","Vendor","200078 (SAP SE)"],
    ["Logistics","VBELN","Sales Document","2000001234"],
    ["Logistics","EBELN","Purchase Document","4500012345"],
    ["Logistics","AUFNR","Order (PP/PM/CO)","1000001234 (Production Order)"],
    ["Asset","ANLN1 / ANLGR","Asset Number / Group","100000 / MACHINERY"],
    ["Quantity","MENGE / MEINS","Quantity / Unit","100 / EA"],
],col_widths=[2.5*cm,2.8*cm,4.0*cm,6.2*cm],hdr_bg=FIC),sp(4)]
story+=[callout("<b>ACDOCA Power Query Example:</b>  Show me gross margin by Profit Centre for October 2026:\n"
    "SELECT PRCTR, SUM(CASE WHEN RACCT LIKE '4%' THEN HSL ELSE 0 END) AS Revenue,\n"
    "       SUM(CASE WHEN RACCT='893000' THEN HSL ELSE 0 END) AS COGS\n"
    "FROM ACDOCA WHERE GJAHR=2026 AND POPER=10 AND RBUKRS='1000'\n"
    "GROUP BY PRCTR\n"
    "In ECC: needed FAGLFLEXT (FI) + COPA extraction + CO reconciliation report — 3 steps.\n"
    "In S/4: ONE query, real-time, zero reconciliation.",
    bg="#dbeafe",border="#3b82f6",tc="#1e40af"),sp(4),PageBreak()]

# ── SECTION 18: COMPLETE TABLE REFERENCE ──────────────────────────────────────
story+=[GradientBanner("18  Complete Table Reference — ECC vs S/4HANA",
    "Every important table — what changed, what stayed, what is new",NAVY,BLUE),sp(6)]
story+=[h2("Tables That CHANGED or DISAPPEARED in S/4HANA")]
story+=[tbl([["Module","ECC Table","S/4HANA","Status","Impact / Action Required"],
    ["FI","BKPF","ACDOCA (view)","Compatibility view","Custom programs using BKPF still work — read-only"],
    ["FI","BSEG","ACDOCA (view)","Compatibility view","Custom reports must be rewritten for ACDOCA"],
    ["FI","GLT0","Calculated","<b>REMOVED</b>","No totals table — balance calculated live from ACDOCA"],
    ["FI","FAGLFLEXT","Calculated","<b>REMOVED</b>","New G/L totals gone — use ACDOCA queries"],
    ["FI","FAGLFLEXA","ACDOCA","<b>MERGED</b>","All FI line items now in ACDOCA"],
    ["CO","COEP","ACDOCA","<b>MERGED</b>","CO and FI in same table — no reconciliation"],
    ["CO","COSS/COSP","Calculated","<b>REMOVED</b>","CO object totals calculated from ACDOCA"],
    ["CO","CE4xxxx","ACDOCA","Deprecated","Costing-based COPA phased out — use account-based"],
    ["MM","MKPF","MATDOC","<b>REPLACED</b>","Material document header → new MATDOC table"],
    ["MM","MSEG","MATDOC","<b>REPLACED</b>","Material document items → new MATDOC table"],
    ["MM","RBKP","ACDOCA","<b>REPLACED</b>","Invoice Verification header → ACDOCA"],
    ["MM","RSEG","ACDOCA","<b>REPLACED</b>","Invoice Verification items → ACDOCA"],
    ["SD","KONV","PRCD_ELEMENTS","<b>REPLACED</b>","Pricing conditions → new faster table"],
    ["FI-AA","ANLC","ACDOCA","<b>REPLACED</b>","Asset periodic values → universal journal"],
    ["FI-AA","ANLZ","ACDOCA (values)","Extended","Time-dep. data kept; values in ACDOCA"],
    ["BP","—","BUT000/BUT100","<b>NEW</b>","Business Partner replaces split KNA1/LFA1"],
    ["ML","CKMLCR","CKMLCR+ACDOCA","<b>MANDATORY</b>","Material Ledger now always active"],
],col_widths=[1.5*cm,2.3*cm,3.0*cm,2.0*cm,6.7*cm],hdr_bg=RED_C),sp(5)]
story+=[h2("Tables That STAYED THE SAME")]
story+=[tbl([["Module","Table","Description","Any Change?"],
    ["MM","MARA","Material Master — General Data","Extended (40-char number optional)"],
    ["MM","MARC","Material Master — Plant Data (MRP, Purchasing)","No change"],
    ["MM","MBEW","Material Valuation (standard price, MAP)","Extended with ML fields"],
    ["MM","MARD","Storage Location Stock","No change — still current"],
    ["MM","MAKT","Material Descriptions (multi-language)","No change"],
    ["MM","EKKO/EKPO","Purchase Order Header/Items","No change"],
    ["SD","VBAK/VBAP","Sales Order Header/Items","No change"],
    ["SD","VBRK/VBRP","Billing Document Header/Items","No change"],
    ["SD","LIKP/LIPS","Delivery Header/Items","No change"],
    ["PP","STKO/STPO","Bill of Materials Header/Items","No change"],
    ["PP","PLKO/PLPO","Routing Header/Operations","No change"],
    ["PP","AUFK","Production/PM/CO Order Master","No change"],
    ["HR","PA0001–PA9999","HR Infotypes","No change"],
    ["FI","T001","Company Codes","No change"],
    ["FI","T052","Payment Terms","No change"],
    ["ALL","NRIV","Number Ranges","No change"],
    ["ALL","T003","Document Types","No change"],
    ["CO","CSKS/CEPC","Cost Centre / Profit Centre","No change"],
    ["MM","EINA/EINE","Purchasing Info Records","No change"],
    ["MM","EORD","Purchasing Source List","No change"],
],col_widths=[1.5*cm,2.5*cm,5.5*cm,6.0*cm],hdr_bg=GREEN_C),sp(4),PageBreak()]

# ── SECTION 19: MIGRATION IMPACT ──────────────────────────────────────────────
story+=[GradientBanner("19  Migration Impact by Module",
    "Complexity rating, key changes, and what your team must do",NAVY,RED_C),sp(6)]
story+=[tbl([["Module","Complexity","Key Change in S/4","What Your Team Must Do"],
    ["FI — G/L","🔴 HIGH","BSEG→ACDOCA, New G/L mandatory,\ndoc splitting mandatory",
     "Activate ledgers, configure splitting rules,\nrewrite custom G/L reports for ACDOCA"],
    ["FI — A/R","🟡 MED","Customer→BP (CVI), credit mgmt FSCM",
     "Migrate customers as BP, configure UKM_BP,\nre-test dunning and payment terms"],
    ["FI — A/P","🟡 MED","Vendor→BP (CVI), IBAN mandatory",
     "Migrate vendors as BP, convert LFBK→TIBAN,\nverify F110 payment run"],
    ["FI — AA","🔴 HIGH","New depreciation engine, values in ACDOCA",
     "Parallel run old vs new AA, validate asset\nvalues, migrate opening balances"],
    ["CO","🔴 HIGH","COEP→ACDOCA, cost elements=G/L,\naccount-based COPA preferred",
     "Remove CE1x cost elements, switch to account\nCOPA, activate ML for all plants"],
    ["MM","🟡 MED","MSEG→MATDOC, ML mandatory,\nmaterial number 40 chars optional",
     "Migrate material masters, reconcile stock\nvalues, activate ML per plant"],
    ["SD","🟡 MED","Customer→BP, KONV→PRCD_ELEMENTS,\ncredit mgmt to FSCM",
     "Re-test all pricing, output, partner det.,\nverify revenue account determination"],
    ["PP","🟢 LOW","MRP Live optional, mostly same",
     "Re-test MRP runs, validate production orders,\ncost estimates with new ML"],
    ["PM","🟢 LOW","Mostly same, asset capitalisation via new AA",
     "Re-test maintenance orders, verify cost\nsettlement to cost centres/assets"],
    ["QM","🟢 LOW","Mostly same",
     "Re-test inspection lots, usage decisions,\nverify stock movement postings"],
    ["HR","🟡 MED","Payroll → ACDOCA (was separate)",
     "Verify payroll FI posting, test cost centre\nassignment, validate IBAN payments"],
    ["TR","🟡 MED","IBAN mandatory, cash mgmt embedded",
     "Convert all bank accounts to IBAN, test\nF110 payment, verify bank statements"],
    ["WM→EWM","🔴 HIGH (if upgrading)","New architecture, new transactions",
     "Separate EWM implementation workstream,\nnew bin structure, new processes"],
],col_widths=[1.8*cm,1.8*cm,4.0*cm,7.9*cm],hdr_bg=RED_C),sp(4),PageBreak()]

# ── SECTION 20: BUILD SEQUENCE ────────────────────────────────────────────────
story+=[GradientBanner("20  End-to-End Build Sequence — Month by Month",
    "From blank system to go-live — the correct implementation order",TEAL,NAVY),sp(6)]
story+=[tbl([["Phase","Month","Activity","Key Config / Tables","Owner"],
    ["FOUNDATION","1","Activate S/4 system, client settings","T000, T005, T002, TCURC, T006","Basis"],
    ["FOUNDATION","1","Chart of Accounts + G/L accounts","T004, SKA1, SKB1, T077S","FI"],
    ["FOUNDATION","1","Company Codes + fiscal year","T001, T009, OB52","FI"],
    ["FOUNDATION","1","Activate New G/L + ledgers + doc splitting","FINSC_LEDGER, FAGL_SPLINFO","FI"],
    ["FOUNDATION","2","Controlling Area + cost elements","TKA01, SKA1 (= cost elements in S/4)","CO"],
    ["FOUNDATION","2","Plants, storage locations","T001W, T001L","MM/Basis"],
    ["FOUNDATION","2","Sales Orgs, Channels, Divisions","TVKO, TVTW, TSPA","SD"],
    ["FOUNDATION","2","Purchasing Orgs + Groups","T024E, T024","MM"],
    ["MODULE CFG","3","FI-AR: customer groups, payment terms, dunning","T077D, T052, T047","FI"],
    ["MODULE CFG","3","FI-AP: vendor groups, payment program, banks","T077K, T042, T012","FI"],
    ["MODULE CFG","3","FI-AA: asset classes, depreciation keys","T090, ANKA, TAFA","FI-AA"],
    ["MODULE CFG","3","MM: material types, valuation classes, OBYC","T134, T025, T030","MM"],
    ["MODULE CFG","4","MM: Activate Material Ledger all plants","CKMLMVOBJ, OMX1","CO/MM"],
    ["MODULE CFG","4","SD: doc types, pricing, output, partner det.","TVAK, T683, TNAPR","SD"],
    ["MODULE CFG","4","PP: work centres, MRP types, lot sizes","CRHD, T438M, T438D","PP"],
    ["MODULE CFG","4","CO: cost centres, profit centres, COPA","CSKS, CEPC, ACDOCA","CO"],
    ["INTEGRATION","5","CVI: BP roles, number ranges, field mapping","BUT_ROLES, CVI_MAP_*","All"],
    ["INTEGRATION","5","Account determination: OBYC, VKOA, AO90","T030, FIAA_ACCOUNT","FI/MM/SD"],
    ["INTEGRATION","5","Credit management: UKM_BP config","UKM_PROF, UKM_BP_ATTR","FI/SD/TR"],
    ["INTEGRATION","6","End-to-end process testing (all modules)","All","All teams"],
    ["MASTER DATA","7","G/L Master, Cost Centres, Profit Centres","SKA1, CSKS, CEPC","FI/CO"],
    ["MASTER DATA","7-8","Business Partners (Customers + Vendors)","BUT000, KNA1, LFA1, TIBAN","All"],
    ["MASTER DATA","8-9","Material Master (MARA, MARC, MBEW, MVKE)","MARA, MARC, MBEW, MVKE","MM"],
    ["MASTER DATA","9","BOM, Routings, Work Centres","STKO, PLKO, CRHD","PP"],
    ["MASTER DATA","9","Asset Master + opening values","ANLA, ANLB, ACDOCA","FI-AA"],
    ["OPEN ITEMS","10","Open POs, Sales Orders, Production Orders","EKKO, VBAK, AUFK","All"],
    ["OPEN ITEMS","11","FI Open Items (AR+AP invoices)","ACDOCA opening entries","FI"],
    ["OPEN ITEMS","11","Stock quantities → reconcile to FI G/L","MARD, MBEW, ACDOCA","MM/FI"],
    ["CUTOVER","12","Parallel run: ECC and S/4 side by side","All","All"],
    ["CUTOVER","12","Cutover weekend: freeze ECC, load final delta","All tables","All"],
    ["GO-LIVE","12","Go-Live + hypercare (2 weeks daily BUPT)","ACDOCA, BUPT, MB5L","All"],
],col_widths=[2.2*cm,1.2*cm,4.5*cm,3.8*cm,2.0*cm],hdr_bg=TEAL,fs=7),sp(6)]

story+=[callout("<b>The Three Non-Negotiable Go-Live Gates:</b>\n"
    "1. ACDOCA balances match ECC legacy system balances (FI reconciliation)\n"
    "2. MARD stock quantity × MBEW price = G/L inventory account balance (stock reconciliation)\n"
    "3. BUPT (BP consistency) = ZERO errors for all Business Partners (master data quality)\n"
    "All three must be GREEN before cutover weekend. No exceptions.",
    bg="#f0fdf4",border="#22c55e",tc="#15803d"),sp(6)]

story+=[hr()]
story+=[Paragraph(
    f"Complete ERP Model — ECC to S/4HANA  ·  All Modules · Config Tables · Real Examples  ·  "
    f"Classification: Internal  ·  {datetime.date.today().strftime('%B %Y')}",
    S("ft",fontSize=7.5,leading=11,textColor=MUTED,fontName="Helvetica",alignment=TA_CENTER))]

# ── BUILD ──────────────────────────────────────────────────────────────────────
doc=SimpleDocTemplate(OUT,pagesize=A4,
    leftMargin=2*cm,rightMargin=2*cm,topMargin=2*cm,bottomMargin=2.2*cm,
    title="Complete ERP Model — ECC to S/4HANA",
    author="Sempra Migration Team")
doc.build(story,onFirstPage=on_page,onLaterPages=on_page)
print(f"\nPDF created: {OUT}")
import os
print(f"    Size   : {round(os.path.getsize(OUT)/1024)} KB")
print(f"    Path   : {os.path.abspath(OUT)}")
