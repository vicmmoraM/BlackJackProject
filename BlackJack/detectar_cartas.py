from ultralytics import YOLO

# 📌 Cargar modelo YOLOv8
model = YOLO("BlackJack/yolov8s_playing_cards.pt")

# 📌 Mapeo de nombres de detección a valores de cartas
card_map = {
    '10C': ('10', 'Tréboles'), '10D': ('10', 'Diamantes'), '10H': ('10', 'Corazones'), '10S': ('10', 'Picas'),
    '2C': ('2', 'Tréboles'), '2D': ('2', 'Diamantes'), '2H': ('2', 'Corazones'), '2S': ('2', 'Picas'),
    '3C': ('3', 'Tréboles'), '3D': ('3', 'Diamantes'), '3H': ('3', 'Corazones'), '3S': ('3', 'Picas'),
    '4C': ('4', 'Tréboles'), '4D': ('4', 'Diamantes'), '4H': ('4', 'Corazones'), '4S': ('4', 'Picas'),
    '5C': ('5', 'Tréboles'), '5D': ('5', 'Diamantes'), '5H': ('5', 'Corazones'), '5S': ('5', 'Picas'),
    '6C': ('6', 'Tréboles'), '6D': ('6', 'Diamantes'), '6H': ('6', 'Corazones'), '6S': ('6', 'Picas'),
    '7C': ('7', 'Tréboles'), '7D': ('7', 'Diamantes'), '7H': ('7', 'Corazones'), '7S': ('7', 'Picas'),
    '8C': ('8', 'Tréboles'), '8D': ('8', 'Diamantes'), '8H': ('8', 'Corazones'), '8S': ('8', 'Picas'),
    '9C': ('9', 'Tréboles'), '9D': ('9', 'Diamantes'), '9H': ('9', 'Corazones'), '9S': ('9', 'Picas'),
    'AC': ('A', 'Tréboles'), 'AD': ('A', 'Diamantes'), 'AH': ('A', 'Corazones'), 'AS': ('A', 'Picas'),
    'JC': ('J', 'Tréboles'), 'JD': ('J', 'Diamantes'), 'JH': ('J', 'Corazones'), 'JS': ('J', 'Picas'),
    'QC': ('Q', 'Tréboles'), 'QD': ('Q', 'Diamantes'), 'QH': ('Q', 'Corazones'), 'QS': ('Q', 'Picas'),
    'KC': ('K', 'Tréboles'), 'KD': ('K', 'Diamantes'), 'KH': ('K', 'Corazones'), 'KS': ('K', 'Picas')
}

def detectar_cartas(imagen, conf=0.5):
    """
    Detecta cartas en una imagen usando YOLOv8.

    :param imagen: Imagen capturada (numpy array).
    :param conf: Umbral de confianza para detección.
    :return: Lista de cartas detectadas sin duplicados.
    """
    results = model(imagen, conf=conf)

    if not results or len(results) == 0 or not hasattr(results[0], "boxes"):
        return []

    cartas_detectadas = {}

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Obtener coordenadas del cuadro
            class_id = int(box.cls[0])
            confianza = box.conf[0].item()
            carta_nombre = result.names[class_id]  # Nombre de la carta

            # 📌 Solo considerar cartas con confianza suficiente
            if confianza >= conf:
                # 📌 Solo tomar la detección con el `y` más pequeño (para evitar dobles detecciones)
                if carta_nombre not in cartas_detectadas or y1 < cartas_detectadas[carta_nombre][1]:
                    cartas_detectadas[carta_nombre] = (confianza, y1)

    # 📌 Guardar solo las cartas detectadas en la parte superior de la imagen
    cartas_finales = list(cartas_detectadas.keys())
    print(f"📸 Cartas detectadas en la imagen: {cartas_finales}")
    
    return cartas_finales