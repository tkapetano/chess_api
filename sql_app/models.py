from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from sql_app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    games = relationship("Game", back_populates="owner")


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="games")
    turns = relationship("Turn", back_populates="game")


class Turn(Base):
    __tablename__ = "turns"

    id = Column(Integer, primary_key=True, index=True)
    fen = Column(String)
    current_player = Column(String)
    current_move = Column(String)
    last_move = Column(String)
    game_id = Column(Integer, ForeignKey("games.id"))

    game = relationship("Game", back_populates="turns")

