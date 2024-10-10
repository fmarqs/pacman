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

    def best_action(self, state):
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
            # Se todas as ações levam a movimentos repetidos, faça um movimento qualquer
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

        # Se a melhor ação for um movimento repetido, escolha aleatoriamente
        if len(best_actions) > 1:
            best_action = r.choice(best_actions)
        else:
            best_action = best_actions[0]

        # Atualiza a lista de posições anteriores com a nova posição do Pac-Man
        new_position = self.moves_pacman(state.get_pos_pacman(), best_action, state.get_size(), state.get_board())
        self.update_previous_positions(new_position)

        print(f"Ação escolhida pelo pacman: {best_action}")
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
        ghost_distance = min(ghost_distances) if ghost_distances else 0

        # Calcula a distância de Manhattan entre Pac-Man e a pílula mais próxima
        pill_distances = [self.manhattan_distance(pacman_position, pill) for pill in pill_positions]
        pill_distance = min(pill_distances) if pill_distances else 0

        # Penalidades e recompensas com pesos ajustáveis
        ghost_penalty = 10 if ghost_distance > 0 else 0
        pill_reward = 5 if pill_distance > 0 else 0

        return score - (ghost_penalty / ghost_distance if ghost_distance > 0 else 0) + (pill_reward / pill_distance if pill_distance > 0 else 0)

    def minimax(self, *, game_state, depth, maximizing_player, alpha, beta):
        """
        Implementa o algoritmo Minimax com poda alfa-beta.
        :param game_state: Estado atual do jogo (objeto da classe game).
        :param depth: Profundidade atual de busca.
        :param maximizing_player: Booleano indicando se é a vez do Pac-Man (maximizing player) ou dos fantasmas (minimizing player).
        :param alpha: Valor alfa para poda.
        :param beta: Valor beta para poda.
        :return: Valor heurístico do melhor movimento.
        """
        # Verifica se a profundidade máxima foi atingida ou se o jogo terminou
        if depth == 0 or game_state.is_terminal():
            return self.heuristic_evaluation(
                pacman_position=game_state.get_pos_pacman(),
                ghost_positions=[game_state.get_pos_ghost(1), game_state.get_pos_ghost(2)],
                pill_positions=self.get_pill_positions(game_state.get_board()),
                score=game_state.score
            )

        if maximizing_player:  # Turno do Pac-Man
            max_eval = float('-inf')
            for move in game_state.get_pacman_moves():
                # Cria um novo estado ao aplicar o movimento do Pac-Man
                new_state = game_state.apply_move(move, is_pacman=True)
                # Avalia o estado com profundidade reduzida e passa a vez para os fantasmas
                eval = self.minimax(game_state=new_state, depth=depth - 1, maximizing_player=False, alpha=alpha, beta=beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                # Poda se possível
                if beta <= alpha:
                    break
            return max_eval
        else:  # Turno dos Fantasmas
            min_eval = float('inf')
            # Obter movimentos possíveis dos fantasmas
            ghost_moves = game_state.get_ghost_moves()
            if not ghost_moves:
                # Se não há movimentos válidos para os fantasmas, retorna a avaliação atual
                return self.heuristic_evaluation(
                    pacman_position=game_state.get_pos_pacman(),
                    ghost_positions=[game_state.get_pos_ghost(1), game_state.get_pos_ghost(2)],
                    pill_positions=self.get_pill_positions(game_state.get_board()),
                    score=game_state.score
                )
            
            for move in ghost_moves:
                # Cria um novo estado ao aplicar o movimento dos fantasmas
                new_state = game_state.apply_move(move, is_pacman=False)
                # Avalia o estado com profundidade reduzida e passa a vez para o Pac-Man
                eval = self.minimax(game_state=new_state, depth=depth - 1, maximizing_player=True, alpha=alpha, beta=beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                # Poda se possível
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
