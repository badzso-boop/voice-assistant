import requests
import sounddevice as sd
from scipy.io.wavfile import write, read
import os

API_ENDPOINT = "http://127.0.0.1:5000/process-audio"
INPUT_FILE = "audio.wav"
OUTPUT_TTS_FILE = "tts_reply.wav"


def play_audio(path):
    print(f"🔊 Lejátszás: {path}")
    sr, audio = read(path)
    sd.play(audio, sr)
    sd.wait()


def main():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Hiba: '{INPUT_FILE}' nem található!")
        return

    print("📤 Fájl küldése API-nak:", INPUT_FILE)

    with open(INPUT_FILE, "rb") as f:
        response = requests.post(
            API_ENDPOINT,
            files={"file": (INPUT_FILE, f, "audio/wav")}
        )

    if response.status_code != 200:
        print("❌ API hiba:", response.text)
        return

    print("🌐 API válasza JSON:", response.json())

    # API JSON = { stt_result, llm_result, tts_file }
    tts_path = response.json().get("tts_file")

    if not tts_path or not os.path.exists(tts_path):
        print("❌ A TTS output fájl nem létezik:", tts_path)
        return

    # Mentsük át egy fix névre is
    os.rename(tts_path, OUTPUT_TTS_FILE)

    print(f"💾 TTS válasz mentve ide: {OUTPUT_TTS_FILE}")

    play_audio(OUTPUT_TTS_FILE)


if __name__ == "__main__":
    main()
