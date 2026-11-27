from ultralytics import YOLO

model = YOLO("yolo11n.pt")
model.train(data="my_data.yaml", epochs=50, imgsz=640, batch=8, device=0)