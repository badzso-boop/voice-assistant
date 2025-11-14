# pip install fastapi uvicorn httpx

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class InputModel(BaseModel):
    text: str

@app.post("/synthesize")
async def process(data: InputModel):
    return {
        "tts-text": data.text + " made with tts api"
    }
