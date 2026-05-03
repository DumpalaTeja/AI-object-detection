import { ChangeEvent, useState } from 'react'
import './App.css'
import UploadForm from './UploadForm'
import VideoPlayer from './components/videoplayer'
import DetectTable from './components/detect-table'
import { SkeletonVideo } from './components/skeleton-video'
import { Detection, analyzeDetections } from './services/apiService'

function App() {
  const [videoFile, setVideoFile] = useState<File | null>(null)
  const [videoURL, setVideoURL] = useState<string | undefined>(undefined)
  const [outputImage, setOutputImage] = useState<string | null>(null)
  const [inProcess, setInProcess] = useState<boolean>(false)
  const [lastDetections, setLastDetections] = useState<Detection[] | null>([])
  const [summary, setSummary] = useState<string>("")

  // 📁 File selection
  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      const selectedVideo = event.target.files[0]
      setVideoFile(selectedVideo)
      const videoObjectURL = URL.createObjectURL(selectedVideo)
      setVideoURL(videoObjectURL)
    }
  }

  // 📊 Detections
  const handleLastDetections = (detections: Detection[] | null) => {
    setLastDetections(detections)
  }

  // 🔄 Processing state
  const handleVideoProcessed = (inProcess: boolean) => {
    setInProcess(inProcess)
  }

  // 🖼️ Output image
  const handleVideoOutput = (imageURL: string) => {
    setOutputImage(imageURL)
  }

  // 🤖 LLM Analyze
  const handleAnalyze = async () => {
    try {
      const result = await analyzeDetections()
      setSummary(result)
    } catch (error) {
      console.error("LLM Error:", error)
    }
  }

  return (
    <main className='w-9/12 flex flex-col mx-auto gap-5'>
      <h1 className='text-2xl font-bold'>AI Object Detection</h1>

      <UploadForm
        videoFile={videoFile}
        onFileChange={handleFileChange}
        onVideoProcessed={handleVideoProcessed}
        onVideoOutput={handleVideoOutput}
        onLastDetections={handleLastDetections}
        inProcess={inProcess}
      />

      <div className="flex gap-5 justify-evenly">
        {/* Input Video */}
        {videoURL && <VideoPlayer videoPath={videoURL} />}

        {/* Loading */}
        {inProcess && <SkeletonVideo />}

        {/* ✅ OUTPUT IMAGE (FIXED) */}
        {outputImage && !inProcess && (
          <img src={outputImage} style={{ width: "500px" }} />
        )}
      </div>

      <DetectTable lastDetections={lastDetections} />

      <div className="flex flex-col items-center gap-3">
        <button
          onClick={handleAnalyze}
          className="px-4 py-2 bg-blue-600 text-white rounded"
        >
          Analyze with AI
        </button>

        {summary && (
          <div className="p-4 rounded w-full bg-white shadow text-black">
            <h3 className="font-bold text-lg mb-2">AI Analysis</h3>
            <p className="text-sm leading-relaxed">{summary}</p>
          </div>
        )}
      </div>
    </main>
  )
}

export default App