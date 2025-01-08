import turtle
import random

# Set up the turtle
turtle.bgcolor('black')
turtle.colormode(255)
turtle.speed(0)

while True:  # Infinite loop to keep repeating
    # Forward drawing
    for x in range(500):
        r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        turtle.pencolor(r, g, b)
        turtle.fd(x + 50)
        turtle.rt(91)
    
    # Reverse drawing
    for x in range(500, 0, -1):
        r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        turtle.pencolor(r, g, b)
        turtle.bk(x + 50)
        turtle.lt(91)

# Keep the window open until clicked
turtle.exitonclick()
