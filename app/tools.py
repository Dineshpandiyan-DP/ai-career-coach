from groq import Groq
from app.config import get_settings 
from app.models import (ResumeReviewRequest,
    MockInterviewRequest,
    LearningRoadmapRequest)

settings=get_settings()
client=Groq(api_key=settings.groq_api_key)

def review_resume(req:ResumeReviewRequest)->tuple[str,int]:
    system_prompt = f"""You are an expert technical recruiter with 15 years
of experience hiring {req.target_role} candidates at top tech companies.

When reviewing resumes always structure your response as:

## ATS Score: X/100
Brief reason for the score.

## Strengths
- Point 1
- Point 2

## Critical Issues
- Issue 1 with specific fix
- Issue 2 with specific fix

## Missing Keywords
List keywords missing for the {req.target_role} role.

Be direct, specific and actionable."""
    user_prompt= f"""Review this resume for the role: {req.target_role}
Candidate has {req.years_of_experience} years of experience.

RESUME:
{req.resume_text}"""
    
    response=client.chat.completions.create(
        model=settings.groq_model,
        messages=[
            {"role":"system","content":system_prompt},
            {"role":"user","content":user_prompt}
        ],
        max_tokens=2048,
        temperature=0.7,)
    result_text=response.choices[0].message.content
    tokens=response.usage.total_tokens
    return result_text,tokens

def run_mock_interview(req:MockInterviewRequest)->tuple[str,int]:
    system_prompt = f"""You are a senior technical interviewer at a top tech company
interviewing a {req.experience_level.value} level {req.role} candidate.

Your behaviour:
- Ask ONE focused interview question at a time
- If previous answer is provided give FEEDBACK first then ask next question
- Score the answer 1 to 10
- Mention what a strong answer would include
- Questions should get progressively harder

Be honest and direct."""
    if req.previous_answer:
        user_prompt = f"""Topic focus: {req.topic or 'general ' + req.role + ' concepts'}

My answer to your last question was:
"{req.previous_answer}"

Please evaluate my answer and ask the next question."""
    else:
        user_prompt = f"""Start the interview.
Topic focus: {req.topic or 'general ' + req.role + ' concepts'}
Ask your first question."""
    response=client.chat.completions.create(
        model=settings.groq_model,
        messages=[
            {"role":"system","content":system_prompt},
            {"role":"user","content":user_prompt},
        ],
        max_tokens=2048,
        temperature=0.7,
    )
    result_text=response.choices[0].message.content
    tokens=response.usage.total_tokens
    return result_text,tokens
def generate_roadmap(req: LearningRoadmapRequest) -> tuple[str, int]:
    system_prompt = f"""You are a senior mentor who has helped
500+ engineers land high paying {req.target_role} jobs at top tech companies.

When creating roadmaps you:
- Are brutally honest about skill gaps
- Give specific resources not just generic advice
- Structure by weeks with daily hour estimates
- Prioritize what interviewers actually test
- End with a GitHub project idea that proves all the skills"""
    skills_str = ", ".join(req.current_skills)

    user_prompt = f"""Create a {req.available_weeks} week roadmap to land a {req.target_role} job.

Current skills: {skills_str}

Structure the roadmap week by week with:
- What to learn each week
- Best free resources
- Daily time commitment
- End of week milestone

Also list top 10 interview topics I must know for {req.target_role} role."""
    response=client.chat.completions.create(
        model=settings.groq_model,
        messages=[
            {"role":"system","content":system_prompt},
            {"role":"user","content":user_prompt},
        ],
        max_tokens=2048,
        temperature=0.5,
)
    result_text=response.choices[0].message.content
    tokens=response.usage.total_tokens
    return result_text,tokens