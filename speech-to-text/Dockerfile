# Base image Python 3.11 slim
FROM python:3.11-slim

# Build tools a llama.cpp-hoz
RUN apt-get update && \
    apt-get install -y build-essential cmake libcurl4-openssl-dev libgomp1 && \
    rm -rf /var/lib/apt/lists/*

# Working directory
WORKDIR /stt-app

# Másoljuk a requirements-et és telepítjük
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV LD_LIBRARY_PATH="/stt-app/whisper.cpp/build/ggml/src:/stt-app/whisper.cpp/build/src:/stt-app/whisper.cpp/build:${LD_LIBRARY_PATH}"

# Port, amin a service fut
EXPOSE 5001

# Indítás uvicorn-nal
CMD ["uvicorn", "stt-app:app", "--host", "0.0.0.0", "--port", "5001", "--reload"]
