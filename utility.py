from game import game

class utility:
    def __init__(self) -> None:
        self.previous_states = []  # Lista para armazenar os últimos N estados
        self.max_history = 10  # Número máximo de estados armazenados
        self.repeated_state_penalty = 200  # Penalidade para estados repetidos


    def get_utility(self, state):
        import random

        if self.is_pacman_win(state):
            return 1000 + state.score

        if state.get_pos_pacman() == state.get_pos_ghost(1) or state.get_pos_pacman() == state.get_pos_ghost(2):
            return state.score - 1000

        distance_to_nearest_food = self.distance_from_near_food(state)
        distance_to_nearest_ghost = min(
            self._euclidean_distance(state.get_pos_pacman(), state.get_pos_ghost(1)),
            self._euclidean_distance(state.get_pos_pacman(), state.get_pos_ghost(2))
        )

        remaining_food = len([food for row in state.get_board() for food in row if food == "*"])

        utility_value = (
            state.score
            + remaining_food * 100  
            - distance_to_nearest_food * 50  
            + distance_to_nearest_ghost * 10  
        )

        if self.is_repeated_state(state):
            utility_value -= self.repeated_state_penalty  # Penalidade mais forte para estados repetidos

        utility_value += random.uniform(-10, 10)  # Adiciona um leve fator de aleatoriedade
        return utility_value

    def is_repeated_state(self, state):
        for previous_state in self.previous_states:
            if self.compare_states(state, previous_state):
                return True
        return False

    def update_previous_state(self, state):
        self.previous_states.append(self.copy_state(state))
        if len(self.previous_states) > self.max_history:
            self.previous_states.pop(0)

    def compare_states(self, state1, state2):
        return (
            state1.get_pos_pacman() == state2.get_pos_pacman() and
            state1.get_pos_ghost(1) == state2.get_pos_ghost(1) and
            state1.get_pos_ghost(2) == state2.get_pos_ghost(2) and
            state1.get_board() == state2.get_board()
        )

    def copy_state(self, state):
        new_state = game()
        new_state.set_pos_pacman(state.get_pos_pacman())
        new_state.set_pos_ghost(1, state.get_pos_ghost(1))
        new_state.set_pos_ghost(2, state.get_pos_ghost(2))
        new_state.set_score(state.score)
        new_state.set_board(state.get_board())
        return new_state

    def is_game_finished(self, state):
        return (
            self.is_pacman_win(state)
            or state.get_pos_pacman() == state.get_pos_ghost(1)
            or state.get_pos_pacman() == state.get_pos_ghost(2)
        )

    def is_pacman_win(self, state):
        for row in state.get_board():
            if "*" in row:
                return False
        return True

    def distance_from_near_food(self, state):
        board = state.get_board()
        pos_pacman = state.get_pos_pacman()
        food_positions = [
            (i, j)
            for i in range(len(board))
            for j in range(len(board[0]))
            if board[i][j] == "*"
        ]
        if not food_positions:
            return 0
        distances = [self._euclidean_distance(pos_pacman, food) for food in food_positions]
        return min(distances)

    def _euclidean_distance(self, point1, point2):
        import math
        return math.sqrt(pow(point1[0] - point2[0], 2) + pow(point1[1] - point2[1], 2))