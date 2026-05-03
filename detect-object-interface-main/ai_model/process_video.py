import cv2
import os
from datetime import datetime
from services.triton_client import infer, postprocess


class DetectionsProcess:
    def __init__(self):
        self.all_detections = []

    def add_detection(self, frame_number, box, class_name, confidence):
        self.all_detections.append({
            "frame_number": frame_number,
            "box": box,
            "class_name": class_name,
            "confidence": float(confidence)
        })


class VideoProcessor:
    def __init__(self, detections_list, input_video_path, confidence, iou):
        self.detections_list = detections_list
        self.input_video_path = input_video_path
        self.confidence = confidence
        self.iou = iou

    def main_process(self):
        cap = cv2.VideoCapture(self.input_video_path)

        if not cap.isOpened():
            raise Exception("❌ Cannot open video")

        os.makedirs("output-images", exist_ok=True)

        frame_number = 0
        last_frame = None

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            try:
                output = infer(frame)
                detections = postprocess(output, self.confidence)

                for det in detections:
                    x, y, w, h = det["bbox"]
                    conf = det["confidence"]

                    x1 = int(x - w / 2)
                    y1 = int(y - h / 2)
                    x2 = int(x + w / 2)
                    y2 = int(y + h / 2)

                    self.detections_list.add_detection(
                        frame_number,
                        {"left": x1, "top": y1, "width": x2 - x1, "height": y2 - y1},
                        "wheat",
                        conf
                    )

                    # Draw box
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)

                last_frame = frame

            except Exception as e:
                print("⚠️ Triton error:", e)

            frame_number += 1

        cap.release()

        # ✅ SAVE FINAL IMAGE
        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".jpg"
        output_path = os.path.join("output-images", filename)

        if last_frame is not None:
            cv2.imwrite(output_path, last_frame)

        print("✅ Image saved:", output_path)

        return filename