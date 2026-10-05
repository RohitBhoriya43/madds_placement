import asyncio
from .agents.jd_agent import JDAgent
from .agents.resume_agent import ResumeAgent
from .agents.skill_gap_agent import SkillGapAgent
from .agents.diligence_agent import DiligenceAgent
from .agents.interview_agent import InterviewAgent
from .agents.synthesizer import Synthesizer

class PlacementSwarm:
    async def run(self, jd: str, resume: str):
        jd_agent, resume_agent = JDAgent(), ResumeAgent()
        print("jd and resume agent running")
        jd_out, resume_out = await asyncio.gather(
            jd_agent.run(jd),
            resume_agent.run(resume),
        )
        
        print("skill gap agent running")
        gap_out = await SkillGapAgent().run(jd_out.data, resume_out.data)
        print("diligence agent running")
        diligence_out = await DiligenceAgent().run(jd, resume,jd_out.data, resume_out.data)
        print("interview agent running")
        interview_out = await InterviewAgent().run(
            jd_out.data,resume_out.data, gap_out.data
        )
        print("synthesis agent running")
        synthesis_out = await Synthesizer().run(
            jd_out.data,
            resume_out.data,
            gap_out.data,
            diligence_out.data,
            interview_out.data,
        )

        return [jd_out, resume_out, gap_out, diligence_out, interview_out, synthesis_out]
