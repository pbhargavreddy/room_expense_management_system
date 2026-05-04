from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=50)


class UserCreate(UserBase):
    password: str = Field(min_length=4, max_length=128)
    role: Literal["admin", "user"] = "user"


class UserLogin(UserBase):
    password: str


class UserSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    role: str
    created_at: datetime


class AuthResponse(BaseModel):
    message: str
    user: UserSummary


class RequestCreate(BaseModel):
    title: str
    description: str


class ResponseCreate(BaseModel):
    payment_screenshot: bytes


class NotificationCreate(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    message: str = Field(min_length=3, max_length=500)
    category: Literal["rent", "current_bill", "water_bill", "maintenance", "general"]
    amount: float | None = Field(default=None, ge=0)
    due_date: date | None = None
    recipient_ids: list[int] = Field(min_length=1)
    sent_by: int


class NotificationRecipientStatus(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    is_read: bool
    read_at: datetime | None


class NotificationOut(BaseModel):
    id: int
    title: str
    message: str
    category: str
    amount: float | None
    due_date: date | None
    created_at: datetime
    sender_name: str
    is_read: bool
    read_at: datetime | None


class NotificationReadResponse(BaseModel):
    message: str
