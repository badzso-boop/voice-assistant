# pip install fastapi uvicorn httpx

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class InputModel(BaseModel):
    text: str

@app.post("/transcribe")
async def process(data: InputModel):
    return {
        "stt-text": data.text + " made with stt api"
    }
