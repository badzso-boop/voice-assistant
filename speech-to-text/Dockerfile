# Base image Python 3.11 slim
FROM python:3.11-slim

# Working directory
WORKDIR /stt-app

# Másoljuk a requirements-et és telepítjük
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Másoljuk a kódot
# COPY stt-app.py .

# Port, amin a service fut
EXPOSE 5001

# Indítás uvicorn-nal
CMD ["uvicorn", "stt-app:app", "--host", "0.0.0.0", "--port", "5001", "--reload"]
