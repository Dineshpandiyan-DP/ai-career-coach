import logging
from fastapi import HTTPException 
from app.config import get_settings
from app.models import (
    AgentRequest,
    AgentResponse,
    AgentTool,
    ResumeReviewRequest,
    MockInterviewRequest,
    LearningRoadmapRequest,
)
from app.tools import review_resume,run_mock_interview,generate_roadmap

logger=logging.getLogger(__name__)
settings=get_settings()

class CareerCoachAgent:
    """
    The main AI Career Coach Agent.
    Receives a tool name and payload.
    Validates payload, calls the right tool, returns response.
    """
    def run(self, request:AgentRequest)->AgentResponse:
        logger.info(f"Agent running tool:{request.tool}")

        if request.tool== AgentTool.RESUME_REVIEW:
            return self._handle_resume_review(request.payload)
        
        elif request.tool== AgentTool.MOCK_INTERVIEW:
            return self._handle_mock_interview(request.payload)
        
        elif request.tool== AgentTool.LEARNING_ROADMAP:
            return self._handle_learning_roadmap(request.payload)
        else:
            raise HTTPException(status_code=400,detail=f"Unknown tool: {request.tool}")
    def _handle_resume_review(self,payload:dict)->AgentResponse:
        try:
            req=ResumeReviewRequest(**payload)
        except Exception as e:
            raise HTTPException(status_code=422,detail=f"Invalid payload for resume review: {e}")
        result,tokens = review_resume(req)
        return AgentResponse(
            success=True,
            tool=AgentTool.RESUME_REVIEW,
            result=result,
            tokens_used=tokens,
            model=settings.groq_model
        )
    def _handle_mock_interview(self, payload: dict) -> AgentResponse:
        try:
            req = MockInterviewRequest(**payload)
        except Exception as e:
            raise HTTPException(
                status_code=422,
                detail=f"Invalid interview payload: {e}"
            )

        result, tokens = run_mock_interview(req)

        return AgentResponse(
            success=True,
            tool=AgentTool.MOCK_INTERVIEW,
            result=result,
            tokens_used=tokens,
            model=settings.groq_model,
        )

    def _handle_learning_roadmap(self, payload: dict) -> AgentResponse:
        try:
            req = LearningRoadmapRequest(**payload)
        except Exception as e:
            raise HTTPException(
                status_code=422,
                detail=f"Invalid roadmap payload: {e}"
            )

        result, tokens = generate_roadmap(req)

        return AgentResponse(
            success=True,
            tool=AgentTool.LEARNING_ROADMAP,
            result=result,
            tokens_used=tokens,
            model=settings.groq_model,
        )

agent=CareerCoachAgent()    