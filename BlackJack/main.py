import cv2
from juego import Juego
from detectar_cartas import detectar_cartas
import configuracion as cfg  # Configuración de la cámara

# 📌 Inicializar el juego
juego = Juego()

# 📌 Configurar la cámara
cap = cv2.VideoCapture(cfg.video_url if cfg.use_droidcam else 0)

if not cap.isOpened():
    print("❌ Error: No se pudo abrir la cámara.")
    exit()

print("📸 Presiona 'c' para capturar una imagen y analizarla.")
print("❌ Presiona 'q' para salir.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Error al capturar el fotograma.")
        break

    # 📌 Mostrar la vista previa de la cámara
    cv2.imshow("Presiona 'c' para capturar | 'q' para salir", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('c'):  # 📸 Capturar imagen y analizarla
        print("📸 Imagen capturada. Analizando...")

        # 📌 Guardar la imagen capturada (opcional)
        cv2.imwrite("captura.jpg", frame)

        # 📌 Detectar cartas en la imagen capturada
        results = detectar_cartas(frame, conf=cfg.umbral_confianza)

        if results and len(results) > 0 and hasattr(results[0], "boxes"):
            cartas_detectadas = []
            for result in results:
                for box in result.boxes:
                    class_id = int(box.cls[0])
                    confianza = box.conf[0].item()
                    carta_nombre = result.names[class_id]  # Nombre de la carta
                    numero_carta = carta_nombre[:-1]  # Extraer solo el número

                    # 📌 Agregar carta al juego si no está repetida
                    if confianza > cfg.umbral_confianza and numero_carta not in cartas_detectadas:
                        cartas_detectadas.append(numero_carta)
                        nueva_carta = juego.repartir_carta()
                        print(f"✅ Se añadió al juego: {nueva_carta.simbolo} {nueva_carta.valor}")

            # 📊 Mostrar puntaje del jugador
            puntaje_jugador = sum([juego.crupier.arbol.puntaje_total(juego.crupier.arbol.raiz)])
            print(f"📊 Total Blackjack Jugador: {puntaje_jugador} puntos")

        else:
            print("❌ No se detectaron cartas en la imagen.")

    elif key == ord('q'):  # ❌ Salir del programa
        print("👋 Saliendo...")
        break

cap.release()
cv2.destroyAllWindows()
