import http.server
import socketserver
import json
import csv
import os
from urllib.parse import urlparse

PORT = 8000
NOTES_DIR = "NOTAS DE EVALUACIÓN"
CSV_FILE = os.path.join(NOTES_DIR, "notas.csv")
JSON_FILE = os.path.join(NOTES_DIR, "notas.json")

# Ensure dir and files exist
os.makedirs(NOTES_DIR, exist_ok=True)
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Fecha", "Nombres", "Apellidos", "DNI", "Codigo", "Campana", "Evaluacion", "Nota", "Total_Preguntas"])

if not os.path.exists(JSON_FILE):
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == "/api/get_grades":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            try:
                with open(JSON_FILE, "r", encoding="utf-8") as f:
                    data = f.read()
            except Exception:
                data = "[]"
            self.wfile.write(data.encode("utf-8"))
        else:
            super().do_GET()

    def do_POST(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == "/api/save_grade":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode("utf-8"))
            
            # Save to JSON
            try:
                with open(JSON_FILE, "r", encoding="utf-8") as f:
                    grades = json.load(f)
            except Exception:
                grades = []
                
            from datetime import datetime
            data["Fecha"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            grades.append(data)
            
            with open(JSON_FILE, "w", encoding="utf-8") as f:
                json.dump(grades, f, ensure_ascii=False, indent=2)
                
            # Save to CSV
            with open(CSV_FILE, "a", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    data["Fecha"],
                    data.get("nombres", ""),
                    data.get("apellidos", ""),
                    data.get("dni", ""),
                    data.get("codigo", ""),
                    data.get("campana", ""),
                    data.get("evaluacion", ""),
                    data.get("nota", 0),
                    data.get("total", 20)
                ])
                
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode("utf-8"))
        else:
            self.send_error(404, "File not found")

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()
