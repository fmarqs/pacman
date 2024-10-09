import random as r
from typing import Tuple, List


class game:
    def __init__(self, size_board=(10, 18), pacman_position=(1, 1), ghost1_position=(1, 16), ghost2_position=(3, 15), score=0):
        self.size_board = size_board
        self.pacman_position = pacman_position
        self.ghost1_position = ghost1_position
        self.ghost2_position = ghost2_position
        self.score = score
        self.board = None
        self.food_count = 0  # Contagem de comidas no tabuleiro
        self.create_board_game()

    def create_board_game(self):
        # Layout fixo para o labirinto com '*' para pontos de comida
        fixed_layout = [
            ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', ' ', '*', '*', '-', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', ' ', '*', '-'],
            ['-', '*', '-', '*', '*', '*', '*', '-', '*', '-', '*', '-', '*', '*', '*', '*', '*', '-'],
            ['-', '*', '-', '*', '-', '-', '*', '-', '*', '-', '*', '*', '-', '-', '*', ' ', '*', '-'],
            ['-', '*', '*', '*', '-', '*', '*', '*', '*', '*', '-', '-', '*', '*', '*', '*', '*', '-'],
            ['-', '*', '-', '-', '*', '*', '-', '-', '-', '*', '*', '-', '*', '*', '-', '-', '*', '-'],
            ['-', '*', '*', '*', '*', '-', '*', '*', '*', '-', '*', '*', '*', '-', '*', '*', '*', '-'],
            ['-', '-', '*', '-', '-', '*', '*', '*', '*', '*', '*', '-', '-', '*', '-', '*', '-', '-'],
            ['-', '*', '*', '*', '*', '*', '*', '-', '-', '*', '*', '*', '*', '*', '*', '*', '*', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-']
        ]

        # Contar o número de comidas no layout fixo
        self.food_count = sum(row.count('*') for row in fixed_layout)

        # Definir o tabuleiro com base no layout fixo
        self.board = fixed_layout

    def get_size(self) -> Tuple[int, int]:
        # Retornar as dimensões do tabuleiro (número de linhas e colunas)
        return self.size_board

    def display(self) -> None:
        for x in range(self.size_board[0]):
            for y in range(self.size_board[1]):
                if (x, y) == self.pacman_position:
                    print("P", end=" ")
                elif (x, y) == self.ghost1_position:
                    print("G1", end=" ")
                elif (x, y) == self.ghost2_position:
                    print("G2", end=" ")
                else:
                    print(self.board[x][y], end=" ")
            print()
        print(f"                                                Score: {self.score}")

    def get_board(self):
        return self.board

    def set_board(self, board: List[List[str]]) -> None:
        self.board = board

    def get_pos_pacman(self) -> Tuple[int, int]:
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

    def move_pacman(self, direction):
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
            self.board[x][y] = ' ' if self.board[x][y] != '*' else '*'  # Deixar a comida no local se houver
            # Atualizar a nova posição do Pacman
            self.pacman_position = (new_x, new_y)
            # Comer comida se existir
            if self.board[new_x][new_y] == '*':
                self.score += 10
                self.food_count -= 1
            # Atualizar o tabuleiro
            self.board[new_x][new_y] = 'P'

    def move_ghosts(self):
        # Movimentação aleatória para os fantasmas
        for ghost_num in [1, 2]:
            ghost_pos = self.get_pos_ghost(ghost_num)
            x, y = ghost_pos

            # Movimentos possíveis (cima, baixo, esquerda, direita)
            possible_moves = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
            valid_moves = [(nx, ny) for (nx, ny) in possible_moves if self.board[nx][ny] not in ['-', 'P', 'G1', 'G2']]

            if valid_moves:
                # Escolher um movimento aleatório válido
                new_pos = r.choice(valid_moves)
                # Atualizar a posição do fantasma no tabuleiro
                self.board[x][y] = '*' if self.board[x][y] == '*' else ' '  # Restaurar comida se existir
                self.set_pos_ghost(ghost_num, new_pos)
                self.board[new_pos[0]][new_pos[1]] = f'G{ghost_num}'

    def start_game(self):
        # Simular movimentos para testes
        self.display()
        for _ in range(5):  # Movimentar 5 vezes para testar
            self.move_pacman('right')
            self.move_ghosts()
            self.display()  # Atualizar e exibir o tabuleiro a cada movimento

    def is_game_over(self) -> bool:
        # Verificar se Pacman está na mesma posição que algum dos fantasmas
        if self.pacman_position == self.ghost1_position or self.pacman_position == self.ghost2_position:
            return True
        # Verificar se não há mais comida no tabuleiro
        if self.food_count <= 0:
            return True
        return False

# Inicializar o jogo e iniciar a simulação
game_instance = game()
game_instance.start_game()
