import logging
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from src.app.jokes import init_db, seed_jokes, get_db_session, get_categories
from src.app.routers import jokes

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Joke Bot Web",
    description="Web-based joke bot with rating system",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jokes.router, prefix="/api", tags=["jokes"])


@app.on_event("startup")
def startup_event():
    # Retry database connection until ready (max 30s)
    db_ready = init_db()
    retries = 0
    while not db_ready and retries < 30:
        logger.info(f"Waiting for database... (attempt {retries + 1})")
        time.sleep(1)
        db_ready = init_db()
        retries += 1

    if db_ready:
        with get_db_session() as db:
            seed_jokes(db)
        cats = get_categories()
        logger.info(f"Database ready, seeded {len(cats)} categories")
    else:
        logger.warning("Database not available after retries, using JSON fallback")
    logger.info("Application started")


static_path = Path(__file__).parent.parent / "static"
if static_path.exists():
    app.mount("/", StaticFiles(directory=str(static_path), html=True), name="static")
