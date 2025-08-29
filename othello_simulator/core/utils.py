from othello_simulator.core.state import BLACK_PLAYER, WHITE_PLAYER


def get_opponent_player(player: int) -> int:
    """Get the opponent player for the given player.

    Parameters
    ----------
    player : int
        The current player (1 for black, 2 for white)

    Returns
    -------
    int
        The opponent player identifier.
    """
    if player == BLACK_PLAYER:
        return WHITE_PLAYER
    return BLACK_PLAYER
