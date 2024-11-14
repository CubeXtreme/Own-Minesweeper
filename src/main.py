# src/main.py

import pygame
import sys
from game import Board

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 40
ROWS, COLS = 10, 10
MINES = 15

# Colores
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

def draw_grid(screen, board):
    for row in range(board.rows):
        for col in range(board.cols):
            cell = board.grid[row][col]
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if cell.is_revealed:
                pygame.draw.rect(screen, GRAY, rect)
                if cell.has_mine:
                    pygame.draw.circle(screen, BLACK, rect.center, CELL_SIZE//4)
                elif cell.adjacent_mines > 0:
                    font = pygame.font.SysFont(None, 24)
                    text = font.render(str(cell.adjacent_mines), True, BLACK)
                    screen.blit(text, text.get_rect(center=rect.center))
            else:
                pygame.draw.rect(screen, WHITE, rect)
                if cell.is_marked:
                    pygame.draw.circle(screen, RED, rect.center, CELL_SIZE//4)
            pygame.draw.rect(screen, BLACK, rect, 1)

def main():
    pygame.init()
    screen = pygame.display.set_mode((COLS * CELL_SIZE, ROWS * CELL_SIZE))
    pygame.display.set_caption("Buscaminas")
    clock = pygame.time.Clock()

    board = Board(ROWS, COLS, MINES)
    running = True
    game_over = False

    while running:
        clock.tick(30)  # 30 FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = pygame.mouse.get_pos()
                row, col = y // CELL_SIZE, x // CELL_SIZE
                if event.button == 1:  # Clic izquierdo
                    board.reveal_cell(row, col)
                    if board.grid[row][col].has_mine:
                        game_over = True
                elif event.button == 3:  # Clic derecho
                    board.toggle_mark_cell(row, col)
        
        # Verificar condición de victoria
        if board.check_victory():
            game_over = True

        # Dibujar el tablero
        screen.fill(BLACK)
        draw_grid(screen, board)

        # Mensajes de fin de juego
        if game_over:
            font = pygame.font.SysFont(None, 48)
            if board.check_victory():
                text = font.render("¡Ganaste!", True, WHITE)
            else:
                text = font.render("¡Perdiste!", True, WHITE)
            screen.blit(text, text.get_rect(center=(COLS * CELL_SIZE // 2, ROWS * CELL_SIZE // 2)))

        pygame.display.flip()

if __name__ == "__main__":
    main()
