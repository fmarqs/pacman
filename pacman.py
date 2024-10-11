import random as r
from typing import List, Tuple
from utility import utility
from game import game

class pacman:
    def __init__(self):
        self.utility = utility()
        self.population_size = 20  # Tamanho da população
        self.generations = 50      # Número de gerações
        self.mutation_rate = 0.1   # Taxa de mutação
        self.sequence_length = 10  # Número de ações em cada indivíduo
        self._ways_possible_for_ghosts = ["up", "down", "left", "right"]

    def best_action(self, state):
        # Inicializa a população com indivíduos aleatórios (sequências de ações)
        population = [self.random_sequence() for _ in range(self.population_size)]
        
        for generation in range(self.generations):
            # Avalia a aptidão de cada indivíduo na população
            fitness_scores = [(ind, self.evaluate_fitness(ind, state)) for ind in population]
            
            # Seleciona os melhores indivíduos com base no fitness
            selected_population = self.selection(fitness_scores)

            # Gera a próxima geração por cruzamento e mutação
            population = self.next_generation(selected_population)
        
        # Escolhe o melhor indivíduo após as gerações
        best_individual = max(population, key=lambda ind: self.evaluate_fitness(ind, state))
        best_action = best_individual[0]  # Retorna a primeira ação da melhor sequência
        
        print(f"Ação escolhida pelo algoritmo genético: {best_action}")
        return best_action

    def random_sequence(self) -> List[str]:
        """ Gera uma sequência aleatória de ações. """
        return [r.choice(self._ways_possible_for_ghosts) for _ in range(self.sequence_length)]
    
    def evaluate_fitness(self, individual: List[str], state) -> float:
        """ Avalia a aptidão de uma sequência de ações simulando o jogo. """
        temp_state = create_copy_state(state)
        score = 0
        
        for action in individual:
            new_state = self.transfer(temp_state, action, is_pacman=True)
            score += new_state.score  # Atualiza a pontuação
            temp_state = new_state  # Continua simulando no novo estado
        
        return score

    def selection(self, fitness_scores: List[Tuple[List[str], float]]) -> List[List[str]]:
        """ Seleciona os melhores indivíduos com base no fitness. """
        fitness_scores.sort(key=lambda x: x[1], reverse=True)  # Ordena por pontuação
        selected = [ind for ind, score in fitness_scores[:self.population_size // 2]]  # Seleciona metade da população
        return selected

    def next_generation(self, selected_population: List[List[str]]) -> List[List[str]]:
        """ Gera a próxima geração por cruzamento e mutação. """
        new_population = []

        # Cruzamento
        for _ in range(self.population_size):
            parent1, parent2 = r.sample(selected_population, 2)
            child = self.crossover(parent1, parent2)
            new_population.append(self.mutation(child))

        return new_population

    def crossover(self, parent1: List[str], parent2: List[str]) -> List[str]:
        """ Realiza o cruzamento entre dois pais. """
        crossover_point = r.randint(0, self.sequence_length - 1)
        return parent1[:crossover_point] + parent2[crossover_point:]

    def mutation(self, individual: List[str]) -> List[str]:
        """ Realiza a mutação em um indivíduo com uma certa probabilidade. """
        for i in range(self.sequence_length):
            if r.random() < self.mutation_rate:
                individual[i] = r.choice(self._ways_possible_for_ghosts)
        return individual

    def transfer(self, state, action, is_pacman):
        """ Atualiza o estado do jogo após uma ação do Pac-Man. """
        new_state = create_copy_state(state)
        if is_pacman:
            xp, yp = state.get_pos_pacman()
            board = state.get_board()
            board_size = state.get_size()

            new_pos_pacman = self.moves_pacman((xp, yp), action, board_size, board)
            new_state.set_pos_pacman(new_pos_pacman)
        else:
            # Movimento dos fantasmas pode ser implementado aqui
            pass

        return new_state

    def moves_pacman(self, pacman_pos: Tuple[int, int], way_posibale: str, board_size: Tuple[int, int], board: List[List[str]]) -> Tuple[int, int]:
        """ Move o Pacman para uma nova posição com base na direção fornecida. """
        x, y = pacman_pos
        ways = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}
        dx, dy = ways[way_posibale]
        new_x, new_y = x + dx, y + dy

        if 0 <= new_x < board_size[0] and 0 <= new_y < board_size[1] and board[new_x][new_y] != "-":
            return (new_x, new_y)
        return pacman_pos

def create_copy_state(state) -> game:
    """ Cria uma cópia do estado atual do jogo. """
    new_board = game()
    new_board.set_pos_pacman(state.get_pos_pacman())
    new_board.set_pos_ghost(1, state.get_pos_ghost(1))
    new_board.set_pos_ghost(2, state.get_pos_ghost(2))
    new_board.set_score(state.score)
    new_board.set_board(state.get_board())
    return new_board
