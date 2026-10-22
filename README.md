# ⚡ Sempra SAP Data Migration Dashboard — v1.0

> **Self-contained, browser-based tracking & reconciliation system for 3-cycle SAP data migrations (DM1 → DM2 → DM3).**  
> Tracks Source vs. Target load counts, Export vs. Import discrepancies, and reconciliation KPIs with zero external cloud dependencies.

---

## 🌐 Live GitHub Interactive Dashboards (Click to Open)

You can launch any interactive dashboard directly in your browser without installing anything:

| Dashboard View | Live GitHub Pages Link | File Reference | Purpose |
| :--- | :--- | :--- | :--- |
| ⚡ **Cross-Cycle Master Cockpit** | **[Launch Master Cockpit](https://kishormarri.github.io/dashboard_sempra/)** | [`Sempra_CrossCycle_Summary_MASTER.html`](Sempra_CrossCycle_Summary_MASTER.html) | Consolidated 3-cycle scorecard, KPI cards, table reconciliation & drill-downs |
| 📋 **SharePoint Embed View** | **[Launch SharePoint View](https://kishormarri.github.io/dashboard_sempra/Sempra_CrossCycle_Summary_SHAREPOINT.html)** | [`Sempra_CrossCycle_Summary_SHAREPOINT.html`](Sempra_CrossCycle_Summary_SHAREPOINT.html) | Clean, responsive view designed for SharePoint iframe embedding |
| 🔵 **DM1 (Mock 1) Dashboard** | **[Launch DM1 Dashboard](https://kishormarri.github.io/dashboard_sempra/Sempra_DM1_Dashboard.html)** | [`Sempra_DM1_Dashboard.html`](Sempra_DM1_Dashboard.html) | Cycle 1 extract vs target table counts & reconciliation |
| 🟣 **DM2 (Mock 2) Dashboard** | **[Launch DM2 Dashboard](https://kishormarri.github.io/dashboard_sempra/Sempra_DM2_Dashboard.html)** | [`Sempra_DM2_Dashboard.html`](Sempra_DM2_Dashboard.html) | Cycle 2 load metrics & transformation progress |
| 🟢 **DM3 (Mock 3) Dashboard** | **[Launch DM3 Dashboard](https://kishormarri.github.io/dashboard_sempra/Sempra_DM3_Dashboard.html)** | [`Sempra_DM3_Dashboard.html`](Sempra_DM3_Dashboard.html) | Cutover dress rehearsal & final validation |
| 📊 **Executive Summary** | **[Launch Executive View](https://kishormarri.github.io/dashboard_sempra/Sempra_DM_Dashboard_PREMIUM.html)** | [`Sempra_DM_Dashboard_PREMIUM.html`](Sempra_DM_Dashboard_PREMIUM.html) | Visual gauges & management status heatmaps |

---

## 🔑 Login Credentials

When prompted on the dashboard login screen, sign in with any of the preset roles (Password: `Admin`):

| Role | Username | Password | Access Level |
| :--- | :--- | :--- | :--- |
| **Read-Only Viewer** | `viewer` | `Admin` | Safe read-only browsing for all team members |
| **Migration Analyst** | `analyst` | `Admin` | Detailed drill-downs & CSV exports |
| **Sempra Manager** | `manager` | `Admin` | Executive & PDF reports export |
| **Platform Admin** | `admin` | `Admin` | Full access (Upload, Auto-Sync, Export, Re-run) |

---

## 🛠️ Full Automation Backend (`automation/`)

For engineers running local live SAP and file ingestion:

| Module | Script Path | Description |
| :--- | :--- | :--- |
| **Source Extractor** | [`automation/01_sap_source_count.py`](automation/01_sap_source_count.py) | Batch extractor for legacy SAP source table records |
| **Target Extractor** | [`automation/02_target_count.py`](automation/02_target_count.py) | Target SAP S/4HANA & staging table count validator |
| **Orchestrator** | [`automation/03_orchestrator.py`](automation/03_orchestrator.py) | Full reconciliation engine & difference calculator |
| **File Watcher Bridge** | [`automation/file_watcher_bridge.py`](automation/file_watcher_bridge.py) | Local bridge streaming Excel drops to the browser |
| **SAP RFC Bridge** | [`automation/sap_bridge.py`](automation/sap_bridge.py) | SAP RFC/ODBC interface & fallback chain |
| **SharePoint Bridge** | [`automation/sp_bridge.py`](automation/sp_bridge.py) | Automated SharePoint synchronization bridge |

---

## 🚀 1-Click Launchers & Running Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Kishormarri/dashboard_sempra.git
   cd dashboard_sempra
   ```

2. **One-Click Launch (Windows):**  
   Double-click [`INSTALL_AND_RUN.bat`](INSTALL_AND_RUN.bat)

3. **Or run manually via CLI:**
   ```bash
   pip install -r requirements.txt
   python launch_dashboard.py
   ```

---

## 📚 Migration Guides & IS-U Reference Hubs

- [`SAP_ERP_Data_Migration_Guide.html`](SAP_ERP_Data_Migration_Guide.html) — Comprehensive migration playbook
- [`Kyano_Mission_Control_User_Guide.html`](Kyano_Mission_Control_User_Guide.html) — Mission control operations guide
- [`SAP_ISU_Reference_Hub.html`](SAP_ISU_Reference_Hub.html) — Central SAP IS-U / CR&B object repository
- [`SAP_ISU_Architecture_Reference.html`](SAP_ISU_Architecture_Reference.html) — Business Partner & Premise models
- [`SAP_ISU_Emigall_Reference.html`](SAP_ISU_Emigall_Reference.html) — EMIGALL migration objects & field mappings
- [`SAP_ISU_BillingSchema_Reference.html`](SAP_ISU_BillingSchema_Reference.html) — Rate structures & billing schemas

---

### 📦 Downloadable Release Packages
* **[Production Release Package (ZIP)](https://github.com/Kishormarri/dashboard_sempra/releases/download/v2.2-all-code-backup-20261022_230006/Sempra_DM_Dashboard_ALL_CODE_COMPLETE_20261022_230006.zip)**
* **[Lightweight HTML-Only Package (ZIP)](https://github.com/Kishormarri/dashboard_sempra/raw/main/Sempra_CrossCycle_Dashboards_ONLY.zip)**
