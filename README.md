# Country Information Agent 🌍

An AI-powered agentic workflow that answers questions about countries using the REST Countries API. Built with **LangGraph**, **FastAPI**, and **Streamlit**.

## 🚀 Live Demo
- **Frontend (UI):** [https://country-ui-208082950137.us-central1.run.app](https://country-ui-208082950137.us-central1.run.app)
- **Backend (API):** [https://country-api-208082950137.us-central1.run.app/docs](https://country-api-208082950137.us-central1.run.app/docs)

---

## 💻 Local Setup

### Prerequisites
- Python 3.11+
- An OpenAI API Key
- (Optional) Docker & Docker Compose

### 1. Clone & Install
```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Variables
Copy the example environment file and fill in your API keys:
```bash
cp .env.example .env
```
Open `.env` and add your `OPENAI_API_KEY`. (Optionally, add your LangSmith API key for tracing).

### 3. Run Locally (Without Docker)
You will need two terminal windows to run both the backend API and the frontend UI.

**Terminal 1: Start the FastAPI Backend**
```bash
source venv/bin/activate
uvicorn app.main:app --reload
# Runs on http://localhost:8000
```

**Terminal 2: Start the Streamlit Frontend**
```bash
source venv/bin/activate
export API_URL="http://localhost:8000/stream"
streamlit run ui.py
# Runs on http://localhost:8501
```

---

## 🐳 Run with Docker Compose
The easiest way to run the full stack is using Docker Compose. It automatically networks the frontend and backend together.

```bash
docker compose up --build
```
- The UI will be available at `http://localhost:8501`
- The API will be available at `http://localhost:8000`

*(To stop the containers, press `Ctrl+C` and run `docker compose down`)*