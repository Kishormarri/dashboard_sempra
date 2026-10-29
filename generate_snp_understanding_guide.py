"""
SNP CrystalBridge - Data Migration SAP ECC to S/4HANA
UNDERSTANDING GUIDE: concepts first, plain language, analogies, glossary, self-check.
Facts come from the SNP documents already used for the reference PDF; analogies are labelled as analogies.
Run: python generate_snp_understanding_guide.py
"""
from snp_common import *
from snp_common import _arrow
from reportlab.platypus import CondPageBreak
from reportlab.platypus import SimpleDocTemplate

OUT = "SNP_CrystalBridge_Understanding_Guide.pdf"


class NestDiagram(Flowable):
    """Scenario > Run > Block > Data object > Table, drawn as nested boxes."""
    def __init__(self, width=CONTENT_W):
        super().__init__(); self.w = width; self.h = 176

    def wrap(self, w, h): return (self.w, self.h)

    def draw(self):
        c = self.canv
        levels = [("SCENARIO", "the whole migration blueprint: systems, selections, mappings, objects", VIOLET),
                  ("RUN", "a named execution plan, for example Export or Import", BLUE),
                  ("BLOCK", "the executable unit (EXP, FOR, IMP, UPL, DEL) that holds data objects", TEAL),
                  ("DATA OBJECT", "one business entity, for example customer master or sales orders", CUSTC),
                  ("TABLES", "header and dependent tables, for example VBAK then VBAP (illustrative)", GREEN_C)]
        for i, (name, desc, col) in enumerate(levels):
            x = 12 * i; y = 8 * i; w = self.w - 24 * i; h = self.h - 28 * i
            c.setFillColor(colors.Color(col.red, col.green, col.blue, alpha=0.07))
            c.setStrokeColor(col); c.setLineWidth(1.2)
            c.roundRect(x, y, w, h, 6, stroke=1, fill=1)
            c.setFillColor(col); c.setFont("Helvetica-Bold", 8.5)
            c.drawString(x + 8, y + h - 14, name)
            nw = c.stringWidth(name, "Helvetica-Bold", 8.5)
            c.setFillColor(DARK); c.setFont("Helvetica", 7)
            c.drawString(x + 8 + nw + 8, y + h - 14, desc)


class TwoWayDiagram(Flowable):
    """Mission Control (plan) and Transformation Cockpit (engine) in plain words."""
    def __init__(self, width=CONTENT_W):
        super().__init__(); self.w = width; self.h = 96

    def wrap(self, w, h): return (self.w, self.h)

    def box(self, x, y, bw, bh, title, lines, col):
        c = self.canv
        c.setFillColor(colors.Color(col.red, col.green, col.blue, alpha=0.10))
        c.setStrokeColor(col); c.setLineWidth(1.3)
        c.roundRect(x, y, bw, bh, 5, stroke=1, fill=1)
        c.setFillColor(col); c.setFont("Helvetica-Bold", 8.5)
        c.drawCentredString(x + bw / 2, y + bh - 14, title)
        c.setFillColor(DARK); c.setFont("Helvetica", 7)
        for i, ln in enumerate(lines):
            c.drawCentredString(x + bw / 2, y + bh - 27 - i * 9.5, ln)

    def draw(self):
        c = self.canv; w = self.w; bw = 190; bh = 86
        self.box(0, 5, bw, bh, "MISSION CONTROL", ["The project manager", "Plans tasks, order, owners", "Presses the buttons for you", "Tracks status and tickets"], VIOLET)
        self.box(w - bw, 5, bw, bh, "TRANSFORMATION COCKPIT", ["The engine room", "Holds the scenario", "Moves and transforms the data", "Reports status back"], TEAL)
        _arrow(c, bw + 4, 62, w - bw - 4, VIOLET)
        c.setFont("Helvetica-Oblique", 7); c.setFillColor(MUTED)
        c.drawCentredString(w / 2, 67, "start block / run")
        _arrow(c, w - bw - 4, 30, bw + 4, TEAL)
        c.drawCentredString(w / 2, 20, "status, progress, errors")


story = []

# -- COVER -------------------------------------------------------------------------
cov = Table([[[
    p("SNP CrystalBridge", S("k", fontSize=11, leading=14, textColor=SKY, fontName="Helvetica-Bold")),
    sp(8),
    p("Understanding Guide<br/>ECC to S/4HANA Data Migration", COVER_TITLE),
    sp(6),
    p("What it is  |  Why it works this way  |  How the pieces fit  |  How to decide  |  Self-check", COVER_SUB),
    sp(16),
    tbl([["AUDIENCE", "BASED ON", "COMPANION DOCUMENTS"],
         ["New and existing members of the Sempra migration team",
          "Kyano MC Guide, User Guide 25.09, Module 5 v25.03, TC 19.03 decks",
          "Reference PDF (detail) and Worked Examples PDF (practice)"]],
        [5.0 * cm, 5.6 * cm, 4.6 * cm], hdr_bg=BLUE),
    sp(14),
    p(f"Prepared: {datetime.date.today().strftime('%B %Y')}  |  Sempra Migration Team  |  Version 1.0",
      S("x", fontSize=9, textColor=colors.HexColor("#94a3b8"), fontName="Helvetica")),
]]], colWidths=[CONTENT_W])
cov.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), NAVY),
    ("TOPPADDING", (0, 0), (-1, -1), 26), ("BOTTOMPADDING", (0, 0), (-1, -1), 26),
    ("LEFTPADDING", (0, 0), (-1, -1), 34), ("RIGHTPADDING", (0, 0), (-1, -1), 34),
]))
story += [cov, sp(12)]
story += [callout(
    "<b>How to read this guide.</b>  Product facts (tools, reports, defaults, behaviour) come from the SNP documents. "
    "Everyday analogies are marked <b>Analogy</b> - they are teaching aids, not SNP statements. Examples with numbers are "
    "marked <b>illustrative</b>. Anything about the Sempra landscape is " + TBC + " and has not been assumed. "
    "Read this guide first, then use the Worked Examples to practise, and the Reference PDF to look up detail.")]
story += [sp(8), h2("Contents")]
toc = [["1", "The Big Picture", "What the tool does and why, in one page"],
       ["2", "Who Does What", "Control, source, target, files; Mission Control versus Transformation Cockpit"],
       ["3", "The Building Blocks", "Scenario, run, block, data object, table"],
       ["4", "Following the Data", "The journey of a record in six steps"],
       ["5", "The Three Levers", "Selections, mapping and rules"],
       ["6", "The Tricky Topics, Simply", "Number ranges, forerunners, DKP, import modes, near-zero downtime"],
       ["7", "Decision Guide", "Which option should I choose"],
       ["8", "Common Mistakes", "What goes wrong and the habit that prevents it"],
       ["9", "Glossary", "Plain-language definitions"],
       ["10", "Self-Check", "Questions with answers, and where to go next"]]
story += [tbl([["#", "Section", "Content"]] + toc, [1.0 * cm, 5.0 * cm, 11.0 * cm], hdr_bg=NAVY), PageBreak()]

# -- 1 BIG PICTURE -------------------------------------------------------------------
story += [CondPageBreak(13 * cm)] + banner("01  The Big Picture", "What CrystalBridge does and why it is built this way")
story += [p("In one sentence: <b>CrystalBridge copies the selected business data out of the old SAP ECC system, changes it on the way so it fits "
            "the new S/4HANA system, loads it, and then proves that it arrived correctly.</b> The ECC source is read, never modified. "
            "All changes happen between the export and the import."), sp(2)]
story += [h2("1.1  Analogy: moving house")]
story += [p("<b>Analogy (not from SNP).</b> Think of a house move. You decide what goes, pack it, store the boxes safely, relabel and "
            "place things in the new house, and finally check nothing is missing. The migration has the same five stages."), sp(2)]
story += [FlowRow([
    ("PLAN", ["Decide scope,", "order and owners", "(Mission Control)"], VIOLET),
    ("PACK", ["Read source data", "by your selections", "(Export)"], CUSTC),
    ("BOXES", ["Compressed files", "kept as they are", "(Staging)"], AMBER),
    ("UNPACK", ["Relabel, apply", "rules, write to", "S/4 (Import)"], GREEN_C),
    ("INSPECT", ["Counts, keys,", "balances, tests", "(Validation)"], TEAL),
], height=66), p("Figure 1 - The five stages of a migration", CAPN), sp(2)]
story += [tbl([
    ["Moving house (analogy)", "In CrystalBridge", "Why it matters"],
    ["Inventory of what to take", "Selections and data objects", "Defines the scope; wrong scope means wrong data."],
    ["Packing the boxes", "Export block", "Source stays untouched, so you can repeat the export safely."],
    ["Boxes in the garage", "Export packages (compressed files)", "Files are never overwritten; a repeat run adds new files."],
    ["New labels on the boxes", "Mapping and rules", "Company code 1000 becomes 2000; formats and keys are adapted."],
    ["Placing items in the new house", "Import block", "The import mode decides what happens if an item already exists."],
    ["Checking the inventory list", "Validation (DCV, balances, tests)", "Evidence for sign-off."],
], [4.6 * cm, 5.4 * cm, 7.0 * cm], first_bold=True), sp(6)]
story += [h2("1.2  Five questions that explain the whole tool")]
story += [tbl([
    ["Question", "Answer in CrystalBridge", "Where you work"],
    ["What moves?", "Whatever your selections and data objects describe, for example company codes and fiscal years.", "Selections, Data Objects tabs"],
    ["How does it change on the way?", "Mapping tables and rules are applied between export and import.", "Mapping tab, Rules"],
    ["Where does it wait?", "In compressed export files (staging), not directly between systems.", "File system, Systems tab"],
    ["How do I run it?", "As runs made of blocks (export, import ...), by hand or from Mission Control.", "Runs and Blocks tabs"],
    ["How do I know it worked?", "Logs, record counts, foreign key checks, balance comparison, application tests.", "Log, DCV, validation tools"],
], [3.8 * cm, 9.0 * cm, 4.2 * cm], first_bold=True), sp(6)]
story += [good("<b>Why this design is safe.</b> Because the source is only read, the export is repeatable. Because files are never overwritten, "
               "every run is traceable. Because rules sit between export and import, you can correct a rule and re-import without "
               "touching the source again.")]
story += [CondPageBreak(8 * cm)]

# -- 2 WHO DOES WHAT -----------------------------------------------------------------
story += [CondPageBreak(13 * cm)] + banner("02  Who Does What", "The systems and the two main tools", TEAL, BLUE)
story += [h2("2.1  Four places in the landscape")]
story += [LandscapeDiagram(), p("Figure 2 - Control system, source, target and file system", CAPN)]
story += [tbl([
    ["Place", "Think of it as", "What happens there", "Typical contact"],
    ["Control system", "Command centre", "Hosts Mission Control and the Transformation Cockpit, the rule base and the shadow DDIC. Generates the export and import programs and watches them run.", "Migration lead, technical consultant"],
    ["Source (SAP ECC)", "The old house", "Generated export programs read the data. Nothing is changed.", "Basis, functional team"],
    ["Target (S/4HANA)", "The new house", "Generated import programs write the data; mapping and rules are applied; post-processing runs here.", "Basis, functional team"],
    ["File system", "The garage", "Holds the compressed export packages between export and import.", "Basis"],
], [2.8 * cm, 2.6 * cm, 8.2 * cm, 3.4 * cm], first_bold=True), sp(4)]
story += [p("The systems talk to each other through RFC connections. Every connection must be on the RFC whitelist of all systems and clients "
            "(maintained in " + mono("/SNP/TCSYS") + "). Sempra values for system IDs, clients and hosts are " + TBC + ".")]

story += [PageBreak(), h2("2.2  Mission Control and the Transformation Cockpit")]
story += [TwoWayDiagram(), p("Figure 3 - The plan and the engine", CAPN)]
story += [tbl([
    ["", "Mission Control (/N/SNP/MC)", "Transformation Cockpit (/N/SNP/TC)"],
    ["Main job", "Plan and orchestrate the project: tasks, dependencies, owners, templates (units).", "Do the data work: scenarios, selections, mappings, rules, runs and blocks."],
    ["Unit of work", "A task (manual, report in dialog, report in background, or summary).", "A block inside a run."],
    ["Status", "Task status and tickets; a task is Blocked until its tickets are resolved.", "Run and block status such as Running, Completed or Crashed."],
    ["Needs", "A licensed project; no extra transports or RFC settings.", "Transports and RFC whitelist on the systems."],
], [2.6 * cm, 7.2 * cm, 7.2 * cm], first_bold=True), sp(4)]
story += [p("<b>How they connect.</b> There is no magic link: a Mission Control task contains a small configuration that calls a cockpit API "
            "report (for example " + mono("/SNP/TE02_API_EXECUTE_BLOCKS") + ") and passes the scenario ID from the project variable " +
            mono("TC_SCENARIO") + ". A refresh class reads the cockpit status back into the task and can create tickets automatically.")]
story += [h2("2.3  The other CrystalBridge parts in one line each")]
story += [tbl([
    ["Part", "One-line meaning"],
    ["CrystalBridge Analysis (AN)", "Looks at the old system before the project: structure, usage, customizing, custom code, interfaces."],
    ["Data Consistency Verification (DCV)", "After the load, checks foreign keys and domain fixed values to find broken references."],
    ["Rule-Based Near-Zero Downtime (RBNZD)", "Moves most data while the source is live and only a small last delta during the cutover."],
    ["Shell Creator (SHC)", "Creates the system shell used as basis for the target in the Bluefield approach."],
], [5.2 * cm, 11.8 * cm], first_bold=True)]
story += [CondPageBreak(8 * cm)]

# -- 3 BUILDING BLOCKS -----------------------------------------------------------------
story += [CondPageBreak(21 * cm)] + banner("03  The Building Blocks", "Scenario, run, block, data object, table", BLUE, CUSTC)
story += [p("Everything in the cockpit sits inside the next bigger thing. Learn this nesting once and the screens make sense."), sp(2)]
story += [NestDiagram(), p("Figure 4 - The nesting from scenario down to tables", CAPN)]
story += [tbl([
    ["Level", "What it is", "What you decide here", "Typical mistake"],
    ["Scenario", "The complete blueprint, identified by a unique ID of up to 30 characters.", "Source and target systems, scope, which objects.", "Reusing one scenario for unrelated purposes."],
    ["Run", "A named execution plan.", "Which blocks belong together and in which order.", "Starting the wrong run in the wrong system."],
    ["Block", "The unit that actually executes. Types: EXP export, FOR forerunner, IMP import, UPL upload, DEL deletion.", "Parallel processes, package size, import mode, sequence.", "Forgetting that import uses the last export unless you pick another."],
    ["Data object", "A business entity at table level with its table hierarchy, for example sales orders.", "Which objects are in the block; per table the export method and import mode.", "Skipping the table analysis first."],
    ["Table", "One DDIC table inside the object, header or dependent.", "How it connects to its parent, selections, rules.", "Wrong connection key, so wrong rows are read."],
], [2.2 * cm, 5.4 * cm, 5.2 * cm, 4.2 * cm], first_bold=True), sp(6)]
story += [h2("3.1  Header and dependent tables")]
story += [p("A data object is a small family tree of tables. The <b>header (start) table</b> is selected by your scope; each "
            "<b>dependent table</b> is found through its key connection to the parent. This is why a correct selection on the header "
            "automatically brings the right items along."), sp(2)]
story += [tbl([
    ["Concept", "Plain explanation", "Detail"],
    ["Start table", "The table your selections apply to.", "Dependent tables read relative to it."],
    ["Connection", "The key fields that link child rows to parent rows.", "Maintained per table in the data object."],
    ["Scout Reader (SR)", "Default. Reads dependent rows for the keys already exported (FOR ALL ENTRIES).", "Dependent tables start after the parent and use its last export."],
    ["Direct Reader (DR)", "Reads with a join instead; independent of the parent export.", "Starts with exactly one process; a restart means a full re-export."],
], [3.2 * cm, 7.2 * cm, 6.6 * cm], first_bold=True), sp(4)]
story += [warn("<b>Prerequisite.</b> Run the <b>Table Analysis</b> first (it fills " + mono("/SNP/CE00TABINFO") + "). Data objects cannot be processed without it.")]
story += [CondPageBreak(8 * cm)]

# -- 4 FOLLOWING THE DATA ----------------------------------------------------------------
story += [CondPageBreak(20 * cm)] + banner("04  Following the Data", "The journey of a record in six steps", TEAL, GREEN_C)
story += [FlowRow([
    ("1 SELECT", ["Define scope", "company code,", "fiscal year"], VIOLET),
    ("2 EXPORT", ["Read source,", "write compressed", "packages"], CUSTC),
    ("3 PACKAGES", ["Raw values kept", "never overwritten"], AMBER),
    ("4 TRANSFORM", ["Mapping and", "rules applied", "on the way in"], TEAL),
    ("5 IMPORT", ["Write to S/4", "per import mode", "and sequence"], GREEN_C),
    ("6 CHECK", ["DCV, counts,", "balances,", "tests"], RED_C),
], height=66), p("Figure 5 - The journey of a record", CAPN), sp(2)]
story += [tbl([
    ["Step", "What happens", "Why it is done this way", "What can go wrong"],
    ["0  Prepare", "Table analysis, validation of selections, mappings and objects, DDIC analysis, syntax check.", "Errors found before a run cost minutes; found in a run they cost hours.", "Skipping validation, then failing mid-run on a missing mapping."],
    ["1  Select", "Selections limit which rows are read: global selections by domain, or field selections on one table.", "Reusable scope: one company code selection works in every table with that field.", "A field selection with no value exports the whole table; a global selection with no value transfers no records."],
    ["2  Export", "Export programs on the source read by selection and write packages.", "Source is only read, so the export can be repeated.", "Source locks or load on busy systems; wrong reader for a huge dependent table."],
    ["3  Packages", "Compressed files stored per scenario, block and table. A restart exports only failed tables.", "Decouples source from target; allows re-import without re-export.", "Deleting a block deletes its files; choosing the wrong export for the import."],
    ["4  Transform", "Value mappings, global and field rules, events, derivations.", "Business changes are applied once, centrally, and are traceable.", "Unmapped value; a rule that skips the wrong record."],
    ["5  Import", "Programs on the target read the packages and write per import mode and sequence.", "Mode decides behaviour for keys that already exist.", "Insert onto existing keys terminates; Modify, Update or Delete used without agreement."],
    ["6  Check", "Compare counts and keys, foreign key checks, balance comparison, application tests.", "Proves completeness and consistency for sign-off.", "Comparing without accounting for mapped values."],
], [1.9 * cm, 5.0 * cm, 5.0 * cm, 5.1 * cm], first_bold=True), sp(6)]
story += [h2("4.1  What runs where")]
story += [tbl([
    ["Block type", "Runs on", "Plain meaning"],
    ["EXP export", "Source", "Pack the data."],
    ["FOR forerunner", "Target", "Rehearsal that only builds mapping entries; nothing is written to the data tables."],
    ["IMP import", "Target", "Unpack and write the data."],
    ["UPL upload", "Target side", "Load a CSV file into a table."],
    ["DEL deletion", "Target", "Clean-up block created from an import block after successful execution."],
], [3.6 * cm, 2.6 * cm, 10.8 * cm], first_bold=True), sp(6)]
story += [h2("4.2  Running options in plain words")]
story += [tbl([
    ["Option", "Plain meaning", "When"],
    ["Simulation", "Do everything except write to the database.", "Before the first real import of a block."],
    ["Restart", "Continue a failed block from the last good package.", "After fixing the cause."],
    ["Reset", "Clear status and intermediate results.", "Only when a complete re-run is intended."],
    ["Background mode", "Run as a background job.", "Production; dialog only for testing and debugging."],
], [3.2 * cm, 8.0 * cm, 5.8 * cm], first_bold=True)]
story += [CondPageBreak(8 * cm)]

# -- 5 THREE LEVERS ------------------------------------------------------------------------
story += [CondPageBreak(20 * cm)] + banner("05  The Three Levers", "Selections, mapping and rules: how you steer the result", VIOLET, BLUE)
story += [h2("5.1  Selections: what goes")]
story += [tbl([
    ["Type", "Plain meaning", "Use when"],
    ["Global selection", "One list of values for a field type, for example company codes; applies to every table with that field.", "Scope that must be identical everywhere."],
    ["Field selection", "A condition on one field of one table.", "A special filter for a single table."],
    ["Declarative (default)", "Conditions are combined with AND.", "Normal case, recommended."],
    ["Free / SQL expert", "You write the condition, including OR and NOT.", "Complex cases only; switching back to declarative loses assigned selections."],
], [3.8 * cm, 8.4 * cm, 4.8 * cm], first_bold=True), sp(4)]
story += [p("Ranges use four parts: sign, option, low, high. Examples from the SNP guide: " + mono("IEQ1000") + " include equal 1000; " +
            mono("ICP100*") + " include pattern; " + mono("IBT10002000") + " include between; " + mono("EEQ9999") + " exclude equal.")]
story += [h2("5.2  Mapping: what changes")]
story += [p("A mapping table translates a source value into a target value. Source data is never changed; the translation happens during the transformation."), sp(2)]
story += [tbl([
    ["Pattern", "Plain meaning", "Example from the guide"],
    ["1:1", "One source value to one target value.", "WERKS 1000 to 1001"],
    ["N:1", "Several source values merge into one target value.", "WERKS 1000 and 2000 to 2001"],
    ["1:N", "One source value to several targets. Not allowed: it causes an error.", "WERKS 1000 to 1001 and 2001"],
    ["X+N:1 (dependent)", "Two source fields together decide one target value.", "WERKS + LGORT to LGORT"],
], [3.6 * cm, 7.6 * cm, 5.8 * cm], first_bold=True), sp(4)]
story += [tbl([
    ["Mapping layer", "Plain meaning"],
    ["Global mapping", "One rule for every field of the same domain, data element or table field."],
    ["Field mapping", "Only one table field; overrides the global mapping."],
    ["Value mapping", "Known value to known value; wildcards and ranges; bulk CSV upload."],
    ["Derivation", "ABAP logic works out the target from other fields."],
    ["Hard-coded / default", "Always a fixed value / a value only when the source field is initial."],
], [4.2 * cm, 12.8 * cm], first_bold=True), sp(4)]
story += [good("<b>Remember.</b> More specific mapping entries win over wildcards. A field that has no import rule is transferred 1:1. "
               "Values are case-sensitive. Validate mappings before every run with " + mono("/SNP/TE02_VALIDATE_MAPPINGS") + ".")]
story += [h2("5.3  Rules and events: what logic runs")]
story += [p("Rules are small ABAP routines that fire at defined moments, called <b>events</b>. Export events run on the source side; import events on the "
            "target side. A global rule applies to every field of a domain; a field rule overrides it for one field."), sp(2)]
story += [tbl([
    ["Moment", "Typical use"],
    ["Before / after table", "Prepare or finish something for the whole table, for example clear an own table."],
    ["Before / after package", "Work on a batch of records, for example insert collected values."],
    ["Before / after data record", "Inspect or change one record; set EV_SKIP to skip it."],
    ["Global export / import rule", "Change a value for every field of a domain, for example the client or the logical system."],
], [4.6 * cm, 12.4 * cm], first_bold=True), sp(4)]
story += [p("Changes made in an earlier event are visible in later events of the same cycle. See the Worked Examples for a rule in action.")]
story += [CondPageBreak(8 * cm)]

# -- 6 TRICKY TOPICS ------------------------------------------------------------------------
story += [CondPageBreak(13 * cm)] + banner("06  The Tricky Topics, Simply", "Each one: in plain words, why it exists, what to remember", RED_C, BLUE)
tricky = [
    ["Number ranges",
     "Documents have numbers from a number range. If the target already uses numbers, copying old numbers could clash.",
     "Strategy per range: Increment (new numbers via NUMBER_GET_NEXT, mappings record old and new), Difference calculation (new = old + an NRIV offset, much faster), "
     "1:1 for internal ranges (numbers adopted), Inactive for external ranges.",
     "Save NRIV before, Update NRIV before import. API_NUMBER_GET_NEXT returns sy-subrc 0 when the offset calculated the value and 4 when NUMBER_GET_NEXT generated it."],
    ["Forerunner (FOR)",
     "A rehearsal block that only builds the mapping for key fields, so later blocks that point to those keys can use the mapping.",
     "It runs after the export and before the import, imports in simulation mode with one process per file and writes nothing to the data tables.",
     "The linked objects must have been exported successfully."],
    ["Duplicate Key Prevention (DKP)",
     "A safety switch that stops duplicates when the parent selection table has more key fields than the connection uses.",
     "It forces one process per table and logs every exported record, so it is slow.",
     "Avoid it with the Direct Reader, a corrected object structure, or a unique selection on the missing key field."],
    ["Import modes",
     "What to do when the key already exists in the target.",
     "Insert (error), Insert ADK (skip), Update (change non-key fields only), Modify (update or insert), Delete (remove by key).",
     "Agree with the business which records are kept before using anything other than Insert. See Worked Example 4."],
    ["Address object",
     "Addresses are shared by many objects, so they are collected by number.",
     "Address numbers are collected by global export rules for domains such as ADRNR; export the address object last and import it first.",
     "Wrong order leaves objects pointing to addresses that do not exist yet."],
    ["Near-zero downtime (RBNZD)",
     "Most data is moved while the source is still live.",
     "Initial load, then several delta loads that shrink each time, then a short final delta at cutover. Triggers on the source record the changes.",
     "Triggers must be on before the initial load; lock number ranges before each delta import."],
    ["Staging manager",
     "A way to prepare or check data in the target without disturbing live tables.",
     "Type D (DDIC): shadow tables switched by renaming. Type C (client): clients AAA to ZZZ.",
     "Use cases include downtime minimisation, recycle bin, foreign key check without writing."],
]
story += [tbl([["Topic", "In plain words", "How it works", "Remember"]] + tricky, [2.6 * cm, 4.2 * cm, 5.6 * cm, 4.6 * cm], first_bold=True), sp(6)]
story += [warn("<b>Training decks versus guide.</b> Several details (forerunners, number-range strategies, offsets) are shown in the 19.03 training decks. "
               "Check release-specific behaviour against the 25.09 user guide before relying on it.")]
story += [CondPageBreak(8 * cm)]

# -- 7 DECISION GUIDE -------------------------------------------------------------------------
story += [CondPageBreak(13 * cm)] + banner("07  Decision Guide", "Which option should I choose?", GREEN_C, BLUE)
story += [tbl([
    ["Situation", "Start with", "Switch when", "Why"],
    ["Normal parent and child tables", "Scout Reader, import mode Insert", "A huge dependent table is slow", "Default is restartable per table; Direct Reader uses a join but one process and full re-export."],
    ["Selection scope for many tables", "Global selection", "One table needs a special filter", "Global is reusable; field selection is local."],
    ["Org unit changes (company code, plant)", "Global mapping object", "One field behaves differently", "Field mapping overrides global."],
    ["A value needs logic", "Derivation or field rule", "Pure lookup is enough", "Lookups are easier to maintain than code."],
    ["Target already has documents", "Number-range strategy Difference calculation", "Offset result is not valid", "Faster; falls back to NUMBER_GET_NEXT."],
    ["Mapping needed before the main import", "Forerunner object", "No linked key domains", "Builds mapping, writes no data."],
    ["First import of a block", "Simulation", "After simulation is clean", "No data written; shows key and duplicate problems."],
    ["Records may exist in target", "Insert ADK or Modify (by agreement)", "Business wants an overwrite or skip", "Insert would terminate on duplicates."],
    ["Test again after a failure", "Restart", "Cause needs a full re-extraction", "Restart continues from the last good package; Reset clears status."],
    ["Large volume, short downtime", "RBNZD delta loads", "Volume is small", "Only the last delta needs downtime."],
    ["Back up target tables before transformation", "RET scenario (save, reset, restore)", "Not needed", "Source equals target; export is the backup, restore imports it with mode INSERT."],
], [4.0 * cm, 4.0 * cm, 3.6 * cm, 5.4 * cm], first_bold=True), sp(6)]
story += [callout("This is a decision aid built from the SNP documents. It is not a mandatory SNP procedure; confirm choices for Sempra objects in the design workshops.")]
story += [h2("7.1  Questions to ask before any run")]
story += [tbl([
    ["#", "Question", "If the answer is no"],
    ["1", "Is the table analysis current?", "Run /SNP/TE02_UPDATE_TABLE_INFO."],
    ["2", "Are selections, mappings and objects validated?", "Run the three validation reports."],
    ["3", "Is the syntax check clean?", "Run /SNP/TE02_API_EXEC_SYNTAX_CHK."],
    ["4", "Do I know which export the import will read?", "Select the export explicitly."],
    ["5", "Do I know what the import mode does to existing keys?", "Check section 6 and Example 4."],
    ["6", "Are number ranges saved and updated?", "Save NRIV, then Update NRIV."],
    ["7", "Is simulation done for new or changed blocks?", "Simulate first."],
], [0.9 * cm, 8.6 * cm, 7.5 * cm]), CondPageBreak(8 * cm)]

# -- 8 COMMON MISTAKES --------------------------------------------------------------------------
story += [CondPageBreak(13 * cm)] + banner("08  Common Mistakes", "What goes wrong and the habit that prevents it", AMBER, RED_C)
story += [tbl([
    ["Mistake", "What happens", "Habit that prevents it"],
    ["Empty field selection assumed to mean nothing", "A field selection with no value exports the whole table.", "Check every field selection before each export."],
    ["Empty global selection assumed to mean everything", "A global selection with no value transfers no records.", "Open the selection overview before the run."],
    ["Unmapped source value", "Import fails with no target value found.", "Validate mappings; add the value; regenerate blocks."],
    ["Switching free selection back to declarative", "All assigned selections are lost.", "Decide the mode early; document it."],
    ["Using Insert when keys exist", "Import terminates with a duplicate key error.", "Choose the mode by agreement; simulate."],
    ["Using Modify, Update or Delete casually", "Unintended overwrite or loss in the target.", "Restrict to named blocks; get sign-off."],
    ["Ignoring the table analysis", "Data objects cannot be processed.", "Make it a standing prerequisite."],
    ["Closing a ticket as ignored", "Status becomes Erroneous; later tasks may fail.", "Fix or document; use FIXED or NO_CHANGE with a comment."],
    ["Forgetting that deleting a block deletes its files", "Export no longer available for import.", "Copy runs for a new cycle instead of deleting."],
    ["Debugging with parallel processes", "The debugger does not stop.", "Debug in dialog with one process."],
    ["Cleaning up after deletion carelessly", "The transformation tree is the transformation history.", "Clean up only after the deletion is verified."],
    ["Skipping the RFC whitelist", "Connection failures at execution.", "Maintain /SNP/TCSYS on all systems and clients; test the connection."],
], [4.8 * cm, 5.4 * cm, 6.8 * cm], first_bold=True), sp(6)]
story += [h2("8.1  How to think when something fails")]
for s in ["<b>Where did it stop?</b> Mission Control task, cockpit run, block, or table. Use the log tab and /SNP/TCPROT.",
          "<b>Was it the data or the setup?</b> Setup problems show in the validation reports; data problems show as table-level errors.",
          "<b>Can I restart?</b> Restart continues from the last good package. Reset clears status; use it only when a full re-run is intended.",
          "<b>What changed since the last good run?</b> Mapping, selection, rule or a new source value. Re-validate before re-running.",
          "<b>Who must know?</b> Tickets in Mission Control block the task until resolved; make sure the owner sees them."]:
    story.append(bul(s))
story += [CondPageBreak(8 * cm)]

# -- 9 GLOSSARY ------------------------------------------------------------------------------------
story += [CondPageBreak(13 * cm)] + banner("09  Glossary", "Plain-language definitions in alphabetical order", NAVY, BLUE)
gl = [
    ["Alias (system)", "A short unique name for a system in a scenario; needed when more than one source system is used."],
    ["API call", "A function you can call inside a rule, for example API_MAPPING_ADD or API_SELECTION_ADD."],
    ["Block", "The executable unit of a run. Types EXP, FOR, IMP, UPL, DEL."],
    ["Bluefield", "Selective migration of chosen entities into a S/4HANA system; combines Greenfield and Brownfield ideas."],
    ["Brownfield", "Converting the existing system to S/4HANA."],
    ["Control system", "The system that hosts Mission Control, the cockpit, the rule base and the shadow DDIC."],
    ["Data object", "A business entity at table level, including its table hierarchy."],
    ["DCV", "Data Consistency Verification: foreign key and fixed value checks after the load."],
    ["DDIC", "SAP Data Dictionary; the shadow DDIC is a copy used for generating programs."],
    ["Derivation", "A rule that works out a target value from other fields."],
    ["Direct Reader (DR)", "Export method using a join; independent of the parent export."],
    ["DKP", "Duplicate Key Prevention; a safety mechanism that slows the export."],
    ["Event", "A defined moment (before table, after record ...) where a rule can run."],
    ["Export / import", "Writing source data to packages / reading packages into the target."],
    ["Forerunner (FOR)", "A block that builds mapping entries without writing data."],
    ["Global selection", "A reusable list of values applied to all tables with a matching field."],
    ["Greenfield", "A new S/4HANA implementation; usually master data and open items only."],
    ["Mapping", "Translation of source values into target values."],
    ["Mission Control", "Project and task orchestration tool (/N/SNP/MC)."],
    ["NRIV", "SAP number range table; CrystalBridge saves, checks and updates its levels."],
    ["Package", "A compressed export file with a limited number of records or size."],
    ["RBNZD", "Rule-Based Near-Zero Downtime."],
    ["RET scenario", "A scenario where source equals target, used to save, reset and restore tables."],
    ["RFC whitelist", "List of permitted RFC connections, maintained in /SNP/TCSYS."],
    ["Run", "A named execution plan made of blocks."],
    ["Scenario", "The complete migration blueprint."],
    ["Scout Reader (SR)", "Default export method using FOR ALL ENTRIES."],
    ["Simulation", "Execution without writing to the database."],
    ["Staging", "Holding data in packages (or shadow tables) between export and import."],
    ["Ticket", "A Mission Control record of a warning or error that blocks the task until resolved."],
    ["Transformation Cockpit", "The engine room tool (/N/SNP/TC)."],
    ["Unit", "A Mission Control project template."],
    ["XPRA / XCLA / SDM", "Post-processing programs on the target after import."],
]
story += [tbl([["Term", "Meaning"]] + gl, [4.0 * cm, 13.0 * cm], first_bold=True), CondPageBreak(8 * cm)]

# -- 10 SELF CHECK ---------------------------------------------------------------------------------
story += [CondPageBreak(13 * cm)] + banner("10  Self-Check", "Test yourself, then see where to go next", GREEN_C, BLUE)
qa = [
    ["1", "Is the ECC source changed by a migration?", "No. It is only read; all changes happen between export and import."],
    ["2", "Where does data wait between export and import?", "In compressed export packages on the file system; files are never overwritten."],
    ["3", "What links a Mission Control task to a cockpit scenario?", "Configuration: the scenario ID in variable TC_SCENARIO and the API report parameters P_SCEN, S_RUN, S_BLOCK. No linking table is named in the SNP documents."],
    ["4", "Name the five block types.", "EXP, FOR, IMP, UPL, DEL."],
    ["5", "What does a field selection with no value do?", "It exports the whole table. A global selection with no value transfers no records."],
    ["6", "Why validate mappings before a run?", "To find source values without a target value; otherwise the import fails."],
    ["7", "What is a 1:N mapping?", "One source value with several targets. It causes an error."],
    ["8", "Which import mode skips existing keys without error?", "Insert ADK."],
    ["9", "What does a forerunner write to the data tables?", "Nothing. It only creates the mapping."],
    ["10", "What does API_NUMBER_GET_NEXT return in sy-subrc?", "0 when the value was calculated from the NRIV offset, 4 when NUMBER_GET_NEXT generated it."],
    ["11", "In which order are addresses handled?", "Export the address object last, import it first."],
    ["12", "What shrinks the downtime in RBNZD?", "Repeated delta loads; only the final delta runs during cutover."],
]
story += [tbl([["#", "Question", "Answer"]] + qa, [0.9 * cm, 6.6 * cm, 9.5 * cm]), sp(8)]
story += [h2("10.1  Where to go next")]
story += [tbl([
    ["If you want to ...", "Go to"],
    ["Practise with concrete values", "Worked Examples PDF (mapping, selections, import modes, number ranges, rules, offsets, RET, Mission Control, troubleshooting)."],
    ["Look up a report, role, parameter or default", "Reference PDF, sections 2 to 14."],
    ["Fill in the Sempra landscape", "Reference PDF, section 2.3 and 2.4 (all fields are " + TBC + ")."],
], [5.2 * cm, 11.8 * cm], first_bold=True), sp(8)]
story += [h2("10.2  Open items")]
story += [tbl([
    ["#", "Open item", "Status"],
    ["1", "Sempra landscape: SIDs, releases, clients, volumes, company codes, dates", TBC],
    ["2", "Whether carve-out content (Module 5 title) should be emphasised for Sempra", TBC],
    ["3", "Further SNP documents to fold in", TBC],
], [0.9 * cm, 12.6 * cm, 3.5 * cm]), sp(10)]
story += [callout("<b>Sources:</b> Kyano Mission Control Complete Reference Guide; CrystalBridge Transformation User Guide 25.09 SP00; Module 5 "
                  "Transformation Advanced (v25.03); Transformation Cockpit SNP2 and Advanced SNP3 training decks (19.03 SP00). "
                  "Analogies are teaching aids. Document generated with IBM Bob.")]

doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm,
                        topMargin=1.8 * cm, bottomMargin=2.0 * cm,
                        title="SNP CrystalBridge Understanding Guide - ECC to S/4HANA",
                        author="Sempra Migration Team")
f = make_on_page("SNP CrystalBridge Understanding Guide - ECC to S/4HANA  |  Sempra Migration Team")
doc.build(story, onFirstPage=f, onLaterPages=f)
print(f"Created {OUT}")




