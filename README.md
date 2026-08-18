# NexusMed - AI Healthcare Assistant

NexusMed is a comprehensive AI-powered healthcare platform that provides intelligent symptom analysis, disease prediction, medicine recommendations, and emergency services.

## Features

### 🤖 AI-Powered Health Assistant
- Symptom analysis and disease prediction
- Medicine recommendations and drug interaction checking
- Medical report analysis (PDF, images)
- Health awareness content generation

### 🚑 Emergency Services
- Real-time ambulance tracking
- Nearby hospital search with bed availability
- Emergency alert system
- Community health alerts

### 📊 Health Management
- Health dashboard with statistics
- Appointment scheduling
- Medical report management
- Personal health records

### 🧠 Multi-Agent Architecture
- Symptom Analysis Agent
- Disease Prediction Agent
- Medicine Recommendation Agent
- Hospital & Ambulance Agent
- Community Health Agent
- Report Analysis Agent
- Knowledge Base Agent

## Tech Stack

### Frontend
- React 18
- Tailwind CSS
- WebSocket for real-time updates
- Vite

### Backend
- Flask
- PostgreSQL (primary database)
- Redis (caching & real-time)
- Socket.IO (WebSocket)
- JWT Authentication

### AI/ML
- OpenAI GPT-3.5/4
- Sentence Transformers
- RAG (Retrieval Augmented Generation)
- OCR for report processing
- Custom disease prediction models

## Installation

### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL
- Redis
- Docker (optional)

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py