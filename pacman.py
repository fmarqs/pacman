from typing import Tuple, List
import random as r
import heapq
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
        return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

    def heuristic_evaluation(self, pacman_position, ghost_positions, pill_positions, score):
        ghost_distances = [self.manhattan_distance(pacman_position, ghost) for ghost in ghost_positions]
        ghost_distance = min(ghost_distances) if ghost_distances else 0

        pill_distances = [self.manhattan_distance(pacman_position, pill) for pill in pill_positions]
        pill_distance = min(pill_distances) if pill_distances else 0

        # Ajustando penalidades e recompensas
        if ghost_distance < 5:
            ghost_penalty = 100
        else:
            ghost_penalty = 10 / ghost_distance

        # Recompensa mais alta para pílulas mais próximas
        pill_reward = 100 / pill_distance if pill_distance > 0 else 0

        return score - ghost_penalty + pill_reward

    def minimax(self, *, game_state, depth, maximizing_player, alpha, beta):
        if depth == 0 or game_state.is_terminal():
            return self.heuristic_evaluation(
                game_state.get_pos_pacman(),
                [game_state.get_pos_ghost(1), game_state.get_pos_ghost(2)],
                self.get_pill_positions(game_state.get_board()),
                game_state.score
            )

        if maximizing_player:
            max_eval = float('-inf')
            for move in game_state.get_pacman_moves():
                new_state = game_state.apply_move(move, is_pacman=True)
                eval = self.minimax(game_state=new_state, depth=depth - 1, maximizing_player=False, alpha=alpha, beta=beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in game_state.get_ghost_moves():
                new_state = game_state.apply_move(move, is_pacman=False)
                eval = self.minimax(game_state=new_state, depth=depth - 1, maximizing_player=True, alpha=alpha, beta=beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
        
    def pacman_decision(self, game_state, minimax_depth=3):
        remaining_food = game_state.get_remaining_food_positions()
        if len(remaining_food) <= 5:
            pacman_pos = game_state.get_pos_pacman()
            closest_pill = min(remaining_food, key=lambda pill: self.heuristic(pacman_pos, pill))
            path = self.a_star_search(game_state, pacman_pos, closest_pill)

            if path:
                next_pos = path[0]
                if next_pos[0] > pacman_pos[0]:
                    return 'down'
                elif next_pos[0] < pacman_pos[0]:
                    return 'up'
                elif next_pos[1] > pacman_pos[1]:
                    return 'right'
                elif next_pos[1] < pacman_pos[1]:
                    return 'left'
        
        return self.minimax(game_state, depth=minimax_depth, maximizing_player=True)

    def a_star_search(self, game_state, start, goal):
        frontier = [(0, start)]
        came_from = {start: None}
        cost_so_far = {start: 0}
        
        while frontier:
            _, current = heapq.heappop(frontier)
            
            if current == goal:
                break
            
            for next in game_state.get_neighbors(current):
                new_cost = cost_so_far[current] + 1  # Cada movimento tem custo 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(goal, next)
                    heapq.heappush(frontier, (priority, next))
                    came_from[next] = current

        # Reconstruir o caminho
        path = []
        current = goal
        while current != start:
            path.append(current)
            current = came_from[current]
        path.reverse()  # Inverter para obter o caminho da origem até o destino
        return path

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_pill_positions(self, board):
        pill_positions = []
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == '*':
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
        x, y = state.get_pos_pacman()
        board = state.get_board()
        board_size = state.get_size()
        actions = []

        if x > 0 and board[x - 1][y] != "-":
            actions.append("up")
        if x < board_size[0] - 1 and board[x + 1][y] != "-":
            actions.append("down")
        if y > 0 and board[x][y - 1] != "-":
            actions.append("left")
        if y < board_size[1] - 1 and board[x][y + 1] != "-":
            actions.append("right")

        return actions

    def moves_pacman(self, pos: Tuple[int, int], action: str, board_size: Tuple[int, int], board) -> Tuple[int, int]:
        x, y = pos
        if action == "up" and x > 0 and board[x - 1][y] != "-":
            return x - 1, y
        elif action == "down" and x < board_size[0] - 1 and board[x + 1][y] != "-":
            return x + 1, y
        elif action == "left" and y > 0 and board[x][y - 1] != "-":
            return x, y - 1
        elif action == "right" and y < board_size[1] - 1 and board[x][y + 1] != "-":
            return x, y + 1
        return pos  # Retorna a posição original se o movimento não for permitido


def create_copy_state(state) -> game:
    # Cria uma cópia do estado atual do jogo
    new_board = game()
    new_board.set_pos_pacman(state.get_pos_pacman())
    new_board.set_pos_ghost(1, state.get_pos_ghost(1))
    new_board.set_pos_ghost(2, state.get_pos_ghost(2))
    new_board.set_score(state.score)
    new_board.set_board(state.get_board())
    return new_board