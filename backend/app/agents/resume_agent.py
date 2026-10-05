from .base import AgentOutput
from .jd_agent import SKILLS
from app.llm import llm
import json

# class ResumeAgent:
#     name = "Resume Analyst"

#     async def run(self, resume: str) -> AgentOutput:
#         low = resume.lower()
#         skills = [s.capitalize() for s in SKILLS if s in low]
#         projects = []
#         for line in resume.splitlines():
#             line = line.strip(" -•\t")
#             if len(line) > 35 and any(k in line.lower() for k in ["project", "service", "application", "api", "platform", "microservice"]):
#                 projects.append(line[:180])
#         return AgentOutput(self.name, {
#             "detected_skills": skills,
#             "projects_or_evidence": projects[:12],
#             "has_backend_evidence": any(x in low for x in ["django", "fastapi", "backend", "rest api", "microservice"]),
#         })


RESUME_SYSTEM_PROMPT = """
You are a Resume Analyst.


Analyze the candidate resume objectively.

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
    "technical_skills": [],
    "programming_languages": [],
    "frameworks": [],
    "databases": [],
    "cloud_devops": [],
    "projects": [],
    "professional_experience": [],
    "measurable_achievements": [],
    "education": [],
    "backend_evidence": [],
    "api_microservices_evidence": [],
    "ai_ml_evidence": []
}


Rules:
- Do not invent candidate experience.
- Do not assume a skill merely because it is similar to another skill.
- Distinguish explicit evidence from inferred evidence.
- Do not invent information.
- Strings inside JSON must use valid JSON escaping.
"""

class ResumeAgent():
    name = "Resume Analyst"

    async def run(self, resume: str) -> str:
        resume_prompt = f"""
            Analyze this resume.

            RESUME:
            {resume}
        """
        response = await llm.generate(
            system=RESUME_SYSTEM_PROMPT,
            prompt=resume_prompt
        )
        try:
            data = response
            # print("ResumeAgent try:", data)
        except Exception as e:
            data = self.fallback_analysis(resume)
        # print("ResumeAgent:", type(data))

        if type(data) == str:
            data = json.loads(data)

    #     data = {
    #     "technical_skills": [
    #       "Python",
    #       "JavaScript",
    #       "TypeScript",
    #       "Java",
    #       "SQL",
    #       "Django",
    #       "Django REST Framework",
    #       "FastAPI",
    #       "Node.js",
    #       "Express.js",
    #       "REST APIs",
    #       "Microservices",
    #       "React.js",
    #       "React Native",
    #       "HTML",
    #       "CSS",
    #       "Tailwind CSS",
    #       "PostgreSQL",
    #       "MySQL",
    #       "MongoDB",
    #       "Redis",
    #       "Elasticsearch",
    #       "AWS S3",
    #       "AWS EC2",
    #       "AWS SES",
    #       "Docker",
    #       "Git"
    #     ],
    #     "programming_languages": [
    #       "Python",
    #       "JavaScript",
    #       "TypeScript",
    #       "Java",
    #       "SQL"
    #     ],
    #     "frameworks": [
    #       "Django",
    #       "Django REST Framework",
    #       "FastAPI",
    #       "Node.js",
    #       "Express.js"
    #     ],
    #     "databases": [
    #       "PostgreSQL",
    #       "MySQL",
    #       "MongoDB",
    #       "Redis",
    #       "Elasticsearch"
    #     ],
    #     "cloud_devops": [
    #       "AWS S3",
    #       "AWS EC2",
    #       "AWS SES",
    #       "Docker",
    #       "Git"
    #     ],
    #     "projects": [
    #       "Customer Portal",
    #       "Picker App",
    #       "Selsmart"
    #     ],
    #     "professional_experience": [
    #       "Full Stack Developer|Attero Recycling Pvt. Ltd.",
    #       "Backend Developer|Rapipay Fintech Pvt. Ltd."
    #     ],
    #     "measurable_achievements": [],
    #     "education": [
    #       "Dcrust University Murthal",
    #       "B. Tech in Computer Science",
    #       "Aug 2017 – July 2020"
    #     ],
    #     "backend_evidence": [
    #       "Architected and developed a scalable Customer Portal from scratch using Python, Django, DRF, MySQL, REST APIs, authentication, role-based access control, and admin dashboards.",
    #       "Architected and maintained scalable backend infrastructure for a B2B2C mutual fund platform using Python, Django, DRF, MySQL, Redis, and Elasticsearch.",
    #       "Developed KYC, Notification, Image Cache, and Tokenization microservices, including a third-party KYC API with 21 verification data points and comprehensive unit testing.",
    #       "Built secure backend services for OTP, email notifications, SVG-to-PNG conversion, and encryption/decryption of sensitive customer data.",
    #       "Migrated the CRM platform from Leadsquared to SimpleCRM and integrated multiple independent microservices with Node.js, JavaScript, and PostgreSQL.",
    #       "Developed the Partner Portal backend and REST APIs, enabling investment fund recommendations through secure, scalable microservice architecture."
    #     ],
    #     "api_microservices_evidence": [
    #       "Designed and integrated secure third-party APIs, enabling seamless client and vendor onboarding, order management, validation, and automated business workflows.",
    #       "Built integrations with multiple third-party services, including outbound calling APIs, AI-based image verification, document/image upload workflows, and automated payment-link generation through SMS/WhatsApp, enabling seamless order verification and payment collection.",
    #       "Implemented the pickup-to-GRN workflow, allowing pickers to capture item images and collect order information at the customer location, perform AI-based item verification, scan item barcodes, and generate GRN/consignment details after successful pickup and payment processing."
    #     ],
    #     "ai_ml_evidence": [
    #       "Implemented AI-based image verification in the Picker App, enabling seamless order verification and payment collection."
    #     ]
    #   }

        return AgentOutput(
            self.name,
            data
        )

    def fallback_analysis(self,resume):
        low = resume.lower()
        skills = [s.capitalize() for s in SKILLS if s in low]
        projects = []
        for line in resume.splitlines():
            line = line.strip(" -•\t")
            if len(line) > 35 and any(k in line.lower() for k in ["project", "service", "application", "api", "platform", "microservice"]):
                projects.append(line[:180])
        return AgentOutput(self.name, {
            "detected_skills": skills,
            "projects_or_evidence": projects[:12],
            "has_backend_evidence": any(x in low for x in ["django", "fastapi", "backend", "rest api", "microservice"]),
        })
    

