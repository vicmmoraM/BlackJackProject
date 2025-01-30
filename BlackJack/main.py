import webbrowser
import subprocess
import time

def iniciar_servidor():
    """Inicia el servidor Flask y abre la interfaz en el navegador."""
    proceso = subprocess.Popen(["python", "app.py"])  # Inicia Flask
    time.sleep(2)  # Espera 2 segundos para asegurarse de que el servidor arranque
    webbrowser.open("http://127.0.0.1:5000/")  # Abre el navegador automáticamente
    return proceso

if __name__ == "__main__":
    servidor = iniciar_servidor()
    print("🔥 Servidor Flask ejecutándose. Presiona Ctrl+C para detenerlo.")
    try:
        servidor.wait()
    except KeyboardInterrupt:
        print("👋 Cerrando servidor...")
        servidor.terminate()
