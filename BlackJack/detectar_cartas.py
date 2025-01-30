from ultralytics import YOLO

# 📌 Cargar el modelo YOLOv8
model = YOLO("yolov8s_playing_cards.pt")

def detectar_cartas(frame, conf=0.5):
    """
    Detecta cartas en un fotograma usando YOLOv8.
    Retorna el objeto results que contiene las detecciones.
    """
    results = model(frame, conf=conf)  # Ejecutar la detección
    return results  # Devolver el objeto YOLOv8 completo
