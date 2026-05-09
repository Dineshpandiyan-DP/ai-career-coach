import logging
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.config import get_settings
from app.models import AgentRequest, AgentResponse, HealthResponse
from app.agent import agent

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",)
logger=logging.getLogger(__name__)
setting=get_settings()

@asynccontextmanager
async def lifespan(app : FastAPI):
    logger.info(f"Starting up {setting.app_name}...")
    logger.info(f"using model:{setting.groq_model}")
    logger.info(f"Debug mode: {setting.debug}")
    yield
    logger.info(f"Shutting down {setting.app_name}...")

app= FastAPI(
     title=setting.app_name,
     version="1.0.0",
     description="AI Agent that helps with carreer coaching tasks",
     lifespan=lifespan,
     docs_url="/docs",
     redoc_url="/redoc")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"Completed request in {process_time:.2f}s with status code {response.status_code}")
    return response

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred. Please try again."},
    )
@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(status="ok", model=setting.groq_model)

@app.post("/agent", response_model=AgentResponse)
async def run_agent(request: AgentRequest):
    logger.info(f"Received agent request for tool: {request.tool}")
    result=agent.run(request)
    return result