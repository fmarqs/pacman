import pygame
import sys
from pygame.locals import *
from game import game
from pacman import pacman
from ghosts import ghosts

# Definir cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Tamanho dos blocos e da janela
BLOCK_SIZE = 35
WINDOW_WIDTH = 28 * BLOCK_SIZE
WINDOW_HEIGHT = 26 * BLOCK_SIZE

# Inicializar o pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pacman Game - IA Integration")

# Variável de controle para indicar se o jogo acabou
game_over = False

# Definir a fonte para a mensagem de "Game Over"
font = pygame.font.SysFont('arial', 36)
font_s = pygame.font.SysFont('arial', 12)

def display_score(screen, score):
    # Renderizar o texto da pontuação
    score_text = font_s.render(f"Score: {score}", True, WHITE)
    
    # Posicionar o texto no canto superior esquerdo da tela
    screen.blit(score_text, (10, 10))


def show_game_over_message(screen):
    """
    Exibe uma mensagem de Game Over no centro da tela.
    """
    game_over_text = font.render('GAME OVER - Pac-Man Capturado!', True, (255, 0, 0))
    text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    screen.blit(game_over_text, text_rect)

def show_victory_message(screen):
    """
    Exibe uma mensagem de vitória no centro da tela.
    """
    victory_text = font.render('VICTORY - Pac-Man Venceu!', True, (0, 255, 0))
    text_rect = victory_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    screen.blit(victory_text, text_rect)


# Função para carregar imagem com verificação de erro
def load_image(file_name):
    try:
        image = pygame.image.load(file_name)
        return pygame.transform.scale(image, (BLOCK_SIZE, BLOCK_SIZE))
    except pygame.error as e:
        print(f"Erro ao carregar a imagem {file_name}: {e}")
        return None

# Carregar imagens dos sprites com verificação
pacman_img = load_image("Sprites/woody_d.png")
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
ghost_ai = ghosts()

# def draw_maze():
#     for y, row in enumerate(game_instance.get_board()):
#         for x, cell in enumerate(row):
#             if cell == "-":
#                 # Desenhar linhas em vez de blocos
#                 pygame.draw.line(screen, BLUE, (x * BLOCK_SIZE, y * BLOCK_SIZE), ((x + 1) * BLOCK_SIZE, y * BLOCK_SIZE), 5)  # Linha superior
#                 pygame.draw.line(screen, BLUE, (x * BLOCK_SIZE, y * BLOCK_SIZE), (x * BLOCK_SIZE, (y + 1) * BLOCK_SIZE), 5)  # Linha esquerda
#                 pygame.draw.line(screen, BLUE, ((x + 1) * BLOCK_SIZE, y * BLOCK_SIZE), ((x + 1) * BLOCK_SIZE, (y + 1) * BLOCK_SIZE), 5)  # Linha direita
#                 pygame.draw.line(screen, BLUE, (x * BLOCK_SIZE, (y + 1) * BLOCK_SIZE), ((x + 1) * BLOCK_SIZE, (y + 1) * BLOCK_SIZE), 5)  # Linha inferior
#             elif cell == "*":
#                 pygame.draw.circle(screen, WHITE, (x * BLOCK_SIZE + BLOCK_SIZE // 2, y * BLOCK_SIZE + BLOCK_SIZE // 2), 5)

def draw_maze():
    for y, row in enumerate(game_instance.get_board()):
        for x, cell in enumerate(row):
            if cell == '-':  # Desenhar uma parede
                # Desenhar as paredes com linhas grossas (3 pixels de espessura)
                pygame.draw.rect(screen, BLUE, pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)
            elif cell == '*':  # Espaços vazios para movimento
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
delay = 0.1  # Defina o valor do delay em segundos

def verificar_colisao(game_instance) -> bool:
    """
    Verifica se Pac-Man colidiu com algum fantasma.
    Retorna True se houver colisão, indicando que o jogo deve terminar com a vitória dos fantasmas.
    """
    pacman_pos = game_instance.get_pos_pacman()
    ghost1_pos = game_instance.get_pos_ghost(1)
    ghost2_pos = game_instance.get_pos_ghost(2)
    return pacman_pos == ghost1_pos or pacman_pos == ghost2_pos

running = True
while running:
    screen.fill(BLACK)
    draw_maze()
    draw_sprites()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Verificar se estamos no estado de Game Over
        if game_over or game_instance.food_count == 0:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                running = False  # Sai do jogo se a tecla "Enter" for pressionada
           
    # Verificar se o jogo terminou
    if game_instance.is_terminal():
        if game_instance.food_count == 0:
            show_victory_message(screen)
            game_over = True
        else:
            show_game_over_message(screen)  
            game_over = True
        
    
    if game_over:
        pygame.display.flip()
        continue
    
    else:
        # Escolher a melhor ação para o Pacman usando a IA
        best_action = pacman_ai.best_action(game_instance)
        game_instance.move_pacman(best_action)
        
        #sprites woody_man 
        if best_action == 'right':
            pacman_img = load_image("Sprites/woody_d.png")

        elif best_action == 'left':
            pacman_img = load_image("Sprites/woody_e.png")
            
        # Verificar colisão após o movimento do Pac-Man
        if verificar_colisao(game_instance):
            game_over = True  # Pac-Man foi capturado por um fantasma
            print("Pacman foi capturado por um fantasma! Jogo Terminado!")
            continue  # Pula a atualização de movimentação e entra em estado de espera


        # Mover os fantasmas com base na lógica interna do jogo
        pos_g1 = game_instance.get_pos_ghost(1)
        pos_g2 = game_instance.get_pos_ghost(2)
        pos_pacman = game_instance.get_pos_pacman()


        poses, d1, d2 = ghost_ai.move_ghosts(
        pos_g1, pos_g2, pos_pacman, game_instance.get_board(), game_instance.get_size()
        )
        print("d1: ", d1)
        print("d2: ", d2)
        
        #sprites fantasma 1 
        if best_action == 'up':
            ghost1_img = load_image("Sprites/10.png")

        elif best_action == 'down':
            ghost1_img = load_image("Sprites/4.png")
            
        elif best_action == 'left':
            ghost1_img = load_image("Sprites/0.png")
        
        elif best_action == 'right':
            ghost1_img = load_image("Sprites/6.png")

        #sprites fantasma 2
        if best_action == 'up':
            ghost2_img = load_image("Sprites/44.png")

        elif best_action == 'down':
            ghost2_img = load_image("Sprites/39.png")
            
        elif best_action == 'left':
            ghost2_img = load_image("Sprites/36.png")
        
        elif best_action == 'right':
            ghost2_img = load_image("Sprites/40.png")
    
        # Atualizar as posições dos fantasmas no jogo
        game_instance.set_pos_ghost(1, poses["ghosts1"])
        game_instance.set_pos_ghost(2, poses["ghosts2"])

        # Verificar colisão após o movimento dos fantasmas
        if verificar_colisao(game_instance):
            game_over = True  # Pac-Man foi capturado por um fantasma
            print("Pacman foi capturado por um fantasma! Jogo Terminado!")
            continue  # Pula a atualização de movimentação e entra em estado de espera

    
    # Atualizar a tela
    display_score(screen, game_instance.score)
    pygame.display.flip()
    clock.tick(30)
    pygame.time.wait(int(delay * 1000))
