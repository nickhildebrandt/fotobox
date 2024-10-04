import http.server
import os
import logging
import socketserver
import threading
from urllib.parse import unquote

class Webserver(http.server.SimpleHTTPRequestHandler):
    def generate_index(self):
        images = sorted([f for f in os.listdir("/fotobox") if f.endswith(".jpg")])
        html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Fotobox</title>
            <style>
                body { margin: 0; padding: 0; background-color: black; }
                .gallery { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 10px; padding: 10px; background-color: black; }
                .gallery img { width: 100%; cursor: pointer; display: block; border: 2px solid white; }
                a { text-align: center; }
            </style>
        </head>
        <body>
            <div class="gallery">
        """
        for img in images:
            html += f'<a href="/image/{img}"><img src="/image/{img}" alt="{img}"></a>'
        html += """
            </div>
        </body>
        </html>
        """
        return html

    def serve_image(self, image_name):
        try:
            with open(f"/fotobox/{image_name}", 'rb') as f:
                self.send_response(200)
                self.send_header("Content-type", "image/jpeg")
                self.end_headers()
                self.wfile.write(f.read())
        except IOError:
            self.send_error(404, "File Not Found")

    def do_GET(self):
        if self.path == "/":
            self.path = "/index.html"
        if self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(self.generate_index().encode())
        elif self.path.startswith("/image/"):
            image_name = unquote(self.path.split("/image/")[1])
            if image_name and image_name.endswith(".jpg"):
                self.serve_image(image_name)
            else:
                self.send_error(404, "File Not Found")
        else:
            self.send_error(404, "File Not Found")

class WebserverThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.server = socketserver.ThreadingTCPServer(("0.0.0.0", 80), Webserver)
        self.server.shutdown_flag = threading.Event()

    def run(self):
        logging.info("Starting webserver on port 80...")
        try:
            self.server.serve_forever()
        except Exception as e:
            logging.error(f"Error in webserver: {e}")
        finally:
            logging.info("Webserver stopped.")

    def stop(self):
        logging.info("Shutting down webserver...")
        self.server.shutdown()
        self.server.server_close()
