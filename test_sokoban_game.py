import pytest
import globals as g
from sokoban_reader import read_sokoban
from sokoban_game import Sokoban


def test_sokoban_game_small():
    result, array = read_sokoban("sokoban00.txt")
    game = Sokoban(array)
    assert(result != None)
    assert(game.movePlayer(g.UP) == False)
    assert(game.completed == False)
    assert(game.movePlayer(g.LEFT) == False)
    assert(game.completed == False)
    assert(game.movePlayer(g.RIGHT) == False)
    assert(game.completed == False)
    assert(game.movePlayer(g.DOWN) == True)
    assert(game.completed == True)
    assert(True)