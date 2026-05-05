# 🚀 AI Object Detection System (End-to-End)

An end-to-end AI-powered object detection system that processes video input, performs real-time object detection using a trained deep learning model, and visualizes results through a web interface. The system is fully containerized using Docker and supports scalable inference via NVIDIA Triton Inference Server.

---

## 📌 Key Features

* 🎥 Upload and process video files
* 🧠 Object detection using YOLO-based model
* 📊 Detection results displayed in structured table
* ⚡ Optimized inference using Triton Server (optional)
* 🌐 Interactive frontend built with React
* 🐳 Fully containerized system using Docker
* 🔁 End-to-end pipeline: Upload → Detect → Visualize

---

## 🏗️ System Architecture

Frontend (React) → Backend API → ML Model (YOLO / ONNX) → Triton Server → Output Visualization

---

## 🛠️ Tech Stack

| Layer      | Technology Used                 |
| ---------- | ------------------------------- |
| Frontend   | React + TypeScript              |
| Backend    | Python (Flask/FastAPI)          |
| Model      | YOLOv8 (trained)                |
| Dataset    | Global Wheat Detection (Kaggle) |
| Inference  | ONNX / NVIDIA Triton            |
| Deployment | Docker + Docker Compose         |

---

## 📂 Project Structure

```
AI-object-detection/
│
├── ai_model/            # Backend API + ML model
├── frontend/            # React frontend
├── triton/              # Triton model repository
├── docker-compose.yml   # Multi-container setup
└── README.md
```

---

## 🚀 Run the Project (Recommended)

### 1️⃣ Clone Repository

```
git clone https://github.com/DumpalaTeja/AI-object-detection
cd AI-object-detection
```

---

### 2️⃣ Run Using Docker

```
docker-compose up --build
```

---

### 3️⃣ Open Application

```
http://localhost:3000
```

---

## 🧪 How It Works

1. Upload a video file
2. Backend processes frames
3. Model performs object detection
4. Results displayed:

   * Output video/image
   * Detection table

---

## 🐳 Docker Hub Deployment

Backend container is available on Docker Hub:

👉 https://hub.docker.com/r/dumpalateja/ai-object-detection

---

### Pull Image

```
docker pull dumpalateja/ai-object-detection:latest
```

---

### Run Backend Only

```
docker run -p 8080:8080 dumpalateja/ai-object-detection
```

---

## 📊 Dataset Used

* 📦 Global Wheat Detection Dataset
* Source: Kaggle
* Size: >500MB
* Used for training object detection model

---

## ⚙️ Model Details

* Architecture: YOLOv8
* Format: ONNX / PyTorch
* Task: Object Detection
* Output:

  * Bounding boxes
  * Confidence scores

---

## 🚧 Triton Inference Server

* Used for scalable model serving
* Supports GPU acceleration (CUDA)
* Connected via backend API

> Note: Triton may be disabled in local runs due to environment/network constraints.

---

## 🤖 LLM Integration (Planned)

* Designed to integrate Generative AI for:

  * Detection summary
  * Intelligent insights
* Temporarily disabled in deployment for stability

---

## 📈 Future Enhancements

* Add LLM-based analysis (OpenAI / Groq)
* Deploy frontend on Vercel
* Deploy backend on Render
* Optimize model using TensorRT
* Add real-time streaming support

---

## 📄 Software Engineering Contribution

This project focuses on:

* System integration
* Model deployment
* Scalable architecture
* Containerization
* End-to-end pipeline implementation

(Not proposing a new algorithm — focuses on engineering design)

---

## 🏆 Achievements

* ✔ End-to-end AI pipeline built
* ✔ Dockerized deployment
* ✔ Scalable inference setup
* ✔ Integrated frontend + backend
* ✔ Real-world dataset training

---

## 📌 License

This project is developed for academic and research purposes.

---

## 👨‍💻 Author

**Teja Dumpala**
GitHub: https://github.com/DumpalaTeja

---

## 🎯 Demo Flow

Upload Video → Detect Objects → View Output → Analyze Results

---

⭐ If you found this useful, feel free to star the repository!
