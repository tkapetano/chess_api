from typing import Optional

from pydantic import BaseModel


class Move(BaseModel):
    register_move: str
    player: str
    last_fen: Optional[str] = None


class Turn(BaseModel):
    fen: str
    current_player: str
    current_move: str
    last_move: str
    game_number: int = 0
