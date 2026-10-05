# from .base import AgentOutput

# class DiligenceAgent:
#     name = "Due-Diligence Agent"

#     async def run(self, jd, resume) -> AgentOutput:
#         questions = [
#             "What are the exact day-to-day responsibilities for this role?",
#             "Which skills are mandatory on day one versus learnable after joining?",
#             "What is the interview process and how many technical rounds are there?",
#             "What engineering stack and deployment environment does the team use?",
#             "How is performance evaluated during the first 6–12 months?",
#             "What are the on-call, weekend, relocation and work-location expectations?",
#             "What compensation components are fixed, variable, bonus, ESOP or conditional?",
#             "Why is the position open: growth, replacement, or a new team?",
#         ]
#         risk_flags = []
#         if "intern" in jd.lower() and "full time" not in jd.lower():
#             risk_flags.append("Clarify conversion criteria if full-time conversion is expected.")
#         if "remote" not in jd.lower() and "hybrid" not in jd.lower() and "onsite" not in jd.lower():
#             risk_flags.append("Work-location policy is not explicit in the supplied JD.")
#         return AgentOutput(self.name, {
#             "verification_questions": questions,
#             "items_to_verify": risk_flags,
#             "note": "These are due-diligence prompts, not allegations about the employer.",
#         })

import json
from .base import AgentOutput
from app.llm import llm


DILIGENCE_SYSTEM_PROMPT = """
You are the Due-Diligence Agent in a multi-agent job opportunity analysis system.

Your task is to analyze a Job Description and Candidate Resume,
along with structured analysis produced by other agents.

You will receive:
1. Original Job Description
2. Original Candidate Resume
3. Structured Job Description Analysis from the JD Analyst
4. Structured Resume Analysis from the Resume Analyst

Your responsibility is to identify:
- Missing or unclear information in the job description
- Important information the candidate should verify
- Ambiguities in responsibilities or expectations
- Questions about interview process
- Questions about compensation
- Questions about work location and working conditions
- Areas where candidate experience should be clarified against role requirements
- Potential gaps that should be discussed with the recruiter/interviewer

IMPORTANT:
- Do not make allegations about the employer.
- Do not assume missing information is negative.
- Missing information should be treated as "needs clarification", not as a risk by itself.
- Do not invent company policies, compensation, interview rounds, responsibilities, or working conditions.
- Use only information provided in the inputs.
- Distinguish documented information from items that require verification.
- Candidate-role gaps are not proof that the candidate is unsuitable.
- Questions should be practical and specific to the supplied JD and resume.
- Avoid generic questions when the supplied information allows a more specific question.

Return ONLY a valid JSON object.

Required JSON structure:

{
    "verification_questions": [],
    "items_to_verify": [],
    "role_clarity": [],
    "candidate_role_fit_questions": [],
    "compensation_questions": [],
    "work_policy_questions": [],
    "interview_process_questions": [],
    "note": ""
}

JSON RULES:
- All arrays must contain strings.
- "note" must be a string.
- Use valid JSON escaping.
- Do not use markdown.
- Do not use ```json.
- Do not add explanations before or after the JSON.
"""






class DiligenceAgent:
    name = "Due-Diligence Agent"

    async def run(self,jd: str,resume: str,jd_analysis: dict,resume_analysis: dict,) -> AgentOutput:

        prompt = f"""
        Analyze this job opportunity for candidate due diligence.

        JOB DESCRIPTION:
        {jd}

        CANDIDATE RESUME:
        {resume}

        STRUCTURED JOB ANALYSIS:
        {json.dumps(jd_analysis, indent=2)}

        STRUCTURED RESUME ANALYSIS:
        {json.dumps(resume_analysis, indent=2)}

        Based on all the above:

        1. Identify unclear or missing information in the JD.
        2. Identify important things the candidate should verify.
        3. Identify areas where the JD requirements and resume evidence
        should be discussed or clarified.
        4. Generate practical questions for the recruiter/interviewer.
        5. Identify work-location, interview-process and compensation
        information that needs clarification.
        6. Do not assume that missing information is a negative sign.
        7. Do not make allegations about the employer.

        Return ONLY valid JSON.
        """

        response = await llm.generate(
            system=DILIGENCE_SYSTEM_PROMPT,
            prompt=prompt,
        )

        if isinstance(response, dict) and response:
            data = response
        elif isinstance(response, str) and response:
            data = json.loads(response)
        else:
            data = self.fallback_analysis(jd, resume)

        # data = {
        #         "verification_questions": [
        #           "Can you provide more information about the specific Azure/GCP/AWS AI platform you are referring to in the job description?",
        #           "Can you provide an example of a project that demonstrates your experience with Generative AI and LLMs?",
        #           "Can you elaborate on the specific requirements of the prompt engineering strategies you mentioned in the job description?"
        #         ],
        #         "items_to_verify": [
        #           "The candidate's experience with RAG (Retrieval-Augmented Generation) and Vector DBs (FAISS, Pinecone, Weaviate)",
        #           "The candidate's experience with Docker and Kubernetes (for model deployment)",
        #           "The candidate's experience with data preprocessing and feature engineering",
        #           "The candidate's experience with NLP libraries (spaCy, NLTK, Transformers)"
        #         ],
        #         "role_clarity": [
        #           "The job description mentions 'agentic AI implementation expertise', but it's not clear what this means. Can you provide more information about this requirement?",
        #           "The job description mentions 'fine-tune and customize foundation models', but it's not clear what specific models are being referred to. Can you provide more information about this requirement?"
        #         ],
        #         "important_keywords": [
        #           "Generative AI",
        #           "LLMs",
        #           "Transformers",
        #           "Python",
        #           "PyTorch",
        #           "Hugging Face Transformers",
        #           "Azure",
        #           "AWS",
        #           "GCP",
        #           "LangChain",
        #           "FastAPI",
        #           "Flask",
        #           "MLflow",
        #           "Weights & Biases"
        #         ],
        #         "ambiguities": [
        #           "The job description mentions 'agentic AI implementation expertise', but it's not clear what this means in the context of the job requirements.",
        #           "The job description mentions 'fine-tune and customize foundation models', but it's not clear what specific models are being referred to."
        #         ],
        #         "work_location": None,
        #         "interview_process": None,
        #         "compensation": None
        #       }

        return AgentOutput(self.name, data)

    def fallback_analysis(self, jd, resume):
        questions = [
            "What are the exact day-to-day responsibilities for this role?",
            "Which skills are mandatory on day one versus learnable after joining?",
            "What is the interview process and how many technical rounds are there?",
            "What engineering stack and deployment environment does the team use?",
            "How is performance evaluated during the first 6–12 months?",
            "What are the on-call, weekend, relocation and work-location expectations?",
            "What compensation components are fixed, variable, bonus, ESOP or conditional?",
            "Why is the position open: growth, replacement, or a new team?",
        ]
        risk_flags = []
        if "intern" in jd.lower() and "full time" not in jd.lower():
            risk_flags.append("Clarify conversion criteria if full-time conversion is expected.")
        if "remote" not in jd.lower() and "hybrid" not in jd.lower() and "onsite" not in jd.lower():
            risk_flags.append("Work-location policy is not explicit in the supplied JD.")
        return {
            "verification_questions": questions,
            "items_to_verify": risk_flags,
            "note": "These are due-diligence prompts, not allegations about the employer.",
        }
