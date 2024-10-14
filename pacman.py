from typing import Tuple, List
import random as r
from game import game
from ghosts import ghosts


class pacman:
    def __init__(self):
        self._ways_possible_for_ghosts = ["up", "down", "left", "right"]
        self.previous_positions = []  # lista para armazenar as posições anteriores do pacman
    
    # função que atualiza as posições anteriores
    def update_previous_positions(self, position):
        if len(self.previous_positions) > 15:  # limite para o histórico de posições
            self.previous_positions.pop(0)  # remove a posição mais antiga
        self.previous_positions.append(position)

    # verifica se o movimento é repetido
    def is_repeated_move(self, new_position):
        # verifica se a nova posição já está nas últimas 15 posições anteriores
        return new_position in self.previous_positions

    # encontra a direção da comida mais próxima se estiver ao redor do pacman
    def _find_nearest_food_direction(self, state, pacman_pos):

        x, y = pacman_pos               # posicao atual do pacman
        board = state.get_board()
        directions = {
            "up": (x - 1, y),
            "down": (x + 1, y),
            "left": (x, y - 1),
            "right": (x, y + 1)
        }

        # verificar cada direção ao redor de pacman para encontrar comida, essa função foi aplicada porque o pacman estava ignorando ao passar ao redor das comidas
        for direction, (new_x, new_y) in directions.items():
            if 0 <= new_x < len(board) and 0 <= new_y < len(board[0]):
                if board[new_x][new_y] == '*':
                    return direction

        return None

    # função para retornar o melhor movimento possivel 
    def best_action(self, state):
        pacman_pos = state.get_pos_pacman()                                                  # pega a posição do pacman
        ghost_positions = [state.get_pos_ghost(1), state.get_pos_ghost(2)]                   # pega a posição dos fantasmas

        # verifica se os fantasmas estão vulneraveis, se sim, não precisa dar prioridade para escapar do fantasma mais proximo, se não, damos prioridade para escapar do fantasma mais proximo
        # a função de verificação is_ghost_nearby foi aplicada para refinar o senso de urgencia do pacman ao chegar perto de algum fantasma. antes, ele ia para muito perto do fantasma, perdendo o jogo
        if not state.ghosts_are_vulnerable:
            # se tiver um fantasmas muito perto, chamamos uma função de escape
            if self.is_ghost_nearby(pacman_pos, ghost_positions):                      
                return self.best_escape_action(state, pacman_pos, ghost_positions)      

        # verifica se pacman está perto de comida e prioriza comer
        nearest_food_direction = self._find_nearest_food_direction(state, pacman_pos)
        if nearest_food_direction:
            return nearest_food_direction


        # caso contrario, usa o minimax para encontrar o melhor movimento possivel
        actions_values = [
            (
                action,
                self.minimax(
                    game_state=self.transfer(create_copy_state(state), action, True),
                    depth=5,                    # o minimax avalia 5 níveis de profundidade no futuro, considerando possíveis movimentos do pacman e dos fantasmas
                    maximizing_player=False,    # o pacman é o maximizador, buscando o melhor resultado, enquanto os fantasmas são minimizadores, buscando capturá-lo
                    alpha=float('-inf'),        # poda alpha-beta -> otimiza a busca eliminando movimentos que não precisam ser avaliados com mais profundidade.
                    beta=float('inf')
                ),
            )
            for action in self._ways_possible_for_pacman(state)
        ]

        # filtra as ações que não levam a um movimento repetido
        actions_values = [(action, value) for action, value in actions_values if not self.is_repeated_move(self.moves_pacman(state.get_pos_pacman(), action, state.get_size(), state.get_board()))]

        # se todas as ações levam a movimentos repetidos, faz um movimento qualquer
        if not actions_values:
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

        # identifica o maior valor entre as ações e seleciona as melhores. Se houver mais de uma ação com o mesmo valor máximo, uma delas é escolhida aleatoriamente
        max_value = max(actions_values, key=lambda temp: temp[1])[1]
        best_actions = [action for action, value in actions_values if value == max_value]

        # Se a melhor ação for um movimento repetido, escolhe aleatoriamente
        best_action = r.choice(best_actions) if len(best_actions) > 1 else best_actions[0]

        # atualiza a lista de posições anteriores com a nova posição do pacman
        new_position = self.moves_pacman(state.get_pos_pacman(), best_action, state.get_size(), state.get_board())
        self.update_previous_positions(new_position)

        return best_action

    # calcula a distancia de manhattan entre dois pontos, utilizamos manhattan ao inves da euclidiana para medir distancia em um grid ortogonal, como é o labirinto
    def manhattan_distance(self, point1, point2):
        return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

    # a heuristica vai avaliar o estado atual do jogo com base na posição do pacman, nas posições dos fantasmas e da posição das pílulas
    def heuristic_evaluation(self, pacman_position, ghost_positions, pill_positions, score):

        # calcula a distância de Manhattan entre pacman e os fantasmas mais próximos
        ghost_distances = [self.manhattan_distance(pacman_position, ghost) for ghost in ghost_positions]
        ghost_distance = min(ghost_distances) if ghost_distances else float('inf')

        # calcula a distância de Manhattan entre pacman e a pílula mais próxima
        pill_distances = [self.manhattan_distance(pacman_position, pill) for pill in pill_positions]
        pill_distance = min(pill_distances) if pill_distances else float('inf')

        # penalidade maior quando o pacman está perto dos fantasmas
        ghost_penalty = 0
        if ghost_distance <= 1:
            ghost_penalty = -100000  # fuga imediata se estiver a 1 bloco
        elif ghost_distance <= 2:
            ghost_penalty = -50000   # penalidade severa se estiver a 2 blocos
        elif ghost_distance <= 3:
            ghost_penalty = -20000   # penalidade moderada se estiver a 3 blocos

        # recompensa pela proximidade da comida
        pill_reward = 50 / pill_distance if pill_distance > 0 else 0

        # o valor heurístico é influenciado pela distância dos fantasmas e das pílulas
        return score + pill_reward + ghost_penalty

    # checa se há algum fantasma com distancia minima de 2 blocos do pacman
    def is_ghost_nearby(self, pacman_pos, ghost_positions, threshold=2):
        for ghost_pos in ghost_positions:
            if self.manhattan_distance(pacman_pos, ghost_pos) <= threshold:
                return True
        return False

    # função para gerar uma ação de escape 
    def best_escape_action(self, state, pacman_pos, ghost_positions):

        best_move = None
        max_distance_from_ghost = -float('inf')

        # aqui a função obtém todas as ações possíveis que o pacman pode fazer no estado atual do jogo
        for action in self._ways_possible_for_pacman(state):
            # para cada ação, a função simula a nova posição do pacman depois de executar o movimento
            new_pos = self.moves_pacman(pacman_pos, action, state.get_size(), state.get_board())
            # calculo da distancia do pacman ate o fantasma mais proximo
            min_ghost_distance = min([self.manhattan_distance(new_pos, ghost) for ghost in ghost_positions])
            # se a distância mínima do pacman até o fantasma mais próximo, depois de fazer o movimento atual, é maior do que a maior distância encontrada até agora
            if min_ghost_distance > max_distance_from_ghost:
                best_move = action                                  # atualiza best_move para armazenar essa ação como a melhor
                max_distance_from_ghost = min_ghost_distance        # atualiza max_distance_from_ghost para refletir essa nova maior distância.

        return best_move

    # mplementa o algoritmo Minimax com poda alfa-beta
    def minimax(self, game_state, depth, maximizing_player, alpha, beta):
        
        # o algoritmo para se a profundidade for igual a 0 ou se o jogo tiver terminado
        if depth == 0 or game_state.game_finished():
            # Ajuste aqui: passa apenas os 5 argumentos corretos
            return self.heuristic_evaluation(
                game_state.get_pos_pacman(),
                [game_state.get_pos_ghost(1), game_state.get_pos_ghost(2)],
                self.get_pill_positions(game_state.get_board()),
                game_state.score
            )

        # vez do pacman
        if maximizing_player: 
            max_eval = float('-inf')                                # inicializa max_eval = -infinito
            for move in game_state.get_pacman_moves():              # para cada movimento possivel do pacman
                new_state = game_state.apply_move(move, is_pacman=True)                 # gera um novo estado do jogo com o movimento aplicado
                eval = self.minimax(game_state=new_state, depth=depth - 1, maximizing_player=False, alpha=alpha, beta=beta)         # chama o minimax para calcular o valor do novo estado
                max_eval = max(max_eval, eval)                      # atualiza max_eval com o valor máximo entre a avaliação atual e o valor retornado
                alpha = max(alpha, eval)                            # atualiza alpha (o valor máximo garantido para o maximizador) e verifica se beta <= alpha (condição de poda)
                if beta <= alpha:
                    break
            return max_eval
        else:  # o mesmo algoritmo é aplicado para a vez do fantasma, mas o objetivo aqui é minimizar a avaliação
            min_eval = float('inf')
            for move in game_state.get_ghost_moves():
                new_state = game_state.apply_move(move, is_pacman=False)
                eval = self.minimax(game_state=new_state, depth=depth - 1, maximizing_player=True, alpha=alpha, beta=beta)
                min_eval = min(min_eval, eval)                     # atualiza min_eval com o valor minimo entre a avaliação atual e o valor retornado
                beta = min(beta, eval)                             # atualiza beta (o valor mínimo garantido para o minimizador) e verifica se beta <= alpha (condição de poda).
                if beta <= alpha:
                    break
            return min_eval

    # encontra todas as posições das pílulas no tabuleiro
    def get_pill_positions(self, board):
        pill_positions = []
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == '*': 
                    pill_positions.append((i, j))
        return pill_positions


    # a função transfer é responsável por aplicar um movimento ao estado atual do jogo (seja do pacman ou dos fantasmas) e retornar uma nova cópia desse estado após o movimento ser aplicado
    def transfer(self, state, action, is_pacman):
        if is_pacman:
            new_state = create_copy_state(state)    # cria uma cópia do estado atual do jogo para evitar modificar o estado original diretamente
            xp, yp = state.get_pos_pacman()         # obtém a posição atual do pacman
            board = state.get_board()
            board_size = state.get_size()

            # a função moves_pacman é chamada para calcular a nova posição do pacman, com base no movimento que foi passado
            new_pos_pacman = self.moves_pacman((xp, yp), action, board_size, board)
            new_state.set_pos_pacman(new_pos_pacman)
            return new_state

        # movimento dos fantamas
        else:
            G = ghosts()                            # cria uma instância da classe ghosts, que controla o comportamento dos fantasmas
            new_state = create_copy_state(state)    
            pos_g1 = state.get_pos_ghost(1)         
            pos_g2 = state.get_pos_ghost(2)
            board = state.get_board()
            board_size = state.get_size()

            # a função move_ghosts_validation é chamada para calcular as novas posições dos fantasmas com base no tabuleiro atual, a posição do pacman e o tamanho do tabuleiro
            new_pos_ghosts = G.moves_ghosts(pos_g1, pos_g2, state.get_pos_pacman(), board, board_size)

            new_state.set_pos_ghost(1, new_pos_ghosts["ghosts1"])
            new_state.set_pos_ghost(2, new_pos_ghosts["ghosts2"])

            return new_state

    # determina as ações possíveis para o Pacman no estado atual do jogo
    def _ways_possible_for_pacman(self, state) -> List[str]:
        x, y = state.get_pos_pacman()
        board = state.get_board()
        board_size = state.get_size()

        actions = []

        # verifica se cada direção está livre e não é uma parede
        if x > 0 and board[x - 1][y] != "-" and board[x - 1][y] not in ['G', 'F']:
            actions.append("up")
        if x < board_size[0] - 1 and board[x + 1][y] != "-" and board[x + 1][y] not in ['G', 'F']:
            actions.append("down")
        if y > 0 and board[x][y - 1] != "-" and board[x][y - 1] not in ['G', 'F']:
            actions.append("left")
        if y < board_size[1] - 1 and board[x][y + 1] != "-" and board[x][y + 1] not in ['G', 'F']:
            actions.append("right")

        return actions

    # Move o Pacman para uma nova posição com base na direção fornecida
    def moves_pacman(self, pacman_pos: Tuple[int, int], way_posibale: str, board_size: Tuple[int, int], board: List[List[str]]) -> Tuple[int, int]:
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