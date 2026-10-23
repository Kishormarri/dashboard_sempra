"""
================================================================================
  SEMPRA DATA MIGRATION PLATFORM — PORTABLE BACKUP GENERATOR
  Creates a clean, lightweight, fully self-contained deployment zip package
  ready to transfer and run on any other user's system / laptop.
================================================================================
"""
import os
import zipfile
import shutil
from datetime import datetime

TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
ZIP_NAME = f"Sempra_DM_Dashboard_Portable_v1.0_{TIMESTAMP}.zip"
DESKTOP_PATH = os.path.join(os.path.expanduser("~"), "Desktop", ZIP_NAME)
WORKSPACE_ROOT = os.path.abspath(os.path.dirname(__file__))

# Folders and patterns to exclude from portable backup
EXCLUDE_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".idea",
    ".vscode",
}

def should_exclude(path):
    parts = os.path.normpath(path).split(os.sep)
    for p in parts:
        if p in EXCLUDE_DIRS:
            return True
        if p.startswith("backup_20"):  # Skip older raw snapshot folders
            return True
    if path.endswith(".zip") and "Sempra_DM_Dashboard_Portable" in path:
        return True
    return False

def create_backup():
    print("=" * 70)
    print("  SEMPRA DM DASHBOARD — CREATING PORTABLE BACKUP PACKAGE")
    print("=" * 70)
    print(f"  Source Root  : {WORKSPACE_ROOT}")
    print(f"  Target File  : {ZIP_NAME}")
    
    file_count = 0
    with zipfile.ZipFile(ZIP_NAME, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        for root, dirs, files in os.walk(WORKSPACE_ROOT):
            # Prune excluded directories
            dirs[:] = [d for d in dirs if not should_exclude(os.path.join(root, d))]
            
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, WORKSPACE_ROOT)
                
                if should_exclude(rel_path):
                    continue
                
                zipf.write(full_path, arcname=rel_path)
                file_count += 1

    size_mb = os.path.getsize(ZIP_NAME) / (1024 * 1024)
    print(f"\n  [SUCCESS] Packaged {file_count} files into '{ZIP_NAME}' ({size_mb:.2f} MB)")

    # Copy to Desktop
    try:
        shutil.copyfile(ZIP_NAME, DESKTOP_PATH)
        print(f"  [COPIED] Desktop Backup : {DESKTOP_PATH}")
    except Exception as e:
        print(f"  [WARN] Could not copy to Desktop: {e}")

    print("\n" + "=" * 70)
    print("  TRANSFER & EXECUTION INSTRUCTIONS FOR OTHER SYSTEMS:")
    print("  1. Copy the ZIP file to the new machine.")
    print("  2. Extract/Unzip all contents to a folder (e.g. C:\\Sempra_DM_Dashboard\\).")
    print("  3. Double-click 'INSTALL_AND_RUN.bat' (installs packages & launches).")
    print("  4. Browser opens automatically to the 3-Cycle Cockpit!")
    print("=" * 70)

if __name__ == "__main__":
    create_backup()
