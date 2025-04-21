# app/main.py
import tempfile
import cv2
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/pitch-speed")
async def pitch_speed(
    video: UploadFile = File(...),
    distance_feet: float = Form(...),
):
    with tempfile.NamedTemporaryFile(delete=True, suffix=".mp4") as temp:
        temp.write(await video.read())
        temp.flush()
        cap = cv2.VideoCapture(temp.name)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        cap.release()

        if not fps or fps < 1:
            fps = 30  # fallback

        duration = frame_count / fps  # seconds
        speed_fps = distance_feet / duration
        speed_mph = speed_fps * 0.681818

        return {
            "speed_mph": round(speed_mph, 2),
            "frames": frame_count,
            "fps": round(fps, 2),
            "duration_sec": round(duration, 3),
        }