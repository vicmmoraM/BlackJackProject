from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt


model = YOLO("yolov8s_playing_cards.pt")
image_path = "test_image2.jpg"


results = model(image_path)


detected_image = results[0].plot()


save_path = "detected_test_image.jpg"
cv2.imwrite(save_path, detected_image)


plt.figure(figsize=(10, 6))
plt.imshow(cv2.cvtColor(detected_image, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.title("Detección de Cartas - YOLOv8")
plt.show()

print(f"✅ Imagen guardada como {save_path}")
