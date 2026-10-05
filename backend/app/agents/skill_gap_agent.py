# from .base import AgentOutput

# class SkillGapAgent:
#     name = "Skill Gap Agent"

#     async def run(self, jd_data, resume_data) -> AgentOutput:
#         required = set(jd_data.get("required_skills", []))
#         candidate = set(resume_data.get("technical_skills", []))
        
#         # matched = sorted(required & candidate)
#         # missing = sorted(required - candidate)
#         required_lower = {x.lower() for x in required}
#         candidate_lower = {x.lower() for x in candidate}

#         matched = sorted(required_lower & candidate_lower)
#         missing = sorted(required_lower - candidate_lower)
#         coverage = round((len(matched) / len(required)) * 100, 1) if required else 0
#         return AgentOutput(self.name, {
#             "matched_skills": matched,
#             "missing_skills": missing,
#             "coverage_percent": coverage,
#             "interpretation": "Coverage is a keyword/evidence signal, not a hiring probability.",
#         })


import json

from .base import AgentOutput
from app.llm import llm


SKILL_GAP_SYSTEM_PROMPT = """
You are a Skill Gap Analysis Agent in a multi-agent job analysis system.

Your task is to compare the skills required by a Job Description against
skills and evidence present in a candidate resume.

IMPORTANT RULES:

- Match skills based on actual evidence in the resume.
- Ignore uppercase/lowercase differences.
- Understand common equivalent terminology where the evidence supports it.
- Do NOT assume that two technologies are equivalent just because they are
  related.
- For example:
  Django != FastAPI
  MySQL != PostgreSQL
  AWS != Azure
  React != React Native
- A broader skill should not automatically prove a more specific skill.
- If a skill appears related but there is insufficient evidence, classify it
  as a partial match instead of a full match.
- Do not invent candidate experience.
- Do not treat a JD preferred skill as mandatory.
- Focus primarily on required skills.
- Preserve the original JD skill wording where possible.

Return ONLY valid JSON.

Required JSON structure:

{
    "matched_skills": [],
    "missing_skills": [],
    "partial_matches": [],
    "evidence": [],
    "skill_observations": []
}

Rules:

- All fields must contain arrays of strings.
- Return valid JSON.
- Do not use markdown.
- Do not use ```json.
- Do not add explanations before or after the JSON.
"""


class SkillGapAgent:
    name = "Skill Gap Agent"

    async def run(
        self,
        jd_data: dict,
        resume_data: dict
    ) -> AgentOutput:

        prompt = f"""
        Compare the required skills from the job description with the
        candidate's resume evidence.

        JOB DESCRIPTION ANALYSIS:
        {json.dumps(jd_data, indent=2)}

        RESUME ANALYSIS:
        {json.dumps(resume_data, indent=2)}

        Perform the following:

        1. Identify required skills that have explicit evidence in the resume.
        2. Identify required skills that have no sufficient evidence.
        3. Identify partial matches where the candidate has related experience
           but the exact required skill is not sufficiently demonstrated.
        4. Provide short evidence for important matched skills.
        5. Provide observations about important skill gaps.

        Do not invent experience.

        Return ONLY valid JSON.
        """

        print("skill gap agent running")

        response = await llm.generate(
            system=SKILL_GAP_SYSTEM_PROMPT,
            prompt=prompt,
        )

        print("Skill Gap response:", response)

        if isinstance(response, dict) and response:
            data = response
        else:
            data = self.fallback_analysis(
                jd_data,
                resume_data,
            )

        # # Calculate coverage deterministically in Python.
        # required_skills = jd_data.get(
        #     "required_skills",
        #     []
        # )

        # matched_skills = data.get(
        #     "matched_skills",
        #     []
        # )

        # coverage = (
        #     round(
        #         (len(matched_skills) / len(required_skills)) * 100,
        #         1,
        #     )
        #     if required_skills
        #     else 0
        # )

        # data["coverage_percent"] = coverage

        # data["interpretation"] = (
        #     "Coverage is a keyword/evidence signal, "
        #     "not a hiring probability."
        # )
    #     data = {
    #     "matched_skills": [
    #       "Python",
    #       "Django",
    #       "FastAPI",
    #       "Git",
    #       "AWS",
    #       "Docker",
    #       "PostgreSQL",
    #       "MySQL",
    #       "MLflow",
    #       "Weights & Biases"
    #     ],
    #     "missing_skills": [
    #       "Generative AI (LLMs, Transformers)",
    #       "PyTorch",
    #       "Hugging Face Transformers",
    #       "LangChain/Langgraph",
    #       "Azure/AWS/GCP cloud platforms",
    #       "REST APIs",
    #       "Flask",
    #       "ML pipeline tools",
    #       "RAG (Retrieval-Augmented Generation)",
    #       "Vector DBs (FAISS, Pinecone, Weaviate)",
    #       "Streamlit/Gradio",
    #       "Kubernetes",
    #       "Data preprocessing & feature engineering",
    #       "NLP libraries: spaCy, NLTK, Transformers",
    #       "Agentic AI implementation expertise",
    #       "Collaborate with data engineers and MLOps teams",
    #       "Integrate GenAI into enterprise applications",
    #       "Evaluate model performance",
    #       "Keep up to date with the latest research"
    #     ],
    #     "partial_matches": [
    #       "JavaScript",
    #       "TypeScript",
    #       "Java",
    #       "SQL",
    #       "Node.js",
    #       "Express.js",
    #       "React.js",
    #       "React Native",
    #       "HTML",
    #       "CSS",
    #       "Tailwind CSS",
    #       "MongoDB",
    #       "Redis",
    #       "Elasticsearch",
    #       "AWS S3",
    #       "AWS EC2",
    #       "AWS SES"
    #     ],
    #     "evidence": [
    #       "Architected and developed a scalable Customer Portal from scratch using Python, Django, DRF, MySQL, REST APIs, authentication, role-based access control, and admin dashboards.",
    #       "Architected and maintained scalable backend infrastructure for a B2B2C mutual fund platform using Python, Django, DRF, MySQL, Redis, and Elasticsearch.",
    #       "Developed KYC, Notification, Image Cache, and Tokenization microservices, including a third-party KYC API with 21 verification data points and comprehensive unit testing.",
    #       "Built secure backend services for OTP, email notifications, SVG-to-PNG conversion, and encryption/decryption of sensitive customer data.",
    #       "Migrated the CRM platform from Leadsquared to SimpleCRM and integrated multiple independent microservices with Node.js, JavaScript, and PostgreSQL.",
    #       "Developed the Partner Portal backend and REST APIs, enabling investment fund recommendations through secure, scalable microservice architecture.",
    #       "Designed and integrated secure third-party APIs, enabling seamless client and vendor onboarding, order management, validation, and automated business workflows.",
    #       "Built integrations with multiple third-party services, including outbound calling APIs, AI-based image verification, document/image upload workflows, and automated payment-link generation through SMS/WhatsApp, enabling seamless order verification and payment collection.",
    #       "Implemented the pickup-to-GRN workflow, allowing pickers to capture item images and collect order information at the customer location, perform AI-based item verification, scan item barcodes, and generate GRN/consignment details after successful pickup and payment processing.",
    #       "Implemented AI-based image verification in the Picker App, enabling seamless order verification and payment collection."
    #     ],
    #     "skill_observations": [
    #       "The candidate has experience with Python, Django, and MySQL, but lacks experience with PyTorch and Hugging Face Transformers.",
    #       "The candidate has experience with AWS and Docker, but lacks experience with Azure and GCP cloud platforms.",
    #       "The candidate has experience with REST APIs, but lacks experience with Flask and ML pipeline tools.",
    #       "The candidate has experience with PostgreSQL and MySQL, but lacks experience with Vector DBs (FAISS, Pinecone, Weaviate).",
    #       "The candidate has experience with Node.js and Express.js, but lacks experience with React.js and React Native.",
    #       "The candidate has experience with HTML, CSS, and Tailwind CSS, but lacks experience with data preprocessing and feature engineering.",
    #       "The candidate has experience with MongoDB and Redis, but lacks experience with Elasticsearch.",
    #       "The candidate has experience with AWS S3 and AWS EC2, but lacks experience with Azure and GCP cloud platforms.",
    #       "The candidate has experience with Git, but lacks experience with CI/CD for ML and MLOps tools.",
    #       "The candidate has experience with AI-based image verification, but lacks experience with Agentic AI implementation expertise and model evaluation."
    #     ],
    #     "coverage_percent": 83.3,
    #     "interpretation": "Coverage is a keyword/evidence signal, not a hiring probability."
    #   }

        required = jd_data.get("required_skills", [])

        matched = data.get("matched_skills", [])
        partial = data.get("partial_matches", [])
        missing = data.get("missing_skills", [])
        required = {x.lower() for x in required}
        matched = {x.lower() for x in matched}
        missing = {x.lower() for x in missing}
        tech_skills = {x.lower() for x in resume_data.get("technical_skills", []) if x.lower() in required}

        total = list(set(list(required) + list(missing)))

        # valid_matched = required & matched
        # print("valid matched", valid_matched)
        valid_matched = []
        for x in matched:
            for y in required:
                if x in y:
                    valid_matched.append(x)
                    break
        total_matched = list(set(list(valid_matched) + list(tech_skills)))
        coverage = (len(total_matched) + len(partial)*0.5) / len(total) * 100
        data["coverage_percent"] = coverage
        return AgentOutput(self.name, data)

    def fallback_analysis(
        self,
        jd_data: dict,
        resume_data: dict,
    ) -> dict:

        required = jd_data.get(
            "required_skills",
            []
        )

        candidate = resume_data.get(
            "technical_skills",
            []
        )

        required_map = {
            str(skill).strip().lower(): str(skill).strip()
            for skill in required
        }

        candidate_lower = {
            str(skill).strip().lower()
            for skill in candidate
        }

        matched = []
        missing = []

        for skill_lower, original_skill in required_map.items():

            if skill_lower in candidate_lower:
                matched.append(original_skill)
            else:
                missing.append(original_skill)

        return {
            "matched_skills": sorted(matched),
            "missing_skills": sorted(missing),
            "partial_matches": [],
            "evidence": [],
            "skill_observations": [],
        }
