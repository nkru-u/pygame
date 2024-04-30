import pygame
import math
import sys
import random

pygame.init()

SIZE_BLOC = 20
FRAME_COLOR = (106, 146, 242)  # цвет экрана
WHITE = (174, 228, 115)
BLUE = (127, 172, 113)
RED = (224, 0, 0)
BLACK = (0, 0, 0)
HEAD_COL = (166, 210, 234)
SNAKE_COLOR = (1, 9, 152)
COUNT_BLOCK = 20
HEAD_MARGIN = 70
MARGIN = 1
WINDOW_SIZE = [SIZE_BLOC * COUNT_BLOCK + 2 * SIZE_BLOC + MARGIN * COUNT_BLOCK,
               SIZE_BLOC * COUNT_BLOCK + 2 * SIZE_BLOC + MARGIN * COUNT_BLOCK + HEAD_MARGIN]

FPS = 60
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Endless Scroll")

bg = pygame.image.load("bg.png").convert()
bg_width = bg.get_width()

scroll = 0
tiles = math.ceil(SCREEN_WIDTH / bg_width) + 1


class SnakeBlock:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_inside(self):
        return 0 <= self.x < COUNT_BLOCK and 0 <= self.y < COUNT_BLOCK

    def __eq__(self, other):
        return isinstance(other, SnakeBlock) and self.x == other.x and self.y == other.y


class Button(pygame.sprite.Sprite):
    def __init__(self, image, position, scale):
        super().__init__()
        self.orig_image = image
        self.image = pygame.transform.scale(image, scale)
        self.rect = self.image.get_rect(center=position)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


def secon_wind():
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption('Snake')
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('courier', 36)

    def draw_block(color, row, column):
        pygame.draw.rect(screen, color, [SIZE_BLOC + column * SIZE_BLOC + MARGIN * (column + 1),
                                         HEAD_MARGIN + SIZE_BLOC + row * SIZE_BLOC + MARGIN * (row + 1),
                                         SIZE_BLOC,
                                         SIZE_BLOC])

    def get_random_empty_block():
        x = random.randint(0, COUNT_BLOCK - 1)
        y = random.randint(0, COUNT_BLOCK - 1)
        empty_block = SnakeBlock(x, y)
        while empty_block in snake_blocks:
            empty_block.x = random.randint(0, COUNT_BLOCK - 1)
            empty_block.y = random.randint(0, COUNT_BLOCK - 1)
        return empty_block

    snake_blocks = [SnakeBlock(1, 1), SnakeBlock(1, 2), SnakeBlock(1, 3)]
    apple_block = get_random_empty_block()
    d_row = 0
    d_col = 1
    total = 0
    speed = 1

    def game_over():
        font_large = pygame.font.SysFont('courier', 72)
        text_game_over = font_large.render("Game Over", True, WHITE)
        text_score = font.render(f"Твои яблоки: {total}", True, WHITE)
        text_restart = font.render("Press R to restart", True, WHITE)

        screen.fill(FRAME_COLOR)
        screen.blit(text_game_over, (WINDOW_SIZE[0] // 2 - text_game_over.get_width() // 2, WINDOW_SIZE[1] // 2 - 100))
        screen.blit(text_score, (WINDOW_SIZE[0] // 2 - text_score.get_width() // 2, WINDOW_SIZE[1] // 2))
        screen.blit(text_restart, (WINDOW_SIZE[0] // 2 - text_restart.get_width() // 2, WINDOW_SIZE[1] // 2 + 100))
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        secon_wind()
                        return True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and d_col != 0:
                    d_row, d_col = -1, 0
                elif event.key == pygame.K_DOWN and d_col != 0:
                    d_row, d_col = 1, 0
                elif event.key == pygame.K_LEFT and d_row != 0:
                    d_row, d_col = 0, -1
                elif event.key == pygame.K_RIGHT and d_row != 0:
                    d_row, d_col = 0, 1

        new_head = SnakeBlock(snake_blocks[-1].x + d_row, snake_blocks[-1].y + d_col)
        if not new_head.is_inside() or new_head in snake_blocks:
            if game_over():
                # Restart game
                snake_blocks = [SnakeBlock(1, 1), SnakeBlock(1, 2), SnakeBlock(1, 3)]
                apple_block = get_random_empty_block()
                d_row = buf_row = 0
                d_col = buf_col = 1
                total = 0
                speed = 1
            else:
                pygame.quit()
                sys.exit()

        snake_blocks.append(new_head)

        if new_head == apple_block:
            total += 1
            speed = total // 5 + 1
            apple_block = get_random_empty_block()
        else:
            snake_blocks.pop(0)

        screen.fill(FRAME_COLOR)
        pygame.draw.rect(screen, HEAD_COL, [0, 0, WINDOW_SIZE[0], HEAD_MARGIN])

        text_total = font.render(f"Total: {total}", 0, (255, 255, 255))
        text_speed = font.render(f"Speed: {speed}", 0, (255, 255, 255))
        screen.blit(text_total, (SIZE_BLOC, SIZE_BLOC))
        screen.blit(text_speed, (SIZE_BLOC + 230, SIZE_BLOC))

        for row in range(COUNT_BLOCK):
            for column in range(COUNT_BLOCK):
                if (row + column) % 2 == 0:
                    color = BLUE
                else:
                    color = WHITE
                draw_block(color, row, column)

        draw_block(RED, apple_block.x, apple_block.y)
        for block in snake_blocks:
            draw_block(SNAKE_COLOR, block.x, block.y)

        pygame.display.flip()
        clock.tick(5 + speed)  # Adjust the speed here


clock = pygame.time.Clock()

# Load button images
start_button_image = pygame.image.load("start_button.png").convert_alpha()
end_button_image = pygame.image.load("end_button.png").convert_alpha()
titl_image = pygame.image.load("titl.png").convert_alpha()


# Define button scales
button_scale = (170, 70)
button_scale_for_titl = (400, 200)


# Create button sprites
start_button = Button(start_button_image, (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 250), button_scale)
end_button = Button(end_button_image, (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150), button_scale)
titl_button = Button(titl_image, (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 450), button_scale_for_titl)

# Create sprite groups
button_sprites = pygame.sprite.Group(start_button, end_button, titl_button)
snake_group = pygame.sprite.Group()

#game loop
run = True
while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.rect.collidepoint(event.pos):
                secon_wind()
            elif end_button.rect.collidepoint(event.pos):
                print("End button clicked!")

    #draw scrolling background
    for i in range(0, tiles):
        screen.blit(bg, (i * bg_width + scroll, 0))

    #scroll background
    scroll -= 5

    #reset scroll
    if abs(scroll) > bg_width:
        scroll = 0

    # Draw buttons
    button_sprites.draw(screen)

    pygame.display.update()

pygame.quit()
