from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum as SQLEnum,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base


class Role(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"
    GUEST = "GUEST"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    full_name: Mapped[str] = mapped_column(String(100), nullable=False)

    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        nullable=False,
    )

    avatar_url: Mapped[Optional[str]] = mapped_column(
        String(2048),
        nullable=True,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    hashed_password: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    bio: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
    )

    address: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    phone_number: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
    )

    role: Mapped[Role] = mapped_column(
        SQLEnum(Role, name="user_role"),
        default=Role.GUEST,
        nullable=False,
    )

    is_verify: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_blocked: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    google_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        unique=True,
        nullable=True,
        index=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    is_pending_deletion: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
