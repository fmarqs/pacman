from typing import Tuple, Dict
import random as r
from game import game

class ghosts:
    def __init__(self) -> None:
        self.game = game()

    def move_ghosts(
        self, pos_ghosts1: Tuple[int, int], pos_ghosts2: Tuple[int, int], pos_pacman: Tuple[int, int], board: list, board_size: Tuple[int, int], random: bool = False
    ) -> Dict[str, Tuple[int, int]]:
        # Verificar se board_size é uma tupla com dois elementos
        if not isinstance(board_size, tuple) or len(board_size) != 2:
            raise ValueError(f"Valor inválido de board_size: {board_size}. Esperado (linhas, colunas).")
        
        # Adicionando paralisação dos fantasmas quando vulneráveis
        print('fantasmas estao vulneraveis?', self.game.ghosts_are_vulnerable)
        if self.game.ghosts_are_vulnerable:
            print('Fantasmas estão paralisados!')
            return {"ghosts1": pos_ghosts1, "ghosts2": pos_ghosts2}, "stopped", "stopped"
        
        
        g1 = pos_ghosts1
        g2 = pos_ghosts2
    

        if r.random() < 0.65:  # 50% chance de seguir Pac-Man, 50% chance de movimento aleatório
            new_pos_ghosts1, direction1 = self._move_towards_target(pos_ghosts1, pos_pacman, board, board_size)
            new_pos_ghosts2, direction2 = self._move_towards_target(pos_ghosts2, pos_pacman, board, board_size)
        
        else:
            random_number = r.randint(1, 4)  # Movimentos aleatórios

            if random_number == 1:
                new_pos_ghosts1 = (g1[0]+1), g1[1]
                new_pos_ghosts2 = (g2[0]-1), g2[1]
                direction1 = 'left'
                direction2 = 'right'

            if random_number == 2:
                new_pos_ghosts1 = g1[0], (g1[1]-1)
                new_pos_ghosts2 = g2[0], (g2[1]+1)
                direction1 = 'up'
                direction2 = 'down'
            
            if random_number == 3:
                new_pos_ghosts1 = (g1[0]-1), g1[1]
                new_pos_ghosts2 = (g2[0]+1), g2[1]
                direction1 = 'right'
                direction2 = 'left'
            
            if random_number == 4:
                new_pos_ghosts1 = g1[0], (g1[1]+1)
                new_pos_ghosts2 = g2[0], (g2[1]-1)
                direction1 = 'down'
                direction2 = 'up'



        if self._is_invalid_move(new_pos_ghosts1, board, board_size):
            new_pos_ghosts1 = pos_ghosts1

        if self._is_invalid_move(new_pos_ghosts2, board, board_size):
            new_pos_ghosts2 = pos_ghosts2

        return {"ghosts1": new_pos_ghosts1, "ghosts2": new_pos_ghosts2}, direction1, direction2

    def _move_towards_target(
        self, pos: Tuple[int, int], target_pos: Tuple[int, int], board: list, board_size: Tuple[int, int]
        ) -> Tuple[int, int]:
            directions = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}

            best_move = pos
            shortest_distance = float("inf")

            for direction, (dx, dy) in directions.items():
                new_x, new_y = pos[0] + dx, pos[1] + dy
                # Verificar se a nova posição é válida (não é parede e não é a posição atual do Pacman)
                if (
                    0 <= new_x < board_size[0] and
                    0 <= new_y < board_size[1] and
                    board[new_x][new_y] not in ["-", "P"]
                ):
                    distance = abs(new_x - target_pos[0]) + abs(new_y - target_pos[1])
                    if distance < shortest_distance:
                        best_move = (new_x, new_y)
                        shortest_distance = distance
                        aux = direction

            return best_move, aux


    def _is_invalid_move(self, pos: Tuple[int, int], board: list, board_size: Tuple[int, int]) -> bool:
        x, y = pos
        return not (0 <= x < board_size[0] and 0 <= y < board_size[1] and board[x][y] != "-")
