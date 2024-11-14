# src/main.py

import pygame
import sys
import time
from game import Board

# Colores
PALETTE = {
    "background": (25, 25, 25),        # Negro muy oscuro
    "cell_unrevealed": (50, 50, 50),   # Gris oscuro
    "cell_revealed": (200, 200, 200),  # Gris claro
    "mine": (255, 0, 0),               # Rojo
    "flag": (0, 0, 255),                # Azul
    "text": (255, 255, 255),            # Blanco
    "victory": (0, 255, 0),             # Verde
    "defeat": (255, 0, 0)               # Rojo
}

# Ruta a los recursos
ICON_PATH = "src/assets/game_icon.ico"
BACKGROUND_IMAGE_PATH = "src/assets/background.png"
MINE_IMAGE_PATH = "src/assets/mine.png"
FLAG_IMAGE_PATH = "src/assets/flag.png"
FONT_PATH = "src/fonts/CustomFont.ttf"

# Definir niveles de dificultad
DIFFICULTIES = {
    "Fácil": {"rows": 9, "cols": 9, "mines": 10},
    "Medio": {"rows": 16, "cols": 16, "mines": 40},
    "Difícil": {"rows": 16, "cols": 30, "mines": 99}
}

# Ubicaciones de los textos
MINES_TEXT_POS = (10, 0)  # Ajustados según la pantalla
TIMER_TEXT_POS = (0, 0)   # Ajustados según la pantalla

# Botón de reiniciar
RESTART_BUTTON_RECT = pygame.Rect(0, 0, 100, 40)  # Posición dinámica
RESTART_COLOR = (70, 130, 180)  # Azul acero
RESTART_TEXT_COLOR = PALETTE["text"]

def get_remaining_mines(board):
    """Calcula las minas restantes basándose en las marcas realizadas por el jugador."""
    marked = sum(cell.is_marked for row in board.grid for cell in row)
    return board.mines - marked

def display_difficulty_menu(screen, font_large, font_medium):
    """Muestra el menú para seleccionar la dificultad del juego."""
    title_text = font_large.render("Selecciona la Dificultad", True, PALETTE["text"])
    screen.blit(title_text, title_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 100)))
    
    y_offset = screen.get_height() // 2 - 30
    buttons = []
    for difficulty in DIFFICULTIES.keys():
        button_rect = pygame.Rect(screen.get_width() // 2 - 100, y_offset, 200, 50)
        pygame.draw.rect(screen, PALETTE["cell_unrevealed"], button_rect)
        text = font_medium.render(difficulty, True, PALETTE["text"])
        screen.blit(text, text.get_rect(center=button_rect.center))
        buttons.append((button_rect, difficulty))
        y_offset += 70
    return buttons

def draw_restart_button(screen, font):
    """Dibuja el botón de reiniciar en la pantalla."""
    # Posicionar el botón en la esquina inferior central
    restart_x = screen.get_width() // 2 - RESTART_BUTTON_RECT.width // 2
    restart_y = screen.get_height() - RESTART_BUTTON_RECT.height - 10
    RESTART_BUTTON_RECT.topleft = (restart_x, restart_y)
    
    pygame.draw.rect(screen, RESTART_COLOR, RESTART_BUTTON_RECT)
    text = font.render("Reiniciar", True, RESTART_TEXT_COLOR)
    screen.blit(text, text.get_rect(center=RESTART_BUTTON_RECT.center))

def draw_info(screen, board, elapsed_time, font):
    """Dibuja la información del juego como minas restantes y temporizador."""
    # Minas restantes
    mines_remaining = get_remaining_mines(board)
    mines_text = font.render(f"Mines: {mines_remaining}", True, PALETTE["text"])
    screen.blit(mines_text, MINES_TEXT_POS)
    
    # Temporizador
    timer_text = font.render(f"Time: {elapsed_time} s", True, PALETTE["text"])
    screen.blit(timer_text, TIMER_TEXT_POS)

def render_text_with_shadow(screen, text, font, text_color, shadow_color, position, shadow_offset=(2, 2)):
    """Renderiza texto con una sombra para mejorar la legibilidad."""
    # Renderizar la sombra
    shadow = font.render(text, True, shadow_color)
    shadow_rect = shadow.get_rect(center=(position[0] + shadow_offset[0], position[1] + shadow_offset[1]))
    screen.blit(shadow, shadow_rect)
    
    # Renderizar el texto principal
    main_text = font.render(text, True, text_color)
    main_rect = main_text.get_rect(center=position)
    screen.blit(main_text, main_rect)

def draw_grid(screen, board, mine_image=None, flag_image=None, font=None):
    """Dibuja el tablero del Buscaminas en la pantalla."""
    for row in range(board.rows):
        for col in range(board.cols):
            cell = board.grid[row][col]
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE + 50, CELL_SIZE, CELL_SIZE)  # +50 para interfaz
            if cell.is_revealed:
                pygame.draw.rect(screen, PALETTE["cell_revealed"], rect)
                if cell.has_mine and mine_image:
                    screen.blit(mine_image, mine_image.get_rect(center=rect.center))
                elif cell.adjacent_mines > 0:
                    text = font.render(str(cell.adjacent_mines), True, PALETTE["text"])
                    screen.blit(text, text.get_rect(center=rect.center))
            else:
                pygame.draw.rect(screen, PALETTE["cell_unrevealed"], rect)
                if cell.is_marked and flag_image:
                    screen.blit(flag_image, flag_image.get_rect(center=rect.center))
            pygame.draw.rect(screen, PALETTE["text"], rect, 1)  # Bordes

def main():
    pygame.init()
    pygame.display.set_caption("Buscaminas")

    # Inicializar variables
    current_difficulty = None
    board = None
    game_over = False
    start_time = None
    elapsed_time = 0
    clock = pygame.time.Clock()

    # Cargar fuentes
    try:
        font_large = pygame.font.Font(FONT_PATH, 48)
    except:
        font_large = pygame.font.SysFont(None, 48)  # Fallback a la fuente predeterminada
    try:
        font_medium = pygame.font.Font(FONT_PATH, 36)
    except:
        font_medium = pygame.font.SysFont(None, 36)  # Fallback a la fuente predeterminada
    try:
        font_small = pygame.font.Font(FONT_PATH, 24)
    except:
        font_small = pygame.font.SysFont(None, 24)  # Fallback a la fuente predeterminada

    # Cargar y establecer el icono de la ventana
    try:
        icon = pygame.image.load(ICON_PATH)
        pygame.display.set_icon(icon)
    except:
        print("No se pudo cargar el icono de la ventana.")

    # Cargar y escalar la imagen de fondo
    try:
        background = pygame.image.load(BACKGROUND_IMAGE_PATH)
    except:
        background = None
        print("No se pudo cargar la imagen de fondo.")

    # Cargar y escalar imágenes de mina y bandera
    try:
        mine_image = pygame.image.load(MINE_IMAGE_PATH)
        mine_image = pygame.transform.scale(mine_image, (40, 40))  # Ajusta según CELL_SIZE
    except:
        mine_image = None
        print("No se pudo cargar la imagen de la mina.")
    
    try:
        flag_image = pygame.image.load(FLAG_IMAGE_PATH)
        flag_image = pygame.transform.scale(flag_image, (40, 40))  # Ajusta según CELL_SIZE
    except:
        flag_image = None
        print("No se pudo cargar la imagen de la bandera.")
    
    # Cargar sonidos
    try:
        reveal_sound = pygame.mixer.Sound("src/sounds/reveal.wav")
    except:
        reveal_sound = None
        print("No se pudo cargar el sonido de revelación.")
    
    try:
        mine_sound = pygame.mixer.Sound("src/sounds/mine.wav")
    except:
        mine_sound = None
        print("No se pudo cargar el sonido de mina.")
    
    try:
        flag_sound = pygame.mixer.Sound("src/sounds/flag.wav")
    except:
        flag_sound = None
        print("No se pudo cargar el sonido de bandera.")
    
    # Cargar música de fondo
    try:
        pygame.mixer.music.load("src/sounds/background_music.mp3")
        pygame.mixer.music.play(-1)  # -1 para repetir indefinidamente
    except:
        print("No se pudo cargar la música de fondo.")
    
    # Bucle principal
    while True:
        if board is None:
            # Selección de dificultad
            # Definir el tamaño de la pantalla basado en la máxima dificultad
            max_rows = max(params["rows"] for params in DIFFICULTIES.values())
            max_cols = max(params["cols"] for params in DIFFICULTIES.values())
            CELL_SIZE = 40
            WIDTH = max_cols * CELL_SIZE
            HEIGHT = max_rows * CELL_SIZE + 100  # +100 para la interfaz y botones

            screen = pygame.display.set_mode((WIDTH, HEIGHT))
            
            # Dibujar el fondo
            if background:
                background_scaled = pygame.transform.scale(background, (WIDTH, HEIGHT))
                screen.blit(background_scaled, (0, 0))
            else:
                screen.fill(PALETTE["background"])
            
            # Dibujar el menú de dificultad
            buttons = display_difficulty_menu(screen, font_large, font_medium)
            pygame.display.flip()
            
            # Manejar eventos para selección de dificultad
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    for button_rect, difficulty in buttons:
                        if button_rect.collidepoint(x, y):
                            current_difficulty = difficulty
                            params = DIFFICULTIES[difficulty]
                            board = Board(params["rows"], params["cols"], params["mines"])
                            start_time = time.time()
                            break

        else:
            # Bucle del juego
            clock.tick(30)  # 30 FPS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                    x, y = pygame.mouse.get_pos()
                    # Ajustar coordenadas según interfaz
                    col = x // CELL_SIZE
                    row = (y - 50) // CELL_SIZE  # 50 píxeles reservados para la interfaz
                    if 0 <= row < board.rows and 0 <= col < board.cols:
                        if event.button == 1:  # Clic izquierdo
                            if reveal_sound:
                                reveal_sound.play()
                            board.reveal_cell_with_animation(row, col, screen)
                            if board.grid[row][col].has_mine:
                                if mine_sound:
                                    mine_sound.play()
                                game_over = True
                        elif event.button == 3:  # Clic derecho
                            board.toggle_mark_cell(row, col)
                            if flag_sound:
                                flag_sound.play()
                
                # Manejar el botón de reiniciar
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    if RESTART_BUTTON_RECT.collidepoint(x, y):
                        # Reiniciar el juego con la misma dificultad
                        params = DIFFICULTIES[current_difficulty]
                        board = Board(params["rows"], params["cols"], params["mines"])
                        game_over = False
                        start_time = time.time()
                        elapsed_time = 0

            # Actualizar el tiempo transcurrido
            if not game_over:
                elapsed_time = int(time.time() - start_time)
            
            # Verificar condición de victoria
            if board.check_victory():
                game_over = True

            # Dibujar el fondo
            if background:
                background_scaled = pygame.transform.scale(background, (WIDTH, HEIGHT))
                screen.blit(background_scaled, (0, 0))
            else:
                screen.fill(PALETTE["background"])
            
            # Dibujar el tablero y otros elementos
            draw_grid(screen, board, mine_image, flag_image, font_small)
            draw_restart_button(screen, font_small)
            draw_info(screen, board, elapsed_time, font_small)
            
            # Mensajes de fin de juego
            if game_over:
                if board.check_victory():
                    message = "¡Ganaste!"
                    color = PALETTE["victory"]
                else:
                    message = "¡Perdiste!"
                    color = PALETTE["defeat"]
                render_text_with_shadow(screen, message, font_large, color, (50, 50, 50), (WIDTH // 2, HEIGHT // 2))
            
            pygame.display.flip()

if __name__ == "__main__":
    main()
