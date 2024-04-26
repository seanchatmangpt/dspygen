import pygame
import random

# Initialize PyGame
pygame.init()

# Define constants
WIDTH, HEIGHT = 400, 500
BLOCK_SIZE = 20
FPS = 60

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Piece:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.matrix = [[1, 1], [1, 1]]

class Game:
    def __init__(self):
        self.board = [[0 for _ in range(10)] for _ in range(20)]
        self.pieces = []
        self.score = 0
        self.clock = pygame.time.Clock()

    def check_collision(self, piece):
        for y, row in enumerate(piece.matrix):
            for x, val in enumerate(row):
                if val == 1:
                    if (x + piece.x >= 10) or (y + piece.y >= 20) or \
                       self.board[y + piece.y][x + piece.x] != 0:
                        return True
        return False

    def update_screen(self, screen):
        for y, row in enumerate(self.board):
            for x, val in enumerate(row):
                if val != 0:
                    pygame.draw.rect(screen, BLUE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def game_loop(self, screen):
        while True:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            piece = Piece()
            while True:
                piece.x = random.randint(0, 9)
                piece.y = 0
                if not self.check_collision(piece):
                    break

            while True:
                self.update_screen(screen)
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    piece.x -= 1
                    if self.check_collision(piece):
                        piece.x += 1
                if keys[pygame.K_RIGHT]:
                    piece.x += 1
                    if self.check_collision(piece):
                        piece.x -= 1

                if random.randint(0, 100) < 10:  # Randomly move the piece down
                    piece.y += 1
                    if self.check_collision(piece):
                        for y, row in enumerate(piece.matrix):
                            for x, val in enumerate(row):
                                print(val)
                                if val == 1:
                                    print(x,y)
                                    #self.board[y + piece.y][x + piece.x] = 1
                        break

            for y, row in enumerate(self.board):
                if all(val == 1 for val in row):
                    del self.board[y]
                    self.score += 10

if __name__ == "__main__":
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tetris")
    game = Game()
    game.game_loop(screen)