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

def test_sokoban_game_medium():
    result, array = read_sokoban("sokoban01.txt")
    game = Sokoban(array)
    assert(result != None)
    assert(game.movePlayer(g.LEFT) == False)
    assert(game.movePlayer(g.RIGHT) == False)
    assert(game.movePlayer(g.UP) == True)
    assert(game.completed == False)
    assert(game.movePlayer(g.LEFT) == True)
    assert(game.movePlayer(g.LEFT) == True)
    assert(game.movePlayer(g.LEFT) == True)
    assert(game.movePlayer(g.LEFT) == True)
    assert(game.movePlayer(g.LEFT) == True)
    assert(game.movePlayer(g.LEFT) == False)
    assert(game.movePlayer(g.DOWN) == True)
    assert(game.completed == False)