from pacman import pacman
from game import game
from ghosts import ghosts
from utility import utility

import time  # Adicione essa linha para importar a função sleep

class play:
    def __init__(self) -> None:
        self.game = game()
        self.score = self.game.score
        self.ghosts = ghosts()
        self.pacman = pacman()
        self.utility = utility()

    def start(self):
        delay = 0.2  # Defina o valor do delay em segundos

        while True:
            self.game.display()

            # Atualizar o estado anterior
            self.utility.update_previous_state(self.game)

            # Verificar se o jogo terminou
            if self.utility.is_game_finished(self.game):
                if self.utility.is_pacman_win(self.game):
                    print("** PACMAN WIN !!!")
                else:
                    print("PACMAN LOST !")
                break

            # Escolher a melhor ação para o Pacman
            best_action = self.pacman.best_action(self.game)
            new_pos_pacman = self.pacman.moves_pacman(
                self.game.get_pos_pacman(),
                best_action,
                self.game.get_size(),
                self.game.get_board(),
            )

            # Atualizar a posição do Pacman no jogo
            self.game.set_pos_pacman(new_pos_pacman)

            # Obter as posições atuais dos fantasmas e do Pacman
            pos_g1 = self.game.get_pos_ghost(1)
            pos_g2 = self.game.get_pos_ghost(2)
            pos_pacman = self.game.get_pos_pacman()

            # Mover os fantasmas com base nas novas posições
            poses = self.ghosts.move_ghosts(
                pos_g1, pos_g2, pos_pacman, self.game.get_board(), self.game.get_size()
            )

            # Atualizar as posições dos fantasmas no jogo
            self.game.set_pos_ghost(1, poses["ghosts1"])
            self.game.set_pos_ghost(2, poses["ghosts2"])

            # Verificar se Pacman foi capturado por um fantasma
            if self.game.get_pos_pacman() == self.game.get_pos_ghost(1) or self.game.get_pos_pacman() == self.game.get_pos_ghost(2):
                print("Pacman is caught by a ghost!")
                break

            # Atualizar pontuação ao comer um ponto
            if self.game.get_board()[self.game.get_pos_pacman()[0]][self.game.get_pos_pacman()[1]] == "*":
                self.game.score += 10
                board = self.game.get_board()
                board[self.game.get_pos_pacman()[0]][self.game.get_pos_pacman()[1]] = " "
                self.game.set_board(board)

            time.sleep(delay)  # Pausar o jogo por 'delay' segundos antes de continuar




if __name__ == "__main__":
    game_instance = play()  # Cria uma instância do jogo
    game_instance.start()   # Inicia o loop principal do jogo
    
