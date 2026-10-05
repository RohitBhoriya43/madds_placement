# import re
# from .base import AgentOutput

# SKILLS = [
#     "python", "django", "fastapi", "flask", "java", "spring boot", "javascript",
#     "typescript", "react", "node.js", "sql", "mysql", "postgresql", "mongodb",
#     "redis", "elasticsearch", "aws", "docker", "kubernetes", "git", "rest api",
#     "microservices", "machine learning", "llm", "rag", "langchain", "langgraph",
#     "data structures", "algorithms", "system design", "pytest"
# ]

# class JDAgent:
#     name = "JD Analyst"

#     async def run(self, jd: str) -> AgentOutput:
#         low = jd.lower()
#         skills = [s for s in SKILLS if s in low]
#         years = re.findall(r"(\d+)\+?\s*(?:years?|yrs?)", low)
#         responsibilities = []
#         for line in jd.splitlines():
#             line = line.strip(" -•\t")
#             if len(line) > 30 and any(x in line.lower() for x in ["develop", "build", "design", "maintain", "implement", "lead"]):
#                 responsibilities.append(line[:180])
#         return AgentOutput(self.name, {
#             "role_signals": self._role_signals(jd),
#             "required_skills": skills,
#             "experience_years_mentions": years,
#             "responsibilities": responsibilities[:10],
#         })

#     def _role_signals(self, jd):
#         low = jd.lower()
#         signals = []
#         for word, label in [
#             ("backend", "Backend"),
#             ("full stack", "Full Stack"),
#             ("data", "Data"),
#             ("machine learning", "ML"),
#             ("ai", "AI"),
#             ("devops", "DevOps"),
#         ]:
#             if word in low:
#                 signals.append(label)
#         return list(dict.fromkeys(signals))


import json
import re

from .base import AgentOutput
from app.llm import llm

SKILLS = [
    "python", "django", "fastapi", "flask", "java", "spring boot", "javascript",
    "typescript", "react", "node.js", "sql", "mysql", "postgresql", "mongodb",
    "redis", "elasticsearch", "aws", "docker", "kubernetes", "git", "rest api",
    "microservices", "machine learning", "llm", "rag", "langchain", "langgraph",
    "data structures", "algorithms", "system design", "pytest"
]


JD_SYSTEM_PROMPT = """
You are a Job Description Analyst.

Analyze the supplied job description.

Return ONLY a valid JSON object.

DO NOT:
- write explanations
- write markdown
- use ```json
- add text before JSON
- add text after JSON

The response must be valid JSON that can be parsed directly using Python json.loads().

Required structure:

{
    "role_signals": [],
    "required_skills": [],
    "preferred_skills": [],
    "IT_skills": [],
    "experience_years": null,
    "responsibilities": [],
    "education": null,
    "location": null,
    "work_mode": null,
    "important_keywords": [],
    "ambiguities": []
}

Rules:
- Use only information from the supplied job description.
- Do not invent information.
- Strings inside JSON must use valid JSON escaping.
"""


class JDAgent:
    name = "JD Analyst"

    async def run(self, jd: str) -> AgentOutput:

        prompt = f"""
Analyze this job description.

JOB DESCRIPTION:
{jd}
"""

        response = await llm.generate(
            system=JD_SYSTEM_PROMPT,
            prompt=prompt
        )

        try:
            data = response
            # print("JDAgent try:", data)
        except Exception as e:
            # print(e,"rrrrrrr")
            data = self.fallback_analysis(jd)
        # print("JDAgent:", type(data))

        if type(data) == str:
            data = json.loads(data)

    #     data= {
    #     "role_signals": [],
    #     "required_skills": [
    #       "Generative AI (LLMs, Transformers)",
    #       "Python",
    #       "PyTorch",
    #       "Hugging Face Transformers",
    #       "Azure/AWS/GCP cloud platforms",
    #       "LangChain/Langgraph or similar orchestration frameworks",
    #       "REST APIs",
    #       "FastAPI",
    #       "Flask",
    #       "ML pipeline tools (MLflow, Weights & Biases)",
    #       "Git",
    #       "CI/CD for ML (e.g., Azure ML, SageMaker pipelines)"
    #     ],
    #     "preferred_skills": [
    #       "RAG (Retrieval-Augmented Generation)",
    #       "Vector DBs (FAISS, Pinecone, Weaviate)",
    #       "Streamlit/Gradio for prototyping",
    #       "Docker",
    #       "Kubernetes (for model deployment)",
    #       "Data preprocessing & feature engineering",
    #       "NLP libraries: spaCy, NLTK, Transformers"
    #     ],
    #     "experience_years": 4,
    #     "responsibilities": [
    #       "Design, build, and deploy generative AI solutions using LLMs",
    #       "Fine-tune and customize foundation models",
    #       "Develop and optimize prompt engineering strategies",
    #       "Implement model pipelines using Python and ML frameworks",
    #       "Agentic AI implementation expertise",
    #       "Collaborate with data engineers and MLOps teams",
    #       "Integrate GenAI into enterprise applications",
    #       "Evaluate model performance",
    #       "Keep up to date with the latest research"
    #     ],
    #     "education": "Bachelor of Engineering, Bachelor of Technology",
    #     "location": None,
    #     "work_mode": None,
    #     "important_keywords": [
    #       "Generative AI",
    #       "LLMs",
    #       "Transformers",
    #       "Python",
    #       "PyTorch",
    #       "Hugging Face Transformers",
    #       "Azure",
    #       "AWS",
    #       "GCP",
    #       "LangChain",
    #       "FastAPI",
    #       "Flask",
    #       "MLflow",
    #       "Weights & Biases"
    #     ],
    #     "ambiguities": []
    #   }

        return AgentOutput(
            self.name,
            data
        )

    def fallback_analysis(self, jd):
        low = jd.lower()

        skills = [
            s for s in SKILLS
            if s in low
        ]

        years = re.findall(
            r"(\d+)\+?\s*(?:years?|yrs?)",
            low
        )

        return {
            "role_signals": self._role_signals(jd),
            "required_skills": skills,
            "preferred_skills": [],
            "experience_years": years,
            "responsibilities": [],
            "education": [],
            "location": "",
            "work_mode": "",
            "important_keywords": skills,
            "ambiguities": [],
        }

    def _role_signals(self, jd):
        low = jd.lower()

        signals = []

        for word, label in [
            ("backend", "Backend"),
            ("full stack", "Full Stack"),
            ("data", "Data"),
            ("machine learning", "ML"),
            ("ai", "AI"),
            ("devops", "DevOps"),
        ]:
            if word in low:
                signals.append(label)

        return list(dict.fromkeys(signals))
