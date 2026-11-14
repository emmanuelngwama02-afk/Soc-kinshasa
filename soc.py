import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

def analyser(lien):
    l = lien.lower()
    score = 0
    raisons = []
    if "faceb00k" in l:
        score += 40
        raisons.append("0 a la place de o")
    if "gratuit" in l or "free" in l or "cadeau" in l or "gagne" in l:
        score += 30
        raisons.append("Mot appat: gratuit/cadeau")
    if l.count("-") > 2 or l.count(".") > 3:
        score += 20
        raisons.append("Trop de tirets/points")
    if "http://" in l:
        score += 10
        raisons.append("Pas de https")
    if score >= 40:
        return "DANGER", score, raisons
    if score >= 20:
        return "SUSPECT", score, raisons
    return "OK", score, raisons

class S(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write("<h1>MON SOC - KINSHASA</h1><p>Colle un lien suspect avant de cliquer</p><form method='POST'><input name='lien' placeholder='Colle lien suspect' style='width:300px'><button>Analyser + Signaler</button></form>".encode())
    def do_POST(self):
        taille = int(self.headers['Content-Length'])
        data = self.rfile.read(taille).decode()
        lien = parse_qs(data).get('lien', [''])[0]
        verdict, score, raisons = analyser(lien)
        print(f"{verdict} ({score}) : {lien}")
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        msg = f"<h1>{verdict} - Score {score}/100</h1><p>{lien}</p><p>{raisons}</p><a href='/'>Retour</a>"
        self.wfile.write(msg.encode())
    def log_message(self, *a):
        pass

PORT = int(os.environ.get("PORT", 8000))
print(f"SOC lance sur port {PORT}")
HTTPServer(('0.0.0.0', PORT), S).serve_forever()
