from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session

from src.app.jokes import get_categories, get_random_joke_weighted, get_joke_by_id, update_joke_rating, get_db_session

router = APIRouter()


class JokeResponse(BaseModel):
    id: int
    category: str
    text: str
    rating: int
    votes: int


class RatingRequest(BaseModel):
    joke_id: int
    is_like: bool


class RatingResponse(BaseModel):
    success: bool
    message: str
    new_rating: int
    new_votes: int


def get_db():
    with get_db_session() as db:
        yield db


@router.get("/categories", response_model=dict[str, str])
def list_categories():
    return get_categories()


@router.get("/joke/{category}", response_model=JokeResponse)
def get_joke(category: str, db: Optional[Session] = Depends(get_db)):
    joke = get_random_joke_weighted(db, category)
    if joke is None:
        raise HTTPException(status_code=404, detail=f"Category '{category}' not found or empty")
    return JokeResponse(
        id=joke.id,
        category=joke.category,
        text=joke.text,
        rating=joke.rating,
        votes=joke.votes,
    )


@router.get("/joke_by_id/{joke_id}", response_model=JokeResponse)
def get_joke_by_id_endpoint(joke_id: int, db: Optional[Session] = Depends(get_db)):
    joke = get_joke_by_id(db, joke_id)
    if joke is None:
        raise HTTPException(status_code=404, detail=f"Joke with id={joke_id} not found")
    return JokeResponse(
        id=joke.id,
        category=joke.category,
        text=joke.text,
        rating=joke.rating,
        votes=joke.votes,
    )


@router.post("/rate", response_model=RatingResponse)
def rate_joke(req: RatingRequest, db: Optional[Session] = Depends(get_db)):
    joke = update_joke_rating(db, req.joke_id, req.is_like)
    if joke is None:
        raise HTTPException(status_code=404, detail="Joke not found or rating requires database")
    return RatingResponse(
        success=True,
        message="👍" if req.is_like else "👎",
        new_rating=joke.rating,
        new_votes=joke.votes,
    )
