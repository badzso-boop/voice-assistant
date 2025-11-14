# Base image Python 3.11 slim
FROM python:3.11-slim

# Working directory
WORKDIR /api-app

# Másoljuk a requirements-et és telepítjük
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Másoljuk a kódot
COPY api-app.py .

# Port, amin a service fut
EXPOSE 5000

# Indítás uvicorn-nal
CMD ["uvicorn", "api-app:app", "--host", "0.0.0.0", "--port", "5000"]
