from pydantic import BaseModel,Field
from typing import Optional
from enum import Enum

class ExperienceLevel(str,Enum):
    FRESHER = "fresher"
    JUNIOR  = "junior"
    MID     = "mid"
    SENIOR  = "senior"
class AgentTool(str,Enum):
    RESUME_REVIEW    = "resume_review"
    MOCK_INTERVIEW   = "mock_interview"
    LEARNING_ROADMAP = "learning_roadmap"
class ResumeReviewRequest(BaseModel):
    resume_text:str=Field(...,min_length=100,max_length=10000,description="full text of the resume")
    target_role: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Job role the candidate is targeting"
    )
    years_of_experience: int = Field(
        ...,
        ge=0,
        le=40,
        description="Total years of professional experience"
    )
class MockInterviewRequest(BaseModel):
    role: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Job role being interviewed for"
    )
    experience_level: ExperienceLevel
    topic: Optional[str] = Field(
        None,
        description="Specific topic to focus on"
    )
    previous_answer: Optional[str] = Field(
        None,
        max_length=3000,
        description="Candidate's answer to previous question"
    )   
class LearningRoadmapRequest(BaseModel):
    target_role: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Job role the candidate wants to land"
    )
    current_skills: list[str] = Field(
        ...,
        min_length=1,
        description="List of skills the candidate already has"
    )
    available_weeks: int = Field(
        ...,
        ge=1,
        le=52,
        description="Number of weeks available to prepare"
    )    
class AgentResponse(BaseModel):
    success: bool
    tool: AgentTool
    result: str = Field(
        ...,
        description="AI generated response text"
    )
    tokens_used: Optional[int] = None
    model: Optional[str] = None
class HealthResponse(BaseModel):
    status: str
    version: str
    model: str
class AgentRequest(BaseModel):
    tool: AgentTool
    payload: dict            