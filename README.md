# Voice Assistant Project

Ez a projekt egy hobby célú **beszélő okos asszisztens** alapját valósítja meg Dockerben. A cél az, hogy egy kliens (pl. Raspberry Pi) hangot küldjön az API-nak, a szerver feldolgozza a kérést különálló szolgáltatásokkal (STT, LLM, TTS), majd visszaküldje a választ.

---

## Projekt struktúra

```
voice-assistant
│ docker-compose.yml
├───api
│ │ api-app.py
│ │ Dockerfile
│ │ requirements.txt
├───client
│ │ client.py
├───large-language-model
│ │ llm-app.py
│ │ Dockerfile
│ │ requirements.txt
├───speech-to-text
│ │ stt-app.py
│ │ Dockerfile
│ │ requirements.txt
└───text-to-speech
│ │ tts-app.py
│ │ Dockerfile
│ │ requirements.txt
```

---

## Szolgáltatások

- **api**: FastAPI alapú központi endpoint `/process`, ami összekapcsolja a STT, LLM és TTS szolgáltatásokat.
- **speech-to-text (STT)**: Hang → szöveg (mock implementáció most csak visszaadja a bemenetet + string).
- **large-language-model (LLM)**: Szöveg feldolgozás, válasz generálás (mock implementáció).
- **text-to-speech (TTS)**: Szöveg → hang (mock implementáció).

---

## Docker használat

### Build és futtatás

```bash
docker compose up --build
```

### Logok nézése

```bash
docker compose logs -f api
docker compose logs -f stt
docker compose logs -f llm
docker compose logs -f tts
```

---

### Fejlesztői setup

- A konténerek `--reload` opcióval futnak, így minden `.py` fájl módosítás automatikusan újraindítja a FastAPI server-t.
- Volume mount-okat a docker-compose.yml biztosítja, így a hoston szerkesztett fájlok azonnal látszanak a konténerben.

### Large Language Model (LLM)

A `large-language-model` mappa tartalmazza a **Llama.cpp**-t és a `llm-app.py` FastAPI szolgáltatást, ami a szöveges kéréseket dolgozza fel és generálja a válaszokat.

1. Llama.cpp klónozása

```bash
git clone https://github.com/ggml-org/llama.cpp.git
```
A klónozott mappa a `large-language-model` alá kerüljön.

2. WSL / Linux build függőségek

```bash
sudo apt update
sudo apt install -y build-essential cmake libcurl4-openssl-dev
```

3. CMake build

Navigálj a `llama.cpp` mappába, majd futtasd:

```bash
cmake -B build
cmake --build build --config Release -j 8
```

- j 8 → párhuzamos build 8 szálon (állítható a CPU teljesítményedhez)
- A build után a bináris elérhető lesz: `large-language-model/llama.cpp/build/bin/llama-cli`

4. Modell letöltése

A Llama.cpp használatához szükséged van egy GGUF formátumú modellre.
- Példa: TinyLLaMA GGUF modell (https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v0.2-GGUF)
- A modellt helyezd el a következő mappába: `large-language-model/models`

5. LLM FastAPI (`llm-app.py`) működése


### Példa API hívás

```bash
curl -X POST http://localhost:5000/process \
-H "Content-Type: application/json" \
-d '{"text": "Hello world"}'
```
### Válasz JSON:
```json
{
  "original_text": "Hello world",
  "stt_response": {"stt-text": "Hello world made with stt api"},
  "llm_response": {"llm-text": "Hello world made with llm api"},
  "tts_response": {"tts-text": "Hello world made with tts api"},
  "final_output": "Próba vége!"
}
```

---

### Következő lépések
- STT, LLM és TTS szolgáltatások éles implementációja.
- Kliens oldali hangrögzítés és lejátszás.
- GitHub Actions workflow a Docker image automatikus buildjére push esetén.
- Raspberry Pi kliens integráció.