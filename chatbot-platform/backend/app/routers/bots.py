import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.models.bot import Bot
from app.models.user import User
from app.schemas.bot import BotCreate, BotOut

router = APIRouter(prefix="/api/bots", tags=["bots"])


@router.post("/", response_model=BotOut, status_code=201)
def create_bot(
    payload: BotCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    bot = Bot(
        name=payload.name,
        description=payload.description,
        organization_id=current_user.organization_id,
    )
    db.add(bot)
    db.commit()
    db.refresh(bot)
    return bot


@router.get("/", response_model=list[BotOut])
def list_bots(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return (
        db.query(Bot)
        .filter(Bot.organization_id == current_user.organization_id)
        .all()
    )


@router.get("/{bot_id}", response_model=BotOut)
def get_bot(
    bot_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    bot = (
        db.query(Bot)
        .filter(Bot.id == bot_id, Bot.organization_id == current_user.organization_id)
        .first()
    )
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    return bot
