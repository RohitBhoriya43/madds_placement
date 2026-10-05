from pathlib import Path
from fastapi import FastAPI, Request,UploadFile,File,Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .config import settings
from .schemas import AnalyzeRequest, AnalysisResponse, AgentResult
from .swarm import PlacementSwarm
from .pdf_extract import extract_text

BASE = Path(__file__).resolve().parents[2]
templates = Jinja2Templates(directory=str(BASE / "frontend"))

app = FastAPI(title=settings.app_name, version="1.0.0")
app.mount("/static", StaticFiles(directory=str(BASE / "frontend/static")), name="static")
swarm = PlacementSwarm()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/health")
async def health():
    return {"status": "ok", "app": settings.app_name, "llm_provider": settings.llm_provider}

@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze(jd_file: UploadFile=File(...),resume_file: UploadFile=File(...)):
    # jd = payload.job_description[:settings.max_text_length]
    # resume = payload.resume_text[:settings.max_text_length] if payload.resume_text else None

    if resume_file:
        print(resume_file.filename)
        resume = extract_text(await resume_file.read(),resume_file.filename)

    if jd_file:
        print(jd_file.filename)
        jd = extract_text(await jd_file.read(),jd_file.filename)
    
    outputs = await swarm.run(jd, resume)
    agents = [
        AgentResult(agent=o.agent, status=o.status, data=o.data)
        for o in outputs
    ]
    final = outputs[-1].data

    return AnalysisResponse(
        project=settings.app_name,
        summary={
            "agents_run": len(outputs),
            "skill_coverage_percent": final.get("skill_coverage_percent", 0),
        },
        agents=agents,
        report=final,
    )
