# 📌 Configuración de la cámara
from ultralytics import YOLO
use_droidcam = True  
video_url = "http://192.168.4.40:4747/video"  
umbral_confianza = 0.5  
model = YOLO("BlackJack/yolov8s_playing_cards.pt")