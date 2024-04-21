import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Tetris')
        self.clock = pygame.time.Clock()
        self.grid = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
        self.next_piece = self.get_random_piece()
        self.current_piece = self.next_piece
        self.next_piece = self.get_random_piece()
        self.score = 0
        self.x = 0
        self.y = 0

    def get_random_piece(self):
        pieces = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']
        return self.get_piece(pieces)

    def get_piece(self, pieces):
        return random.choice(pieces)

    def draw_grid(self):
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if self.grid[i][j] == 1:
                    pygame.draw.rect(self.screen, BLACK, (j, i, 1, 1))

    def draw_current_piece(self):
        for i in range(len(self.current_piece)):
            for j in range(len(self.current_piece[i])):
                if self.current_piece[i][j] == 1:
                    pygame.draw.rect(self.screen, RED, ((j + self.x, i + self.y), 1, 1))

    def move_piece(self):
        self.x += 1
        if self.x + len(self.current_piece[0]) > WIDTH:
            self.x = 0
            self.y += 1
            if self.y + len(self.current_piece) > HEIGHT:
                self.y = 0
                self.current_piece = self.next_piece
                self.next_piece = self.get_random_piece()
                self.score += 1

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
            self.screen.fill(WHITE)
            self.draw_grid()
            self.draw_current_piece()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

if __name__ == '__main__':
    game = Tetris()
    game.run()