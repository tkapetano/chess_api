from typing import List, Optional
from pydantic import BaseModel


class TurnBase(BaseModel):
    fen: str
    current_player: str
    current_move: str
    last_move: Optional[str] = None


class TurnCreate(TurnBase):
    pass


class Turn(TurnBase):
    id: int
    game_id: int

    class Config:
        orm_mode = True


class GameBase(BaseModel):
    title: str
    description: Optional[str] = None


class GameCreate(GameBase):
    pass


class Game(GameBase):
    id: int
    owner_id: int
    turns: List[Turn] = []

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
