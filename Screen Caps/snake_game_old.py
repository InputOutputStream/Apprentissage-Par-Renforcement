import turtle
import time
import random

class SnakeGame:
    def __init__(self, width=600, height=600, speed=20):
        # Initialize game settings and screen
        self.width = width
        self.height = height
        self.speed = speed
        self.delay = 0.1
        self.level = 0.01
        self.score = 0
        self.high_score = 0

        self.wn = turtle.Screen()
        self.wn.title("Snake Game")
        self.wn.bgcolor("green")
        self.wn.setup(width=self.width, height=self.height)
        self.wn.tracer(0)

        # Initialize snake head
        self.head = turtle.Turtle()
        self.head.speed(0)
        self.head.shape("square")
        self.head.color("black")
        self.head.penup()
        self.head.goto(0, 0)
        self.head.direction = "stop"

        # Initialize food
        self.food = turtle.Turtle()
        self.food.speed(0)
        self.food.shape("circle")
        self.food.color("red")
        self.food.penup()
        self.food.goto(0, 100)

        self.segments = []

        # Initialize score display
        self.pen = turtle.Turtle()
        self.pen.speed(0)
        self.pen.shape("square")
        self.pen.color("white")
        self.pen.penup()
        self.pen.hideturtle()
        self.pen.goto(0, 260)
        self.pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 24, "normal"))

        # Set up controls and reset the game
        self.setup_controls()
        self.reset_game()

    def setup_controls(self):
        # Set up control bindings
        self.wn.listen()
        self.wn.onkeypress(self.go_up, "w")
        self.wn.onkeypress(self.go_down, "s")
        self.wn.onkeypress(self.go_left, "a")
        self.wn.onkeypress(self.go_right, "d")

    def go_up(self):
        # Change direction to up
        if self.head.direction != "down":
            self.head.direction = "up"

    def go_down(self):
        # Change direction to down
        if self.head.direction != "up":
            self.head.direction = "down"

    def go_left(self):
        # Change direction to left
        if self.head.direction != "right":
            self.head.direction = "left"

    def go_right(self):
        # Change direction to right
        if self.head.direction != "left":
            self.head.direction = "right"

    def _move(self):
        # Move the snake in the current direction
        if self.head.direction == "up":
            y = self.head.ycor()
            self.head.sety(y + self.speed)

        if self.head.direction == "down":
            y = self.head.ycor()
            self.head.sety(y - self.speed)

        if self.head.direction == "left":
            x = self.head.xcor()
            self.head.setx(x - self.speed)

        if self.head.direction == "right":
            x = self.head.xcor()
            self.head.setx(x + self.speed)

    def reset_game(self):
        # Reset the game state
        self.head.goto(0, 0)
        self.head.direction = "stop"
        for segment in self.segments:
            segment.goto(1000, 1000)
        self.segments.clear()
        self.score = 0
        self.delay = 0.1
        self.update_score()

    def _check_collisions(self):
        # Check for collisions with walls
        if self.head.xcor() > (self.width // 2 - self.speed) or self.head.xcor() < (-self.width // 2 + self.speed) or self.head.ycor() > (self.height // 2 - self.speed) or self.head.ycor() < (-self.height // 2 + self.speed):
            time.sleep(1)
            self.reset_game()

        # Check for collisions with self
        for segment in self.segments:
            if segment.distance(self.head) < self.speed:
                time.sleep(1)
                self.reset_game()

    def _check_food_collision(self):
        # Check if the snake has eaten the food
        if self.head.distance(self.food) < self.speed:
            # Move the food to a new random position
            x = random.randint(-self.width // 2 + self.speed, self.width // 2 - self.speed)
            y = random.randint(-self.height // 2 + self.speed, self.height // 2 - self.speed)
            self.food.goto(x, y)

            # Add a new segment to the snake
            new_segment = turtle.Turtle()
            new_segment.speed(0)
            new_segment.shape("square")
            new_segment.color("grey")
            new_segment.penup()
            self.segments.append(new_segment)

            # Speed up the game and update the score
            self.delay -= 0.001
            self.score += 10

            if self.score > self.high_score:
                self.high_score = self.score

            self.update_score()

    def update_score(self):
        # Update the score display
        self.pen.clear()
        self.pen.write(f"Score: {self.score}  High Score: {self.high_score}", align="center", font=("Courier", 24, "normal"))

    def play_step(self):
        # Main game loop step
        self.wn.update()
        self._check_collisions()
        self._check_food_collision()

        # Move the segments of the snake
        for index in range(len(self.segments) - 1, 0, -1):
            x = self.segments[index - 1].xcor()
            y = self.segments[index - 1].ycor()
            self.segments[index].goto(x, y)

        if len(self.segments) > 0:
            x = self.head.xcor()
            y = self.head.ycor()
            self.segments[0].goto(x, y)

        self._move()
        time.sleep(self.delay)
        return False, self.score

if __name__ == "__main__":
    game = SnakeGame()

    # game loop
    while True:
        game_over, score = game.play_step()

        if game_over:
            break

    print('Final Score', score)
