import cv2
import numpy as np
from ultralytics import YOLO

# Cargar el modelo de YOLOv8
model = YOLO("yolov8s_playing_cards.pt")  

def detectar_cartas(frame):
    """ Detecta cartas en la imagen usando YOLOv8 y devuelve los nombres detectados. """
    results = model(frame)
    cartas_detectadas = []
    
    if results and hasattr(results[0], "boxes") and len(results[0].boxes) > 0:
        frame_copy = frame.copy()
        detecciones = {}

        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                carta_nombre = result.names[class_id]
                x_min = int(box.xyxy[0][0])  # 📌 Tomar la posición X

                # 📌 Si esta carta ya fue detectada, ignorarla
                if carta_nombre not in detecciones.values():
                    detecciones[x_min] = carta_nombre

                    # Dibujar rectángulo alrededor de la carta detectada
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(frame_copy, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame_copy, carta_nombre, (x1, y1 - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # 📌 Ordenar cartas de izquierda a derecha y eliminar duplicados
        cartas_detectadas = list(dict(sorted(detecciones.items())).values())

        if cartas_detectadas:
            print(f"✅ Cartas detectadas correctamente: {cartas_detectadas}")
        else:
            print("❌ No se detectaron cartas correctamente.")

        # 📌 Mostrar la imagen con las detecciones antes de devolver el resultado
        cv2.imshow("Detección de Cartas", frame_copy)
        cv2.waitKey(1000)

    return cartas_detectadas if cartas_detectadas else ["NO DETECTADO"]
