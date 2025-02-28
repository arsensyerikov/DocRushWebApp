from fastapi import FastAPI, UploadFile, File, Form
from typing import List

app = FastAPI()
@app.post("/create-post/")
async def create_post(description: str = Form(...), images: List[UploadFile] = File(...)):
    image_filenames = []
    for image in images:
        image_filenames.append(image.filename)
    return {
        "description": description,
        "images": image_filenames
    }