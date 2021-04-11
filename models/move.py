from typing import Optional

from pydantic import BaseModel


class Move(BaseModel):
    register_move: str
    # Number of the turn before, i.e. the turn on which to register the move in order to produce the next turn.
    ref_turn_number: int
    player: str
    last_fen: Optional[str] = None
