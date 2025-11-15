# pip install fastapi uvicorn httpx

import subprocess
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

app = FastAPI()

WHISPER_CPP_BIN = "/stt-app/whisper.cpp/build/bin/whisper-cli"
MODEL_PATH = "/stt-app/whisper.cpp/models/ggml-base.en.bin"

class InputModel(BaseModel):
    text: str

@app.post("/transcribe-test")
async def process(data: InputModel):
    return {
        "stt-text": data.text + " made with stt api"
    }


@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    """
    Feltöltött wav/mp3 fájlt vesz, 
    átadja a Whisper.cpp CLI-nek, 
    és visszaadja a transzkripciót.
    """

    # 1️⃣ Ideiglenes fájl létrehozása
    tmp_file_path = f"/tmp/{file.filename}"
    with open(tmp_file_path, "wb") as f:
        f.write(await file.read())

    # 2️⃣ Futtatjuk a Whisper.cpp CLI-t
    try:
        result = subprocess.run(
            [WHISPER_CPP_BIN, "-m", MODEL_PATH, "-f", tmp_file_path],
            capture_output=True,
            text=True,
            check=True
        )
        text = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        text = f"Error: {e.stderr}"

    return {"text": text}