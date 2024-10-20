import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Randomized Moving Stock Charts")

# Define neon-like colors for the stock lines
NEON_COLORS = [
    (255, 0, 255),  # Magenta
    (0, 255, 255),  # Cyan
    (255, 255, 0),  # Yellow
    (0, 255, 0),    # Lime
    (0, 0, 255),    # Blue
    (255, 165, 0),  # Orange
    (255, 20, 147), # Pink
]

# Define stock line parameters
num_charts = 100  # Number of stock lines
chart_length = 100  # Number of points in each stock chart
line_speed = 2  # Speed of the moving charts

# Initialize stock charts with random starting points
stock_lines = []
for _ in range(num_charts):
    stock_data = []
    start_x = random.randint(0, width // 2)  # Start somewhere on the left half of the screen
    start_y = random.randint(100, height - 100)  # Random Y position for the starting point

    for i in range(chart_length):
        stock_data.append((start_x + i * line_speed, start_y))
    stock_lines.append({
        "points": stock_data,
        "color": random.choice(NEON_COLORS),
        "volatility": random.uniform(1, 5)  # Random volatility factor for each line
    })

# Function to update stock prices (simulate price changes)
def update_stock_line(stock_line):
    for i in range(1, len(stock_line["points"])):
        # Shift x-axis points to the left (simulate forward movement)
        stock_line["points"][i] = (stock_line["points"][i][0] - line_speed, stock_line["points"][i][1])

        # Generate random stock price change (Y-axis) to simulate stock volatility
        price_change = random.uniform(-stock_line["volatility"], stock_line["volatility"])
        new_y = max(50, min(stock_line["points"][i][1] + price_change, height - 50))  # Keep within screen bounds
        stock_line["points"][i] = (stock_line["points"][i][0], new_y)

    # Add a new point to the end of the chart (simulating continuation)
    new_x = stock_line["points"][-1][0] + line_speed
    new_y = stock_line["points"][-1][1] + random.uniform(-stock_line["volatility"], stock_line["volatility"])
    new_y = max(50, min(new_y, height - 50))  # Keep within screen bounds
    stock_line["points"].append((new_x, new_y))

    # Remove the first point to keep the line moving
    stock_line["points"].pop(0)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with black to reset for the next frame
    screen.fill((0, 0, 0))

    # Update and draw each stock line
    for stock_line in stock_lines:
        # Update stock line with new prices
        update_stock_line(stock_line)

        # Draw the stock line as a continuous line connecting its points
        pygame.draw.lines(screen, stock_line["color"], False, stock_line["points"], 3)

    # Update the display
    pygame.display.flip()

    # Limit the frame rate to make the movement smooth
    pygame.time.delay(50)

# Quit Pygame
pygame.quit()
