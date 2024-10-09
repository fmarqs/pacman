from typing import Tuple, List
import random as r


class pacman:
    def __init__(self):
        pass

    def best_action(self, game) -> str:
        # Escolha a melhor ação com base no estado atual do jogo
        pos_pacman = game.get_pos_pacman()
        board = game.get_board()
        valid_actions = self.valid_actions(pos_pacman, board, game.get_size())
        return r.choice(valid_actions)  # Escolhe uma ação aleatória entre as válidas

    def moves_pacman(
        self, pos: Tuple[int, int], action: str, board_size: Tuple[int, int], board: List[List[str]]
    ) -> Tuple[int, int]:
        directions = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}
        dx, dy = directions.get(action, (0, 0))
        new_x, new_y = pos[0] + dx, pos[1] + dy

        if 0 <= new_x < board_size[0] and 0 <= new_y < board_size[1] and board[new_x][new_y] != "-":
            return new_x, new_y  # Retorna a nova posição se não for uma parede
        return pos  # Caso contrário, mantém a posição atual

    def valid_actions(self, pos: Tuple[int, int], board: List[List[str]], board_size: Tuple[int, int]) -> List[str]:
        directions = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}
        valid = []
        for action, (dx, dy) in directions.items():
            new_x, new_y = pos[0] + dx, pos[1] + dy
            if 0 <= new_x < board_size[0] and 0 <= new_y < board_size[1] and board[new_x][new_y] != "-":
                valid.append(action)
        return valid
