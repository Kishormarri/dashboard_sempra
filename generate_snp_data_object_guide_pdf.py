"""Generates the comprehensive SNP Data Object Export & Import Guide PDF with Diagrams & Snapshots."""
import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, PageBreak, KeepTogether, CondPageBreak)
from reportlab.platypus.flowables import Flowable
from snp_common import (
    W, H, CONTENT_W, NAVY, BLUE, SKY, TEAL, CUSTC, VIOLET, AMBER, RED_C, GREEN_C,
    LTGREY, BORDER, MUTED, DARK, WHITE,
    p, h2, h3, sp, bul, mono, code, tbl, banner, warn, good,
    COVER_TITLE, COVER_SUB, FlowRow, make_on_page
)

def create_guide_pdf():
    pdf_filename = "SNP_DataObject_Export_Import_Complete_Guide.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm
    )
    story = []

    # -- COVER PAGE -------------------------------------------------------------
    story.append(sp(15))
    cover_table = Table([[
        Paragraph("SNP CrystalBridge & Transformation Cockpit<br/><font size=15 color='#38bdf8'>Data Object Creation, Export, Import & Rules Master Guide</font>", COVER_TITLE)
    ]], colWidths=[CONTENT_W])
    cover_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("TOPPADDING", (0, 0), (-1, -1), 22),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 18),
        ("LEFTPADDING", (0, 0), (-1, -1), 16),
        ("RIGHTPADDING", (0, 0), (-1, -1), 16),
        ("LINEBELOW", (0, -1), (-1, -1), 4, SKY),
    ]))
    story.append(cover_table)
    story.append(sp(12))

    meta_text = f"<b>Author:</b> SNP Migration Architecture & Technical Specialist Team<br/><b>Document Version:</b> 1.0 Complete Technical Reference<br/><b>Date:</b> {datetime.date.today().strftime('%B %d, %Y')}<br/><b>Target Audience:</b> SAP Technical Consultants, Migration Leads, ABAP Engineers"
    story.append(p(meta_text))
    story.append(sp(10))

    story.extend(banner("Executive Process Summary", "End-to-end data transformation pipeline from ECC Source to S/4HANA Target", NAVY, BLUE))
    story.append(sp(6))
    
    flow_steps = [
        ("1. DESIGN", ["Data Object", "Hierarchy", "Reader (SR/DR)"], CUSTC),
        ("2. FILTER", ["Selections", "Global Domains", "SQL Expert"], TEAL),
        ("3. EXPORT", ["EXP Block", "Export Rules", "Compress Files"], BLUE),
        ("4. MAP", ["1:1 / N:1 / X+N:1", "Derivations", "Validate TE02"], VIOLET),
        ("5. IMPORT", ["IMP Block", "Import Modes", "Target Write"], GREEN_C),
    ]
    story.append(FlowRow(flow_steps, height=70))
    story.append(sp(10))

    story.append(p("This technical document details the complete step-by-step procedure for configuring, extracting, transforming, and importing data using <b>SNP CrystalBridge (Transformation Cockpit / TC2019)</b>. It includes exact UI snapshots, architecture flows, reader methods, rule hierarchies, and import modes."))

    story.append(PageBreak())

    # -- SECTION 1: ARCHITECTURE & DATA OBJECT CREATION -------------------------
    story.extend(banner("01  Architecture & Data Object Creation", "System landscape, Shadow DDIC, object header, and table connections", NAVY, VIOLET))
    story.append(sp(4))
    story.append(h2("1.1 Landscape Foundation & Shadow DDIC"))
    story.append(p("Before creating Data Objects, ensure RFC connections are established across Control, Source (ECC), and Target (S/4HANA) systems, and start the TC Daemon via " + mono("/SNP/TE01_DAEMON") + ". The Shadow DDIC synchronizes table definitions and manages schema deltas (e.g. MATNR 18 to 40 characters or KONV to PRCD_ELEMENTS)."))
    
    story.append(h2("1.2 Creating Data Object Header"))
    story.append(p("Data Objects act as logical containers grouping root business tables with all dependent child tables, selections, and local transformation logic."))
    
    do_params = [
        ["Parameter", "Setting / Value", "Technical Function"],
        ["Object ID", "DO_SD_SALES_ORDER", "Unique uppercase identifier in Transformation Cockpit."],
        ["Title", "Sales Orders Header & Items", "Human-readable description of the migration entity."],
        ["Status", "A (Active)", "Only active objects are compiled into transformation blocks."],
        ["Data Type", "T (Transaction)", "Categorizes data into Transaction (T), Master (M), or Customizing (C)."],
        ["Flags", "Relevant for Export / Import, NZD", "Enables export/import inclusion and near-zero downtime logging."],
        ["Predecessors", "DO_BC_ADDRESS, DO_SD_CUSTOMER", "Enforces sequence (e.g., addresses must exist before customers/orders)."]
    ]
    story.append(tbl(do_params, [3.8*cm, 4.6*cm, 8.6*cm], first_bold=True))
    story.append(sp(6))

    story.append(h3("Transformation Cockpit Snapshot: Data Object Creation"))
    snap_do = r"""+========================================================================================================+
| [SNP Transformation Cockpit] - Data Object Maintenance: DO_SD_SALES_ORDER                [Client 100]  |
+========================================================================================================+
| Object ID        : [ DO_SD_SALES_ORDER          ]  Status: (o) A - Active   ( ) I - Inactive          |
| Title            : [ Sales Orders - Open and Historical Documents                             ]       |
| Data Type        : [ T ] (T: Transaction, M: Master Data, C: Customizing)                             |
| Execution Flags  : [X] Relevant for Export    [X] Relevant for Import    [X] NZD Compliant            |
| Predecessors     : Export: DO_SD_CUSTOMER    | Import: DO_BC_ADDRESS -> DO_SD_CUSTOMER                |
+========================================================================================================+"""
    story.extend(code(snap_do))

    story.append(CondPageBreak(8*cm))

    # -- SECTION 2: TABLE CONNECTIONS & READERS ---------------------------------
    story.append(h2("1.3 Table Connections & Reader Selection (Scout vs. Direct Reader)"))
    story.append(p("Child tables are assigned under the root table (e.g., VBAK -> VBAP -> VBEP). SNP provides two specialized extraction readers:"))
    
    readers = [
        ["Reader Type", "Mechanism", "When to Use", "Behavior"],
        ["Scout Reader (SR)", "FOR ALL ENTRIES on parent export", "Standard parent-child hierarchies", "Processes in 2 steps. Dependent table waits for parent export."],
        ["Direct Reader (DR)", "INNER JOIN SQL statement", "Massive child tables (KONV, BSEG)", "Single SQL statement. Fully independent parallel extraction."]
    ]
    story.append(tbl(readers, [3.4*cm, 4.8*cm, 4.4*cm, 4.4*cm], first_bold=True))
    story.append(sp(6))

    story.append(h3("Transformation Cockpit Snapshot: Table Hierarchy & Readers"))
    snap_tree = r"""+========================================================================================================+
| [-] [DO] DO_SD_SALES_ORDER  [Status: ACTIVE] [Type: T - Transaction]                                    |
|     |-- [T] VBAK  (Sales Header)    [Root Selection Table]   Reader: Scout (SR)    Status: ACTIVE       |
|     |   |-- [T] VBAP  (Sales Item)      [Dependent Table]    Reader: Scout (SR)    Status: ACTIVE       |
|     |   |   |-- [T] VBEP  (Schedule)    [Dependent Table]    Reader: Scout (SR)    Status: ACTIVE       |
|     |   |   \-- [T] KONV  (Pricing)     [Dependent Table]    Reader: Direct (DR)   Status: ACTIVE       |
|     |   \-- [T] VBKD  (Business Data)   [Dependent Table]    Reader: Scout (SR)    Status: ACTIVE       |
+========================================================================================================+"""
    story.extend(code(snap_tree))

    story.append(PageBreak())

    # -- SECTION 3: SELECTIONS & EXPORT RULES -----------------------------------
    story.extend(banner("02  Selections, Export Rules & Events", "Filter criteria, domain rules, and source lifecycle event hooks", BLUE, TEAL))
    story.append(sp(4))
    
    story.append(h2("2.1 Filtering & Selection Strategies"))
    story.append(bul("<b>Field Selection (Local):</b> Direct filter applied to table fields (e.g., " + mono("VBAK-AUART IN ('OR', 'QT')") + ")."))
    story.append(bul("<b>Global Selection (Universal):</b> Universal filter applied to a Domain (e.g., Domain " + mono("BUKRS = 1000, 1100") + ") inherited across all tables."))
    story.append(bul("<b>Free Selection (SQL Expert Mode):</b> OpenSQL WHERE-clause for complex multi-field criteria."))
    story.append(sp(4))

    story.append(h2("2.2 All Possible Export Rules & Events"))
    story.append(p("Export rules run on the source ECC system during extraction. Events allow custom ABAP logic at defined execution moments:"))

    exp_events = [
        ["Event / Rule", "Level / Scope", "Parameters", "Typical Technical Purpose"],
        ["Process Init", "Run start", "Memory buffers", "Initializes variables and clears temporary export caches."],
        ["Before Table", "Table start", "IV_TABNAME", "Checks table readiness, allocates buffer tables."],
        ["Before Package", "Package start", "IT_PACKAGE_KEYS", "Pre-allocates chunk size, starts performance timer."],
        ["Before Record", "Each row", "IS_RECORD (Read)", "Evaluates record validity across multiple fields."],
        ["Global Export Rule", "Domain level", "CV_VALUE, IS_RECORD", "Address collection (ADRNR), GDPR data scrambling."],
        ["After Record", "Each row", "CS_RECORD, EV_SKIP", "Set EV_SKIP = 'X' to drop obsolete/closed records."],
        ["After Package", "Package end", "CT_PACKAGE", "Performs batch aggregations and checksum verification."],
        ["After Table", "Table end", "IV_TOTAL_ROWS", "Writes extracted counts to execution tracking tables."]
    ]
    story.append(tbl(exp_events, [3.2*cm, 2.6*cm, 3.8*cm, 7.4*cm], first_bold=True))
    story.append(sp(6))

    story.append(h3("Transformation Cockpit Snapshot: Export Event Code Editor (EV_SKIP)"))
    snap_exp_code = r"""*----------------------------------------------------------------------*
* SNP Export Event: After Data Record Processing (Table: VBAK)
* Logic: Skip completely closed/cancelled orders older than 2020
*----------------------------------------------------------------------*
IF cs_record-gbstk = 'C' AND cs_record-erdat < '20200101'.
  ev_skip = 'X'.  " Excludes record from being written to export file
  EXIT.
ENDIF."""
    story.extend(code(snap_exp_code))

    story.append(CondPageBreak(8*cm))

    # -- SECTION 4: EXPORT EXECUTION --------------------------------------------
    story.append(h2("2.3 Export Block (EXP) Creation & Execution"))
    story.append(p("The Export Block packages active data objects, allocates parallel work processes (e.g., 12 RFC workers), and divides data into compressed package files (e.g., 50,000 rows/package) stored at " + mono("[share]/<Scenario>/<Block>/<Table>/pkg_*.dat.gz") + ". Files are immutable and never overwritten."))

    story.append(h3("Transformation Cockpit Snapshot: Export Execution Monitor"))
    snap_exp_mon = r"""+========================================================================================================+
| [SNP Transformation Cockpit] - Export Block Execution Monitor: BLK_SD_EXP_01              [Client 100]  |
+========================================================================================================+
| Table | Reader | Total Records | Packages (Done/Total) | Processed MB | Status        | Speed (rec/s)  |
|-------+--------+---------------+-----------------------+--------------+---------------+----------------|
| VBAK  | SR     |       500,000 | 10 / 10  [COMPLETED]  | 142 MB       | [COMPLETED]   | 45,000         |
| VBAP  | SR     |     3,800,000 | 76 / 76  [COMPLETED]  | 890 MB       | [COMPLETED]   | 62,000         |
| KONV  | DR     |     8,500,000 | 170 / 170 [COMPLETED] | 1,820 MB     | [COMPLETED]   | 85,000         |
+========================================================================================================+"""
    story.extend(code(snap_exp_mon))

    story.append(PageBreak())

    # -- SECTION 5: MAPPINGS & NUMBER RANGES ------------------------------------
    story.extend(banner("03  Mapping Matrix & Number Range Strategies", "Value conversions, composite rules, and target collision prevention", VIOLET, BLUE))
    story.append(sp(4))

    story.append(h2("3.1 Transformation Mapping Framework"))
    
    maps = [
        ["Mapping Type", "Scope", "Example", "Description"],
        ["1:1 Value Mapping", "Domain / Field", "BUKRS 1000 -> 2000", "Direct one-to-one translation."],
        ["N:1 Consolidation", "Domain / Field", "BUKRS 1000, 1100 -> 2000", "Harmonizes multiple source codes into one target code."],
        ["X+N:1 Dependent", "Composite Keys", "WERKS 1000 + LGORT 0001 -> FG01", "Two source fields determine one target value."],
        ["Derivation Rule", "Table Field", "Profit Center derived from Plant", "Dynamic ABAP logic calculating target value."],
        ["Hard-Coded", "Table Field", "VKORG = 'US01'", "Static constant assigned unconditionally."],
        ["Default Value", "Table Field", "VSTEL = '1000' (if initial)", "Assigned only when source field is initial/blank."]
    ]
    story.append(tbl(maps, [3.2*cm, 2.6*cm, 4.8*cm, 6.4*cm], first_bold=True))
    story.append(sp(6))

    story.append(good("<b>Validation Rule:</b> Always execute " + mono("/SNP/TE02_VALIDATE_MAPPINGS") + " before starting the import. Any unmapped value flagged in red must be resolved to prevent import failures."))
    story.append(sp(4))

    story.append(h2("3.2 Number Range Strategies"))
    nr_strats = [
        ["Strategy", "Mechanism", "Best For"],
        ["Increment (API)", "Generates new numbers via NUMBER_GET_NEXT; logs cross-reference.", "Master data (Customers, Vendors, Materials)."],
        ["Difference (+Offset)", "Calculates New = Old + Offset (e.g. +5,000,000). Fast, lock-free.", "High-volume transactional documents (SD, FI, MM)."],
        ["1:1 Adoption", "Adopts source document number unchanged.", "Dedicated target migration clients."],
        ["Inactive", "Bypasses number range engine.", "External numbering scenarios."]
    ]
    story.append(tbl(nr_strats, [3.6*cm, 7.4*cm, 6.0*cm], first_bold=True))
    story.append(sp(6))

    story.append(CondPageBreak(8*cm))

    # -- SECTION 6: IMPORT BLOCK, MODES & EVENTS --------------------------------
    story.extend(banner("04  Import Block, Modes & Lifecycle Events", "Target insertion modes, field rule overrides, and commit sequencing", GREEN_C, NAVY))
    story.append(sp(4))

    story.append(h2("4.1 Complete Import Modes Matrix"))
    
    modes = [
        ["Import Mode", "If Key Exists in Target DB", "If Key Does NOT Exist", "Typical Application"],
        ["INSERT (Default)", "Fails / Terminates (Duplicate Key)", "Inserts new record", "Strict cutover & clean target clients."],
        ["INSERT_ADK", "Skips record silently (no error)", "Inserts new record", "Loading archive/historical master data."],
        ["UPDATE", "Updates non-key fields", "Skips record", "Refreshing attributes on pre-existing data."],
        ["MODIFY", "Updates non-key fields", "Inserts new record", "Delta synchronization & master data merge."],
        ["DELETE", "Deletes target record", "No action", "Test data cleanup / Rollback blocks."],
        ["APPEND / SUM", "Adds numeric amounts to existing row", "Inserts new record", "Trial balances / GL financial ledger merge."]
    ]
    story.append(tbl(modes, [3.2*cm, 4.6*cm, 4.2*cm, 5.0*cm], first_bold=True))
    story.append(sp(6))

    story.append(h2("4.2 Import Events & Field Rules"))
    story.append(p("Import rules run on the Target S/4HANA system. A <b>Field Rule</b> contains custom ABAP for a specific field and <b>overrides</b> any Global Import Rule for that field. Events allow dynamic mode switching per record (e.g., setting " + mono("TE_IMPORT_MODE = 'UPDATE'") + ")."))

    story.append(h3("Transformation Cockpit Snapshot: Import Block & Mode Grid"))
    snap_imp = r"""+========================================================================================================+
| [SNP Transformation Cockpit] - Import Block Configuration: BLK_SD_IMP_01                  [Client 200]  |
+========================================================================================================+
| Seq  | Table Name | Target Table Name | Import Mode | Option | Target Redirect? | Status                   |
|------+------------+-------------------+-------------+--------+------------------+--------------------------|
| 0010 | ADRC       | ADRC              | INSERT      | NONE   | [ ] No           | [READY]                  |
| 0020 | KNA1       | BUT000            | MODIFY      | NONE   | [ ] No           | [READY]                  |
| 0030 | VBAK       | VBAK              | INSERT      | NONE   | [ ] No           | [READY]                  |
| 0040 | VBAP       | VBAP              | INSERT      | NONE   | [ ] No           | [READY]                  |
| 0050 | KONV       | PRCD_ELEMENTS     | MODIFY      | NONE   | [X] Redirect     | [READY]                  |
+========================================================================================================+"""
    story.extend(code(snap_imp))

    story.append(PageBreak())

    # -- SECTION 7: VERIFICATION & RECONCILIATION -------------------------------
    story.extend(banner("05  Reconciliation, Consistency & Transaction Matrix", "Post-import verification, FK checks, and master transaction reference", NAVY, BLUE))
    story.append(sp(4))

    story.append(h2("5.1 Post-Import Verification & Foreign Key Integrity"))
    story.append(bul("<b>Record Count Reconciliation:</b> Validate that Source Exported Count = Target Inserted Count + Skipped (EV_SKIP) + Filtered Rows."))
    story.append(bul("<b>Foreign Key Integrity Check:</b> Execute transaction " + mono("/SNP/TE02_FK_CHECK") + " on target to ensure zero orphan records exist."))
    story.append(bul("<b>Selective Restartability:</b> If a package fails, fixing the root cause allows restarting <i>only failed packages</i> without duplicate inserts."))
    story.append(sp(4))

    story.append(h3("Transformation Cockpit Snapshot: Reconciliation & Foreign Key Check"))
    snap_recon = r"""+========================================================================================================+
| [SNP Transformation Cockpit] - Post-Import Reconciliation & Consistency Check             [Client 200]  |
+========================================================================================================+
| Table | Source Exported | Target Inserted | Skipped (EV_SKIP) | Discrepancy | Status                   |
|-------+-----------------+-----------------+-------------------+-------------+--------------------------|
| VBAK  |         510,000 |         500,000 |            10,000 |           0 | [BALANCED - MATCH]       |
| VBAP  |       3,850,000 |       3,800,000 |            50,000 |           0 | [BALANCED - MATCH]       |
| KONV  |       8,500,000 |       8,500,000 |                 0 |           0 | [BALANCED - MATCH]       |
+--------------------------------------------------------------------------------------------------------+
| Foreign Key Check (/SNP/TE02_FK_CHECK): Parent VBAK <-> Child VBAP | Total Orphans: 0 | Status: [PASSED]|
+========================================================================================================+"""
    story.extend(code(snap_recon))

    story.append(h2("5.2 Key Transaction Codes & Programs Matrix"))
    tc_matrix = [
        ["Transaction / Program", "Technical Name", "Core Purpose"],
        ["Transformation Cockpit", "/SNP/TC or /SNP/TE02", "Main UI for Data Objects, Selections, Rules, Mappings, Blocks."],
        ["Daemon Controller", "/SNP/TE01_DAEMON", "Starts background compiler and RFC worklist coordinators."],
        ["Validate Mappings", "/SNP/TE02_VALIDATE_MAPPINGS", "Pre-import validation scanning for unmapped source values."],
        ["Automated Block Runner", "/SNP/TE02_API_EXECUTE_BLOCKS", "API/CLI engine for scheduled background block runs."],
        ["Table Catalog to CSV", "/SNP/TE02_TABLES_TO_CSV", "Exports complete table catalogs and rules to CSV."],
        ["Data Object Builder", "/SNP/TF_CO_DOB_700_DIA_ALL", "Creates and configures Data Objects for custom Z* tables."],
        ["Foreign Key Check", "/SNP/TE02_FK_CHECK", "Validates referential integrity across imported target tables."]
    ]
    story.append(tbl(tc_matrix, [3.8*cm, 4.8*cm, 8.4*cm], first_bold=True))
    story.append(sp(8))

    story.append(good("<b>End of Document.</b> Master technical reference generated for SNP CrystalBridge Migration Architecture."))

    on_page = make_on_page("SNP CrystalBridge - Data Object Creation, Export, Import & Rules Guide")
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"Successfully generated: {pdf_filename}")

if __name__ == "__main__":
    create_guide_pdf()
