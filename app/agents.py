# app/agents.py
"""
Agent definitions and orchestrator for the Multi-Agent Research Team.
This file exposes `run_team(topic: str)` which returns a dict with keys:
  research, analysis, strategy, coordinator
"""

import asyncio
from typing import Dict
from .utils import call_openrouter


async def researcher(topic: str) -> str:
    prompt = (
        f"You are a Researcher. Provide concise, factual background information about the following topic. "
        f"List the types of sources you would consult. Be thorough but concise (max 500 words).\n\n"
        f"Topic: {topic}"
    )
    return await call_openrouter(prompt)

async def analyst(topic: str, research_text: str = "") -> str:
    prompt = (
        f"You are an Analyst. Based on the research summary and the topic, identify key patterns, risks, "
        f"opportunities, and trade-offs. Produce a clear bulleted list and a short (2-3 sentence) summary.\n\n"
        f"Topic: {topic}\n\nResearch Summary:\n{research_text}"
    )
    return await call_openrouter(prompt)

async def strategist(topic: str, research_text: str = "", analysis_text: str = "") -> str:
    prompt = (
        f"You are a Strategist. Using the research and analysis, propose 3 practical, prioritized next steps "
        f"(short term, mid term, long term). For each step include one metric to track success.\n\n"
        f"Topic: {topic}\n\nResearch:\n{research_text}\n\nAnalysis:\n{analysis_text}"
    )
    return await call_openrouter(prompt)

async def coordinator(topic: str, researcher_out: str, analyst_out: str, strategist_out: str) -> str:
    prompt = (
        "You are the Project Coordinator. Combine the team outputs into a single concise briefing for executives. "
        "Include a 2-paragraph summary and a 3-line recommended action item list.\n\n"
        f"Topic: {topic}\n\nResearcher Output:\n{researcher_out}\n\nAnalyst Output:\n{analyst_out}\n\nStrategist Output:\n{strategist_out}"
    )
    return await call_openrouter(prompt)


async def _run_team_async(topic: str) -> Dict[str, str]:
    """
    Internal async orchestrator: runs researcher first, then analyst & strategist in parallel,
    then coordinator to synthesize.
    """
    researcher_out = await researcher(topic)

    analyst_task = asyncio.create_task(analyst(topic, research_text=researcher_out))
    strategist_task = asyncio.create_task(strategist(topic, research_text=researcher_out))
    analyst_out, strategist_out = await asyncio.gather(analyst_task, strategist_task)

    coordinator_out = await coordinator(topic, researcher_out, analyst_out, strategist_out)

    return {
        "research": researcher_out,
        "analysis": analyst_out,
        "strategy": strategist_out,
        "coordinator": coordinator_out,
    }

def run_team(topic: str) -> Dict[str, str]:
    """
    Public helper to run the team from synchronous contexts.
    It runs the internal async orchestrator and returns the results dict.
    NOTE: If you call this from an already-running event loop (e.g., some async servers),
    you should use the _run_team_async coroutine directly instead of this helper.
    """
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(_run_team_async(topic))
    finally:
        loop.close()
