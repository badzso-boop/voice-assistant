# Base image Python 3.11 slim
FROM python:3.11-slim

# Working directory
WORKDIR /tts-app

# Install OS packages required for audio + TTS
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Másoljuk a requirements-et és telepítjük
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Port, amin a service fut
EXPOSE 5003

# Indítás uvicorn-nal
CMD ["uvicorn", "tts-app:app", "--host", "0.0.0.0", "--port", "5003", "--reload"]
