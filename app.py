from flask import Flask, request, redirect
import datetime

app = Flask(__name__)

@app.route('/')
def logger():
    # Obtenemos la IP real (Render usa proxies, por eso buscamos X-Forwarded-For)
    ip_provisional = request.headers.get('X-Forwarded-For', request.remote_addr)
    ip_real = ip_provisional.split(',')[0] # Limpiamos la cadena por si vienen varias
    
    # Guardamos la IP con la hora en un archivo
    with open("log.txt", "a") as f:
        f.write(f"Fecha: {datetime.datetime.now()} - IP: {ip_real}\n")
    
    # Redirigimos al profesor a cualquier sitio (ejemplo: Wikipedia)
    return redirect("https://es.wikipedia.org/wiki/Dirección_IP")

@app.route('/ver-resultados')
def ver():
    # Ruta secreta para que tú veas quién ha caído
    try:
        with open("log.txt", "r") as f:
            return f"<pre>{f.read()}</pre>"
    except:
        return "Nadie ha entrado todavía."

if __name__ == "__main__":
    app.run()