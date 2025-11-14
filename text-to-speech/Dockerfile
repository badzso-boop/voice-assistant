# Base image Python 3.11 slim
FROM python:3.11-slim

# Working directory
WORKDIR /tts-app

# Másoljuk a requirements-et és telepítjük
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Másoljuk a kódot
# COPY tts-app.py .

# Port, amin a service fut
EXPOSE 5003

# Indítás uvicorn-nal
CMD ["uvicorn", "tts-app:app", "--host", "0.0.0.0", "--port", "5003", "--reload"]
