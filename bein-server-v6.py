"""Minimal test"""
import urllib.request, urllib.parse, ssl, json
from http.server import HTTPServer, BaseHTTPRequestHandler

UA = "BuzCup/2.0 (+https://buzcup.net; Flutter; Dart) AppleCoreMedia/1.0"
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

def proxy(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        r = urllib.request.urlopen(req, context=ssl_ctx, timeout=20)
        return r.status, dict(r.headers), r.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read()

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        p = self.path
        print(f"REQ: {repr(p)}")
        
        if p.startswith('/api/channel?'):
            ch = urllib.parse.parse_qs(p.split('?')[1]).get('ch',[''])[0]
            s, h, b = proxy(f'https://man1ted.com/get.php?ch={ch}')
            self.send_response(s)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b)
            return
        
        if p.startswith('/stream/'):
            q = p.find('?')
            pp = p[8:q] if q >= 0 else p[8:]
            qs = p[q+1:] if q >= 0 else ""
            
            if pp == 'load':
                t = urllib.parse.parse_qs(qs).get('target',[''])[0]
                print(f"LOAD: {t[:80]}...")
                s, h, b = proxy(t)
                self.send_response(s)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', 'application/vnd.apple.mpegurl')
                self.end_headers()
                self.wfile.write(b)
                return
            
            t = f"https://man1ted.com/watch/{pp}" + (f"?{qs}" if qs else "")
            print(f"PROXY: {pp}?{qs[:50]}")
            s, h, b = proxy(t)
            self.send_response(s)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', h.get('Content-Type', 'video/MP2T'))
            self.end_headers()
            self.wfile.write(b)
            return
        
        if p == '/':
            with open('/home/zs/match-site.html', 'rb') as f:
                html = f.read().replace(b'https://man1ted.com/get.php?', b'/api/channel?')
                html = html.replace(b"const PROXY_PREFIX = '/m3u8?target=';", b"const PROXY_PREFIX = '/stream/load?target=';")
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(html)))
            self.end_headers()
            self.wfile.write(html)
            return
        
        self.send_error(404)

HTTPServer(('0.0.0.0', 8000), H).serve_forever()
