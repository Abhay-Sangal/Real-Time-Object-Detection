import torch
from pathlib import Path
from PIL import Image
import cv2
import argparse
import torchvision
from ultralytics import YOLO
# Step 3: Load the YOLOv5 model
def load_model(weights):
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=False)
    checkpoint = torch.load(weights, map_location='cpu')
    model.load_state_dict(checkpoint['model'])
    return model

def detect_objects(model, img):
    results = model(img)
    return results.pandas().xyxy[0]

def main(weights, video_path):
    model = load_model(weights)

    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert BGR frame to RGB and then to PIL image
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(frame_rgb)

        # Step 4: Detect objects in the frame
        detections = detect_objects(model, pil_image)

        # Draw bounding boxes on the frame
        for _, row in detections.iterrows():
            x_min, y_min, x_max, y_max = row['xmin'], row['ymin'], row['xmax'], row['ymax']
            label = row['name']
            confidence = row['confidence']
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            cv2.putText(frame, f'{label} {confidence:.2f}', (x_min, y_min - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        # Display the frame with bounding boxes
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', type=str, default='yolov5s.pt', help='last.pt')
    parser.add_argument('--video', type=str, help='traffic.mp4')
    args = parser.parse_args()

    main(weights=args.weights, video_path=args.video)
