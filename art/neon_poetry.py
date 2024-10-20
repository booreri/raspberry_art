import pygame
import random
import requests

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Scrolling Neon Poetry")

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

# Function to fetch random lines of poetry from the PoetryDB API
def fetch_poetry_lines():
    api_url = "https://poetrydb.org/random/10/lines.json"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        lines = [line for poem in data for line in poem['lines']]  # Flatten the list of lines
        return lines
    else:
        print("Error fetching poetry:", response.status_code)
        return ["Error fetching poetry."]  # Fallback in case of error

# Fetch poetry lines
poetry_lines = fetch_poetry_lines()

# Font setup
pygame.font.init()
font_size = 32
font = pygame.font.SysFont('Arial', font_size, bold=True)

# Poetry movement parameters
text_speed = 2  # Controls how fast the text moves across the screen
text_objects = []  # Store each text object with its position

# Initialize the first set of text objects with random colors and initial positions
for line in poetry_lines:
    color = random.choice(NEON_COLORS)
    text_surface = font.render(line, True, color)
    # Start each line off-screen on the right
    start_x = width
    start_y = random.randint(50, height - text_surface.get_height() - 50)
    text_objects.append({
        "surface": text_surface,
        "x": start_x,
        "y": start_y,
        "color": color
    })

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with black to reset for the next frame
    screen.fill((0, 0, 0))

    # Move and draw each line of poetry across the screen
    for text_obj in text_objects:
        # Move the text to the left by the speed value
        text_obj["x"] -= text_speed
        
        # If the text moves off the left side of the screen, reset it to the right side
        if text_obj["x"] + text_obj["surface"].get_width() < 0:
            text_obj["x"] = width
            text_obj["y"] = random.randint(50, height - text_obj["surface"].get_height() - 50)
            text_obj["color"] = random.choice(NEON_COLORS)  # Change the color on each reset

        # Draw the text at its updated position
        screen.blit(text_obj["surface"], (text_obj["x"], text_obj["y"]))

    # Update the display
    pygame.display.flip()

    # Wait a short period to control the speed of the movement (slows down the movement)
    pygame.time.delay(20)  # Adjust this value to make it faster/slower

# Quit Pygame
pygame.quit()
