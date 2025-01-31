import os
import subprocess
import webbrowser
import time

def main():
    # Get the absolute path to app.py
    current_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(current_dir, "app.py")

    #Define port
    port = 8501

    # Launch Streamlit using subprocess
    process = subprocess.Popen([
        "streamlit",
        "run",
        app_path,
        "--client.toolbarMode=minimal",
        "browser.serverAddress=localhost",
        "browser.gatherUsageStats=false",
        f"--server.port={port}",
        "--server.fileWatcherType=none",
        "--server.headless=true"
    ])

    # Wait a moment for the server to start
    time.sleep(2)

    # Open browser
    webbrowser.open(f"http:localhost:{port}")

    # Wait for the process to complete
    process.wait()

if __name__ == "__main__":
    main()
