import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import requests
import time

# --- KONFIG ---
SAMPLE_RATE = 44100
CHANNELS = 1
THRESHOLD = 0.0005          # hangerő küszöb
SILENCE_DURATION = 1.0     # hány másodperc csend után álljon le
API_ENDPOINT = "http://127.0.0.1:5000/process-audio"  # ide az API-d URL-je
OUTPUT_FILE = "recorded.wav"


def is_loud(chunk, threshold):
    volume = np.linalg.norm(chunk) / len(chunk)
    return volume > threshold


def main():
    print("🎤 Mikrofon figyelése... (Ctrl+C kilép)")

    recording = []
    is_recording = False
    silence_start = None

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, blocksize=1024) as stream:
        while True:
            data, _ = stream.read(1024)
            chunk = np.array(data, dtype=np.float32)

            volume = np.linalg.norm(np.array(data, dtype=np.float32)) / 1024
            print(f"Hangerő: {volume:.4f}")

            if not is_recording:
                if is_loud(chunk, THRESHOLD):
                    print("🔴 Hang észlelve → rögzítés indul!")
                    is_recording = True
                    recording = [chunk]
                    silence_start = None
            else:
                recording.append(chunk)

                if is_loud(chunk, THRESHOLD):
                    silence_start = None
                else:
                    if silence_start is None:
                        silence_start = time.time()
                    else:
                        if time.time() - silence_start > SILENCE_DURATION:
                            print("🟢 Csend → rögzítés leáll, fájl mentése...")

                            audio = np.concatenate(recording, axis=0)
                            write(OUTPUT_FILE, SAMPLE_RATE, audio)
                            print(f"💾 Mentve: {OUTPUT_FILE}")

                            # --- API hívás ---
                            print("📤 Fájl küldése API-nak...")
                            try:
                                with open(OUTPUT_FILE, "rb") as f:
                                    r = requests.post(
                                        API_ENDPOINT,
                                        files={"file": (OUTPUT_FILE, f, "audio/wav")}
                                    )
                                print("🌐 API válasza:", r.text)
                            except Exception as e:
                                print("❌ API hiba:", e)

                            # vissza figyelés módba
                            is_recording = False
                            recording = []
                            silence_start = None
                            print("🎤 Figyelés folytatódik...")


if __name__ == "__main__":
    main()
