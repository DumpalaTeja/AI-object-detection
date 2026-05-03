import { ChangeEvent, useState } from "react"
import axios from 'axios'
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { Button } from "./components/ui/button";
import { Input } from "./components/ui/input";
import { Label } from "./components/ui/label";
import {
    Detection,
    detectObjects,
    getLastDetections,
    uploadFile
} from "./services/apiService";

interface UploadFileProps {
    videoFile: File | null
    onFileChange: (event: ChangeEvent<HTMLInputElement>) => void
    onVideoProcessed: (inProcess: boolean) => void
    onVideoOutput: (video: string) => void
    onLastDetections: (detections: Detection[] | null) => void
    inProcess: boolean
}

const UploadForm = ({
    videoFile,
    onFileChange,
    onVideoProcessed,
    onVideoOutput,
    onLastDetections,
    inProcess
}: UploadFileProps) => {

    const [confidence, setConfidence] = useState<number>(0.7)
    const [iou, setIOU] = useState<number>(0.5)

    const handleConfidenceChange = (event: ChangeEvent<HTMLInputElement>) => {
        const val = parseFloat(event.target.value)
        if (!isNaN(val) && val >= 0 && val <= 1) {
            setConfidence(val)
        }
    }

    const handleIOUChange = (event: ChangeEvent<HTMLInputElement>) => {
        const val = parseFloat(event.target.value)
        if (!isNaN(val) && val >= 0 && val <= 1) {
            setIOU(val)
        }
    }

    const handleUpload = async () => {
        try {
            if (!videoFile) throw new Error('No input video.')

            onVideoProcessed(true)

            // 1. Upload
            await uploadFile(videoFile)

            // 2. Detect
            const processedVideoName = await detectObjects(confidence, iou)

            console.log("NEW VIDEO:", processedVideoName)

            if (!processedVideoName) {
                throw new Error('Processing failed')
            }

            // 3. FIX: NO CACHE VIDEO URL
            const videoURL = `http://localhost:8080/result/${processedVideoName}?t=${Date.now()}`

            // 4. Show video
            onVideoOutput(videoURL)

            // 5. Load detections
            const detections = await getLastDetections()
            onLastDetections(detections)

            onVideoProcessed(false)

        } catch (error) {
            onVideoProcessed(false)

            if (axios.isAxiosError(error) && error.response) {
                toast.error("Error: " + error.response.data.message)
            } else {
                toast.error((error as Error).message)
            }
        }
    }

    return (
        <div className="flex place-content-center gap-3 mt-3">

            <div className="grid grid-cols-4 gap-x-3 w-full">
                <Label>Choose Video</Label>
                <Label>Confidence</Label>
                <Label className="col-span-2">IOU</Label>

                <Input type="file" onChange={onFileChange} required />
                <Input type="number" value={confidence} onChange={handleConfidenceChange} />
                <Input type="number" value={iou} onChange={handleIOUChange} />

                <Button onClick={handleUpload} disabled={inProcess}>
                    Detect Objects
                </Button>
            </div>

            <ToastContainer position="bottom-right" theme="dark" />
        </div>
    )
}

export default UploadForm