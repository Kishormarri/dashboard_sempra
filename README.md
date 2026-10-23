# ⚡ Sempra SAP Data Migration Dashboard — v1.0

> **Self-contained, browser-based tracking & reconciliation system for 3-cycle SAP data migrations (DM1 → DM2 → DM3).**  
> Tracks Source vs. Target load counts, Export vs. Import discrepancies, and reconciliation KPIs with zero external cloud dependencies.

---

## 🚀 Quick Start Guide (For All Team Members)

You have **two simple ways** to run and view the dashboards depending on what you need:

```
┌───────────────────────────────────────────────────────────────────────────────────┐
│                                                                                   │
│  ✨ OPTION 1: INSTANT VIEW (No Python, No Setup, Runs on Any Laptop)             │
│  ───────────────────────────────────────────────────────────────────             │
│  1. Download: Sempra_CrossCycle_Dashboards_ONLY.zip                               │
│  2. Unzip and double-click Sempra_CrossCycle_Summary_MASTER.html                  │
│  3. Log in with: Username: admin | Password: Admin                                │
│                                                                                   │
│  ⚡ OPTION 2: FULL AUTOMATION SERVER (Live Excel Bridge + Auto-Sync)              │
│  ───────────────────────────────────────────────────────────────────             │
│  1. Clone or Download this repository                                             │
│  2. Double-click INSTALL_AND_RUN.bat                                              │
│  3. The cockpit opens automatically at http://localhost:5003/                     │
│                                                                                   │
└───────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📦 What's Included

| Dashboard / File | Description | Recommended For |
| :--- | :--- | :--- |
| [`Sempra_CrossCycle_Summary_MASTER.html`](Sempra_CrossCycle_Summary_MASTER.html) | **Cross-Cycle Master Cockpit** — Consolidated 3-cycle reconciliation (DM1, DM2, DM3), multi-level drill-downs, charts, and KPI cards. | Program managers, migration leads, analysts |
| [`Sempra_CrossCycle_Summary_SHAREPOINT.html`](Sempra_CrossCycle_Summary_SHAREPOINT.html) | **SharePoint Embed View** — Clean, lightweight view designed specifically for Microsoft SharePoint iframe / web part embedding. | SharePoint portals, executive status sites |
| [`Sempra_CrossCycle_Dashboards_ONLY.zip`](Sempra_CrossCycle_Dashboards_ONLY.zip) | **Lightweight Package** — Contains strictly the 2 standalone HTML dashboards (~140 KB). | Teammates who just want the dashboards |
| [`Sempra_DM_Dashboard_LATEST_BACKUP.zip`](Sempra_DM_Dashboard_LATEST_BACKUP.zip) | **Full Deployment Package** — Contains all dashboards, automation bridge, and guides. | Developers and migration engineers |

---

## 🔑 Login Credentials

When prompted on the dashboard login screen, use any of the preset roles (Password is case-sensitive: `Admin`):

| Role | Username | Password | Access Level |
| :--- | :--- | :--- | :--- |
| **Platform Admin** | `admin` | `Admin` | Full access (Upload, Auto-Sync, Export, Re-run) |
| **Sempra Manager** | `manager` | `Admin` | Executive & PDF reports export |
| **Migration Analyst**| `analyst` | `Admin` | Analytical drill-downs & CSV exports |
| **Read-Only Viewer** | `viewer` | `Admin` | View-only access |

---

## 🖥️ Running Full Automation (Step-by-Step)

### Prerequisites
- Windows 10/11 or macOS / Linux
- Python 3.8+ (Make sure to check **"Add Python to PATH"** when installing Python)
- Google Chrome, Microsoft Edge, or Mozilla Firefox

### Step 1: Clone or Download
```bash
git clone https://github.com/Kishormarri/dashboard_sempra.git
cd dashboard_sempra
```

### Step 2: Launch Platform
- **Windows:** Double-click [`INSTALL_AND_RUN.bat`](INSTALL_AND_RUN.bat)  
- **Or via Terminal/Command Prompt:**
  ```bash
  pip install -r requirements.txt
  python launch_dashboard.py
  ```

### What Happens:
1. Python dependencies (`flask`, `flask-cors`, `openpyxl`, `pandas`, `xlrd`) are verified.
2. The **File Watcher Bridge** starts at `http://localhost:5002`.
3. The **Web Server** starts at `http://localhost:5003`.
4. Your browser automatically opens:
   ```
   http://localhost:5003/Sempra_CrossCycle_Summary_MASTER.html
   ```

---

## 📊 Data Files (Optional — For Custom Excel Drops)

The local automation bridge reads cycle Excel files from local folders:
```
C:\Users\<YOUR_USERNAME>\.bob\DM1\Reflist_m1.xlsx
C:\Users\<YOUR_USERNAME>\.bob\DM1\DM1_ES2-SQ1 Export-Import.xlsx
C:\Users\<YOUR_USERNAME>\.bob\DM2\DM2 REF.xlsx
C:\Users\<YOUR_USERNAME>\.bob\DM2\EXPORT IMPORT_DM2.xlsx
C:\Users\<YOUR_USERNAME>\.bob\DM3\ref dm3.xlsx
```
*You can also upload custom files directly through the dashboard UI at runtime without touching Python config!*

---

## 📚 Migration Guides & IS-U Architecture References

The repository also includes end-to-end reference documentation for the migration team:

- [`SAP_ERP_Data_Migration_Guide.html`](SAP_ERP_Data_Migration_Guide.html) — Migration strategy & wave execution guide
- [`SAP_ISU_Reference_Hub.html`](SAP_ISU_Reference_Hub.html) — Central SAP IS-U / CR&B object repository
- [`SAP_ISU_Architecture_Reference.html`](SAP_ISU_Architecture_Reference.html) — Business Partner, Contract Account, Premise models
- [`SAP_ISU_Emigall_Reference.html`](SAP_ISU_Emigall_Reference.html) — EMIGALL migration objects & legacy field mappings
- [`SAP_ISU_BillingSchema_Reference.html`](SAP_ISU_BillingSchema_Reference.html) — Rate structures, billing schemas & operands
- [`Kyano_Mission_Control_User_Guide.html`](Kyano_Mission_Control_User_Guide.html) — Mission Control cockpit user guide

---

## 💡 Troubleshooting & FAQ

* **Q: The dashboard shows "Bridge offline" in the status bar.**  
  **A:** That is completely normal when viewing the static HTML file. The dashboard works offline with cached and uploaded data. To enable live auto-sync, run `python launch_dashboard.py`.
* **Q: Can I share just one file via email or SharePoint?**  
  **A:** Yes! You can send `Sempra_CrossCycle_Summary_MASTER.html` or `Sempra_CrossCycle_Summary_SHAREPOINT.html` directly. They are 100% self-contained.
* **Q: Are real database credentials or customer data committed here?**  
  **A:** No. `.gitignore` strictly blocks all raw Excel, CSV, and log files. No production data leaves your local machine.

---

### License & Project Info
Internal Project — Sempra Energy IT Data Migration Programme.
