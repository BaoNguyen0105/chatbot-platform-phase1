import enum
import uuid

from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin, UUIDMixin


class ConversationStatus(str, enum.Enum):
    OPEN = "open"
    CLOSED = "closed"
    PENDING = "pending"


class Conversation(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "conversations"

    bot_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("bots.id"), nullable=False
    )
    bot: Mapped["Bot"] = relationship(back_populates="conversations")

    # External end-user identifier (web visitor id, FB PSID, WA number, etc.)
    external_user_id: Mapped[str] = mapped_column(String(255), nullable=False)
    channel: Mapped[str] = mapped_column(String(50), default="web", nullable=False)

    status: Mapped[ConversationStatus] = mapped_column(
        Enum(ConversationStatus, name="conversation_status"),
        default=ConversationStatus.OPEN,
        nullable=False,
    )

    # Flow execution state (Phase 3) - current node, variables, etc.
    session_state: Mapped[dict] = mapped_column(JSONB, default=dict, server_default="{}")

    messages: Mapped[list["Message"]] = relationship(
        back_populates="conversation", order_by="Message.created_at"
    )


class MessageSender(str, enum.Enum):
    USER = "user"
    BOT = "bot"
    AGENT = "agent"


class Message(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "messages"

    conversation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False
    )
    conversation: Mapped["Conversation"] = relationship(back_populates="messages")

    sender: Mapped[MessageSender] = mapped_column(
        Enum(MessageSender, name="message_sender"), nullable=False
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # For attachments, quick replies, AI metadata etc.
    extra_data: Mapped[dict] = mapped_column(JSONB, default=dict, server_default="{}")
