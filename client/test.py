import sounddevice as sd
import numpy as np

SAMPLE_RATE = 44100
CHANNELS = 1
BLOCKSIZE = 1024

def main():
    print("🎤 Mikrofon teszt, Ctrl+C kilép")

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, blocksize=BLOCKSIZE) as stream:
        while True:
            data, _ = stream.read(BLOCKSIZE)
            volume = np.linalg.norm(np.array(data, dtype=np.float32)) / BLOCKSIZE
            print(f"Hangerő: {volume:.4f}")

if __name__ == "__main__":
    main()
