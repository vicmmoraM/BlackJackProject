from ultralytics import YOLO
import cv2

# 📌 Cargar el modelo preentrenado
model = YOLO("yolov8s_playing_cards.pt")

# 📌 Configurar la cámara (DroidCam o webcam)
use_droidcam = True  # Pon False si quieres usar la webcam

if use_droidcam:
    video_url = "http://192.168.100.6:4747/video"  # Cambia según tu IP en DroidCam
    cap = cv2.VideoCapture(video_url)
else:
    cap = cv2.VideoCapture(0)  # Usa 0 para la webcam

# 📌 Verificar si la cámara se abre correctamente
if not cap.isOpened():
    print("❌ Error: No se pudo abrir la cámara.")
    exit()

# 📌 Para evitar imprimir repetidamente la misma detección
ultima_carta_detectada = None

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Error al capturar el fotograma.")
        break

    # 📌 Ejecutar detección con confianza mínima del 50%
    results = model(frame, conf=0.5)  # Aumentamos la confianza

    # 📌 Extraer nombres de las cartas detectadas
    cartas_detectadas = []
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])  # ID de la clase detectada
            confianza = box.conf[0].item()  # Nivel de confianza
            carta = model.names[class_id]  # Nombre de la carta detectada
            
            # 📌 Filtrar detecciones con confianza alta
            if confianza > 0.5 and carta not in cartas_detectadas:
                cartas_detectadas.append(carta)

    # 📌 Imprimir solo si hay una nueva detección diferente
    if cartas_detectadas and cartas_detectadas != ultima_carta_detectada:
        print(f"✅ Cartas detectadas ({int(confianza*100)}% de confianza): {', '.join(cartas_detectadas)}")
        ultima_carta_detectada = cartas_detectadas

    # 📌 Dibujar detecciones en el fotograma
    detected_frame = results[0].plot()

    # 📌 Mostrar el video con las detecciones
    cv2.imshow("Detección de Cartas - YOLOv8", detected_frame)

    # 📌 Salir con 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
