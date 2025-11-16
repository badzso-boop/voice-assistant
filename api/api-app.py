# pip install fastapi uvicorn httpx

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import re
import httpx
import uuid

app = FastAPI()

STT_URL = "http://stt:5001/transcribe"
LLM_URL = "http://llm:5002/respond"
TTS_URL = "http://tts:5003/synthesize"

class InputModel(BaseModel):
    text: str

def clean_text(text: str) -> str:
    # 1. Szögletes zárójelek és tartalmuk törlése
    text = re.sub(r"\[.*?\]", "", text)
    
    # 2. Minden szám törlése
    text = re.sub(r"\d+", "", text)

    # 3. Új sorok eltávolítása
    text = text.replace("\n", " ")

    # 4. Dupla szóközök kiszedése
    text = re.sub(r"\s+", " ", text).strip()

    return text

@app.post("/process")
async def process(data: InputModel):
    async with httpx.AsyncClient(timeout=100.0) as client:
        # POST 1 → STT
        stt_resp = await client.post("http://stt:5001/transcribe-test", json={"text": data.text})
        
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


@app.post("/process-audio")
async def process_audio(file: UploadFile = File(...)):
    # 1. Küldjük el a hangfájlt az STT servicenek
    async with httpx.AsyncClient(timeout=100.0) as client:
        stt_resp = await client.post(
            STT_URL,
            files={"file": (file.filename, await file.read(), file.content_type)}
        )

    cleaned_stt = clean_text(stt_resp.json().get("text", ""))

    # 2. Küldjük el az LLM-nek
    async with httpx.AsyncClient(timeout=None) as client:
        llm_resp = await client.post(
            LLM_URL,
            json={"text": cleaned_stt}
        )

    cleaned_llm = clean_text(llm_resp.json().get("llm-text", ""))

    # 3. Küldjük el a TTS-nek (majd később hangot fog visszaadni)
    async with httpx.AsyncClient(timeout=None) as client:
        tts_resp = await client.post(
            TTS_URL,
            json={"text": cleaned_llm}
        )

    # Save TTS response file
    output_audio_path = f"tts_output_{uuid.uuid4()}.wav"
    with open(output_audio_path, "wb") as f:
        f.write(tts_resp.content)

    return {
        "stt_result": cleaned_stt,
        "llm_result": cleaned_llm,
        "tts_file": output_audio_path
    }