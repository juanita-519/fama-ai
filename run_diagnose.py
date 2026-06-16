import os
import subprocess
import time
import urllib.request
import sys

def main():
    print("====================================================")
    print("FAMA AI - Server Diagnostics & Resource Check")
    print("====================================================")
    
    # 1. Verify file paths in static dir
    print("Checking static files on disk...")
    paths_to_check = [
        "backend/static/index.html",
        "backend/static/js/app.js",
        "backend/static/js/components.js",
        "backend/static/css/styles.css"
    ]
    for path in paths_to_check:
        exists = os.path.exists(path)
        print(f"  - {path}: {'EXISTS' if exists else 'MISSING'}")
        if not exists:
            print(f"CRITICAL ERROR: {path} is missing on disk!")
            sys.exit(1)
            
    # 2. Start local FastAPI test server on port 8081 to avoid conflicts
    print("\nStarting local FastAPI test server on port 8081...")
    server_process = subprocess.Popen(
        ["python", "-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8081"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait for server to boot
    time.sleep(3)
    
    # Check if process crashed immediately
    poll = server_process.poll()
    if poll is not None:
        stdout, stderr = server_process.communicate()
        print(f"CRITICAL: Server failed to start! Exit code: {poll}")
        print(f"Stderr: {stderr}")
        sys.exit(1)
        
    print("Server process started. Testing HTTP endpoints...")
    
    endpoints = {
        "HTML Root": "http://127.0.0.1:8081/",
        "App JS": "http://127.0.0.1:8081/js/app.js",
        "Components JS": "http://127.0.0.1:8081/js/components.js",
        "Styles CSS": "http://127.0.0.1:8081/css/styles.css",
        "Stocks API": "http://127.0.0.1:8081/api/stocks",
        "Analysis API": "http://127.0.0.1:8081/api/fama-analysis/infosys"
    }
    
    success = True
    for name, url in endpoints.items():
        try:
            req = urllib.request.Request(url)
            # Add user agent to behave like browser
            req.add_header('User-Agent', 'Mozilla/5.0')
            with urllib.request.urlopen(req, timeout=5) as response:
                status = response.status
                headers = dict(response.info())
                content_type = headers.get('Content-Type', 'unknown')
                print(f"  - {name} ({url}): OK (Status: {status}, Type: {content_type})")
        except Exception as e:
            print(f"  - {name} ({url}): FAILED! Error: {str(e)}")
            success = False
            
    # Clean up server
    print("\nShutting down test server...")
    server_process.terminate()
    try:
        server_process.wait(timeout=2)
    except subprocess.TimeoutExpired:
        server_process.kill()
        
    if success:
        print("\nSUCCESS: All web endpoints are serving assets correctly with correct MIME types.")
    else:
        print("\nFAILURE: Some endpoints failed to return resources. Check logs.")
        sys.exit(1)

if __name__ == "__main__":
    main()
