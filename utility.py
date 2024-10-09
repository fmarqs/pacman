class utility:
    def __init__(self) -> None:
        pass

    def get_utility(self, state):
      # Prioridade alta para vencer o jogo
      if self.is_pacman_win(state):
          return 1000 + state.score

      # Prioridade baixa para perder o jogo
      if state.get_pos_pacman() == state.get_pos_ghost(1) or state.get_pos_pacman() == state.get_pos_ghost(2):
          return state.score - 1000

      # Calcular a distância para o alimento mais próximo
      distance_to_nearest_food = self.distance_from_near_food(state)

      # Calcular a distância para o fantasma mais próximo (para evitar)
      distance_to_nearest_ghost = min(
          self._euclidean_distance(state.get_pos_pacman(), state.get_pos_ghost(1)),
          self._euclidean_distance(state.get_pos_pacman(), state.get_pos_ghost(2))
      )

      # Calcular a quantidade de alimentos restantes
      remaining_food = len([food for row in state.get_board() for food in row if food == "*"])

      # Ajustar a utilidade baseada em estar perto do alimento e longe dos fantasmas
      return (
          state.score
          + remaining_food * 100  # Recompensa por alimentos restantes
          - distance_to_nearest_food * 50  # Penalidade por estar longe do alimento
          + distance_to_nearest_ghost * 10  # Recompensa por manter distância dos fantasmas
      )

    

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

      if not food_positions:  # Se não há alimentos restantes
          return 0

      distances = [self._euclidean_distance(pos_pacman, food) for food in food_positions]
      return min(distances)  # Retorna a menor distância até um alimento

    def _euclidean_distance(self, point1, point2):
      import math
      return math.sqrt(pow(point1[0] - point2[0], 2) + pow(point1[1] - point2[1], 2))
