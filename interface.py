import pygame
import sys
from pygame.locals import *
from game import game
from pacman import pacman
from ghosts import ghosts
from typing import Tuple

# definindo cores utilizadas na interface gráfica
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Inicializando o tamanho dos blocos e da janela do jogo
BLOCK_SIZE = 35
WINDOW_WIDTH = 28 * BLOCK_SIZE
WINDOW_HEIGHT = 26 * BLOCK_SIZE

# Inicializando o pygame, biblioteca de games utilizada pra programar o jogo
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("IA Joga: Pac-Man")

# Variável de controle para indicar se o jogo acabou
game_over = False
ghost_recovery_timer_1 = 0
ghost_recovery_timer_2 = 0

# Definindo a fonte para a mensagem de "Game Over"
font = pygame.font.SysFont('arial', 46)
font_s = pygame.font.SysFont('arial', 12)


def display_score(screen, score):

    # Renderizando  o texto da pontuação
    score_text = font_s.render(f"Score: {score}", True, WHITE)
    
    # Posicionando o texto no canto superior esquerdo da tela
    screen.blit(score_text, (10, 10))

# Exibe mensagem de game over no centro da tela
def show_game_over_message(screen):

    game_over_text = font.render('GAME OVER', True, (255, 0, 0))
    text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    screen.blit(game_over_text, text_rect)

# Exibe a mensagem de vitória no centro da tela
def show_victory_message(screen):

    victory_text = font.render('VICTORY', True, (0, 255, 0))
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

# Carrega imagens dos sprites com verificação
pacman_img = load_image("Sprites/woody_d.png")
ghost1_img = load_image("Sprites/0.png")
ghost2_img = load_image("Sprites/17.png")

# Cria uma instância do jogo e da IA do Pac-Man
game_instance = game()
pacman_ai = pacman()
ghost_ai = ghosts()

# Função para desenhar o labirinto definido no arquivo game.py
# "-": Desenha uma parede
# "*": Desenha uma comida
# "o": Desenha uma comida especial
def draw_maze():
    for y, row in enumerate(game_instance.get_board()):
        for x, cell in enumerate(row):
            if cell == '-':  
                pygame.draw.rect(screen, BLUE, pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)
            elif cell == '*':  
               pygame.draw.circle(screen, WHITE, (x * BLOCK_SIZE + BLOCK_SIZE // 2, y * BLOCK_SIZE + BLOCK_SIZE // 2), 5)
            elif cell == 'o': 
               pygame.draw.circle(screen, WHITE, (x * BLOCK_SIZE + BLOCK_SIZE // 2, y * BLOCK_SIZE + BLOCK_SIZE // 2), 10)


# Função para renderizar sprites na tela
def draw_sprites():
    # Desenha Pacman
    pacman_x, pacman_y = game_instance.get_pos_pacman()
    screen.blit(pacman_img, (pacman_y * BLOCK_SIZE, pacman_x * BLOCK_SIZE))

    # Desenha fantasmas
    ghost1_x, ghost1_y = game_instance.get_pos_ghost(1)
    screen.blit(ghost1_img, (ghost1_y * BLOCK_SIZE, ghost1_x * BLOCK_SIZE))

    ghost2_x, ghost2_y = game_instance.get_pos_ghost(2)
    screen.blit(ghost2_img, (ghost2_y * BLOCK_SIZE, ghost2_x * BLOCK_SIZE))

# Loop principal do jogo
clock = pygame.time.Clock()
delay = 0 # Define o valor do delay em segundos

# Verifica se o pacman colidiu com algum fantasma
def verificar_colisao(game_instance) -> Tuple[bool, int]:
    # Retorna (True, numero do fantasma ( 1 ou 2)) se houver colisão, indicando que o jogo deve terminar com a vitória dos fantasmas ou que Pacman comeu o fantasma.
    pacman_pos = game_instance.get_pos_pacman()
    ghost1_pos = game_instance.get_pos_ghost(1)
    ghost2_pos = game_instance.get_pos_ghost(2)
    
    if pacman_pos == ghost1_pos:
        return True, 1  # Pacman colidiu com o fantasma 1
    elif pacman_pos == ghost2_pos:
        return True, 2  # Pacman colidiu com o fantasma 2
    
    return False, None

# Loop principal do jogo
running = True
while running:
    screen.fill(BLACK)          
    draw_maze()
    draw_sprites()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Verifica se estamos no estado de Game Over
        if game_over or game_instance.food_count == 0:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                running = False  # Sai do jogo se a tecla "Enter" for pressionada

    # Se os fantasmas estiverem vulneraveis, verifica se o power_mode_timer é maior que zero, se sim, decrementa ele, se não, volta os fantasmas para o comportamento normal
    if(game_instance.ghosts_are_vulnerable):
            if game_instance.power_mode_timer > 0:          
                game_instance.power_mode_timer -= 1
            else:
                game_instance.ghosts_are_vulnerable = False  # Fantasmas voltam ao comportamento normal
            
           
    # Verificar se o jogo terminou
    if game_instance.game_finished():
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
        # Escolhe a melhor ação para o Pacman usando a IA
        best_action = pacman_ai.best_action(game_instance)
        game_instance.move_pacman_validation(best_action)
        
        #sprites woody_man 
        if best_action == 'right':
            pacman_img = load_image("Sprites/woody_d.png")

        elif best_action == 'left':
            pacman_img = load_image("Sprites/woody_e.png")

        # chama a função verificar_colisao para ver se houve colisao do pacman com fantasmas
        colidiu, fantasma = verificar_colisao(game_instance)
        ghost_recovery_timer = 0
     
        # Verificar colisão após o movimento do Pac-Man
        if colidiu:
            if game_instance.ghosts_are_vulnerable:
                # Pacman come o fantasma vulnerável e ele vai para a prisão
                
                # Enviar o fantasma comido para a prisão
                if fantasma == 1:
                    game_instance.set_pos_ghost(1, (12, 13))  # Fantasma 1 vai para a prisão
                    ghost_recovery_timer_1 = 10               # Seta o tempo de recuperação do fantasma preso para 10 unidades de tempo
                elif fantasma == 2:
                    game_instance.set_pos_ghost(2, (12, 14))  # Fantasma 2 vai para a prisão
                    ghost_recovery_timer_2 = 10               # Seta o tempo de recuperação do fantasma preso para 10 unidades de tempo

            else:
                # Caso contrário, Pacman foi capturado
                game_over = True  # Pacman foi capturado por um fantasma
                continue  # Pula a atualização de movimentação e entra em estado de espera

        # função para ver se tem algum fantasma na prisao
        def ghost_in_prison(ghost):
            ghost_pos = game_instance.get_pos_ghost(ghost)
            if 10 <= ghost_pos[0] == 12 and 11 <= ghost_pos[1] <= 16:
                return True

            return False

        # Se o tempo de recuperação do fantasma é maior que 0, decrementa ele. Se o tempo de recuperação for igual a zero e ele estiver dentro da prisão, ele volta ao jogo
        if ghost_recovery_timer_1 > 0:
            ghost_recovery_timer_1 -= 1
        elif ghost_recovery_timer_1 == 0 and ghost_in_prison(1):
            game_instance.set_pos_ghost(1, (8, 14))  # Fantasma 1 volta ao jogo

        # Se o tempo de recuperação do fantasma é maior que 0, decrementa ele. Se o tempo de recuperação for igual a zero e ele estiver dentro da prisão, ele volta ao jogo
        if ghost_recovery_timer_2 > 0:
            ghost_recovery_timer_2 -= 1
        elif ghost_recovery_timer_2 == 0 and ghost_in_prison(2):
            game_instance.set_pos_ghost(2, (8, 14))  # Fantasma 2 volta ao jogo


        # Mover os fantasmas com base na lógica interna do jogo
        pos_g1 = game_instance.get_pos_ghost(1)
        pos_g2 = game_instance.get_pos_ghost(2)
        pos_pacman = game_instance.get_pos_pacman()


        if not game_instance.ghosts_are_vulnerable:
            poses, d1, d2 = ghost_ai.moves_ghosts(
            pos_g1, pos_g2, pos_pacman, game_instance.get_board(), game_instance.get_size()
            )
                 # Atualizar as posições dos fantasmas no jogo
            game_instance.set_pos_ghost(1, poses["ghosts1"])
            game_instance.set_pos_ghost(2, poses["ghosts2"])

        # Se os fantasmas estiverem vulneraveis, eles ficam brancos
        if game_instance.ghosts_are_vulnerable:
            ghost1_img = load_image("Sprites/81.png")
            ghost2_img = load_image("Sprites/81.png")
        else: 
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
    
   

    # Atualizar a tela
    display_score(screen, game_instance.score)
    pygame.display.flip()
    clock.tick(30)
    pygame.time.wait(int(delay * 1000))
