from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from ultralytics import YOLO
import shutil
import os

app = FastAPI()
model = YOLO("model/my_yolov8n_model.pt")  # Load your YOLO model

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "runs/detect/predict"

# Ensure the upload and output folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    
    # Save the uploaded file temporarily
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run the prediction on the uploaded file
    results = model.predict(source=file_path, save=True, conf=0.25)  # Save output to 'runs/detect/predict'

    # Dynamically find the saved result image(s)
    output_img_path = None
    
    # Check if any files were saved in the output folder
    if results:
        # If results contain prediction files, get the first saved image path
        output_img_path = results[0].path  # Get the path of the first saved image
    
    if output_img_path:
        return FileResponse(output_img_path, media_type="image/jpeg")
    else:
        return {"error": "No prediction result found."}
