"""
================================================================================
  SEMPRA DATA MIGRATION DASHBOARD — LOCAL LAUNCHER
  Starts the File Watcher Bridge (port 5002) + a static HTTP server (port 5003)
  then opens the CrossCycle Summary dashboard in the browser via http://.
  Run: python launch_dashboard.py
================================================================================
"""
import subprocess
import sys
import os
import time
import webbrowser
import urllib.request
import threading
import http.server

BRIDGE_PORT   = 5002
STATIC_PORT   = 5003
BRIDGE_PING   = f"http://localhost:{BRIDGE_PORT}/ping"
DASHBOARD     = "Sempra_CrossCycle_Summary_MASTER.html"
BRIDGE_SCRIPT = os.path.join("automation", "file_watcher_bridge.py")
WORK_DIR      = os.path.dirname(os.path.abspath(__file__))

print("=" * 64)
print("  Sempra Data Migration Dashboard — Local Launcher")
print("=" * 64)

# ── 1. Start bridge server ────────────────────────────────────────
print(f"\n[1/3] Starting File Watcher Bridge on port {BRIDGE_PORT}...")
try:
    subprocess.Popen(
        ["powershell", "-NoExit", "-Command",
         f"cd '{WORK_DIR}'; $env:PYTHONIOENCODING='utf-8'; python {BRIDGE_SCRIPT}"],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    print("      Bridge launched in new window.")
except Exception as e:
    print(f"      Could not launch bridge: {e}")
    print(f"      Run manually: python {BRIDGE_SCRIPT}")

# ── 2. Start static HTTP server for dashboard files ───────────────
print(f"\n[2/3] Starting static HTTP server on port {STATIC_PORT}...")
os.chdir(WORK_DIR)

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args): pass   # suppress request logs

def _run_static():
    server = http.server.HTTPServer(("127.0.0.1", STATIC_PORT), QuietHandler)
    server.serve_forever()

t = threading.Thread(target=_run_static, daemon=True)
t.start()
print(f"      Static server running at http://localhost:{STATIC_PORT}/")

# ── 3. Wait for bridge ────────────────────────────────────────────
print(f"\n[3/3] Waiting for bridge...")
for attempt in range(20):
    time.sleep(1)
    try:
        with urllib.request.urlopen(BRIDGE_PING, timeout=2) as r:
            if r.status == 200:
                print(f"      Bridge online (attempt {attempt+1})")
                break
    except Exception:
        print(f"      ... {attempt+1}/20")
else:
    print("      Bridge did not respond — opening anyway.")

# ── 4. Open dashboard via HTTP (not file://) ──────────────────────
url = f"http://localhost:{STATIC_PORT}/{DASHBOARD}"
webbrowser.open(url)
print(f"\n  Opened: {url}")
print("  Close this window to stop the static server.")
print("=" * 64)

# Keep process alive so static server keeps running
try:
    while True: time.sleep(60)
except KeyboardInterrupt:
    print("\nStopped.")
