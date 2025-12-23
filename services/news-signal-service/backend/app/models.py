from __future__ import annotations

import uuid

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime
from typing import Optional


# Shared properties
class UserBase(SQLModel):
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    full_name: Optional[str] = None



# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserRegister(SQLModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: Optional[str] = None


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: Optional[EmailStr] = None  # type: ignore
    password: Optional[str] = None


class UserUpdateMe(SQLModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


# Database model, database table inferred from class name
# class User(UserBase, table=True):
#     id: int = Field(default_factory=None, primary_key=True)
#     hashed_password: str
#     #items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)

# News-Feed-Service WebApi
class User(SQLModel, table=True):
    __tablename__ = "users"   # ✅ 여기서 테이블 이름 지정

    id: Optional[int]  = Field(default=None, primary_key=True)
    name: str
    email: EmailStr
    is_active: bool = True

class UserCreate(SQLModel):
    name: str
    email: EmailStr
    #password: str   # plain text, validation용

class UserRead(SQLModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool

# rules configuration DTO
class NotificationRuleCreate(SQLModel):
    keyword: str
    channels: list["NotificationChannelCreate"]

    def to_db(self, *, user_id: int) -> NotificationRuleDB:
        return NotificationRuleDB(
            user_id=user_id,
            keyword=self.keyword,
        )
class NotificationChannelCreate(SQLModel):
    channel: str            # email | slack
    delivery_mode: str      # realtime | digest
    frequency: Optional[str] = None

    def to_db(self, *, rule_id: int) -> NotificationChannelDB:
        return NotificationChannelDB(
            rule_id=rule_id,
            channel=self.channel,
            delivery_mode=self.delivery_mode,
            frequency=self.frequency,
            is_active=True,
        )
class NotificationRuleRead(SQLModel):
    id: int
    keyword: str

    @classmethod
    def from_db(cls, rule: NotificationRuleDB):
        return cls(
            id=rule.id,
            keyword=rule.keyword,
        )

class NotificationRuleDB(SQLModel, table=True):
    __tablename__ = "notification_rules"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    keyword: str = Field(index=True)
    is_active: bool = Field(default=True)

    created_at: datetime = Field(default_factory=datetime.utcnow)

class NotificationChannelDB(SQLModel, table=True):
    __tablename__ = "notification_channels"

    id: Optional[int] = Field(default=None, primary_key=True)

    rule_id: int = Field(index=True)

    channel: str               # "email" | "slack"
    delivery_mode: str         # "realtime" | "digest"
    frequency: Optional[str] = None  # "hourly" | "daily" | None

    is_active: bool = Field(default=True)
    last_sent_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)



# # Properties to return via API, id is always required
class UserPublic(UserBase):
    id: int


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=255)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)  # type: ignore


# Database model, database table inferred from class name
class Item(SQLModel, table=True):
    __tablename__ = "news_keywords"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    news_id: int
    keyword: str
    score: Optional[float]  = None
    extractor_version: Optional[str]  = None
    created_at: datetime

# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: int
    owner_id: int


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: Optional[int] = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=128)

class NewsKeywordPublic(SQLModel):
    id: int
    news_id: int
    keyword: str
    score: Optional[float]  = None
    extractor_version: Optional[str] = None
    created_at: datetime
