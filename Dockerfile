# 1️⃣ Basis-Image
FROM python:3.11-slim

# 2️⃣ Arbeitsverzeichnis im Container
WORKDIR /app

# 3️⃣ Requirements kopieren und installieren (Docker Caching nutzen)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4️⃣ Restlichen App-Code kopieren
COPY . .

# 5️⃣ Startbefehl
# Passe "app.main:app" an deine Struktur an: app/main.py mit app = FastAPI()
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
