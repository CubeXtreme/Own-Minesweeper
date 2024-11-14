# src/game.py

import random
import pygame

class Cell:
    def __init__(self):
        self.has_mine = False
        self.is_revealed = False
        self.is_marked = False
        self.adjacent_mines = 0

class Board:
    def __init__(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.grid = [[Cell() for _ in range(cols)] for _ in range(rows)]
        self.place_mines()
        self.calculate_adjacent_mines()

    def place_mines(self):
        placed = 0
        while placed < self.mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if not self.grid[row][col].has_mine:
                self.grid[row][col].has_mine = True
                placed += 1

    def calculate_adjacent_mines(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col].has_mine:
                    continue
                count = 0
                for r in range(max(0, row-1), min(self.rows, row+2)):
                    for c in range(max(0, col-1), min(self.cols, col+2)):
                        if self.grid[r][c].has_mine:
                            count += 1
                self.grid[row][col].adjacent_mines = count

    def reveal_cell(self, row, col):
        cell = self.grid[row][col]
        if cell.is_revealed or cell.is_marked:
            return
        cell.is_revealed = True
        if cell.adjacent_mines == 0 and not cell.has_mine:
            for r in range(max(0, row-1), min(self.rows, row+2)):
                for c in range(max(0, col-1), min(self.cols, col+2)):
                    if not self.grid[r][c].is_revealed:
                        self.reveal_cell(r, c)

    def toggle_mark_cell(self, row, col):
        cell = self.grid[row][col]
        if not cell.is_revealed:
            cell.is_marked = not cell.is_marked

    def check_victory(self):
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.grid[row][col]
                if not cell.has_mine and not cell.is_revealed:
                    return False
        return True

    def reveal_cell_with_animation(self, row, col, screen):
        """
        Revela una celda con una animación de desvanecimiento usando un enfoque iterativo.
        """
        stack = [(row, col)]
        REVEAL_COLOR = (180, 180, 180)  # Gris claro
        ANIMATION_STEPS = 10
        DELAY = 30  # Milisegundos entre cada paso de la animación

        while stack:
            current_row, current_col = stack.pop()
            if not (0 <= current_row < self.rows and 0 <= current_col < self.cols):
                continue  # Evita índices fuera de rango
            cell = self.grid[current_row][current_col]
            if cell.is_revealed or cell.is_marked:
                continue
            cell.is_revealed = True

            rect = pygame.Rect(current_col * 40, current_row * 40 + 50, 40, 40)  # Ajusta según la interfaz
            for i in range(1, ANIMATION_STEPS + 1):
                alpha = int((i / ANIMATION_STEPS) * 255)
                temp_surface = pygame.Surface((rect.width, rect.height))
                temp_surface.set_alpha(alpha)
                temp_surface.fill(REVEAL_COLOR)
                screen.blit(temp_surface, rect.topleft)
                pygame.display.flip()
                pygame.time.delay(DELAY)

            if cell.adjacent_mines == 0 and not cell.has_mine:
                for r in range(max(0, current_row-1), min(self.rows, current_row+2)):
                    for c in range(max(0, current_col-1), min(self.cols, current_col+2)):
                        neighbor = self.grid[r][c]
                        if not neighbor.is_revealed and not neighbor.has_mine:
                            stack.append((r, c))
