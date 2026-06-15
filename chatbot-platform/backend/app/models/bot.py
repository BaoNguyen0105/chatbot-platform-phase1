import uuid

from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin, UUIDMixin


class Bot(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "bots"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Placeholder for flow definition (Phase 3) and settings
    config: Mapped[dict] = mapped_column(JSONB, default=dict, server_default="{}")

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False
    )
    organization: Mapped["Organization"] = relationship(back_populates="bots")

    conversations: Mapped[list["Conversation"]] = relationship(back_populates="bot")
