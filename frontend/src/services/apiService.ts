import axios from "axios";
import { toast } from "react-toastify";

const BASE_URL = "http://localhost:8080";

export const apiService = axios.create({
  baseURL: BASE_URL,
});

export type Detection = {
  frame: number;
  class: string;
  confidence: number;
};

// ✅ Upload
export const uploadFile = async (videoFile: File) => {
  const formData = new FormData();
  formData.append("video", videoFile);

  const res = await apiService.post("/upload", formData);

  toast.success(res.data.message);
};

// ✅ Detect
export const detectObjects = async (confidence: number, iou: number) => {
  const res = await apiService.post("/detect", {
    confidence,
    iou,
  });

  if (res.status !== 200) {
    throw new Error("Detection failed");
  }

  toast.success(res.data.message);

  return res.data.output_video;
};

// ✅ Get detections
export const getLastDetections = async (): Promise<Detection[]> => {
  const res = await apiService.get("/detections");
  return res.data;
};

// ✅ NEW — LLM Analyze
export const analyzeDetections = async (): Promise<string> => {
  const res = await apiService.get("/analyze");
  return res.data.summary;
};