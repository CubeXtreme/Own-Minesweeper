# tests/test_game.py

import unittest
from src.game import Board

class TestBoard(unittest.TestCase):
    def setUp(self):
        # Crear un tablero de 5x5 con 5 minas para pruebas
        self.board = Board(5, 5, 5)
    
    def test_mine_count(self):
        # Verificar que se hayan colocado exactamente 5 minas
        mine_count = sum(cell.has_mine for row in self.board.grid for cell in row)
        self.assertEqual(mine_count, 5, "El número de minas colocadas debería ser 5")
    
    def test_adjacent_mines_calculation(self):
        # Revelar una celda sin mina y verificar el conteo de minas adyacentes
        # Dado que la ubicación de minas es aleatoria, esta prueba es básica
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                if not self.board.grid[row][col].has_mine:
                    self.board.reveal_cell(row, col)
                    adjacent = self.board.grid[row][col].adjacent_mines
                    self.assertTrue(0 <= adjacent <= 8, "El conteo de minas adyacentes debe estar entre 0 y 8")
    
    def test_reveal_mine(self):
        # Encontrar una mina y verificar que al revelarla, el juego termine (simulación)
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                if self.board.grid[row][col].has_mine:
                    self.board.reveal_cell(row, col)
                    self.assertTrue(self.board.grid[row][col].is_revealed, "La mina debería estar revelada")
    
    def test_mark_cell(self):
        # Marcar una celda y verificar que esté marcada
        self.board.toggle_mark_cell(0, 0)
        self.assertTrue(self.board.grid[0][0].is_marked, "La celda (0,0) debería estar marcada")
        # Desmarcar la misma celda
        self.board.toggle_mark_cell(0, 0)
        self.assertFalse(self.board.grid[0][0].is_marked, "La celda (0,0) debería estar desmarcada")

if __name__ == '__main__':
    unittest.main()
