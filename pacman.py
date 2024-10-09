from typing import Tuple, List
import random as r


class pacman:
    def __init__(self, depth: int = 2):
        self.depth = depth  # Profundidade da árvore de min-max

    def best_action(self, game) -> str:
        # Escolher a melhor ação com o algoritmo min-max
        pos_pacman = game.get_pos_pacman()
        board = game.get_board()
        valid_actions = self.valid_actions(pos_pacman, board, game.get_size())
        
        # Aplicar min-max para encontrar a melhor ação
        best_move, _ = self.min_max(game, self.depth, True)
        return best_move

    def min_max(self, game, depth: int, is_pacman_turn: bool) -> Tuple[str, int]:
        if depth == 0 or game.is_game_over():
            return None, self.evaluate(game)

        if is_pacman_turn:
            # Pacman maximiza o score
            max_eval = float('-inf')
            best_action = None
            pos_pacman = game.get_pos_pacman()
            valid_actions = self.valid_actions(pos_pacman, game.get_board(), game.get_size())

            for action in valid_actions:
                new_pos_pacman = self.moves_pacman(pos_pacman, action, game.get_size(), game.get_board())
                game.set_pos_pacman(new_pos_pacman)  # Simular movimento
                _, eval = self.min_max(game, depth - 1, False)
                game.set_pos_pacman(pos_pacman)  # Reverter movimento

                if eval > max_eval:
                    max_eval = eval
                    best_action = action

            return best_action, max_eval
        else:
            # Fantasmas minimizam o score
            min_eval = float('inf')
            pos_g1 = game.get_pos_ghost(1)
            pos_g2 = game.get_pos_ghost(2)
            possible_moves_g1 = self.valid_actions(pos_g1, game.get_board(), game.get_size())
            possible_moves_g2 = self.valid_actions(pos_g2, game.get_board(), game.get_size())

            for g1_move in possible_moves_g1:
                new_pos_g1 = self.moves_pacman(pos_g1, g1_move, game.get_size(), game.get_board())
                game.set_pos_ghost(1, new_pos_g1)  # Simular movimento de G1

                for g2_move in possible_moves_g2:
                    new_pos_g2 = self.moves_pacman(pos_g2, g2_move, game.get_size(), game.get_board())
                    game.set_pos_ghost(2, new_pos_g2)  # Simular movimento de G2
                    _, eval = self.min_max(game, depth - 1, True)

                    # Reverter movimentos dos fantasmas
                    game.set_pos_ghost(1, pos_g1)
                    game.set_pos_ghost(2, pos_g2)

                    if eval < min_eval:
                        min_eval = eval

            return None, min_eval

    def evaluate(self, game) -> int:
        # Função de avaliação: valoriza a proximidade da comida e penaliza a proximidade dos fantasmas
        pos_pacman = game.get_pos_pacman()
        pos_g1 = game.get_pos_ghost(1)
        pos_g2 = game.get_pos_ghost(2)

        dist_g1 = abs(pos_pacman[0] - pos_g1[0]) + abs(pos_pacman[1] - pos_g1[1])
        dist_g2 = abs(pos_pacman[0] - pos_g2[0]) + abs(pos_pacman[1] - pos_g2[1])

        # Valoriza estar longe dos fantasmas
        score = dist_g1 + dist_g2

        # Valoriza comer comida (se Pacman estiver em uma célula de comida)
        if game.get_board()[pos_pacman[0]][pos_pacman[1]] == '*':
            score += 50

        return score

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
