import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 300
screen_height = 600
block_size = 30

# Define the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tetris")

# Colors
colors = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 165, 0),
    (0, 255, 255),
    (128, 0, 128)
]

# Tetrimino shapes
shapes = [
    [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']],

    [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']],

    [['.....',
      '..0..',
      '..0..',
      '..0..',
      '..0..'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']],

    [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']],

    [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']],

    [['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '..00.',
      '...0.',
      '...0.',
      '.....'],
     ['.....',
      '.....',
      '...0.',
      '.000.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']],

    [['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '...0.',
      '...0.',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]
]

# Tetrimino class
class Tetrimino:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.shape = random.choice(shapes)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0

    def image(self):
        return self.shape[self.rotation % len(self.shape)]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)

# Create grid
def create_grid(locked_positions={}):
    grid = [[(0, 0, 0) for x in range(screen_width // block_size)] for y in range(screen_height // block_size)]
    for y in range(screen_height // block_size):
        for x in range(screen_width // block_size):
            if (x, y) in locked_positions:
                c = locked_positions[(x, y)]
                grid[y][x] = c
    return grid

# Draw grid
def draw_grid(surface, grid):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            pygame.draw.rect(surface, grid[y][x], (x * block_size, y * block_size, block_size, block_size), 0)
    draw_gridlines(surface)

# Draw grid lines
def draw_gridlines(surface):
    for y in range(screen_height // block_size):
        pygame.draw.line(surface, (128, 128, 128), (0, y * block_size), (screen_width, y * block_size))
    for x in range(screen_width // block_size):
        pygame.draw.line(surface, (128, 128, 128), (x * block_size, 0), (x * block_size, screen_height))

# Clear rows
def clear_rows(grid, locked):
    increment = 0
    for y in range(len(grid) - 1, -1, -1):
        row = grid[y]
        if (0, 0, 0) not in row:
            increment += 1
            del locked[y]
            for key in sorted(list(locked), key=lambda k: k[1])[::-1]:
                if key[1] < y:
                    newKey = (key[0], key[1] + 1)
                    locked[newKey] = locked.pop(key)
    return increment

# Check if position is valid
def valid_space(shape, grid):
    accepted_positions = [[(x, y) for x in range(screen_width // block_size) if grid[y][x] == (0, 0, 0)] for y in range(screen_height // block_size)]
    accepted_positions = [x for item in accepted_positions for x in item]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True

# Convert shape format
def convert_shape_format(shape):
    positions = []
    format = shape.image()

    for y, line in enumerate(format):
        row = list(line)
        for x, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + x, shape.y + y))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0], pos[1])

    return positions

# Main function
def main():
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = Tetrimino(5, 0)
    next_piece = Tetrimino(5, 0)
    clock = pygame.time.Clock()
    fall_time = 0

    while run:
        grid = create_grid(locked_positions)
        fall_speed = 0.27

        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotate()
                    if not valid_space(current_piece, grid):
                        current_piece.rotate()
                        current_piece.rotate()
                        current_piece.rotate()

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = colors[current_piece.color]

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = colors[current_piece.color]
            current_piece = next_piece
            next_piece = Tetrimino(5, 0)
            change_piece = False

            clear_rows(grid, locked_positions)

        draw_grid(screen, grid)
        pygame.display.update()

    pygame.display.quit()

main()


