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
        self.food_count = 0  # Contagem de comidas no tabuleiro
        self.create_board_game()
        self.ghosts_are_vulnerable = False
        self.power_mode_timer = 0

    def create_board_game(self):
        # Novo layout do labirinto fornecido
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

        # Inicializa o tabuleiro com o layout fornecido
        self.board = [list(row) for row in maze_layout]

        # Contar o número de comidas no layout fornecido
        self.food_count = 271

    def get_size(self) -> Tuple[int, int]:
        # Retornar as dimensões do tabuleiro (número de linhas e colunas)
        return self.size_board

    def get_board(self):
        return self.board

    def set_board(self, board: List[List[str]]) -> None:
        self.board = board

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

    def set_score(self, new_score: int) -> None:
        """Define um novo valor para o score do jogo."""
        self.score = new_score

    def activate_power_mode(self):
        self.power_mode_timer = 40
        self.ghosts_are_vulnerable = True  # Fantasmas ficam vulneráveis


    def move_pacman_validation(self, direction):
        # Posição atual do Pacman
        x, y = self.pacman_position
        new_x, new_y = x, y

        # Determinar nova posição baseada na direção
        if direction == 'up':
            new_x = x - 1
        elif direction == 'down':
            new_x = x + 1
        elif direction == 'left':
            new_y = y - 1
        elif direction == 'right':
            new_y = y + 1

        # Verificar se a nova posição é válida e não é parede ou fantasma
        if self.board[new_x][new_y] not in ['-', 'G1', 'G2']:
            # Limpar a posição anterior do Pacman
            self.board[x][y] = ' '  # Sempre limpar a célula anterior

            # Atualizar a nova posição do Pacman
            self.pacman_position = (new_x, new_y)

             # Atualizar a nova posição do Pacman, considerando portais
            if new_x == 11 and new_y == 0:  # Portal à esquerda
                self.pacman_position = (11, 27)  # Teleporta para o lado direito
            elif new_x == 11 and new_y == 27:  # Portal à direita
                self.pacman_position = (11, 0)  # Teleporta para o lado esquerdo
            else:
                self.pacman_position = (new_x, new_y)

            # Verificar se Pacman comeu algo (comida ou especial)
            if self.board[new_x][new_y] == '*':
                self.score += 10
                self.food_count -= 1
                self.board[new_x][new_y] = ' '  # Remover a comida

            elif self.board[new_x][new_y] == 'o':  # Comida especial
                self.score += 10
                self.food_count -= 1
                self.activate_power_mode()
                self.board[new_x][new_y] = ' '  # Remover comida especial

    def move_ghosts_validation(self):
        for ghost_num in [1, 2]:
            ghost_pos = self.get_pos_ghost(ghost_num)
            x, y = ghost_pos

            # Movimentos possíveis (cima, baixo, esquerda, direita)
            possible_moves = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

            # Verificar se os movimentos são válidos (dentro dos limites e sem teleportes)
            valid_moves = [
                (nx, ny) for (nx, ny) in possible_moves
                if 0 <= nx < self.size_board[0] and 0 <= ny < self.size_board[1]
                and self.board[nx][ny] not in ['-', 'P', f'G{ghost_num}', f'G{3 - ghost_num}']
            ]

            if valid_moves:
                # Escolher um movimento aleatório válido
                new_pos = r.choice(valid_moves)

                # Limpar a posição anterior do fantasma
                if self.board[x][y] == f'G{ghost_num}':
                    self.board[x][y] = ' '  # Limpa a posição anterior do fantasma

                # Mover o fantasma para a nova posição, preservando a comida se houver
                self.set_pos_ghost(ghost_num, new_pos)
                self.board[new_pos[0]][new_pos[1]] = f'G{ghost_num}'

    def get_pacman_moves(self) -> List[str]:
        """
        Retorna todos os movimentos possíveis para o Pac-Man no estado atual do jogo.
        Os movimentos possíveis são ('up', 'down', 'left', 'right') se não houver paredes.
        :return: Lista de movimentos possíveis para o Pac-Man.
        """
        x, y = self.pacman_position
        board_size = self.get_size()

        possible_moves = []
        # Verificar se Pac-Man pode se mover para cima
        if x > 0 and self.board[x - 1][y] not in ['-', 'G1', 'G2']:
            possible_moves.append('up')
        # Verificar se Pac-Man pode se mover para baixo
        if x < board_size[0] - 1 and self.board[x + 1][y] not in ['-', 'G1', 'G2']:
            possible_moves.append('down')
        # Verificar se Pac-Man pode se mover para a esquerda
        if y > 0 and self.board[x][y - 1] not in ['-', 'G1', 'G2']:
            possible_moves.append('left')
        # Verificar se Pac-Man pode se mover para a direita
        if y < board_size[1] - 1 and self.board[x][y + 1] not in ['-', 'G1', 'G2']:
            possible_moves.append('right')

        return possible_moves
    
    def get_ghost_moves(self) -> List[Tuple[int, int]]:
        """
        Retorna todos os movimentos possíveis para os fantasmas no estado atual do jogo.
        Os movimentos possíveis são ('up', 'down', 'left', 'right') se não houver paredes.
        :return: Lista de movimentos possíveis para cada fantasma.
        """
        ghost_moves = []

        # Adiciona movimentos para cada fantasma
        for ghost_num in [1, 2]:
            ghost_pos = self.get_pos_ghost(ghost_num)
            x, y = ghost_pos

            # Lista de movimentos possíveis (cima, baixo, esquerda, direita)
            possible_moves = [
                (x - 1, y),  # up
                (x + 1, y),  # down
                (x, y - 1),  # left
                (x, y + 1)   # right
            ]

            # Filtrar movimentos válidos (não colidem com paredes ou pacman)
            valid_moves = [move for move in possible_moves if self.is_valid_move(move)]
            ghost_moves.extend(valid_moves)

        return ghost_moves

    def is_valid_move(self, position: Tuple[int, int]) -> bool:
        """
        Verifica se a posição é válida no tabuleiro.
        :param position: Tuple contendo as coordenadas (x, y).
        :return: True se a posição é válida, False caso contrário.
        """
        x, y = position
        return (
            0 <= x < self.size_board[0] and
            0 <= y < self.size_board[1] and
            self.board[x][y] not in ['-', 'P', 'G', 'G2']  # Não pode ser parede, pacman ou outro fantasma
        )

    def game_finished(self) -> bool:
        """
        Verifica se o estado atual do jogo é terminal.
        O jogo termina se Pac-Man for capturado por um fantasma ou se todas as comidas forem comidas.
        :return: True se o estado do jogo é terminal, False caso contrário.
        """
        # Verificar se Pac-Man foi capturado por um fantasma
        if self.get_pos_pacman() == self.get_pos_ghost(1) or self.get_pos_pacman() == self.get_pos_ghost(2):
            return True

        # Verificar se todas as comidas foram comidas
        if self.food_count == 0:
            return True

        # Caso contrário, o jogo não terminou
        return False

    def create_copy_state(self) -> 'game':
        """
        Cria uma cópia profunda do estado atual do jogo.
        :return: Nova instância da classe game com o mesmo estado.
        """
        # Criar uma nova instância da classe game com os mesmos parâmetros iniciais
        new_state = game(
            size_board=self.get_size(),
            pacman_position=self.get_pos_pacman(),
            ghost1_position=self.get_pos_ghost(1),
            ghost2_position=self.get_pos_ghost(2),
            score=self.score
        )

        # Copiar o tabuleiro
        new_board = [row[:] for row in self.get_board()]  # Cópia profunda do tabuleiro (lista de listas)
        new_state.set_board(new_board)

        return new_state



    def apply_move(self, move: str, is_pacman: bool) -> 'game':
        """
        Aplica um movimento no estado atual do jogo.
        :param move: Direção do movimento ('up', 'down', 'left', 'right').
        :param is_pacman: Booleano indicando se o movimento é do Pac-Man (True) ou dos fantasmas (False).
        :return: Novo estado do jogo após o movimento ser aplicado.
        """
        # Cria uma cópia do estado atual para evitar mudanças no estado original
        new_state = self.create_copy_state()  # Chamada corrigida para usar self.create_copy_state()

        if is_pacman:
            # Aplica movimento para o Pac-Man
            new_state.move_pacman_validation(move)
        else:
            # Aplica movimento para os fantasmas (considerando que o movimento é aleatório ou predefinido)
            new_state.move_ghosts_validation()  # Esse método deve mover todos os fantasmas

        return new_state


