import asyncio
from app.swarm import PlacementSwarm

def test_swarm_returns_all_agents():
    jd = "Backend Developer. Required: Python, Django, REST API, MySQL, Redis, Docker."
    resume = "Backend Developer with Python Django REST API and MySQL experience."
    outputs = asyncio.run(PlacementSwarm().run(jd, resume))
    assert len(outputs) == 6
    assert outputs[-1].agent == "Decision Synthesizer"
    assert "matched_skills" in outputs[-1].data["evidence"]
