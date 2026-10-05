from pydantic import BaseModel, Field
from typing import List, Dict, Any,Optional
from fastapi import File, UploadFile, Form

class AnalyzeRequest(BaseModel):
    job_description: str = Field(min_length=20)

    resume_text: Optional[str] = None

    @classmethod
    def as_form(
        cls,
        job_description: Optional[str] = Form(None),
        resume_text: Optional[str] = Form(None),
    ):
        return cls(
            job_description=job_description.strip() if job_description else None,
            resume_text=resume_text.strip() or None
            if resume_text else None,
        )
class AgentResult(BaseModel):
    agent: str
    status: str
    data: Dict[str, Any]

class AnalysisResponse(BaseModel):
    project: str
    summary: Dict[str, Any]
    agents: List[AgentResult]
    report: Dict[str, Any]
