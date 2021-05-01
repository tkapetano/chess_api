from typing import List

import chess
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from models.move import Move
from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine
from sql_app.schemas import TurnCreate

models.Base.metadata.create_all(bind=engine)
router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@router.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/games/", response_model=List[schemas.Game])
def read_games(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_games(db, skip=skip, limit=limit)


@router.get("/users/{user_id}/games/", response_model=List[schemas.Game])
def read_games_for_user(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    games = crud.get_games(db, owner_id=user_id, skip=skip, limit=limit)
    if games is None:
        raise HTTPException(status_code=404, detail="No Games for this user found or user not found")
    return games


@router.post("/users/{user_id}/games/", response_model=schemas.Game)
def create_new_game_for_user(user_id: int, game: schemas.GameCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_user_game(db=db, game=game, user_id=user_id)


@router.get("/users/{user_id}/{game_id}/", response_model=schemas.Game)
def read_games_for_user(user_id: int, game_id: int, db: Session = Depends(get_db)):
    games = crud.get_games(db, owner_id=user_id, game_id=game_id)
    if games is None:
        raise HTTPException(status_code=404, detail=f"Game with id {game_id} not found")
    return games


@router.post("/users/{user_id}/{game_id}/move", response_model=schemas.Turn)
def create_register_new_move_for_game(
        game_id: int, move: Move = Depends(), db: Session = Depends(get_db)):
    # Check db logic: Is the referenced turn the correct one?
    last_turn = crud.get_latest_turn_for_game(db, game_id=game_id)
    if last_turn is None:
        raise HTTPException(status_code=404, detail="Reference Game or Turn not found.")
    if last_turn.id != move.ref_turn_number:
        raise HTTPException(status_code=400, detail="Turn already registered.")
    new_turn_id = move.ref_turn_number + 1
    if crud.get_turn(db, game_id=game_id, turn_id=new_turn_id) is not None:
        raise HTTPException(status_code=400, detail="Turn already registered.")

    # Check game logic: Is this a valid move to register?
    last_fen = last_turn.fen
    board = chess.Board(last_fen)
    chess_move = chess.Move.from_uci(move.register_move)
    current_player = last_turn.current_player
    if last_turn.current_player != move.player:
        raise HTTPException(status_code=400, detail=f"Wrong player to register a move,"
                                                    f" it is {last_turn.current_player}'s move.")
    if chess_move not in board.legal_moves:
        raise HTTPException(status_code=400, detail=f"Illegal chess move {move} for board {last_fen}.")

    # update chess logic
    board.push(chess_move)
    next_player = 'b' if current_player == 'w' else 'w'
    next_turn = TurnCreate(fen=board.fen(), current_player=next_player, current_move=chess_move.uci(),
                           last_move=last_turn.current_move)
    return crud.create_turn(db=db, turn=next_turn, new_turn_id=new_turn_id, game_id=game_id)


@router.get("/users/{user_id}/{game_id}/turns", response_model=List[schemas.Turn])
def read_turns_for_game(game_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    turns = crud.get_turns_for_game(db, game_id=game_id, skip=skip, limit=limit)
    return turns

