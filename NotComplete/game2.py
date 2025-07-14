import turtle
import time
import random
import numpy as np

class SnakeGame:
    def __init__(self, width=600, height=600, speed=60):
        self.width = width
        self.height = height
        self.speed = speed
        self.delay = 0.1
        self.level = 0.01
        self.score = 0
        self.high_score = 0
        self.frame_iteration = 0

        self.wn = turtle.Screen()
        self.wn.title("Snake Game")
        self.wn.bgcolor("green")
        self.wn.setup(width=self.width, height=self.height)
        self.wn.tracer(0)

        self.head = turtle.Turtle()
        self.head.speed(0)
        self.head.shape("square")
        self.head.color("black")
        self.head.penup()
        self.head.goto(0, 0)
        self.head.direction = "up"

        self.food = turtle.Turtle()
        self.food.speed(0)
        self.food.shape("circle")
        self.food.color("red")
        self.food.penup()
        self.food.goto(0, 100)

        self.segments = []

        self.pen = turtle.Turtle()
        self.pen.speed(0)
        self.pen.shape("square")
        self.pen.color("white")
        self.pen.penup()
        self.pen.hideturtle()
        self.pen.goto(0, 260)
        self.pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 24, "normal"))

        # self.setup_controls()
        self.reset_game()

    def setup_controls(self):
        self.wn.listen()
        self.wn.onkeypress(self.go_up, "w")
        self.wn.onkeypress(self.go_down, "s")
        self.wn.onkeypress(self.go_left, "a")
        self.wn.onkeypress(self.go_right, "d")

    def go_up(self):
        if self.head.direction != "down":
            self.head.direction = "up"

    def go_down(self):
        if self.head.direction != "up":
            self.head.direction = "down"

    def go_left(self):
        if self.head.direction != "right":
            self.head.direction = "left"

    def go_right(self):
        if self.head.direction != "left":
            self.head.direction = "right"

    def _move(self, action):
        # [straight, right, left]
        clock_wise = ["right", "down", "left", "up",]
        idx = clock_wise.index(self.head.direction)
        
        if np.array_equal(action, [1,0,0]):
            new_direction = clock_wise[idx] #No change
            
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx+1) % 4
            new_direction = clock_wise[next_idx] #Right Turn
        
        else: #[0, 0, 1]
            next_idx = (idx-1) % 4
            new_direction = clock_wise[next_idx] #Right Turn
        
        self.head.direction = new_direction
            
        y = self.head.ycor()
        x = self.head.xcor()

        if self.head.direction == 'down':
            self.head.sety(y + self.speed)

        if self.head.direction == 'up':
            self.head.sety(y - self.speed) 

        if self.head.direction == 'left':
            self.head.setx(x - self.speed)

        if self.head.direction == 'right':
            self.head.setx(x + self.speed)

    def reset_game(self):
        self.head.goto(0, 0)
        self.head.direction = "up"
        for segment in self.segments:
            segment.goto(1000, 1000)
        self.segments.clear()
        self.score = 0
        self.delay = 0.1
        self.update_score()

    def _check_collisions(self, pt=None):
        if pt is not None:
            if pt.xcor > 290 or pt.xcor < -290 or pt.ycor > 290 or pt.ycor < -290:
                time.sleep(1)
                self.reset_game()
                return True
            
        else:
            pt = self.head
            if pt.xcor() > 290 or pt.xcor() < -290 or pt.ycor() > 290 or pt.ycor() < -290:
                time.sleep(1)
                self.reset_game()
                return True
            

        for segment in self.segments:
            if segment.distance(pt) < self.speed:
                time.sleep(1)
                self.reset_game()
                return True
        return False

    def _check_food_collision(self):
        if self.head.distance(self.food) < self.speed:
            x = random.randint(-290, 290)
            y = random.randint(-290, 290)
            self.food.goto(x, y)

            new_segment = turtle.Turtle()
            new_segment.speed(0)
            new_segment.shape("square")
            new_segment.color("grey")
            new_segment.penup()
            self.segments.append(new_segment)

            self.delay -= 0.001
            self.score += 10

            if self.score > self.high_score:
                self.high_score = self.score

            self.update_score()
            return True
        
        return False

    def update_score(self):
        self.pen.clear()
        self.pen.write(f"Score: {self.score}  High Score: {self.high_score}", align="center", font=("Courier", 24, "normal"))

    def play_step(self, action):
        reward =  0
        game_over = False
        self.frame_iteration += 1
        
        self.wn.update()
        if self._check_collisions() or self.frame_iteration > 100*len(self.segments):
            reward -= 10
            game_over = True
        
        if self._check_food_collision():
            reward += 10
            game_over = False


        for index in range(len(self.segments) - 1, 0, -1):
            x = self.segments[index - 1].xcor()
            y = self.segments[index - 1].ycor()
            self.segments[index].goto(x, y)

        if len(self.segments) > 0:
            x = self.head.xcor()
            y = self.head.ycor()
            self.segments[0].goto(x, y)

        self._move(action)
        time.sleep(self.delay)
        return reward, game_over, self.score

