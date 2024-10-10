import pygame
import sys
from pygame.locals import *
from game import game
from pacman import pacman

# Definir cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Tamanho dos blocos e da janela
BLOCK_SIZE = 40
WINDOW_WIDTH = 18 * BLOCK_SIZE
WINDOW_HEIGHT = 10 * BLOCK_SIZE

# Inicializar o pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pacman Game - IA Integration")

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

# Criar uma instância do jogo e da IA do Pac-Man
game_instance = game()
pacman_ai = pacman()

# Função para desenhar o labirinto
def draw_maze():
    for y, row in enumerate(game_instance.get_board()):
        for x, cell in enumerate(row):
            if cell == "-":
                pygame.draw.rect(screen, BLUE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            elif cell == "*":
                pygame.draw.circle(screen, WHITE, (x * BLOCK_SIZE + BLOCK_SIZE // 2, y * BLOCK_SIZE + BLOCK_SIZE // 2), 5)

# Função para renderizar sprites na tela
def draw_sprites():
    # Desenhar Pacman
    pacman_x, pacman_y = game_instance.get_pos_pacman()
    screen.blit(pacman_img, (pacman_y * BLOCK_SIZE, pacman_x * BLOCK_SIZE))

    # Desenhar fantasmas
    ghost1_x, ghost1_y = game_instance.get_pos_ghost(1)
    screen.blit(ghost1_img, (ghost1_y * BLOCK_SIZE, ghost1_x * BLOCK_SIZE))

    ghost2_x, ghost2_y = game_instance.get_pos_ghost(2)
    screen.blit(ghost2_img, (ghost2_y * BLOCK_SIZE, ghost2_x * BLOCK_SIZE))

# Loop principal do jogo
clock = pygame.time.Clock()
delay = 0.75  # Defina o valor do delay em segundos

while True:
    screen.fill(BLACK)
    draw_maze()
    draw_sprites()

    # Eventos de teclado para fechar o jogo
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Verificar se o jogo terminou
    if game_instance.is_terminal():
        if game_instance.food_count == 0:
            print("** PACMAN WIN !!!")
        else:
            print("PACMAN LOST !")
        break

    # Escolher a melhor ação para o Pacman usando a IA
    best_action = pacman_ai.best_action(game_instance)
    game_instance.move_pacman(best_action)

    # Mover os fantasmas com base na lógica interna do jogo
    game_instance.move_ghosts()

    # Atualizar a tela
    pygame.display.flip()
    clock.tick(10)
    pygame.time.wait(int(delay * 1000))
