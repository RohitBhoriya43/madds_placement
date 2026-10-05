# MADDS — Multi-Agent Due Diligence Swarm for Placement

MADDS is a portfolio-ready multi-agent AI project for placement/job due diligence.

## What it does

Given a Job Description and Resume, MADDS runs a swarm of specialized agents:

1. **JD Analyst** — extracts role, responsibilities, required skills and seniority.
2. **Resume Analyst** — extracts candidate skills, experience and projects.
3. **Skill Gap Agent** — compares JD requirements with the resume.
4. **Company/Role Due-Diligence Agent** — identifies questions/risks that should be verified before applying/interviewing.
5. **Interview Agent** — generates technical and behavioral interview areas.
6. **Decision Synthesizer** — produces a structured, evidence-based placement report.

The project is designed to be safe for job decisions: it does not claim to predict hiring outcomes. It provides evidence, gaps, questions and preparation areas so a candidate can make their own decision.

## Stack

- Python 3.11+
- FastAPI
- Pydantic
- LangGraph-style orchestration implemented with a lightweight async swarm (no paid API required)
- Ollama optional for local LLM inference
- Jinja2 + vanilla HTML/CSS/JS frontend
- Docker / Docker Compose
- Pytest

## Quick start

### 1. Local Python

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Open http://localhost:8000

### 2. Optional Ollama

Install Ollama, pull a model, then:

```bash
ollama pull llama3.2:3b
```

Set:

```bash
export LLM_PROVIDER=ollama
export OLLAMA_MODEL=llama3.2:3b
export OLLAMA_BASE_URL=http://localhost:11434
```

If Ollama is unavailable, MADDS automatically uses a deterministic local analysis engine so the demo still works.

### 3. Docker

```bash
docker compose up --build
```

Open http://localhost:8000

## API

`POST /api/analyze`

```json
{
  "job_description": "...",
  "resume_text": "..."
}
```

`GET /api/health`

Swagger: http://localhost:8000/docs

## Suggested demo

Use a Backend Python Developer JD and a backend resume. Show:

- requirement extraction
- candidate evidence
- matched / partial / missing skills
- due-diligence questions
- interview preparation
- final report

## Portfolio bullets

- Built a multi-agent placement due-diligence platform using FastAPI and asynchronous agent orchestration to analyze job descriptions and resumes.
- Designed specialized JD, resume, skill-gap, due-diligence and interview agents with a final evidence-based synthesis layer.
- Added local Ollama inference with deterministic fallback, Docker configuration, REST APIs and a browser dashboard for recruiter/candidate demos.
