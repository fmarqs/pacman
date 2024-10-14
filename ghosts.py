from typing import Tuple, Dict
import random as r
from game import game

class ghosts:
    def __init__(self) -> None:
        self.game = game()

    # 
    def moves_ghosts(
        self, pos_ghosts1: Tuple[int, int], pos_ghosts2: Tuple[int, int], pos_pacman: Tuple[int, int], board: list, board_size: Tuple[int, int], random: bool = False
    ) -> Dict[str, Tuple[int, int]]:
        # Verifica se board_size é uma tupla com dois elementos
        if not isinstance(board_size, tuple) or len(board_size) != 2:
            raise ValueError(f"Valor inválido de board_size: {board_size}. Esperado (linhas, colunas).")
        
        # Adicionando paralisação dos fantasmas quando vulneráveis
        if self.game.ghosts_are_vulnerable:
            return {"ghosts1": pos_ghosts1, "ghosts2": pos_ghosts2}, "stopped", "stopped"
        
        # instancia posição dos fantasmas
        g1 = pos_ghosts1
        g2 = pos_ghosts2
    

        if r.random() < 0.75:  # 75% chance de seguir Pac-Man, 25% chance de movimento aleatório
            new_pos_ghosts1, direction1 = self._move_towards_pacman(pos_ghosts1, pos_pacman, board, board_size)
            new_pos_ghosts2, direction2 = self._move_towards_pacman(pos_ghosts2, pos_pacman, board, board_size)
        
        else:
            random_number = r.randint(1, 4)  # Movimentos aleatórios

            # função gera um número aleatório entre 1 e 4, e com base nisso, o fantasma se move em uma das quatro direções possíveis: cima, baixo, esquerda ou direita:

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

        # verifica se os movimentos são inválidos, se o movimento for inválido, o fantasma permanece na posição original
        if self._is_invalid_move(new_pos_ghosts1, board, board_size):
            new_pos_ghosts1 = pos_ghosts1

        if self._is_invalid_move(new_pos_ghosts2, board, board_size):
            new_pos_ghosts2 = pos_ghosts2

        # retorna as novas posições dos fantasmas
        return {"ghosts1": new_pos_ghosts1, "ghosts2": new_pos_ghosts2}, direction1, direction2

    # esta função tem o objetivo de mover um fantasma em direção ao pacman
    def _move_towards_pacman(
        self, pos: Tuple[int, int], target_pos: Tuple[int, int], board: list, board_size: Tuple[int, int]
        ) -> Tuple[int, int]:
            directions = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}  # define os deslocamentos para as quatro direções possíveis

            best_move = pos                         # best_move é inicialmente a posição atual do fantasma
            shortest_distance = float("inf")        # shortest_distance é definido como infinito (float("inf")), para garantir que qualquer distância calculada seja menor que esse valor na primeira iteração

            # a função itera sobre cada direção (up, down, left, right), aplicando o deslocamento correspondente (dx, dy) à posição atual do fantasma para calcular a nova posição (new_x, new_y)
            for direction, (dx, dy) in directions.items():
                new_x, new_y = pos[0] + dx, pos[1] + dy
                # verifica se a nova posição é válida (não é parede e não é a posição atual do Pacman)
                if (
                    0 <= new_x < board_size[0] and
                    0 <= new_y < board_size[1] and
                    board[new_x][new_y] not in ["-", "P"]
                ):  
                    distance = abs(new_x - target_pos[0]) + abs(new_y - target_pos[1])      # calcula a distância de Manhattan entre a nova posição e o alvo (target_pos)
                    # Se a distância calculada para a nova posição é menor que shortest_distance (a menor distância encontrada até agora), a função atualiza best_move para essa nova posição e armazena a direção em aux
                    if distance < shortest_distance:
                        best_move = (new_x, new_y)
                        shortest_distance = distance
                        aux = direction
            # A função retorna a melhor nova posição encontrada (best_move) e a direção que o fantasma deve seguir (aux)
            return best_move, aux

    # verifica se o movimento é invalido
    def _is_invalid_move(self, pos: Tuple[int, int], board: list, board_size: Tuple[int, int]) -> bool:
        x, y = pos
        return not (0 <= x < board_size[0] and 0 <= y < board_size[1] and board[x][y] != "-")
