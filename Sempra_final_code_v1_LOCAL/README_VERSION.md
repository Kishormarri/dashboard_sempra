# Sempra DM Dashboard — Version 1: LOCAL

## Purpose
Run on your own PC with the Python bridge reading Excel files from your C: drive.

## How to Run
1. Double-click `INSTALL_AND_RUN.bat`  
   OR manually:
   ```
   python automation/file_watcher_bridge.py
   ```
2. Open `index.html` in your browser

## Data Source
- Bridge reads Excel files from: `C:\Users\KishorMarri\.bob\DM1\`, `DM2\`, `DM3\`
- Port: `localhost:5002`

## Files
| File | Purpose |
|---|---|
| `index.html` | Main cross-cycle dashboard |
| `Sempra_DM1_Dashboard.html` | DM1 individual level |
| `Sempra_DM2_Dashboard.html` | DM2 individual level |
| `Sempra_DM3_Dashboard.html` | DM3 individual level |
| `Sempra_CrossCycle_Summary_MASTER.html` | Cross-cycle summary |
| `automation/file_watcher_bridge.py` | Python bridge (port 5002) |
| `automation/sap_bridge.py` | SAP automation bridge (port 5001) |

## Notes
- Bridge must be running for Auto-Sync to work
- Login: `admin` / `Admin`
- Does NOT work on GitHub Pages (no Python server online)
