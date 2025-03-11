import logging
from typing import Annotated

from fastapi import APIRouter, Query, status

from src.api.dependencies import SessionDep
from src.api.exceptions import NotFoundError
from src.api.schemas import ApiResponse, ErrorResponse
from src.schemas.anime import Anime
from src.services.anime import AnimeService

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/animes",
    tags=["Animes"],
)


@router.get(
    "",
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[list[Anime]]},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse},
    },
)
async def get_animes(
    session: SessionDep,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=0, le=100)] = 50,
):
    anime_service = AnimeService(session)
    anime_list = await anime_service.get_all(offset, limit)

    if not anime_list:
        raise NotFoundError

    return ApiResponse(data=anime_list)


@router.get(
    "/{id}",
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[Anime]},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse},
    },
)
async def get_single_anime(
    session: SessionDep,
    id: int,
):
    anime_service = AnimeService(session)
    anime = await anime_service.get_single_by_id(id)

    if not anime:
        logger.debug("Anime not found (id=%d)", id)
        raise NotFoundError

    return ApiResponse(data=anime)
