from typing import Optional

from sqlalchemy import String, Enum as SQLEnum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from enum import Enum

class Role(str, Enum):
    ADMIN="Admin"
    CUSTOMER="Customer"
    GUEST="Guest"

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    address: Mapped[Optional[str]]
    phone_number: Mapped[Optional[int]]
    role: Mapped[Role] = mapped_column(SQLEnum(Role), default=Role.GUEST, nullable=False)