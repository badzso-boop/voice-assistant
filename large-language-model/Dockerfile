# Base image Python 3.11 slim
FROM python:3.11-slim

# Build tools a llama.cpp-hoz
RUN apt-get update && \
    apt-get install -y build-essential cmake libcurl4-openssl-dev && \
    rm -rf /var/lib/apt/lists/*

# Working directory
WORKDIR /llm-app

# Másoljuk a requirements-et és telepítjük
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# libllama.so betöltésére
ENV LD_LIBRARY_PATH="/llm-app/llama.cpp/build/bin:${LD_LIBRARY_PATH}"

# Vissza az app mappába
WORKDIR /llm-app

# Port, amin a service fut
EXPOSE 5002

# Indítás uvicorn-nal
CMD ["uvicorn", "llm-app:app", "--host", "0.0.0.0", "--port", "5002", "--reload"]
