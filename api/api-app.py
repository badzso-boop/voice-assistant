# pip install fastapi uvicorn httpx

from fastapi import FastAPI
from pydantic import BaseModel
import httpx

app = FastAPI()

STT_URL = "http://stt:5001/transcribe"
LLM_URL = "http://llm:5002/respond"
TTS_URL = "http://tts:5003/synthesize"

class InputModel(BaseModel):
    text: str

@app.post("/process")
async def process(data: InputModel):
    async with httpx.AsyncClient() as client:
        # POST 1 → STT
        stt_resp = await client.post(STT_URL, json={"text": data.text})
        
        # POST 2 → LLM
        llm_resp = await client.post(LLM_URL, json={"text": data.text})
        
        # POST 3 → TTS
        tts_resp = await client.post(TTS_URL, json={"text": data.text})

    # Itt írd bele a saját válaszszöveged:
    final_text = "Próba vége!"

    return {
        "original_text": data.text,
        "stt_response": stt_resp.json(),
        "llm_response": llm_resp.json(),
        "tts_response": tts_resp.json(),
        "final_output": final_text
    }
