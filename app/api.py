# app/api.py
"""
Simple FastAPI app exposing an endpoint to run the multi-agent pipeline.
This file is optional to run if you want a programmatic HTTP interface.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio

from .agents import run_team

app = FastAPI(title="Multi-Agent Research Team API")


class TopicRequest(BaseModel):
    topic: str


@app.post("/run")
async def run_endpoint(req: TopicRequest):
    if not req.topic or not req.topic.strip():
        raise HTTPException(status_code=400, detail="topic is required")
    try:
        result = await asyncio.to_thread(run_team, req.topic)
        return {"success": True, "topic": req.topic, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"failed to run team: {e}")
