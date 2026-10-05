# from .base import AgentOutput

# class InterviewAgent:
#     name = "Interview Prep Agent"

#     async def run(self, jd_data, gap_data) -> AgentOutput:
#         skills = jd_data.get("required_skills", [])
#         missing = gap_data.get("missing_skills", [])
#         topics = []
#         for s in skills[:10]:
#             topics.append(f"Explain your practical experience with {s} and discuss one implementation trade-off.")
#         if "system design" in skills:
#             topics.append("Design a scalable service and explain caching, database, observability and failure handling.")
#         if "data structures" in skills or "algorithms" in skills:
#             topics.append("Prepare arrays, strings, hashing, trees, graphs and complexity analysis.")
#         return AgentOutput(self.name, {
#             "technical_topics": topics[:12],
#             "gap_topics": [f"Study and practice: {x}" for x in missing[:8]],
#             "behavioral_topics": [
#                 "Explain a production issue you diagnosed and fixed.",
#                 "Describe a disagreement in an engineering decision and how it was resolved.",
#                 "Explain one project where you owned backend/API design end-to-end.",
#             ],
#         })


import json

from .base import AgentOutput
from app.llm import llm


INTERVIEW_SYSTEM_PROMPT = """
You are an Interview Preparation Agent in a multi-agent job analysis system.

Your task is to generate a personalized technical and behavioral interview
preparation plan for a candidate based on:

1. Job Description analysis
2. Candidate Resume analysis
3. Candidate skill-gap analysis

The goal is to prepare the candidate for the actual role.

IMPORTANT RULES:

- Use only information provided in the inputs.
- Do not invent candidate experience.
- Do not claim that the candidate has a skill unless it appears in the
  supplied resume analysis.
- Clearly distinguish between existing experience and skills that need study.
- Prioritize skills explicitly required by the JD.
- Give more attention to missing or weak skills.
- Generate practical interview questions, not generic questions.
- Include implementation and trade-off questions for technical skills.
- Include scenario-based questions where appropriate.
- Include questions based on the candidate's actual projects and experience.
- Do not make assumptions about the company's actual interview process.
- Do not claim that these are the exact questions the company will ask.

Return ONLY a valid JSON object.

Required JSON structure:

{
    "technical_topics": [],
    "technical_questions": [],
    "skill_gap_topics": [],
    "project_based_questions": [],
    "system_design_topics": [],
    "coding_topics": [],
    "behavioral_topics": [],
    "preparation_priorities": [],
    "note": ""
}

JSON RULES:

- All arrays must contain strings.
- "note" must be a string.
- Return valid JSON.
- Do not use markdown.
- Do not use ```json.
- Do not add text before or after the JSON.
"""


class InterviewAgent:
    name = "Interview Prep Agent"

    async def run(
        self,
        jd_data: dict,
        resume_data: dict,
        gap_data: dict,
    ) -> AgentOutput:

        prompt = f"""
        Create a personalized interview preparation plan for this candidate.

        JOB DESCRIPTION ANALYSIS:
        {json.dumps(jd_data, indent=2)}

        RESUME ANALYSIS:
        {json.dumps(resume_data, indent=2)}

        SKILL GAP ANALYSIS:
        {json.dumps(gap_data, indent=2)}

        Analyze the above information and generate:

        1. Technical topics based on required JD skills.
        2. Practical technical interview questions.
        3. Topics the candidate should study based on missing skills.
        4. Questions based on the candidate's actual projects and experience.
        5. System design topics if relevant to the role.
        6. Coding/DSA topics if relevant to the role.
        7. Behavioral questions relevant to the candidate's experience.
        8. Preparation priorities.

        For technical questions, prefer questions that test:
        - practical implementation
        - debugging
        - architecture
        - scalability
        - trade-offs
        - production scenarios

        For project questions, use actual projects and technologies
        present in the resume analysis.

        Do not invent experience or technologies.

        Return ONLY valid JSON.
        """

        response = await llm.generate(
            system=INTERVIEW_SYSTEM_PROMPT,
            prompt=prompt,
        )

        print("Interview response:", response,type(response))

        if isinstance(response, dict) and response:
            data = response
        elif isinstance(response, str) and response:
            data = json.loads(response)
        else:
            data = self.fallback_analysis(
                jd_data,
                resume_data,
                gap_data,
            )

    #     data = {
    #     "technical_topics": [
    #       "Generative AI (LLMs, Transformers)",
    #       "PyTorch",
    #       "Hugging Face Transformers",
    #       "Azure/AWS/GCP cloud platforms",
    #       "LangChain/Langgraph",
    #       "REST APIs",
    #       "FastAPI",
    #       "Flask",
    #       "ML pipeline tools (MLflow, Weights & Biases)",
    #       "Git",
    #       "CI/CD for ML (e.g., Azure ML, SageMaker pipelines)",
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
    #     "technical_questions": [
    #       "Design a generative AI model using LLMs and PyTorch. How would you optimize its performance?",
    #       "Implement a REST API using FastAPI and Flask. How would you handle errors and exceptions?",
    #       "Describe the architecture of a cloud-based ML pipeline using Azure/AWS/GCP. How would you ensure scalability?",
    #       "Write a Python function to perform data preprocessing and feature engineering. How would you handle missing values?",
    #       "Implement a Vector DB using FAISS. How would you optimize its performance for large datasets?",
    #       "Design a system to integrate GenAI into an enterprise application. How would you handle security and scalability?",
    #       "Describe the trade-offs between using PyTorch and Hugging Face Transformers for a generative AI model. How would you choose one over the other?",
    #       "Implement a CI/CD pipeline using Azure ML and SageMaker. How would you handle errors and exceptions?",
    #       "Write a Python function to perform AI-based image verification. How would you handle false positives and negatives?",
    #       "Describe the benefits and drawbacks of using Streamlit/Gradio for prototyping. How would you choose one over the other?"
    #     ],
    #     "skill_gap_topics": [
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
    #     "project_based_questions": [
    #       "Describe the backend infrastructure of the Customer Portal you developed using Python, Django, and MySQL. How did you handle scalability?",
    #       "Implement the Partner Portal backend and REST APIs using Node.js, JavaScript, and PostgreSQL. How did you handle security?",
    #       "Describe the AI-based image verification system you implemented in the Picker App using Python and TensorFlow. How did you handle false positives and negatives?"
    #     ],
    #     "system_design_topics": [
    #       "Design a cloud-based ML pipeline using Azure/AWS/GCP. How would you ensure scalability?",
    #       "Design a system to integrate GenAI into an enterprise application. How would you handle security and scalability?",
    #       "Describe the architecture of a Vector DB using FAISS. How would you optimize its performance for large datasets?"
    #     ],
    #     "coding_topics": [
    #       "Write a Python function to perform data preprocessing and feature engineering. How would you handle missing values?",
    #       "Implement a REST API using FastAPI and Flask. How would you handle errors and exceptions?",
    #       "Write a Python function to perform AI-based image verification. How would you handle false positives and negatives?"
    #     ],
    #     "behavioral_topics": [
    #       "Describe a situation where you had to collaborate with data engineers and MLOps teams. How did you handle conflicts?",
    #       "Describe a situation where you had to integrate GenAI into an enterprise application. How did you handle security and scalability?",
    #       "Describe a situation where you had to evaluate model performance. How did you handle false positives and negatives?"
    #     ],
    #     "preparation_priorities": [
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
    #     "note": "Focus on practical implementation and debugging questions. Use actual projects and technologies present in the resume analysis."
    #   }

        

        return AgentOutput(self.name, data)

    def fallback_analysis(
        self,
        jd_data: dict,
        resume_data: dict,
        gap_data: dict,
    ) -> dict:

        skills = jd_data.get("required_skills", [])
        missing = gap_data.get("missing_skills", [])
        projects = resume_data.get("projects", [])

        topics = []

        for skill in skills[:10]:
            topics.append(
                f"Explain your practical experience with {skill} "
                f"and discuss one implementation trade-off."
            )

        system_design_topics = []

        skill_names = [
            str(skill).lower()
            for skill in skills
        ]

        if "system design" in skill_names:
            system_design_topics.append(
                "Design a scalable service and explain caching, "
                "database design, observability and failure handling."
            )

        coding_topics = []

        if (
            "data structures" in skill_names
            or "algorithms" in skill_names
            or "dsa" in skill_names
        ):
            coding_topics.append(
                "Prepare arrays, strings, hashing, trees, graphs "
                "and complexity analysis."
            )

        project_questions = []

        for project in projects[:5]:
            project_questions.append(
                f"Explain the architecture, your contribution, "
                f"key challenges and trade-offs in this project: {project}"
            )

        return {
            "technical_topics": topics[:12],

            "technical_questions": topics[:10],

            "skill_gap_topics": [
                f"Study and practice: {skill}"
                for skill in missing[:8]
            ],

            "project_based_questions": project_questions,

            "system_design_topics": system_design_topics,

            "coding_topics": coding_topics,

            "behavioral_topics": [
                "Explain a production issue you diagnosed and fixed.",
                "Describe a disagreement in an engineering decision and how it was resolved.",
                "Explain one project where you owned backend/API design end-to-end.",
            ],

            "preparation_priorities": [
                f"Prepare practical examples for {skill}"
                for skill in skills[:5]
            ],

            "note": (
                "Interview preparation is based on the supplied "
                "JD, resume and skill-gap analysis."
            ),
        }
