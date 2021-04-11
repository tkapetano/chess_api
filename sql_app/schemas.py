from typing import List, Optional
from pydantic import BaseModel


class GameBase(BaseModel):
    title: str
    description: Optional[str] = None
    num_turns: int = 0


class GameCreate(GameBase):
    pass


class Game(GameBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    games: List[Game] = []

    class Config:
        orm_mode = True
