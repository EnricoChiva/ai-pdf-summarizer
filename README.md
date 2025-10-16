# 🧠 AI PDF Summarizer – Azure OpenAI + Vector Search

Ein intelligenter PDF-Analyzer, der große Dokumente automatisch zusammenfasst – unterstützt durch **Azure OpenAI**, **Azure AI Search (VectorDB)** und **Python FastAPI**.  
Ideal für lange Berichte, wissenschaftliche Texte oder Geschäftsunterlagen.

---
<br>

## 🚀 Projektübersicht

Dieses Projekt zerlegt PDF-Dokumente in sinnvolle Textabschnitte (*Chunks*), analysiert sie mithilfe von **Large Language Models (LLMs)** und erstellt daraus eine prägnante, strukturierte Gesamtzusammenfassung.

Die Anwendung zeigt, wie man:
- große PDFs performant verarbeitet,
- semantische Suche und Embeddings einsetzt,
- mehrere LLMs in einer **Map-Reduce-ähnlichen Pipeline** kombiniert,
- und Azure OpenAI mit FastAPI integriert.
---
<br>

## 🧩 Architektur

PDF Upload → Chunking → Embedding → Azure AI Search → LLM Summaries → Combined Summary


### Komponenten:
| Service | Aufgabe |
|----------|----------|
| `pdf_service.py` | Extrahiert Text aus PDF-Dateien |
| `chunk_service.py` | Teilt den Text in Chunks (max. 1000 Tokens) |
| `embedding_service.py` | Erstellt Embeddings für jeden Chunk |
| `storage_service.py` | Speichert Chunks + Embeddings in Azure AI Search |
| `ai_service.py` | Kommuniziert mit Azure OpenAI (Maverick & o3) |
| `pipeline_service.py` | Orchestriert die gesamte Verarbeitung |
| `api/routes.py` | REST API (FastAPI) für Upload & Zusammenfassung |

---
<br>

## 🧠 Technischer Ablauf

1. **PDF Upload:**  
   Eine PDF wird als Byte-Stream hochgeladen.

2. **Chunking:**  
   Der Text wird in Abschnitte (≈ 1000 Tokens) aufgeteilt.

3. **Embedding + Speicherung:**  
   Jeder Chunk erhält einen semantischen Vektor und wird in **Azure AI Search** gespeichert.

4. **Pre-Summarization (Llama-4 Maverick):**  
   Jeder Chunk wird von einem schnellen LLM analysiert und inhaltlich zusammengefasst.

5. **Final-Summarization (o3-mini):**  
   Alle Chunks werden kombiniert und zu einer kohärenten Gesamtzusammenfassung synthetisiert.

6. **Rückgabe ans Frontend:**  
   Das Frontend zeigt die strukturierte Zusammenfassung.

---
<br>

## 🧰 Tech-Stack

| Technologie | Beschreibung |
|--------------|--------------|
| **Python 3.13** | Hauptsprache |
| **FastAPI** | REST API Framework |
| **Azure OpenAI Service** | LLMs: Llama-4-Maverick, o3-mini |
| **Azure AI Search** | Speicherung & Vektorsuche |
| **Pydantic Settings** | Typsichere Umgebungsvariablen |
| **AsyncIO** | Asynchrone Parallelverarbeitung |
| **Uvicorn** | Entwicklungsserver |

---
<br>

## 🧠 Features

Asynchrone Verarbeitung mit asyncio

Modularer Service-Aufbau

Automatisches Chunking + Token-Optimierung

Zwei-stufige Summarisierung (Map-Reduce-ähnlich)

Azure AI Search Integration

Konfigurierbar per .env

Erweiterbar für Q&A / RAG / Semantische Suche

---
<br>


## 💡 Lernziele & Fokus

Dieses Projekt demonstriert praxisnah:

AI-Pipeline-Design mit mehreren Modellen

Prompt Engineering & Token-Optimierung

Datenpersistenz & Vektorsuche

Asynchrones Python-Design (async/await)

Saubere Service-Architektur

---
<br>


## 🧩 Mögliche Erweiterungen

🗂 Frontend mit React oder Angular → PDF Upload + Summary Viewer

🤖 Q&A Chat über Vektorsuche (RAG)

📄 Zusammenfassungen mit Quellenzitaten (chunk_id / page_number)

🧾 Automatische Report-Generierung (Markdown / PDF)

---
<br>


## ⚙️ Setup & Installation

### 1. Repository klonen
git clone https://github.com/<dein-username>/ai-pdf-summarizer.git
cd ai-pdf-summarizer


### 2. Virtuelle Umgebung

python -m venv .venv
source .venv/bin/activate  # macOS / Linux
#### oder
.venv\Scripts\activate     # Windows


### 3. Abhängigkeiten installieren

pip install -r requirements.txt


### 4. .env.dev konfigurieren


#### Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://<dein-endpunkt>.openai.azure.com/
AZURE_OPENAI_API_KEY=<dein-api-key>

#### Modelle
AZURE_OPENAI_MODEL_o3=o3-mini
AZURE_DEPLOYMENT_NAME_o3=o3-mini
API_VERSION_O3=2024-12-01-preview

AZURE_OPENAI_MODEL_MAVERICK=Llama-4-Maverick-17B-128E-Instruct-FP8
AZURE_DEPLOYMENT_NAME_MAVERICK=Llama-4-Maverick-Alpha
API_VERSION_MAVERICK=2024-05-01-preview

#### Azure Search
SEARCH_API_ENDPOINT=https://<deine-search-instance>.search.windows.net
SEARCH_API_KEY=<dein-key>
SEARCH_API_INDEX=pdf-chunks


### 5. Server starten

uvicorn app.main:app --reload
API läuft unter http://127.0.0.1:8000
