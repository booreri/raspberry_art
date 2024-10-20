import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Randomized Neon Pattern")

# Define some colors for the neon effect
NEON_COLORS = [
    (255, 0, 255),  # Magenta
    (0, 255, 255),  # Cyan
    (255, 255, 0),  # Yellow
    (0, 255, 0),    # Lime
    (0, 0, 255),    # Blue
    (255, 165, 0),  # Orange
    (255, 20, 147), # Pink
]

# Function to draw random shapes with neon effects
def draw_neon_pattern():
    # Choose a random color from the neon palette
    color = random.choice(NEON_COLORS)
    
    # Choose a random shape: circle, rectangle, or line
    shape_type = random.choice(["circle", "rect", "line"])
    
    if shape_type == "circle":
        # Randomize position and radius
        pos = (random.randint(0, width), random.randint(0, height))
        radius = random.randint(10, 100)
        thickness = random.randint(1, 5)  # Line thickness
        pygame.draw.circle(screen, color, pos, radius, thickness)
    
    elif shape_type == "rect":
        # Randomize rectangle dimensions and position
        rect_width = random.randint(50, 200)
        rect_height = random.randint(50, 200)
        pos = (random.randint(0, width - rect_width), random.randint(0, height - rect_height))
        thickness = random.randint(1, 5)  # Line thickness
        pygame.draw.rect(screen, color, pygame.Rect(pos, (rect_width, rect_height)), thickness)
    
    elif shape_type == "line":
        # Randomize start and end points for the line
        start_pos = (random.randint(0, width), random.randint(0, height))
        end_pos = (random.randint(0, width), random.randint(0, height))
        thickness = random.randint(1, 5)  # Line thickness
        pygame.draw.line(screen, color, start_pos, end_pos, thickness)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with black to reset for the next frame
    screen.fill((0, 0, 0))
    
    # Draw neon patterns
    for _ in range(50):  # Drawing multiple shapes for a more complex pattern
        draw_neon_pattern()

    # Update the display
    pygame.display.flip()

    # Limit the frame rate to make the pattern changes smooth
    pygame.time.delay(100)

# Quit Pygame
pygame.quit()
