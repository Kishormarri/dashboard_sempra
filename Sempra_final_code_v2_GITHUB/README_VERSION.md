# Sempra DM Dashboard — Version 2: GITHUB PAGES

## Live URL
https://kishormarri.github.io/dashboard_sempra/

## GitHub Repo
https://github.com/Kishormarri/dashboard_sempra

## Purpose
Deployed on GitHub Pages — works fully online, no Python bridge needed.
Real Excel data is baked directly into the HTML at build time.

## How it Works
- Page opens → auto-login as Sempra Viewer (no password needed)
- Real DM1/DM2/DM3 data loads automatically from baked localStorage seed
- ⚡ Auto-Sync All Cycles button → full animation (DM1→DM2→DM3) with real data
- Every 2 minutes → auto-refresh runs automatically

## Data Baked In (from your Excel files)
| Cycle | Tables | Match % | Source |
|---|---|---|---|
| DM1 | 7,710 | 89% | `Reflist_m1.xlsx` + `DM1_ES2-SQ1 Export-Import.xlsx` |
| DM2 | 7,715 | 87% | `DM2 REF.xlsx` + `EXPORT IMPORT_DM2.xlsx` |
| DM3 | 7,751 | 87% | `ref dm31.xlsx` + `DM3 EXPORT IMPORT LOG_20261018.xlsx` |

## To Update Data on GitHub Pages
1. Put new Excel files in `C:\Users\KishorMarri\.bob\DM1\`, `DM2\`, `DM3\`
2. Run: `python bake_data.py`
3. Run: `python replace_placeholder.py`
4. Run: `git add index.html && git commit -m "update data" && git push origin main`
5. Wait ~2 min → live at the URL above

## Files
| File | Purpose |
|---|---|
| `index.html` | Main dashboard — GitHub Pages version with baked data |
| `Sempra_DM1_Dashboard.html` | DM1 individual level |
| `Sempra_DM2_Dashboard.html` | DM2 individual level |
| `Sempra_DM3_Dashboard.html` | DM3 individual level |
| `Sempra_CrossCycle_Summary_MASTER.html` | Cross-cycle summary |

## Key Differences from V1 LOCAL
| Feature | V1 Local | V2 GitHub |
|---|---|---|
| Data source | Live from C: drive via bridge | Baked into HTML at build time |
| Login | Password required | Auto-login (no password) |
| Auto-Sync | Reads live Excel files | Uses baked real data |
| Requires Python | Yes | No |
| Works offline | Yes (after bridge start) | Yes (fully static) |
