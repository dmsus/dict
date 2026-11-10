from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.models import Entry
from app.schemas import EntryInput, EntryOut, Error

router = APIRouter(prefix="/api/v1/entries", tags=["Entries"])


@router.get(
    "/search",
    response_model=EntryOut,
    responses={
        400: {"model": Error, "description": "Отсутствует или некорректный параметр word"},
        404: {"model": Error, "description": "Слово не найдено"},
    },
)
async def search_entry(
    word: str = Query(..., min_length=1, max_length=255, description="Искомое слово"),
    session: AsyncSession = Depends(get_session),
):
    """Регистронезависимый поиск слова."""
    stmt = select(Entry).where(Entry.word.ilike(word))
    entry = (await session.execute(stmt)).scalar_one_or_none()

    if entry is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "Word not found"},
        )
    return entry


@router.post(
    "",
    response_model=EntryOut,
    status_code=status.HTTP_201_CREATED,
    responses={
        409: {"model": Error, "description": "Слово уже существует"},
    },
)
async def create_entry(
    payload: EntryInput,
    session: AsyncSession = Depends(get_session),
):
    """Добавить слово. Если слово уже есть — 409."""
    word = payload.word.strip()
    translation = payload.translation.strip()

    if not word or not translation:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"error": "Fields 'word' and 'translation' must not be empty"},
        )

    # Проверка с учётом регистра (регистронезависимая уникальность).
    exists = await session.scalar(select(Entry.id).where(Entry.word.ilike(word)))
    if exists is not None:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"error": "Word already exists"},
        )

    entry = Entry(word=word, translation=translation)
    session.add(entry)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"error": "Word already exists"},
        )

    await session.refresh(entry)
    return entry


@router.get("", response_model=list[EntryOut])
async def list_entries(session: AsyncSession = Depends(get_session)):
    """Список всех слов (для отладки)."""
    stmt = select(Entry).order_by(Entry.created_at)
    return (await session.execute(stmt)).scalars().all()
