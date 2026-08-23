import http.server
import socketserver
import threading
import webbrowser
import os
import sys

# ---------------------------------------------------------
# Local test server for the Soderstrand personal website
# ---------------------------------------------------------

PORT = 8000

# Always serve the folder containing this test_local.py file.
SITE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SITE_DIR)


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    # Keep the CMD window readable by suppressing normal request logging.
    def log_message(self, format, *args):
        pass


print("=" * 60)
print("Soderstrand Personal Website - Local Test Server")
print("=" * 60)
print()
print(f"Website folder: {SITE_DIR}")
print(f"Local server:   http://localhost:{PORT}/")
print()
print("The website will now open in Microsoft Edge.")
print()
print("When you are finished viewing the website:")
print("  1. Return to this CMD window.")
print("  2. Press ENTER.")
print("  3. The local server will shut down.")
print("  4. Press ENTER again to close this CMD window.")
print()
print("-" * 60)

try:
    server = socketserver.TCPServer(("127.0.0.1", PORT), QuietHandler)
except OSError as e:
    print()
    print(f"ERROR: Could not start the local server on port {PORT}.")
    print(f"Details: {e}")
    print()
    input("Press ENTER to close this window...")
    sys.exit(1)

server_thread = threading.Thread(target=server.serve_forever)
server_thread.daemon = True
server_thread.start()

# Open the local website in Microsoft Edge.
url = f"http://localhost:{PORT}/index.html"
edge_path = os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe")
if not os.path.exists(edge_path):
    edge_path = os.path.expandvars(r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe")

if os.path.exists(edge_path):
    webbrowser.register("edge", None, webbrowser.BackgroundBrowser(edge_path))
    webbrowser.get("edge").open(url)
else:
    # Fall back to the system's default browser if Edge is not found
    webbrowser.open(url)

# Keep the server running until ENTER is pressed in CMD.
input("Press ENTER here when you are finished viewing the website... ")

print()
print("Shutting down the local server...")

# Close the listening socket directly.
# This avoids the Python 3.13 shutdown() wait that can hang here.
server.server_close()

# Give the server thread a moment to notice the closed socket.
server_thread.join(timeout=2)

print("The local server is now CLOSED.")
print()
input("Press ENTER again to close this CMD window... ")
