from typing import Union
import os
from fastapi import *
import uuid
import subprocess
from fastapi.middleware.cors import CORSMiddleware
from processing import *
from response import *


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
RAW_VIDEO_DIR = "../frontend/public/videos/raw"
PROCESSED_VIDEO_DIR = "../frontend/public/videos/processed"

os.makedirs(RAW_VIDEO_DIR, exist_ok=True)
os.makedirs(PROCESSED_VIDEO_DIR, exist_ok=True)

def process_video(job_id: str):
    job = job_store[job_id]
    fileName = job["video_filename"][:-4]
    input_path = job["video_path"]

    output_path = os.path.join(PROCESSED_VIDEO_DIR, f"{fileName}_processed.mp4")
    outputAngles = processVideo(input_path, output_path)
    userRequest = ("These are the angles of my relevant body parts during my shot. "
    "Based on these values, and your science-based knowledge as a basketball coach, "
    "inform me on how I can improve as a player and what my strengths and weaknesses are: \n\n{}"
    ).format(str(outputAngles))
    recommendation = generateResponse(userRequest)


    job_store[job_id]["status"] = "completed"
    job_store[job_id]["processed_video_path"] = output_path
    job_store[job_id]["recommendation"] = recommendation

    print(job_store)

@app.post("/upload-video/") 
async def upload_video(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    file_ext = os.path.splitext(file.filename)[1]

    if file_ext.lower() not in VALID_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only MP4 files are allowed")

    job_id = str(uuid.uuid4())  # Generate a unique job ID
    video_path = os.path.join(RAW_VIDEO_DIR, file.filename)

    with open(video_path, "wb") as f:
        f.write(await file.read())

    job_store[job_id] = {
        "status": "processing",
        "video_filename": file.filename,
        "video_path": video_path
    }
    background_tasks.add_task(process_video, job_id)

    return {"job_id": job_id, "message": "Video uploaded and stored successfully"}

@app.get("/list-videos/")
def list_videos():

    raw_videos = []
    processed_videos = []

    for key, job in job_store.items():
        if job["status"] == "completed":
            processed_videos.append({
                "job_id": key,
                "video_path": job["processed_video_path"][18:]
            })
        raw_videos.append({
            "job_id": key,
            "video_path": job["video_path"][18:]
        })

    output = {
        "raw": raw_videos,
        "processed": processed_videos
    }

    return output

@app.get("/job/{job_id}")
def get_job_status(job_id: str):
    return job_store.get(job_id, {"error": "Job not found"})