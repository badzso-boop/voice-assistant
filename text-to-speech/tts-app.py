from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from TTS.api import TTS
import uuid
import os


app = FastAPI()

# Load TTS model once at startup
# CPU-only model
model = TTS("tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)


class InputModel(BaseModel):
    text: str
    speaker: str | None = None


@app.post("/synthesize")
async def synthesize(data: InputModel):
    output_file = f"output_{uuid.uuid4()}.wav"

    model.tts_to_file(
        text=data.text,
        file_path=output_file,
        speaker=data.speaker if data.speaker else None
    )

    return FileResponse(output_file, media_type="audio/wav", filename="tts_output.wav")
