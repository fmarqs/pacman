from typing import Tuple, List
import random as r


class game:
    """
    for frist arg ----> refs to Y
    for secend arg ----> refs to X
    """
    def __init__(
        self,
        size_board=(6, 20),  # Aumentei o tamanho do tabuleiro para acomodar melhor os elementos
        number_of_wall=15,
        pacman_position=(1, 1),  # Ajuste a posição inicial do Pacman para dentro dos limites
        ghost1_position=(1, 16),  # Ajuste a posição inicial do Ghost 1 para dentro dos limites
        ghost2_position=(2, 16),  # Ajuste a posição inicial do Ghost 2 para dentro dos limites
        score=0,
    ) -> None:
        # Garantindo que as coordenadas estejam dentro do tamanho do tabuleiro
        if pacman_position[0] >= size_board[0] or pacman_position[1] >= size_board[1]:
            raise ValueError("A posição inicial do Pacman está fora dos limites do tabuleiro.")
        if ghost1_position[0] >= size_board[0] or ghost1_position[1] >= size_board[1]:
            raise ValueError("A posição inicial do Ghost 1 está fora dos limites do tabuleiro.")
        if ghost2_position[0] >= size_board[0] or ghost2_position[1] >= size_board[1]:
            raise ValueError("A posição inicial do Ghost 2 está fora dos limites do tabuleiro.")

        self.size_board = size_board
        self.number_of_wall = number_of_wall
        self.pacman_position = pacman_position
        self.ghost1_position = ghost1_position
        self.ghost2_position = ghost2_position
        self.score = score
        self.board = None
        self.food_count = 0  # Novo contador de comidas
        self.create_board_game()

    def get_score(self) -> int:
        return self.score

    def get_pos_pacman(self) -> Tuple:
        return self.pacman_position

    def get_pos_ghost(self, choice: int) -> Tuple:
        if choice == 1:
            return self.ghost1_position
        elif choice == 2:
            return self.ghost2_position

    def get_board(self) -> List:
        return self.board

    def set_board(self, board) -> None:
        self.board = board

    def set_pos_pacman(self, new_pos) -> None:
        self.pacman_position = new_pos

    def set_pos_ghost(self, choice: int, new_pos) -> Tuple:
        if choice == 1:
            self.ghost1_position = new_pos
        elif choice == 2:
            self.ghost2_position = new_pos

    def set_score(self, score):
        self.score = score

    def get_size(self):
        return self.size_board

    def create_board_game(self) -> None:
        # Inicializa o tabuleiro com paredes ao redor e comidas em todos os espaços livres
        self.board = [["-" if i == 0 or i == self.size_board[0] - 1 or j == 0 or j == self.size_board[1] - 1
                       else "*" for j in range(self.size_board[1])] for i in range(self.size_board[0])]

        # Adiciona paredes internas
        counter = 1
        while counter <= self.number_of_wall:
            i, j = r.randint(1, self.size_board[0] - 2), r.randint(1, self.size_board[1] - 2)
            if (
                (i, j) == self.pacman_position
                or (i, j) == self.ghost1_position
                or (i, j) == self.ghost2_position
                or self.board[i][j] == "-"
            ):
                continue

            self.board[i][j] = "-"
            counter += 1

        # Remove comida das posições de Pacman e Fantasmas
        if self.pacman_position[0] < self.size_board[0] and self.pacman_position[1] < self.size_board[1]:
            self.board[self.pacman_position[0]][self.pacman_position[1]] = " "

        if self.ghost1_position[0] < self.size_board[0] and self.ghost1_position[1] < self.size_board[1]:
            self.board[self.ghost1_position[0]][self.ghost1_position[1]] = " "

        if self.ghost2_position[0] < self.size_board[0] and self.ghost2_position[1] < self.size_board[1]:
            self.board[self.ghost2_position[0]][self.ghost2_position[1]] = " "

        # Conta a quantidade inicial de comida
        self.food_count = sum(row.count(".") for row in self.board)

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

    def check_victory(self) -> bool:
        # Verifica se todas as comidas foram consumidas
        return self.food_count == 0

    def eat_food(self):
        # Verifica se o Pacman comeu uma comida
        if self.board[self.pacman_position[0]][self.pacman_position[1]] == "*":
            self.board[self.pacman_position[0]][self.pacman_position[1]] = " "
            self.food_count -= 1
            self.score += 10
