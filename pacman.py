from typing import Tuple, List
import random as r
from utility import utility
from game import game
from ghosts import ghosts


class pacman:
    def __init__(self):
        self._ways_possible_for_ghosts = ["up", "down", "left", "right"]
        self.utility = utility()
        self.previous_positions = []  # Lista para armazenar as posições anteriores do Pac-Man
    
    def update_previous_positions(self, position):
        if len(self.previous_positions) > 10:  # Limite para o histórico de posições
            self.previous_positions.pop(0)  # Remove a posição mais antiga
        self.previous_positions.append(position)

    def is_repeated_move(self, new_position):
        # Verifica se a nova posição já está nas últimas 10 posições anteriores
        return new_position in self.previous_positions

    def _find_nearest_food_direction(self, state, pacman_pos):
        """
        Encontra a direção da comida mais próxima se estiver ao redor de Pacman.
        :param state: O estado atual do jogo.
        :param pacman_pos: A posição atual do Pacman.
        :return: Direção para se mover em direção à comida ou None.
        """
        x, y = pacman_pos
        board = state.get_board()
        directions = {
            "up": (x - 1, y),
            "down": (x + 1, y),
            "left": (x, y - 1),
            "right": (x, y + 1)
        }

        # Verificar cada direção ao redor de Pacman para encontrar comida
        for direction, (new_x, new_y) in directions.items():
            if 0 <= new_x < len(board) and 0 <= new_y < len(board[0]):
                if board[new_x][new_y] == '*':
                    return direction

        return None

    def best_action(self, state):
        pacman_pos = state.get_pos_pacman()
        ghost_positions = [state.get_pos_ghost(1), state.get_pos_ghost(2)]

        # Se há um fantasma por perto, tenta escapar
        if self.is_ghost_nearby(pacman_pos, ghost_positions):
            return self.best_escape_action(state, pacman_pos, ghost_positions)

        # Verifica se Pacman está perto de comida e prioriza comer
        nearest_food_direction = self._find_nearest_food_direction(state, pacman_pos)
        if nearest_food_direction:
            return nearest_food_direction


        # Caso contrário, usa o Minimax para determinar a melhor ação
        actions_values = [
            (
                action,
                self.minimax(
                    game_state=self.transfer(create_copy_state(state), action, True),
                    depth=5,
                    maximizing_player=False,
                    alpha=float('-inf'),
                    beta=float('inf')
                ),
            )
            for action in self._ways_possible_for_pacman(state)
        ]

        # Filtra as ações que não levam a um movimento repetido
        actions_values = [(action, value) for action, value in actions_values if not self.is_repeated_move(self.moves_pacman(state.get_pos_pacman(), action, state.get_size(), state.get_board()))]

        if not actions_values:
            # Se todas as ações levam a movimentos repetidos, faz um movimento qualquer
            actions_values = [
                (
                    action,
                    self.minimax(
                        game_state=self.transfer(create_copy_state(state), action, True),
                        depth=5,
                        maximizing_player=False,
                        alpha=float('-inf'),
                        beta=float('inf')
                    ),
                )
                for action in self._ways_possible_for_pacman(state)
            ]

        max_value = max(actions_values, key=lambda temp: temp[1])[1]
        best_actions = [action for action, value in actions_values if value == max_value]

        # Se a melhor ação for um movimento repetido, escolhe aleatoriamente
        best_action = r.choice(best_actions) if len(best_actions) > 1 else best_actions[0]

        # Atualiza a lista de posições anteriores com a nova posição do Pacman
        new_position = self.moves_pacman(state.get_pos_pacman(), best_action, state.get_size(), state.get_board())
        self.update_previous_positions(new_position)

        return best_action

    def manhattan_distance(self, point1, point2):
        """
        Calcula a distância de Manhattan entre dois pontos.
        :param point1: Tuple com as coordenadas (x, y) do primeiro ponto.
        :param point2: Tuple com as coordenadas (x, y) do segundo ponto.
        :return: Distância de Manhattan entre os dois pontos.
        """
        return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

    def heuristic_evaluation(self, pacman_position, ghost_positions, pill_positions, score):
        """
        Avalia o estado atual do jogo com base na posição do Pac-Man, posições dos fantasmas e posição das pílulas.
        :param pacman_position: Posição atual do Pac-Man.
        :param ghost_positions: Lista com as posições dos fantasmas.
        :param pill_positions: Lista com as posições das pílulas restantes.
        :param score: Pontuação atual do jogo.
        :return: Valor heurístico para o estado atual.
        """
        # Calcula a distância de Manhattan entre Pac-Man e os fantasmas mais próximos
        ghost_distances = [self.manhattan_distance(pacman_position, ghost) for ghost in ghost_positions]
        ghost_distance = min(ghost_distances) if ghost_distances else float('inf')

        # Calcula a distância de Manhattan entre Pac-Man e a pílula mais próxima
        pill_distances = [self.manhattan_distance(pacman_position, pill) for pill in pill_positions]
        pill_distance = min(pill_distances) if pill_distances else float('inf')

        # Penalidade maior quando Pac-Man está perto dos fantasmas
        ghost_penalty = 0
        if ghost_distance <= 1:
            ghost_penalty = -100000  # Fuga imediata se estiver a 1 bloco
        elif ghost_distance <= 2:
            ghost_penalty = -50000   # Penalidade severa se estiver a 2 blocos
        elif ghost_distance <= 3:
            ghost_penalty = -20000   # Penalidade moderada se estiver a 3 blocos

        # Recompensa pela proximidade da comida
        pill_reward = 50 / pill_distance if pill_distance > 0 else 0

        # O valor heurístico é influenciado pela distância dos fantasmas e das pílulas
        return score + pill_reward + ghost_penalty

    def is_ghost_nearby(self, pacman_pos, ghost_positions, threshold=2):
        """
        Checks if any ghost is within a certain distance from Pacman.
        :param pacman_pos: Tuple of Pacman's position (x, y).
        :param ghost_positions: List of ghost positions [(x1, y1), (x2, y2)].
        :param threshold: The minimum distance to consider a ghost as nearby.
        :return: True if any ghost is within the threshold, otherwise False.
        """
        for ghost_pos in ghost_positions:
            if self.manhattan_distance(pacman_pos, ghost_pos) <= threshold:
                return True
        return False

    def best_escape_action(self, state, pacman_pos, ghost_positions):
        """
        Determines the best escape action for Pacman when a ghost is nearby.
        :param state: Current game state.
        :param pacman_pos: Current position of Pacman.
        :param ghost_positions: List of ghost positions [(x1, y1), (x2, y2)].
        :return: Direction that moves Pacman farther from the closest ghost.
        """
        best_move = None
        max_distance_from_ghost = -float('inf')

        for action in self._ways_possible_for_pacman(state):
            new_pos = self.moves_pacman(pacman_pos, action, state.get_size(), state.get_board())
            # Check the distance to the nearest ghost after the move
            min_ghost_distance = min([self.manhattan_distance(new_pos, ghost) for ghost in ghost_positions])
            if min_ghost_distance > max_distance_from_ghost:
                best_move = action
                max_distance_from_ghost = min_ghost_distance

        return best_move


    def _valid_moves_from(self, position: Tuple[int, int], board: List[List[str]]) -> List[str]:
        """
        Determines all valid moves Pacman can make from a given position.
        :param position: Tuple with Pacman's current position (x, y).
        :param board: The current state of the game board.
        :return: List of valid directions ('up', 'down', 'left', 'right').
        """
        x, y = position
        board_size = len(board), len(board[0])  # Size of the board
        moves = []

        directions = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}

        for direction, (dx, dy) in directions.items():
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < board_size[0] and 0 <= new_y < board_size[1]:
                if board[new_x][new_y] not in ["-", "G1", "G2"]:  # Valid if not a wall or ghost
                    moves.append(direction)

        return moves

    def minimax(self, game_state, depth, maximizing_player, alpha, beta):
        """
        Implementa o algoritmo Minimax com poda alfa-beta.
        :param game_state: Estado atual do jogo (objeto da classe game).
        :param depth: Profundidade atual de busca.
        :param maximizing_player: Booleano indicando se é a vez do Pac-Man (maximizing player) ou dos fantasmas (minimizing player).
        :param alpha: Valor alfa para poda.
        :param beta: Valor beta para poda.
        :return: Valor heurístico do melhor movimento.
        """
        if depth == 0 or game_state.is_terminal():
            # Ajuste aqui: passa apenas os 5 argumentos corretos
            return self.heuristic_evaluation(
                game_state.get_pos_pacman(),
                [game_state.get_pos_ghost(1), game_state.get_pos_ghost(2)],
                self.get_pill_positions(game_state.get_board()),
                game_state.score
            )

        if maximizing_player:  # Pac-Man's turn
            max_eval = float('-inf')
            for move in game_state.get_pacman_moves():
                new_state = game_state.apply_move(move, is_pacman=True)
                eval = self.minimax(game_state=new_state, depth=depth - 1, maximizing_player=False, alpha=alpha, beta=beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:  # Ghosts' turn
            min_eval = float('inf')
            for move in game_state.get_ghost_moves():
                new_state = game_state.apply_move(move, is_pacman=False)
                eval = self.minimax(game_state=new_state, depth=depth - 1, maximizing_player=True, alpha=alpha, beta=beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def get_pill_positions(self, board):
        """
        Encontra todas as posições das pílulas no tabuleiro.
        :param board: Representação do tabuleiro.
        :return: Lista com as coordenadas das pílulas.
        """
        pill_positions = []
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == '*':  # Identificar as pílulas
                    pill_positions.append((i, j))
        return pill_positions

    def transfer(self, state, action, is_pacman):
        if is_pacman:
            new_state = create_copy_state(state)
            xp, yp = state.get_pos_pacman()
            board = state.get_board()
            board_size = state.get_size()

            new_pos_pacman = self.moves_pacman((xp, yp), action, board_size, board)
            new_state.set_pos_pacman(new_pos_pacman)
            return new_state

        else:
            G = ghosts()
            new_state = create_copy_state(state)
            pos_g1 = state.get_pos_ghost(1)
            pos_g2 = state.get_pos_ghost(2)
            board = state.get_board()
            board_size = state.get_size()

            new_pos_ghosts = G.move_ghosts(pos_g1, pos_g2, state.get_pos_pacman(), board, board_size)

            new_state.set_pos_ghost(1, new_pos_ghosts["ghosts1"])
            new_state.set_pos_ghost(2, new_pos_ghosts["ghosts2"])

            return new_state

    def _ways_possible_for_pacman(self, state) -> List[str]:
        # Determina as ações possíveis para o Pacman no estado atual do jogo
        x, y = state.get_pos_pacman()
        board = state.get_board()
        board_size = state.get_size()

        actions = []

        # Verifica se cada direção está livre e não é uma parede
        if x > 0 and board[x - 1][y] != "-" and board[x - 1][y] not in ['G', 'F']:
            actions.append("up")
        if x < board_size[0] - 1 and board[x + 1][y] != "-" and board[x + 1][y] not in ['G', 'F']:
            actions.append("down")
        if y > 0 and board[x][y - 1] != "-" and board[x][y - 1] not in ['G', 'F']:
            actions.append("left")
        if y < board_size[1] - 1 and board[x][y + 1] != "-" and board[x][y + 1] not in ['G', 'F']:
            actions.append("right")

        return actions

    def moves_pacman(self, pacman_pos: Tuple[int, int], way_posibale: str, board_size: Tuple[int, int], board: List[List[str]]) -> Tuple[int, int]:
        # Move o Pacman para uma nova posição com base na direção fornecida
        x, y = pacman_pos
        ways = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}
        dx, dy = ways[way_posibale]
        new_x, new_y = x + dx, y + dy

        if 0 <= new_x < board_size[0] and 0 <= new_y < board_size[1] and board[new_x][new_y] != "-":
            return (new_x, new_y)
        return pacman_pos


def create_copy_state(state) -> game:
    # Cria uma cópia do estado atual do jogo
    new_board = game()
    new_board.set_pos_pacman(state.get_pos_pacman())
    new_board.set_pos_ghost(1, state.get_pos_ghost(1))
    new_board.set_pos_ghost(2, state.get_pos_ghost(2))
    new_board.set_score(state.score)
    new_board.set_board(state.get_board())
    return new_board