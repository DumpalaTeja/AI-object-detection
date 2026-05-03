import tritonclient.http as httpclient
import numpy as np
import cv2

# connect to Triton (your port 8010)
client = httpclient.InferenceServerClient(url="localhost:8010")

def preprocess(frame):
    img = cv2.resize(frame, (640, 640))
    img = img.astype(np.float32) / 255.0
    img = np.transpose(img, (2, 0, 1))
    img = np.expand_dims(img, axis=0)  # shape (1,3,640,640)
    return img

def infer(frame):
    image = preprocess(frame)

    inputs = httpclient.InferInput("images", image.shape, "FP32")
    inputs.set_data_from_numpy(image)

    outputs = httpclient.InferRequestedOutput("output0")

    response = client.infer(
        model_name="wheat_model",
        inputs=[inputs],
        outputs=[outputs]
    )

    return response.as_numpy("output0")

def postprocess(output, conf_threshold=0.5):
    output = output.squeeze()  # shape (5, 8400)

    detections = []

    for i in range(output.shape[1]):
        x, y, w, h, conf = output[:, i]

        if conf > conf_threshold:
            detections.append({
                "bbox": [float(x), float(y), float(w), float(h)],
                "confidence": float(conf),
                "class": 0
            })

    return detections