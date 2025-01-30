import cv2
from cosas.juego import Juego
import cosas.configuracion as cfg  # Configuración de la cámara

# 📌 Inicializar el juego
juego = Juego()

# 📌 Mostrar la baraja en consola para que el jugador la ordene físicamente
juego.baraja.mostrar_baraja()

# 📌 Configurar la cámara (DroidCam o webcam)
cap = cv2.VideoCapture(cfg.video_url if cfg.use_droidcam else 0)

if not cap.isOpened():
    print("❌ Error: No se pudo abrir la cámara.")
    exit()

print("📸 Presiona 'c' para capturar la imagen de tus cartas.")
print("❌ Presiona 'q' para salir.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Error al capturar el fotograma.")
        break

    # 📌 Mostrar la vista previa de la cámara
    cv2.imshow("Presiona 'c' para capturar tus cartas | 'q' para salir", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('c'):  # 📸 Capturar imagen y analizarla
        print("📸 Imagen capturada. Analizando...")

        # 📌 Guardar la imagen capturada (opcional)
        cv2.imwrite("captura.jpg", frame)

        # 📌 Capturar cartas del jugador con detección sin duplicados
        cartas_detectadas = juego.capturar_cartas_jugador(frame)

        # 📌 Imprimir lo que realmente se detectó
        print(f"🔍 Cartas detectadas antes de validación: {cartas_detectadas}")

        if not cartas_detectadas or cartas_detectadas == ["NO DETECTADO"]:
            print("❌ No se detectaron cartas correctamente. Inténtalo de nuevo.")
            continue  # Volver al bucle para intentar otra captura

        # 📌 Asignar las cartas detectadas al jugador
        juego.jugador_mano = cartas_detectadas

        print(f"🃏 Cartas finales del Jugador: {juego.jugador_mano}")

        # 📌 Jugar la ronda con las cartas correctas
        resultado = juego.iniciar_ronda(frame)

        print(f"🏆 Resultado Final: {resultado}")

        # 📌 Mostrar la imagen analizada con detecciones
        cv2.imshow("Imagen Capturada - Análisis", frame)
        cv2.waitKey(1000)  # Mostrar durante 1 segundo antes de continuar

    elif key == ord('q'):  # ❌ Salir del programa
        print("👋 Saliendo...")
        break

cap.release()
cv2.destroyAllWindows()