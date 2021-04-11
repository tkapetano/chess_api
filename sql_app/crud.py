from sqlalchemy.orm import Session
from sql_app import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_games(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Game).offset(skip).limit(limit).all()


def create_user_game(db: Session, game: schemas.GameCreate, user_id: int):
    db_game = models.Game(**game.dict(), owner_id=user_id)
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game


def get_turns_for_game(db: Session, game_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Turn).filter(models.Turn.game_id == game_id).offset(skip).limit(limit).all()


def get_latest_turn_for_game(db: Session, game_id: int):
    return db.query(models.Turn).filter(models.Turn.game_id == game_id).last()


def get_turn(db: Session, game_id: int, turn_id: int):
    return db.query(models.Turn).filter(models.Turn.game_id == game_id).filter(models.Turn.id == turn_id)


def create_turn(db: Session, turn: schemas.TurnCreate, new_turn_id: int, game_id: int):
    db_turn = models.Turn(**turn.dict(), game_id=game_id)
    db.add(db_turn)
    db.commit()
    db.refresh(db_turn)
    return db_turn
