import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Randomized Synapse Pattern")

# Define neon-like colors
NEON_COLORS = [
    (255, 0, 255),  # Magenta
    (0, 255, 255),  # Cyan
    (255, 255, 0),  # Yellow
    (0, 255, 0),    # Lime
    (0, 0, 255),    # Blue
    (255, 165, 0),  # Orange
    (255, 20, 147), # Pink
]

# Function to draw circular nodes (representing neurons)
def draw_node(pos, color):
    radius = random.randint(10, 20)  # Neuron size (smaller for synapse)
    pygame.draw.circle(screen, color, pos, radius)

# Function to draw connecting lines (representing synapse connections)
def draw_synapse_line(start_pos, end_pos, color):
    thickness = random.randint(2, 5)  # Thickness of the connections
    pygame.draw.line(screen, color, start_pos, end_pos, thickness)

# Function to create synapse-like patterns
def draw_synapse_pattern():
    # Choose random colors for each pattern
    node_color = random.choice(NEON_COLORS)
    synapse_color = random.choice(NEON_COLORS)

    # Random starting point for a node (neuron)
    start_pos = (random.randint(0, width), random.randint(0, height))

    # Draw the node (neuron)
    draw_node(start_pos, node_color)

    # Create a random number of connected nodes (dendrites/axons)
    num_connections = random.randint(2, 6)  # Number of synapse connections

    for _ in range(num_connections):
        # Create the end position of the synapse connection
        angle = random.uniform(0, 2 * math.pi)  # Random direction
        distance = random.randint(50, 150)  # Random distance from the neuron
        end_pos = (
            start_pos[0] + int(math.cos(angle) * distance),
            start_pos[1] + int(math.sin(angle) * distance)
        )

        # Ensure the connection stays within the window bounds
        end_pos = (min(max(0, end_pos[0]), width), min(max(0, end_pos[1]), height))

        # Draw the connecting synapse line
        draw_synapse_line(start_pos, end_pos, synapse_color)

        # Draw the next neuron at the end of the connection (for recursive effect)
        draw_node(end_pos, node_color)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with black to reset for the next frame
    screen.fill((0, 0, 0))

    # Draw synapse patterns
    for _ in range(20):  # Draw multiple synapse structures
        draw_synapse_pattern()

    # Update the display
    pygame.display.flip()

    # Limit the frame rate to make the synapse animation smooth
    pygame.time.delay(100)

# Quit Pygame
pygame.quit()
