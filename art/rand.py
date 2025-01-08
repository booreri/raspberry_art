import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
ROWS, COLS = 6, 8  # Number of rows and columns in the grid

# Create a function to generate a random RGB color
def random_color():
    """Generate a random RGB color."""
    return random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)

# Create a color grid
def generate_color_grid(rows, cols):
    """Generate a grid of random colors."""
    return [[random_color() for _ in range(cols)] for _ in range(rows)]

# Initialize the screen in fullscreen mode
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()  # Get the actual screen size
RECT_WIDTH = WIDTH // COLS
RECT_HEIGHT = HEIGHT // ROWS
pygame.display.set_caption("Abstract Mood Art")

# Main loop
running = True
color_grid = generate_color_grid(ROWS, COLS)

# Clock for controlling frame rate
clock = pygame.time.Clock()

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Exit fullscreen on ESC
                running = False

    # Clear the screen
    screen.fill((200, 200, 200))  # Background gray

    # Draw rectangles
    for row in range(ROWS):
        for col in range(COLS):
            color = color_grid[row][col]
            x = col * RECT_WIDTH
            y = row * RECT_HEIGHT
            pygame.draw.rect(screen, color, (x, y, RECT_WIDTH, RECT_HEIGHT))

    # Update colors in the grid gradually
    for row in range(ROWS):
        for col in range(COLS):
            if random.random() < 0.1:  # Occasionally update a color
                color_grid[row][col] = random_color()

    # Update the display
    pygame.display.flip()

    # Limit frame rate
    clock.tick(10)  # Adjust for slower/faster updates

# Quit Pygame
pygame.quit()