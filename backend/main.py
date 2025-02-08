from typing import Union
import os
from fastapi import *
import uuid
import subprocess
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*", "http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

job_store = {}
VALID_EXTENSIONS = {".mp4"}
VIDEO_DIR = "videos"
os.makedirs(VIDEO_DIR, exist_ok=True)

def process_video(job_id: str):
    job = job_store[job_id]
    input_path = job["video_path"]
    output_path = os.path.join(VIDEO_DIR, f"{job_id}_processed.mp4")

    # Convert video format using FFmpeg
    subprocess.run(["ffmpeg", "-i", input_path, output_path])

    job_store[job_id]["status"] = "completed"
    job_store[job_id]["processed_video_path"] = output_path

    print(job_store)

@app.post("/upload-video/") 
async def upload_video(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    file_ext = os.path.splitext(file.filename)[1]

    if file_ext.lower() not in VALID_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only MP4 files are allowed")

    job_id = str(uuid.uuid4())  # Generate a unique job ID
    video_path = os.path.join(VIDEO_DIR, file.filename)

    # Save the video file
    with open(video_path, "wb") as f:
        f.write(await file.read())
    

    # Store job metadata in dictionary
    job_store[job_id] = {
        "status": "processing",
        "video_filename": file.filename,
        "video_path": video_path
    }
    background_tasks.add_task(process_video, job_id)

    return {"job_id": job_id, "message": "Video uploaded and stored successfully"}

@app.get("/job/{job_id}")
def get_job_status(job_id: str):
    return job_store.get(job_id, {"error": "Job not found"})

