#!/usr/bin/env python3
"""
Simple HTTP server for Neon City.
Run this and open http://localhost:8080
"""

import http.server
import socketserver
import os
import webbrowser

PORT = 8888

os.chdir(os.path.dirname(os.path.abspath(__file__)))

Handler = http.server.SimpleHTTPRequestHandler

print("=" * 50)
print("NEON CITY Server")
print("=" * 50)
print(f"\nStarting server at http://localhost:{PORT}")
print(f"\nPages:")
print(f"  City:    http://localhost:{PORT}/index.html")
print(f"  Gallery: http://localhost:{PORT}/gallery.html")
print(f"\nPress Ctrl+C to stop")
print("=" * 50)

webbrowser.open(f"http://localhost:{PORT}/index.html")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
