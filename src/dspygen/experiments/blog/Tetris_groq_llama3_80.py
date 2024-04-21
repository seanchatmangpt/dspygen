import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Tetris')
        self.clock = pygame.time.Clock()
        self.grid = [[0 for _ in range(10)] for _ in range(20)]
        self.next_piece = self.get_random_piece()
        self.current_piece = self.next_piece
        self.next_piece = self.get_random_piece()
        self.score = 0
        self.x = 0
        self.y = 0
        self.speed = 1

    def get_random_piece(self):
        pieces = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']
        return self.get_piece(pieces)

    def get_piece(self, pieces):
        return random.choice(pieces)

    def draw_grid(self):
        for i in range(20):
            for j in range(10):
                if self.grid[i][j] == 1:
                    pygame.draw.rect(self.screen, BLACK, (j * 30, i * 30, 30, 30), 1)

    def draw_current_piece(self):
        for i in range(len(self.current_piece)):
            for j in range(len(self.current_piece[i])):
                if self.current_piece[i][j] == 1:
                    if self.current_piece == 'I':
                        color = CYAN
                    elif self.current_piece == 'J':
                        color = BLUE
                    elif self.current_piece == 'L':
                        color = ORANGE
                    elif self.current_piece == 'O':
                        color = YELLOW
                    elif self.current_piece == 'S':
                        color = GREEN
                    elif self.current_piece == 'T':
                        color = MAGENTA
                    elif self.current_piece == 'Z':
                        color = RED
                    pygame.draw.rect(self.screen, color, ((j + self.x) * 30, (i + self.y) * 30, 30, 30))

    def move_piece(self):
        self.y += 1
        if self.y + len(self.current_piece) > 20:
            self.y = 0
            self.current_piece = self.next_piece
            self.next_piece = self.get_random_piece()
            self.score += 1
            self.speed += 0.1

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.x -= 1
                    elif event.key == pygame.K_RIGHT:
                        self.x += 1
                    elif event.key == pygame.K_DOWN:
                        self.y += 1
                    elif event.key == pygame.K_UP:
                        self.y -= 1
            self.move_piece()
            self.screen.fill(BLACK)
            pygame.draw.rect(self.screen, WHITE, (0, 0, 300, 600), 1)
            self.draw_grid()
            self.draw_current_piece()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

if __name__ == '__main__':
    game = Tetris()
    game.run()