from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import secrets
import socket
import qrcode

def get_lan_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    finally:
        s.close()

def start_server(password: str, port: int = 8000):
    token = secrets.token_urlsafe(32)

    class MyHandler(BaseHTTPRequestHandler):
        def _send_html(self):
            import html as html_lib
            from textwrap import dedent

            pw = html_lib.escape(password)  

            html = dedent(f"""\
            <!doctype html>
            <html lang="en">
            <head>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1" />
            <title>Bamboopass</title>
            <style>
                :root {{
                --bg1: #0b1220;
                --bg2: #101b33;
                --card: rgba(255,255,255,.08);
                --card2: rgba(255,255,255,.06);
                --text: #e9eefc;
                --muted: rgba(233,238,252,.7);
                --border: rgba(255,255,255,.12);
                --shadow: 0 20px 60px rgba(0,0,0,.45);
                --radius: 18px;
                }}

                * {{ box-sizing: border-box; }}
                body {{
                margin: 0;
                min-height: 100vh;
                display: grid;
                place-items: center;
                font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial;
                color: var(--text);
                background:
                    radial-gradient(900px 500px at 20% 15%, rgba(106, 90, 205, .45), transparent 55%),
                    radial-gradient(800px 500px at 80% 20%, rgba(0, 195, 255, .35), transparent 55%),
                    linear-gradient(180deg, var(--bg1), var(--bg2));
                padding: 18px;
                }}

                .card {{
                width: min(560px, 100%);
                background: linear-gradient(180deg, var(--card), var(--card2));
                border: 1px solid var(--border);
                border-radius: var(--radius);
                box-shadow: var(--shadow);
                overflow: hidden;
                }}

                .top {{
                padding: 18px 18px 14px 18px;
                border-bottom: 1px solid var(--border);
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 12px;
                }}

                .brand {{
                display: flex;
                align-items: center;
                gap: 10px;
                font-weight: 800;
                letter-spacing: .2px;
                }}

                .dot {{
                width: 12px; height: 12px;
                border-radius: 999px;
                background: radial-gradient(circle at 30% 30%, #9ae6ff, #6a5acd 70%);
                box-shadow: 0 0 0 4px rgba(106,90,205,.18);
                }}

                .badge {{
                font-size: 12px;
                color: var(--muted);
                border: 1px solid var(--border);
                padding: 6px 10px;
                border-radius: 999px;
                background: rgba(0,0,0,.14);
                white-space: nowrap;
                }}

                .content {{ padding: 18px; }}

                h2 {{
                margin: 0 0 6px 0;
                font-size: 18px;
                }}

                p {{
                margin: 0 0 16px 0;
                color: var(--muted);
                line-height: 1.45;
                font-size: 13px;
                }}

                .codebox {{
                display: grid;
                gap: 10px;
                background: rgba(0,0,0,.22);
                border: 1px solid var(--border);
                border-radius: 14px;
                padding: 14px;
                }}

                .code {{
                font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace;
                font-size: 16px;
                line-height: 1.35;
                word-break: break-all;
                user-select: all;
                padding: 10px 12px;
                border-radius: 12px;
                border: 1px dashed rgba(255,255,255,.18);
                background: rgba(255,255,255,.04);
                }}

                .row {{
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
                align-items: center;
                justify-content: space-between;
                }}

                .btn {{
                appearance: none;
                border: 1px solid var(--border);
                background: rgba(255,255,255,.10);
                color: var(--text);
                border-radius: 12px;
                padding: 10px 12px;
                font-weight: 700;
                cursor: pointer;
                transition: transform .04s ease, background .15s ease;
                display: inline-flex;
                align-items: center;
                gap: 8px;
                }}

                .btn:active {{ transform: translateY(1px); }}
                .btn:hover {{ background: rgba(255,255,255,.14); }}

                .hint {{
                font-size: 12px;
                color: var(--muted);
                display: flex;
                align-items: center;
                gap: 8px;
                }}

                .toast {{
                position: fixed;
                left: 50%;
                bottom: 18px;
                transform: translateX(-50%);
                background: rgba(0,0,0,.55);
                border: 1px solid var(--border);
                padding: 10px 12px;
                border-radius: 12px;
                color: var(--text);
                font-size: 13px;
                opacity: 0;
                pointer-events: none;
                transition: opacity .2s ease, transform .2s ease;
                }}
                .toast.show {{
                opacity: 1;
                transform: translateX(-50%) translateY(-6px);
                }}
            </style>
            </head>
            <body>
            <div class="card">
                <div class="top">
                <div class="brand"><span class="dot"></span> Bamboopass</div>
                <div class="badge">one-time link</div>
                </div>

                <div class="content">
                <h2>Your password</h2>
                <p>Tap the password or press Copy. This link is single-use.</p>

                <div class="codebox">
                    <div id="pw" class="code" onclick="copyPw()">{pw}</div>

                    <div class="row">
                    <button class="btn" onclick="copyPw()">📋 Copy</button>
                    <div class="hint">Tip: tap the password to copy</div>
                    </div>
                </div>
                </div>
            </div>

            <div id="toast" class="toast">Copied ✅</div>

            <script>
                async function copyPw() {{
                const text = document.getElementById('pw').innerText;
                try {{
                    await navigator.clipboard.writeText(text);
                    showToast('Copied ✅');
                }} catch (e) {{
                    const ta = document.createElement('textarea');
                    ta.value = text;
                    document.body.appendChild(ta);
                    ta.select();
                    document.execCommand('copy');
                    ta.remove();
                    showToast('Copied ✅');
                }}
                }}

                function showToast(msg) {{
                const t = document.getElementById('toast');
                t.textContent = msg;
                t.classList.add('show');
                setTimeout(() => t.classList.remove('show'), 900);
                }}
            </script>
            </body>
            </html>
            """)

            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-store, max-age=0")
            self.send_header("Pragma", "no-cache")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))


        def do_GET(self):
            nonlocal token
            parsed_url = urlparse(self.path)
            token_receive = parse_qs(parsed_url.query).get("token", [None])[0]

            if token is None:
                self.send_response(403); self.end_headers()
                self.wfile.write(b"Token already used / disabled")
                return

            if not token_receive or token_receive != token:
                self.send_response(403); self.end_headers()
                self.wfile.write(b"Invalid or missing token")
                return

            # one-time
            token = None
            self._send_html()

    server = HTTPServer(("0.0.0.0", port), MyHandler)

    lan_ip = get_lan_ip()
    url = f"http://{lan_ip}:{port}/?token={token}"

    print("LAN_IP:", lan_ip)
    print("OPEN ON PHONE:", url)
    print("\nQR Code (scan this):\n")
    qr = qrcode.QRCode(border=1)
    qr.add_data(url)
    qr.make(fit=True)
    qr.print_ascii(invert=True)

    return server, token
