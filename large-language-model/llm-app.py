# pip install fastapi uvicorn httpx

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class InputModel(BaseModel):
    text: str

@app.post("/respond")
async def process(data: InputModel):
    return {
        "llm-text": data.text + " made with llm api"
    }
