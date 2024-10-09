import pygame
import sys
from pygame.locals import *

# Definir cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Tamanho dos blocos e da janela
BLOCK_SIZE = 40
WINDOW_WIDTH = 18 * BLOCK_SIZE
WINDOW_HEIGHT = 10 * BLOCK_SIZE

# Inicializar o pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pacman Game")

# Função para carregar imagem com verificação de erro
def load_image(file_name):
    try:
        image = pygame.image.load(file_name)
        return pygame.transform.scale(image, (BLOCK_SIZE, BLOCK_SIZE))
    except pygame.error as e:
        print(f"Erro ao carregar a imagem {file_name}: {e}")
        return None

# Carregar imagens dos sprites com verificação
pacman_img = load_image("Sprites/95.png")
ghost1_img = load_image("Sprites/0.png")
ghost2_img = load_image("Sprites/17.png")

# Verificar se todas as imagens foram carregadas corretamente
if not pacman_img or not ghost1_img or not ghost2_img:
    print("Falha ao carregar uma ou mais imagens. Verifique os caminhos e arquivos.")
    pygame.quit()
    sys.exit()

# Layout do labirinto
maze_layout = [
    "------------------",
    "-***--***********-",
    "-********-*-*****-",
    "-****---*-**--***-",
    "-********-*******-",
    "-**----****----**-",
    "-********-*******-",
    "--*--********--*--",
    "-******--********-",
    "------------------"
]

# Função para desenhar o labirinto
def draw_maze():
    for y, row in enumerate(maze_layout):
        for x, cell in enumerate(row):  
            if cell == "-":
                pygame.draw.rect(screen, BLUE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            elif cell == "*":
                pygame.draw.circle(screen, WHITE, (x * BLOCK_SIZE + BLOCK_SIZE // 2, y * BLOCK_SIZE + BLOCK_SIZE // 2), 5)

# Posições iniciais do Pacman e dos fantasmas
pacman_pos = [1, 1]  # Posição inicial do Pacman
ghost1_pos = [13, 1]  # Posição inicial do primeiro fantasma
ghost2_pos = [14, 3]  # Posição inicial do segundo fantasma

# Função para mover o Pacman
def move_pacman(direction):
    if direction == "up" and maze_layout[pacman_pos[1] - 1][pacman_pos[0]] not in "-":
        pacman_pos[1] -= 1
    elif direction == "down" and maze_layout[pacman_pos[1] + 1][pacman_pos[0]] not in "-":
        pacman_pos[1] += 1
    elif direction == "left" and maze_layout[pacman_pos[1]][pacman_pos[0] - 1] not in "-":
        pacman_pos[0] -= 1
    elif direction == "right" and maze_layout[pacman_pos[1]][pacman_pos[0] + 1] not in "-":
        pacman_pos[0] += 1

# Função para renderizar sprites na tela
def draw_sprites():
    # Desenhar Pacman
    screen.blit(pacman_img, (pacman_pos[0] * BLOCK_SIZE, pacman_pos[1] * BLOCK_SIZE))
    # Desenhar fantasmas
    screen.blit(ghost1_img, (ghost1_pos[0] * BLOCK_SIZE, ghost1_pos[1] * BLOCK_SIZE))
    screen.blit(ghost2_img, (ghost2_pos[0] * BLOCK_SIZE, ghost2_pos[1] * BLOCK_SIZE))

# Loop principal do jogo
clock = pygame.time.Clock()
while True:
    screen.fill(BLACK)
    draw_maze()
    draw_sprites()

    # Eventos de teclado para mover o Pacman
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                move_pacman("up")
            elif event.key == K_DOWN:
                move_pacman("down")
            elif event.key == K_LEFT:
                move_pacman("left")
            elif event.key == K_RIGHT:
                move_pacman("right")

    # Atualizar a tela
    pygame.display.flip()
    clock.tick(10)
