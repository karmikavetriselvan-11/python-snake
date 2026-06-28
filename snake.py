import turtle
import time
import random

delay = 0.1

# Score
score = 0
high_score = 0

# Screen
wn = turtle.Screen()
wn.title("Snake Game")
wn.bgcolor("black")
wn.setup(width=600, height=600)
wn.tracer(0)

# Snake Head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("lime")
head.penup()
head.goto(0, 0)
head.direction = "Stop"

# Food
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
# Start food at a grid-aligned position
food.goto(0, 100)

segments = []

# Score Display
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0  High Score: 0", align="center",
          font=("Arial", 18, "bold"))

# Controls
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def move():
    x = head.xcor()
    y = head.ycor()

    if head.direction == "up":
        head.sety(y + 20)

    if head.direction == "down":
        head.sety(y - 20)

    if head.direction == "left":
        head.setx(x - 20)

    if head.direction == "right":
        head.setx(x + 20)

wn.listen()
wn.onkeypress(go_up, "Up")
wn.onkeypress(go_down, "Down")
wn.onkeypress(go_left, "Left")
wn.onkeypress(go_right, "Right")

def reset_game():
    global score, delay
    time.sleep(1)
    head.goto(0, 0)
    head.direction = "Stop"

    # Hide and clear old segments properly
    for segment in segments:
        segment.goto(1000, 1000)
        segment.hideturtle()
    segments.clear()

    score = 0
    delay = 0.1

    pen.clear()
    pen.write(f"Score: {score}  High Score: {high_score}",
              align="center", font=("Arial", 18, "bold"))

# Main Loop wrapped in try-except to handle window close gracefully
try:
    while True:
        wn.update()

        # Border Collision
        if (head.xcor() > 290 or head.xcor() < -290 or
            head.ycor() > 290 or head.ycor() < -290):
            reset_game()

        # Food Collision
        if head.distance(food) < 20:
            # Place food on the 20-pixel grid
            x = random.randint(-14, 14) * 20
            y = random.randint(-14, 14) * 20
            food.goto(x, y)

            new_segment = turtle.Turtle()
            new_segment.speed(0)
            new_segment.shape("square")
            new_segment.color("green")
            new_segment.penup()
            segments.append(new_segment)

            # Reduce delay to speed up game, with a lower limit
            delay = max(0.01, delay - 0.001)

            score += 10
            if score > high_score:
                high_score = score

            pen.clear()
            pen.write(f"Score: {score}  High Score: {high_score}",
                      align="center", font=("Arial", 18, "bold"))

        # Move Body
        for index in range(len(segments)-1, 0, -1):
            x = segments[index-1].xcor()
            y = segments[index-1].ycor()
            segments[index].goto(x, y)

        if len(segments) > 0:
            segments[0].goto(head.xcor(), head.ycor())

        move()

        # Body Collision
        for segment in segments:
            if segment.distance(head) < 20:
                reset_game()
                break

        time.sleep(delay)

except (turtle.Terminator, Exception):
    # Gracefully exit if user closes the window
    pass
