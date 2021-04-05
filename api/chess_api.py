import fastapi
import chess

from models.move import Turn, Move

router = fastapi.APIRouter()


@router.get('/api/chess', response_model=Turn)
async def do_i_need_an_umbrella(data: Move = fastapi.Depends()):
    # needs to load last fen if not passed in data
    last_fen = data.last_fen
    if last_fen:
        board = chess.Board(last_fen)
    else:
        ## TODO: implement
        raise NotImplementedError
    move = chess.Move.from_uci(data.register_move)
    # check player
    current_player = data.player

    if move in board.legal_moves:
        board.push(move)
    else:
        ## TODO: return invalid move
        raise ValueError

    return Turn(fen=board.fen(), current_player=current_player, current_move=move.uci(), last_move='')
