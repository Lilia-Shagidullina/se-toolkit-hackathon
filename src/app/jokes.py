import json
import logging
import random
from pathlib import Path
from typing import Optional, Generator
from contextlib import contextmanager

from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from src.app.settings import Settings

logger = logging.getLogger(__name__)

settings = Settings()

JOKE_DATA_FILE = Path(__file__).parent.parent.parent / "jokes.json"

# Database setup — lazy initialization
engine = None
SessionLocal = None
Base = declarative_base()
_db_available = False


def _try_connect_db() -> bool:
    global engine, SessionLocal, _db_available
    try:
        engine = create_engine(settings.database_url, pool_pre_ping=True)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        # Test connection
        with engine.connect() as conn:
            conn.execute(__import__("sqlalchemy").text("SELECT 1"))
        _db_available = True
        logger.info("Database connected")
        return True
    except Exception as e:
        logger.warning(f"Database unavailable, using JSON fallback: {e}")
        engine = None
        SessionLocal = None
        _db_available = False
        return False


def init_db() -> bool:
    if not _db_available:
        _try_connect_db()
    if _db_available and engine is not None:
        Base.metadata.create_all(bind=engine)
    return _db_available


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """Get database session — either from DB or a fake JSON-backed session"""
    if _db_available and SessionLocal is not None:
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    else:
        # Return a fake session — JSON fallback handles everything
        yield None  # type: ignore


def seed_jokes(db: Session) -> None:
    """Load jokes from JSON into database if empty"""
    if not _db_available:
        return

    with open(JOKE_DATA_FILE, "r", encoding="utf-8") as f:
        jokes_data = json.load(f)

    existing = db.query(Joke).first()  # type: ignore
    if existing is not None:
        return

    for category, jokes in jokes_data.items():
        for joke in jokes:
            db.add(Joke(  # type: ignore
                category=category,
                text=joke["text"],
                rating=joke.get("rating", 0),
                votes=joke.get("votes", 0),
            ))
    db.commit()
    logger.info(f"Seeded jokes from {len(jokes_data)} categories")


class Joke(Base):
    __tablename__ = "jokes"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(50), nullable=False, index=True)
    text = Column(Text, nullable=False)
    rating = Column(Integer, default=0)
    votes = Column(Integer, default=0)


def _load_json_jokes() -> dict:
    with open(JOKE_DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_json_jokes(data: dict) -> None:
    with open(JOKE_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _compute_weight(rating: int) -> float:
    """Compute a positive weight from rating.
    
    Ensures:
    - High ratings have high weight
    - Negative ratings still have positive (but low) weight
    - If all jokes have negative ratings, they all still appear
    """
    return 1.5 ** rating  # 1, 1.5, 2.25, 3.375... / 0.67, 0.44, 0.29...


def get_random_joke_weighted(db: Optional[Session], category: str) -> Optional[Joke]:
    if _db_available and db is not None:
        jokes = db.query(Joke).filter(Joke.category == category).all()  # type: ignore
        if not jokes:
            return None
        weights = [_compute_weight(joke.rating) for joke in jokes]
        index = random.choices(range(len(jokes)), weights=weights, k=1)[0]
        return jokes[index]
    else:
        # JSON fallback
        jokes_data = _load_json_jokes()
        jokes_list = jokes_data.get(category, [])
        if not jokes_list:
            return None
        weights = [_compute_weight(joke.get("rating", 0)) for joke in jokes_list]
        index = random.choices(range(len(jokes_list)), weights=weights, k=1)[0]
        joke = jokes_list[index]
        # Create a fake Joke object with minimal attributes
        fake = Joke()
        fake.id = index
        fake.category = category
        fake.text = joke["text"]
        fake.rating = joke.get("rating", 0)
        fake.votes = joke.get("votes", 0)
        return fake


def get_joke_by_id(db: Optional[Session], joke_id: int) -> Optional[Joke]:
    if _db_available and db is not None:
        joke = db.query(Joke).filter(Joke.id == joke_id).first()  # type: ignore
        return joke
    else:
        logger.warning("Cannot get joke by ID without database")
        return None


def update_joke_rating(db: Optional[Session], joke_id: int, is_like: bool) -> Optional[Joke]:
    if _db_available and db is not None:
        joke = db.query(Joke).filter(Joke.id == joke_id).first()  # type: ignore
        if joke is None:
            return None
        joke.rating = joke.rating + 1 if is_like else joke.rating - 1
        joke.votes += 1
        db.commit()
        db.refresh(joke)
        return joke
    else:
        # JSON fallback — find by category and index
        # This won't work well without knowing category/index, so we skip
        logger.warning("Cannot rate joke without database")
        return None


def get_categories() -> dict[str, str]:
    return {
        "Happy": "Happy",
        "Sad": "Sad",
        "Scary": "Scary",
        "Angry": "Angry",
        "Mysterious": "Mysterious",
    }
