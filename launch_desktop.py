#!/usr/bin/env python3
"""
OmniConvert Native Desktop App Launcher
Launches the converter as a dedicated standalone desktop application window.
"""
import sys
import os
import time
import subprocess
import threading
import webbrowser
import urllib.request

PORT = 8000
HOST = "127.0.0.1"
URL = f"http://{HOST}:{PORT}"

def is_server_running():
    try:
        with urllib.request.urlopen(URL, timeout=1) as response:
            return response.status == 200
    except Exception:
        return False

def start_server():
    import uvicorn
    # Change working directory to script location
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    uvicorn.run("main:app", host=HOST, port=PORT, log_level="warning")

def open_standalone_window():
    # Wait for server to be responsive
    for _ in range(30):
        if is_server_running():
            break
        time.sleep(0.2)

    # Try launching in dedicated App Mode (borderless standalone window)
    opened = False
    
    # 1. macOS Chrome / Edge / Brave App Mode
    if sys.platform == "darwin":
        browsers = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
            "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
        ]
        for b in browsers:
            if os.path.exists(b):
                subprocess.Popen([b, f"--app={URL}"])
                opened = True
                break

    # 2. Windows Chrome / Edge App Mode
    elif sys.platform == "win32":
        paths = [
            os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"),
        ]
        for p in paths:
            if os.path.exists(p):
                subprocess.Popen([p, f"--app={URL}"])
                opened = True
                break

    # 3. Linux Chrome / Chromium App Mode
    elif sys.platform.startswith("linux"):
        for cmd in ["google-chrome", "chromium-browser", "chromium"]:
            try:
                subprocess.Popen([cmd, f"--app={URL}"])
                opened = True
                break
            except FileNotFoundError:
                continue

    # Fallback to default browser
    if not opened:
        webbrowser.open(URL)

if __name__ == "__main__":
    print("=====================================================")
    print("⚡ Launching OmniConvert Desktop Application...")
    print(f"🌐 Server: {URL}")
    print("=====================================================")

    # If server is not already running, start it in a background thread
    if not is_server_running():
        t = threading.Thread(target=start_server, daemon=True)
        t.start()

    # Open window
    open_standalone_window()

    # Keep main thread alive if server is running inside this process
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting OmniConvert. Goodbye!")
        sys.exit(0)
