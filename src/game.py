# src/game.py

import random
import pygame

# Definir CELL_SIZE globalmente
CELL_SIZE = 40

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

    def reveal_cell_with_animation(self, row, col, screen, last_update_time):
        """
        Revela una celda con una animación de desvanecimiento usando un enfoque basado en tiempo.
        """
        cell = self.grid[row][col]
        if cell.is_revealed or cell.is_marked:
            return last_update_time
        cell.is_revealed = True

        # Definir colores para la animación
        REVEAL_COLOR = (180, 180, 180)  # Gris claro
        ANIMATION_STEPS = 10
        ANIMATION_DURATION = 300  # Milisegundos totales para la animación
        step_duration = ANIMATION_DURATION / ANIMATION_STEPS

        # Calcular el tiempo para la siguiente actualización
        current_time = pygame.time.get_ticks()
        if last_update_time is None:
            last_update_time = current_time

        elapsed = current_time - last_update_time
        if elapsed < step_duration:
            return last_update_time  # Esperar al siguiente paso

        # Calcular el paso actual de la animación
        step = int(elapsed / step_duration)
        if step > ANIMATION_STEPS:
            step = ANIMATION_STEPS

        alpha = int((step / ANIMATION_STEPS) * 255)
        temp_surface = pygame.Surface((CELL_SIZE, CELL_SIZE))
        temp_surface.set_alpha(alpha)
        temp_surface.fill(REVEAL_COLOR)

        rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE + 50, CELL_SIZE, CELL_SIZE)  # +50 para interfaz
        screen.blit(temp_surface, rect.topleft)

        pygame.display.update(rect)  # Actualizar solo la celda actual

        last_update_time = current_time

        # Si la celda tiene 0 minas adyacentes, revelar recursivamente
        if cell.adjacent_mines == 0 and not cell.has_mine:
            for r in range(max(0, row-1), min(self.rows, row+2)):
                for c in range(max(0, col-1), min(self.cols, col+2)):
                    neighbor = self.grid[r][c]
                    if not neighbor.is_revealed and not neighbor.has_mine:
                        last_update_time = self.reveal_cell_with_animation(r, c, screen, last_update_time)

        return last_update_time
