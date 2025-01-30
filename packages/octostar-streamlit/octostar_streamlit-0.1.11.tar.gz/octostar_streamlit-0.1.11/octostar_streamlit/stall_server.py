import http.server
import socketserver
import time

class StallRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)  # Optional: Send a response header if you want partial success
        self.end_headers()
        while True:
            time.sleep(1)  # Keep the connection alive forever

PORT = 8501
with socketserver.TCPServer(("", PORT), StallRequestHandler) as httpd:
    print(f"Stalling server running on port {PORT}")
    httpd.serve_forever()
