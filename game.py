import random as r
from typing import Tuple, List

class game:
    def __init__(self, size_board=(26, 28), pacman_position=(14, 14), ghost1_position=(3, 4), ghost2_position=(21, 24), score=0):
        self.size_board = size_board
        self.pacman_position = pacman_position
        self.ghost1_position = ghost1_position
        self.ghost2_position = ghost2_position
        self.score = score
        self.board = None
        self.food_count = 0  
        self.create_board_game()
        self.ghosts_are_vulnerable = False
        self.power_mode_timer = 0

    def create_board_game(self):
        # labirinto do jogo
        maze_layout = [
        "----------------------------",  # 1
        "-************--************-",  # 2
        "-*----*-----*--*-----*----*-",  # 3
        "-o************************o-",  # 4
        "-*----*--*--------*--*----*-",  # 5
        "-******--****--****--******-",  # 6
        "------*-----*--*-----*------",  # 7
        "------*-----*--*-----*------",  # 8
        "------*--**********--*------",  # 9
        "------*--*--------*--*------",  # 10
        "------*--*-      -*--*------",  # 11
        " *********-      -********* ",  # 12
        "------*--*-      -*--*------",  # 13
        "------*--*--------*--*------",  # 14
        "------*--**********--*------",   # 15
        "-************--************-",  # 16
        "-*----*-----*--*-----*----*-", # 17
        "-*----*-----*--*-----*----*-",  # 18
        "-***--****************--***-",  # 19
        "---*--*--*--------*--*--*---",  # 20
        "---*--*--*--------*--*--*---",  # 21
        "-o*****--****--****--*****o-",  # 22
        "-*----------*--*----------*-",  # 23
        "-*----------*--*----------*-",  # 24
        "-**************************-",  # 25
        "----------------------------",  # 26
    ]

        # aplica o labirinto no tabuleiro
        self.board = [list(row) for row in maze_layout]

        # contador de comida inicial do labirinto
        self.food_count = 272

    # retorna as dimensoes do tabuleiro
    def get_size(self) -> Tuple[int, int]:
        return self.size_board

    # retorna o tabuleiro
    def get_board(self):
        return self.board

    # configura o labirinto
    def set_board(self, board: List[List[str]]) -> None:
        self.board = board

    # pega a posição do pacman (x,y)
    def get_pos_pacman(self) -> Tuple[int, int]:
        if self.pacman_position == [11, 28]:
            self.pacman_position = [1, 1]
        elif self.pacman_position == [11, 0]:
            self.pacman_position = [11, 27]
        return self.pacman_position

    def set_pos_pacman(self, new_pos: Tuple[int, int]) -> None:
        self.pacman_position = new_pos

    def get_pos_ghost(self, choice: int) -> Tuple[int, int]:
        if choice == 1:
            return self.ghost1_position
        elif choice == 2:
            return self.ghost2_position

    def set_pos_ghost(self, choice: int, new_pos: Tuple[int, int]):
        if choice == 1:
            self.ghost1_position = new_pos
        elif choice == 2:
            self.ghost2_position = new_pos

    #  define um novo valor para o score do jogo
    def set_score(self, new_score: int) -> None:
        self.score = new_score

    # ativa o modo power em que os fantasmas ficam parados e vulneraveis
    def activate_power_mode(self):
        self.power_mode_timer = 40              # o modo power dura 40 unidades de tempo
        self.ghosts_are_vulnerable = True       # seta os fantasmas pra vulneravel


    # valida a movimentação do pacman
    def move_pacman_validation(self, direction):
        # posição atual do Pacman
        x, y = self.pacman_position
        new_x, new_y = x, y

        # determina nova posição baseada no direction recebido
        if direction == 'up':
            new_x = x - 1
        elif direction == 'down':
            new_x = x + 1
        elif direction == 'left':
            new_y = y - 1
        elif direction == 'right':
            new_y = y + 1

        # verifica se a nova posição é válida (não é parede nem fantasma)
        if self.board[new_x][new_y] not in ['-', 'G1', 'G2']:

            # atualiza a posição do pacman
            self.pacman_position = (new_x, new_y)

             # atualiza a nova posição do pacman, considerando portais
            if new_x == 11 and new_y == 0:  # portal à esquerda
                self.pacman_position = (11, 27)  # teleporta para o lado direito
            elif new_x == 11 and new_y == 27:  # portal à direita
                self.pacman_position = (11, 0)  # teleporta para o lado esquerdo
            else:
                self.pacman_position = (new_x, new_y)

            # verificar se pacman comeu a comida normal
            if self.board[new_x][new_y] == '*':
                self.score += 10                # +10 pontos se comer a comida normal
                self.food_count -= 1            # diminui a contagem de comidas presentes no tabuleiro
                self.board[new_x][new_y] = ' '  # remove a comida ao comer
            
            # verifica se pacman comeu a comida especial
            elif self.board[new_x][new_y] == 'o': 
                self.score += 10    
                self.food_count -= 1
                self.activate_power_mode()      # ativa o power mode
                self.board[new_x][new_y] = ' '  # remove comida especial

    # valida movimentação dos fantasmas
    def move_ghosts_validation(self):
        for ghost_num in [1, 2]:

            # pega posição atual do fantasma
            ghost_pos = self.get_pos_ghost(ghost_num)
            x, y = ghost_pos

            # movimentos possíveis para o fantasma (cima, baixo, esquerda, direita)
            possible_moves = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

            # verifica se os movimentos são válidos (dentro dos limites e sem teleportes)
            valid_moves = [
                (nx, ny) for (nx, ny) in possible_moves
                if 0 <= nx < self.size_board[0] and 0 <= ny < self.size_board[1]
                and self.board[nx][ny] not in ['-', 'P', f'G{ghost_num}', f'G{3 - ghost_num}']
            ]

            if valid_moves:
                # escolhe um movimento aleatório válido
                new_pos = r.choice(valid_moves)

                # Mover o fantasma para a nova posição
                self.set_pos_ghost(ghost_num, new_pos)
                self.board[new_pos[0]][new_pos[1]] = f'G{ghost_num}'

    # retorna todos os movimentos possíveis para o Pac-Man no estado atual do jogo
    def get_pacman_moves(self) -> List[str]:

        # pega posição atual do pacman e o tamanho do tabuleiro
        x, y = self.pacman_position
        board_size = self.get_size()

        possible_moves = []
        # verifica se pacman pode se mover para cima
        if x > 0 and self.board[x - 1][y] not in ['-', 'G1', 'G2']:
            possible_moves.append('up')
        # verifica se pacman pode se mover para baixo
        if x < board_size[0] - 1 and self.board[x + 1][y] not in ['-', 'G1', 'G2']:
            possible_moves.append('down')
        # verifica se pacman pode se mover para a esquerda 
        if y > 0 and self.board[x][y - 1] not in ['-', 'G1', 'G2']:
            possible_moves.append('left')
        # verifica se pacman pode se mover para a direita
        if y < board_size[1] - 1 and self.board[x][y + 1] not in ['-', 'G1', 'G2']:
            possible_moves.append('right')

        return possible_moves
    
    # retorna todos os movimentos possíveis para os fantasmas no estado atual do jogo
    def get_ghost_moves(self) -> List[Tuple[int, int]]:
        ghost_moves = []

        # adiciona movimentos para cada fantasma
        for ghost_num in [1, 2]:
            ghost_pos = self.get_pos_ghost(ghost_num)
            x, y = ghost_pos

            # lista de movimentos possíveis (cima, baixo, esquerda, direita)
            possible_moves = [
                (x - 1, y),  # up
                (x + 1, y),  # down
                (x, y - 1),  # left
                (x, y + 1)   # right
            ]

            # filtra movimentos válidos (não colidem com paredes ou pacman)
            valid_moves = [move for move in possible_moves if self.is_valid_move(move)]
            ghost_moves.extend(valid_moves)

        return ghost_moves

    # verifica se a posição é valida no tabuleiro
    def is_valid_move(self, position: Tuple[int, int]) -> bool:
        x, y = position
        return (
            0 <= x < self.size_board[0] and
            0 <= y < self.size_board[1] and
            self.board[x][y] not in ['-', 'P', 'G', 'G2']  # não pode ser parede, pacman ou outro fantasma
        )

    # verifica se o jogo acabou
    def game_finished(self) -> bool:

        # verifica se o pacman foi capturado por um fantasma
        if self.get_pos_pacman() == self.get_pos_ghost(1) or self.get_pos_pacman() == self.get_pos_ghost(2):
            return True

        # verifica se todas as comidas foram comidas
        if self.food_count == 0:
            return True

        # caso contrário, o jogo não terminou
        return False

    # cria uma copia do estado atual do jogo
    def create_copy_state(self) -> 'game':
        # criaa uma nova instância da classe game com os mesmos parâmetros iniciais
        new_state = game(
            size_board=self.get_size(),
            pacman_position=self.get_pos_pacman(),
            ghost1_position=self.get_pos_ghost(1),
            ghost2_position=self.get_pos_ghost(2),
            score=self.score
        )

        # copia o tabuleiro
        new_board = [row[:] for row in self.get_board()]
        new_state.set_board(new_board)

        return new_state


    # aplica um movimento no estado atual do jogo
    def apply_move(self, move: str, is_pacman: bool) -> 'game':

        # cria uma cópia do estado atual para evitar mudanças no estado original
        new_state = self.create_copy_state()  # chamada corrigida para usar self.create_copy_state()

        if is_pacman:
            # aplica movimento para o pacman
            new_state.move_pacman_validation(move)
        else:
            # aplica movimento para os fantasmas (considerando que o movimento é aleatório ou predefinido)
            new_state.move_ghosts_validation()  # Esse método deve mover todos os fantasmas

        return new_state


