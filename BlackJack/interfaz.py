import cv2
import threading
import tkinter as tk
from tkinter import Label, Frame
from ultralytics import YOLO
from PIL import Image, ImageTk  # Corregido para soportar imágenes en Tkinter
import time

# Cargar modelo YOLO
model = YOLO("yolov8s_playing_cards.pt")

# Configuración inicial de la cámara (solo DroidCam)
video_url = "http://192.168.100.6:4747/video"  # Cambia según la IP de DroidCam
cap = cv2.VideoCapture(video_url)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reducir el buffer de frames para menor latencia
cap.set(cv2.CAP_PROP_FPS, 30)  # Intentar forzar un FPS más alto
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

class BlackjackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BlackJack - Detección de Cartas")
        self.root.geometry("800x600")
        self.root.configure(bg="#2C3E50")
        
        # Marco para la cámara
        self.frame_video = Frame(self.root, bg="#34495E")
        self.frame_video.pack(pady=10)
        
        # Etiqueta de la cámara
        self.video_label = Label(self.frame_video, bg="#34495E")
        self.video_label.pack()
        
        # Etiqueta para mostrar la carta detectada
        self.card_label = Label(self.root, text="Carta detectada: Ninguna", font=("Arial", 16), fg="white", bg="#2C3E50")
        self.card_label.pack(pady=10)
        
        # Iniciar la captura de video en un hilo
        self.running = True
        self.last_detection_time = time.time()
        self.last_detected_card = None  # Para evitar detecciones duplicadas
        self.video_thread = threading.Thread(target=self.update_camera, daemon=True)
        self.video_thread.start()
    
    def update_camera(self):
        while self.running:
            ret, frame = cap.read()
            if not ret:
                continue
            
            # Convertir frame a formato compatible con Tkinter
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.flip(frame, 1)  # Voltear horizontalmente para una vista más natural
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            
            self.root.after(10, self.update_image, imgtk)
            
            # Realizar detección solo si han pasado 0.5 segundos desde la última detección
            if time.time() - self.last_detection_time > 0.5:
                self.last_detection_time = time.time()
                threading.Thread(target=self.detect_cards, args=(frame,), daemon=True).start()
    
    def update_image(self, imgtk):
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)
    
    def detect_cards(self, frame):
        results = model.predict(frame, verbose=False, conf=0.5, iou=0.5, device='cpu')
        detected_cards = set()  # Usamos un conjunto para evitar duplicados
        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                card_name = model.names[class_id]
                detected_cards.add(card_name)  # Agregamos al conjunto para evitar duplicados
        
        # Si hay una carta nueva detectada, actualizar la UI
        if detected_cards and detected_cards != self.last_detected_card:
            self.last_detected_card = detected_cards
            card_text = ', '.join(detected_cards)
            self.root.after(10, lambda: self.card_label.config(text=f"Carta detectada: {card_text}"))
    
    def close(self):
        self.running = False
        cap.release()
        self.root.quit()

# Iniciar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = BlackjackApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()