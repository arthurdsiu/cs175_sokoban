import pytest
import globals as g
from sokoban_reader import read_sokoban
from sokoban_game import Sokoban


def test_sokoban_game_small():
    game = Sokoban(Sokoban.readFile("sokoban00.txt"))
    assert(game != None)
    assert(game.movePlayer(g.UP) == False)
    assert(game.completed == False)
    assert(game.movePlayer(g.LEFT) == False)
    assert(game.completed == False)
    assert(game.movePlayer(g.RIGHT) == False)
    assert(game.completed == False)
    assert(game.movePlayer(g.DOWN) == True)
    assert(game.completed == True)

def test_sokoban_game_medium():
    game = Sokoban(Sokoban.readFile("sokoban01.txt"))
    assert(game != None)
    assert(game.movePlayer(g.LEFT) == False)
    assert(game.movePlayer(g.RIGHT) == False)
    assert(game.movePlayer(g.UP) == True)
    assert(game.completed == False)
    assert(game.movePlayer(g.LEFT) == True)
    assert(game.movePlayer(g.LEFT) == True)
    assert(game.movePlayer(g.LEFT) == True)
    assert(game.movePlayer(g.LEFT) == True)
    assert(game.movePlayer(g.LEFT) == True)
    assert(game.movePlayer(g.LEFT) == True)
    assert(game.movePlayer(g.DOWN) == True)
    assert(game.completed == False)