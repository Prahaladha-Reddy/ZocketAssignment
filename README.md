---
# ZocketAssignment

This project is a full-stack Ad-Tech NLP platform for automated market research, ad rewriting, slogan analysis, and deep research. It combines a FastAPI backend (with LLM-powered endpoints) and a modern Streamlit frontend for interactive use.
---

## Features

- **Ad Rewriter:** Iteratively polishes ad copy for different tones and platforms, with user feedback loop.
- **Slogan Analyzer:** Analyzes and answers questions about brand slogans using a built-in dataset and LLMs.
- **Deep Research:** Performs automated, multi-step research on any tech/business topic using web search, scraping, and LLM synthesis.
- **Modern UI:** Streamlit dashboard with tabs for each major feature.
- **API-first:** All features are available via REST API for programmatic access.

---

## Project Structure

- `app.py` — FastAPI backend exposing all API endpoints.
- `main.py` — Core orchestration logic for research, slogan analysis, and ad rewriting.
- `add_rewriter.py` — Ad rewriter logic using LangGraph and LLMs.
- `streamlit_app.py` — Streamlit frontend dashboard.
- `slogan_analysisagant.py` — Slogan analysis agent logic.
- `simplesearc.py`, `inital_search_results.py`, etc. — Web search and scraping utilities.
- `models.py` — Pydantic models for API and state.
- `slogan_genarator/brand_slogans.csv` — Slogan dataset for analysis.
- `Dockerfile` — For containerized deployment.

---

## Technical Document

For a detailed technical walkthrough and deeper design decisions, please refer to the [**Technical Document (Google Drive)**](https://drive.google.com/file/d/16PGSkTOnWNuKKoneWRc4jvHPMmT-RYN7/view?usp=sharing).

---

##Frontend

### 1. Iterative Ad Rewriter

![Iterative Ad Rewriter](./screenshots/ad_rewriter.png)

---

### 2. Slogan Dataframe Analyzer

![Slogan Dataframe Analyzer](./screenshots/slogan_dataframe.png)

---

### 3. Deep Research in Tech

![Deep Research in Tech](./screenshots/deepresearch.png)

## Backend API (FastAPI)

### Endpoints

- **POST `/add_rewriter`**
  Input:

  ```json
  {
    "initial_ad": "Buy our shoes — you get better quality!",
    "tone": "fun",
    "platform": "Instagram",
    "polished_ad": "",
    "is_ok": false,
    "feed_back": ""
  }
  ```

  Output:

  ```json
  {
    "response": {
      "initial_ad": "...",
      "tone": "...",
      "platform": "...",
      "polished_ad": "...",
      "is_ok": false,
      "feed_back": "..."
    }
  }
  ```

  - Iteratively rewrites ad copy, incorporating user feedback.

- **POST `/slogan_analyzer`**
  Input:

  ```json
  { "query": "What are the top 3 slogans used by Amazon?" }
  ```

  Output:

  ```json
  { "response": "..." }
  ```

  - Answers questions about brand slogans using the built-in dataset and LLMs.

- **POST `/analyze`**
  Input:

  ```json
  { "query": "Research deep on the Q3 of apple 2024 sales" }
  ```

  Output:

  ```json
  { "response": "Comprehensive answer synthesized from multiple sources." }
  ```

  - Performs deep, multi-step research using web search, scraping, and LLMs.

---

## Frontend (Streamlit)

Run with:

```bash
streamlit run streamlit_app.py
```

### Tabs

- **Ad Rewriter (loop):**

  - Enter ad text, select tone and platform, and iteratively polish the ad with feedback.
  - Each round is tracked in a revision history.
  - Uses `/add_rewriter` endpoint.

- **Slogan Analyzer:**

  - Enter a slogan-related question (e.g., "What are the top 3 slogans used by Amazon?").
  - Uses `/slogan_analyzer` endpoint and displays the LLM's answer.

- **Deep Research:**

  - Enter any tech/business research question.
  - Uses `/analyze` endpoint for multi-step, LLM-powered research.

---

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Prahaladha-Reddy/ZocketAssignment.git
   cd ZocketAssignment
   ```

2. **Create a virtual environment and activate it:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   uv sync
   ```

4. **Set up environment variables:**
   Create a `.env` file in the project root:

   ```
   SERPER_API_KEY=your_serper_api_key
   GOOGLE_API_KEY=your_google_api_key
   ```

---

## Usage

### Run the Backend API

```bash
uvicorn app:app --reload
```

### Run the Frontend

```bash
streamlit run streamlit_app.py
```

---

## Docker

To run everything in Docker:

```bash
docker build -t zocketassignment .
docker run -p 8000:8000 zocketassignment
```

---

## Dependencies

- Python 3.10+
- FastAPI, Uvicorn, Streamlit
- LangChain, LangGraph, LLM providers (Google, Groq, OpenAI, etc.)
- SERPER API, Firecrawl, KaggleHub (for datasets)
- See `pyproject.toml` for the full list.

---

## API Reference

See above for endpoint details. All endpoints accept and return JSON.

---

## Notes

- The project relies on external APIs (SERPER, Google Generative AI, etc.). Make sure you have valid API keys.
- The system is designed for research and prototyping; production use may require additional error handling and robustness.
- The Streamlit frontend is a user-friendly dashboard for all major features.

---
