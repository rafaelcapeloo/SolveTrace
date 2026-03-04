"""
SolveTrace — FastAPI Application Entry Point

Open-source competitive programming problem explainer powered by LLMs.
"""

from contextlib import asynccontextmanager
import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import init_db
from app.api import problems, analysis

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown lifecycle events."""
    await init_db()
    print(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} is ready")
    yield
    print(f"👋 {settings.APP_NAME} shutting down")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Open-source competitive programming problem explainer — paste a URL, get a step-by-step solution approach.",
    lifespan=lifespan,
)

# --- Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routers ---
app.include_router(problems.router, prefix="/api/problems", tags=["Problems"])
app.include_router(analysis.router, prefix="/api/analyze", tags=["Analysis"])


@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "operational",
        "docs": "/docs",
    }


@app.get("/api/health", tags=["Health"])
async def health():
    """Detailed health check."""
    return {
        "status": "healthy",
        "database": "connected",
        "llm_provider": settings.LLM_PROVIDER,
    }


@app.get("/api/config", tags=["Config"])
async def get_config():
    """Return available LLM providers and current configuration."""
    providers = []

    # Ollama is dynamic: we query the local API to see what models are pulled
    ollama_models = []
    ollama_available = False
    try:
        async with httpx.AsyncClient(timeout=1.5) as client:
            resp = await client.get(f"{settings.OLLAMA_BASE_URL}/api/tags")
            if resp.status_code == 200:
                ollama_models = [m["name"] for m in resp.json().get("models", [])]
                ollama_available = len(ollama_models) > 0
    except Exception:
        pass

    providers.append({
        "id": "ollama",
        "name": "Ollama (Local)",
        "available": ollama_available,
        "description": "Run models locally with Ollama",
        "models": ollama_models or [settings.OLLAMA_MODEL],
    })

    # Gemini
    providers.append({
        "id": "gemini",
        "name": "Google Gemini",
        "available": bool(settings.GEMINI_API_KEY),
        "description": "Google's Gemini API",
        "models": [settings.GEMINI_MODEL],
    })

    # OpenAI
    providers.append({
        "id": "openai",
        "name": "OpenAI",
        "available": bool(settings.OPENAI_API_KEY),
        "description": "OpenAI GPT models",
        "models": [settings.OPENAI_MODEL],
    })

    return {
        "current_provider": settings.LLM_PROVIDER,
        "providers": providers,
    }
