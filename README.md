# Voice Assistant Project

Ez a projekt egy hobby célú **beszélő okos asszisztens** alapját valósítja meg Dockerben. A cél az, hogy egy kliens (pl. Raspberry Pi) hangot küldjön az API-nak, a szerver feldolgozza a kérést különálló szolgáltatásokkal (STT, LLM, TTS), majd visszaküldje a választ.

---

## Projekt struktúra

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