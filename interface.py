import pygame
import sys

# Inicializa o Pygame
pygame.init()

# Definir tamanho do tabuleiro e das células
cell_size = 30
board_size = (9, 18)  # Número de linhas e colunas

# Definir tamanho da janela
screen_size = (board_size[1] * cell_size, board_size[0] * cell_size)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Pacman Game")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Desenhar tabuleiro
def draw_board(board, pacman_pos, ghost1_pos, ghost2_pos):
    screen.fill(BLACK)
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            rect = pygame.Rect(j * cell_size, i * cell_size, cell_size, cell_size)
            if cell == '-':
                pygame.draw.rect(screen, BLUE, rect)
            elif cell == '*':
                pygame.draw.circle(screen, WHITE, rect.center, cell_size // 4)
            elif (i, j) == pacman_pos:
                pygame.draw.circle(screen, YELLOW, rect.center, cell_size // 2)
            elif (i, j) == ghost1_pos:
                pygame.draw.circle(screen, RED, rect.center, cell_size // 2)
            elif (i, j) == ghost2_pos:
                pygame.draw.circle(screen, RED, rect.center, cell_size // 2)
            else:
                pygame.draw.rect(screen, BLACK, rect, 1)

# Jogo exemplo
board = [
    ["*", "*", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
    ["*", " ", "*", "*", "-", "-", " ", "-", "*", "*", "*", "-", "*", "*", " ", "-"],
    ["-", "-", "-", "*", "*", "*", "-", "-", "*", "-", "-", "-", "*", "*", "*", "-", "-"],
    ["*", "*", "*", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"]
]

pacman_pos = (1, 1)
ghost1_pos = (1, 5)
ghost2_pos = (1, 14)

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_board(board, pacman_pos, ghost1_pos, ghost2_pos)
    pygame.display.flip()

pygame.quit()
sys.exit()
