import cv2
from detectar_cartas import detectar_cartas  # Función para detectar cartas con YOLOv8
import configuracion as cfg  # Configuración de la cámara

# 📌 Configurar la cámara (DroidCam o webcam)
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

                    # 📌 Agregar carta a la lista de detección
                    cartas_detectadas.append(carta_nombre)

            print(f"✅ Cartas detectadas: {', '.join(cartas_detectadas)}")
        else:
            print("❌ No se detectaron cartas en la imagen.")

        # 📌 Mostrar la imagen analizada con detecciones
        detected_frame = results[0].plot() if results and len(results) > 0 else frame
        cv2.imshow("Imagen Capturada - Análisis", detected_frame)
        cv2.waitKey(0)  # Esperar hasta que el usuario cierre la imagen

    elif key == ord('q'):  # ❌ Salir del programa
        print("👋 Saliendo...")
        break

cap.release()
cv2.destroyAllWindows()
