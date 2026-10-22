# Sempra SAP Data Migration Dashboard — v1.0

> **Self-contained, browser-based tracking system for 3-cycle SAP data migrations (DM1 → DM2 → DM3).**
> One Python bridge serves local Excel files to the browser. No cloud. No login. No licences.

---

## What It Does

This dashboard is a live reconciliation scorecard for SAP data migration cycles.
It reads your migration Excel files, deduplicates Export/Import records using a
`DISTINCT` algorithm, and shows — for each cycle — how many SAP tables migrated
correctly, how many are mismatched, and how many are still outstanding.

**Key numbers:**
- **3** migration cycles tracked simultaneously (DM1, DM2, DM3)
- **< 10 seconds** to sync all three cycles with one button click
- **0** manual steps — fully automated once launched
- **100%** local — no data ever leaves your machine

---

## Prerequisites

| Requirement | Version | Check |
|---|---|---|
| Python | 3.8+ | `python --version` |
| pip packages | — | `pip install flask flask-cors openpyxl pandas xlrd reportlab fpdf2 python-docx` |
| Browser | Chrome 90+ or Edge 90+ | — |
| OS | Windows (paths use backslashes) | — |

---

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/Kishormarri/dashboard_sempra.git
cd dashboard_sempra

# 2. One-Click Launch (Windows)
Double-click INSTALL_AND_RUN.bat

# OR run manually via CLI:
pip install -r requirements.txt
python launch_dashboard.py
```

The launcher will:
1. Start the **File Bridge** on `http://localhost:5002`
2. Start a **static HTTP server** on `http://localhost:5003`
3. Open `http://localhost:5003/Sempra_CrossCycle_Summary_MASTER.html` in your browser automatically

> **Important:** Always open via `http://localhost:5003/` — never by double-clicking the HTML file.
> The file:// protocol blocks the bridge fetch calls (CORS).

---

## Data Files — Where to Place Them

The bridge reads Excel files from these paths by default. Create the folders and drop your files in:

```
C:\Users\<YOUR_USERNAME>\.bob\DM1\Reflist_m1.xlsx
C:\Users\<YOUR_USERNAME>\.bob\DM1\DM1_ES2-SQ1 Export-Import.xlsx
C:\Users\<YOUR_USERNAME>\.bob\DM2\DM2 REF.xlsx
C:\Users\<YOUR_USERNAME>\.bob\DM2\EXPORT IMPORT_DM2.xlsx
C:\Users\<YOUR_USERNAME>\.bob\DM3\ref dm3.xlsx
```

**To change the paths** (if your folder structure is different):
Open `automation/file_watcher_bridge.py` and edit the `DEFAULT_CONFIG` block near the top:

```python
DEFAULT_CONFIG = {
    "DM1": {"ref_path": r"C:\YOUR\PATH\DM1", "exp_path": r"C:\YOUR\PATH\DM1", ...},
    "DM2": {"ref_path": r"C:\YOUR\PATH\DM2", "exp_path": r"C:\YOUR\PATH\DM2", ...},
    "DM3": {"ref_path": r"C:\YOUR\PATH\DM3", "exp_path": r"C:\YOUR\PATH\DM3", ...},
}
```

> **Note:** Data files (`.xlsx`, `.csv`) are excluded from this repo via `.gitignore`.
> They contain migration data and should never be committed to version control.

---

## How to Use

1. Click **⚡ Auto-Sync All Cycles** in the top toolbar
2. Watch three coloured circles (blue/purple/green) spin as each cycle syncs
3. All three cycle cards update with match %, table counts, and status badges
4. Switch between **Business / Technical / Performance** tabs for different views
5. Click **DM1 / DM2 / DM3** nav buttons to drill into per-table detail

Results auto-refresh every **2 minutes**. Results also persist in `localStorage` across page reloads.

---

## Project Structure

```
sempra-dm-dashboard/
│
├── Sempra_CrossCycle_Summary_MASTER.html   # Main dashboard — 3 cycles, all views
├── Sempra_DM1_Dashboard.html               # DM1 per-table detail
├── Sempra_DM2_Dashboard.html               # DM2 per-table detail
├── Sempra_DM3_Dashboard.html               # DM3 per-table detail (REF-only mode)
│
├── launch_dashboard.py                     # One-click launcher
├── README.md
│
├── automation/
│   ├── file_watcher_bridge.py              # File bridge — port 5002 (REQUIRED)
│   ├── sap_bridge.py                       # SAP RFC bridge — port 5001 (optional)
│   ├── 01_sap_source_count.py              # Batch SAP source count extractor
│   ├── 02_target_count.py                  # Batch target count extractor
│   └── 03_orchestrator.py                  # Full pipeline orchestrator
│
├── generate_pdf_proper.py                  # Regenerates the professional PDF docs
└── generate_docs.py                        # Regenerates Word + basic PDF docs
```

---

## Colour & Status Key

| Colour | Meaning |
|---|---|
| 🟢 **Green** | Fully reconciled — Source = Target AND EXP count = IMP count |
| 🟡 **Amber** | Migration in progress or source/target mismatch |
| 🔴 **Red** | EXP ≠ IMP record count, or table not migrated |
| ⬜ **Grey** | No data loaded yet / table excluded |
| 🔵 **Blue** | DM1 Cycle 1 brand colour |
| 🟣 **Purple** | DM2 Cycle 2 brand colour |
| 🟢 **Green** | DM3 Cycle 3 brand colour |

---

## Architecture

```
Browser  (HTML + Vanilla JS + SheetJS v0.18.5)
    │
    │  GET http://localhost:5002/file?cycle=DM1&type=ref
    │  ← gzip-compressed .xlsx bytes (ETag caching)
    ▼
file_watcher_bridge.py   (Flask, port 5002)
    │  In-memory cache + gzip + ETag/304 support
    │
    │  reads raw bytes from disk
    ▼
Local Excel files   (.xlsx)
```

- **No data ever leaves the machine** — all servers bind to `127.0.0.1`
- **SheetJS** parses Excel entirely in the browser — no server-side parsing
- **localStorage** persists last results across reloads without re-syncing
- **Dynamic bridge URL** — uses `window.location.hostname`, works on any IP

---

## Optional: SAP Live Counts (sap_bridge.py)

If you have SAP RFC access (`pyrfc` installed), run the SAP bridge for live SE16N-style table counts:

```bash
pip install pyrfc   # requires SAP NW RFC SDK — see PyRFC docs
python automation/sap_bridge.py
```

This starts a local API at `http://localhost:5001` with three fallback methods:
1. `EM_GET_NUMBER_OF_ENTRIES` (SE16N internal FM — fastest)
2. `RFC_READ_TABLE` (standard fallback)
3. `BBP_RFC_READ_TABLE` (alternative fallback)

Without `pyrfc` it runs in **demo mode** with deterministic simulated counts for testing.

---

## Regenerate Documentation

```bash
# Professional PDF (ReportLab — 16 pages, full colour)
python generate_pdf_proper.py

# Word + basic PDF
python generate_docs.py
```

---

## Adapting for a Different Project

1. **File paths** — edit `DEFAULT_CONFIG` in `automation/file_watcher_bridge.py`
2. **Column indices** — edit `COL_TABLE`, `COL_SRC`, `COL_TGT` constants at the top of each dashboard `<script>` block
3. **Cycle labels** — edit the `CYCLES` array and `_bgRunCycle` paths in `Sempra_CrossCycle_Summary_MASTER.html`

---

## Release Notes — v1.0

- Full 3-cycle background automation (no iframe, no page navigation)
- DISTINCT deduplication fix across all 6 aggregation points (EXP/IMP double-count eliminated)
- REF-only mode with animated amber "Migration In Progress" banner (DM3)
- Sync status circles in toolbar — non-disruptive, auto-hide after 5s
- All disruptive popup panels removed — replaced with inline badge boxes
- Rainbow sweep animation on Auto-Sync button while running
- SE16N 3-method fallback chain in SAP bridge
- Colour-coded Excel export from SAP bridge (/export_excel endpoint)
- Dynamic bridge URL (window.location.hostname) — works on any machine/IP
- Auto-refresh 2-minute countdown with pause/resume
- Professional 16-page PDF documentation (ReportLab)

---

## License

Internal use only — Sempra Energy IT Programme.