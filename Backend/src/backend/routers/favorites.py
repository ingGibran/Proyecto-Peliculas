from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from backend.database import Favorite, Movie, User, get_session
from backend.routers.users import CurrentUserDependency


router = APIRouter(prefix="/favorites", tags=["favorites"])
SessionDependency = Annotated[Session, Depends(get_session)]


class FavoriteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    movie_id: int
    movie_title: str
    poster_url: str | None
    created_at: datetime


def _favorite_read(favorite: Favorite, movie: Movie) -> FavoriteRead:
    return FavoriteRead(
        id=favorite.id,
        movie_id=movie.id,
        movie_title=movie.title,
        poster_url=movie.poster_url,
        created_at=favorite.created_at,
    )


@router.get("/me", response_model=list[FavoriteRead])
def list_my_favorites(
    current_user: CurrentUserDependency,
    session: SessionDependency,
) -> list[FavoriteRead]:
    results = session.exec(
        select(Favorite, Movie)
        .join(Movie, Favorite.movie_id == Movie.id)
        .where(Favorite.user_id == current_user.id)
        .order_by(Favorite.created_at.desc())
    ).all()
    return [_favorite_read(favorite, movie) for favorite, movie in results]


@router.post(
    "/{movie_id}",
    response_model=FavoriteRead,
    status_code=status.HTTP_201_CREATED,
)
def add_favorite(
    movie_id: int,
    current_user: CurrentUserDependency,
    session: SessionDependency,
) -> FavoriteRead:
    movie = session.get(Movie, movie_id)
    if movie is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found.",
        )

    favorite = Favorite(user_id=current_user.id, movie_id=movie.id)
    session.add(favorite)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This movie is already in your favorites.",
        ) from None
    session.refresh(favorite)
    return _favorite_read(favorite, movie)


@router.delete("/{movie_id}", response_model=FavoriteRead)
def remove_favorite(
    movie_id: int,
    current_user: CurrentUserDependency,
    session: SessionDependency,
) -> FavoriteRead:
    result = session.exec(
        select(Favorite, Movie)
        .join(Movie, Favorite.movie_id == Movie.id)
        .where(
            Favorite.movie_id == movie_id,
            Favorite.user_id == current_user.id,
        )
    ).first()
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Favorite not found.",
        )

    favorite, movie = result
    session.delete(favorite)
    session.commit()
    return _favorite_read(favorite, movie)