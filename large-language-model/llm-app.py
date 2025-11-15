# pip install fastapi uvicorn httpx

import subprocess
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

MODEL_PATH = "models/llama-2-13b-chat.Q4_0.gguf"
LLAMA_CPP_BIN = "/llm-app/llama.cpp/build/bin/llama-cli"

class InputModel(BaseModel):
    text: str

@app.post("/respond-test")
async def process(data: InputModel):
    return {
        "llm-text": data.text + " made with llm api"
    }

@app.post("/respond")
async def process(data: InputModel):
    try:
        result = subprocess.run(
            [LLAMA_CPP_BIN, "-m", MODEL_PATH, "-p", data.text, "-n", "512"],  # -n = token limit
            capture_output=True,
            text=True,
            check=True
        )
        output_text = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        output_text = f"Error: {e.stderr}"

    return {
        "llm-text": output_text
    }
