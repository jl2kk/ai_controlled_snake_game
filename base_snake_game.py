import os
import sys
import pygame
import random
from collections import namedtuple

pygame.init()

font = pygame.font.Font(None, 25)

BLOCK_SIZE = 20
START_SPEED = 20


class Color:
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def value(self):
        return (self.red, self.green, self.blue)


class Direction:
    RIGHT = "right"
    LEFT = "left"
    UP = "up"
    DOWN = "down"

    opposites = {
        RIGHT: LEFT,
        LEFT: RIGHT,
        UP: DOWN,
        DOWN: UP,
    }

    @staticmethod
    def opposite(direction):
        return Direction.opposites[direction]


## Point == X,Y coordinates of snake and food
Point = namedtuple("Point", "x, y")


class SnakeGame:
    def __init__(self):
        self.width = 640
        self.height = 480
        self.display = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.direction = Direction.RIGHT
        self.head = Point(self.width / 2, self.height / 2)
        self.snake = []
        for i in range(3):
            self.snake.append(Point(self.head.x - i * BLOCK_SIZE, self.head.y))
        self.score = 0
        self.food = None
        self.speed = START_SPEED
        self.place_food()
        self.colors = {
            "snake": Color(0, 0, 255).value(),
            "food": Color(200, 0, 0).value(),
            "background": Color(0, 0, 0).value(),
        }

    def place_food(self):
        snake_points = set(self.snake)
        all_possible_food_locations = [
            Point(x, y)
            for x in range(0, self.width, BLOCK_SIZE)
            for y in range(0, self.height, BLOCK_SIZE)
        ]

        free_locations = set(all_possible_food_locations) - snake_points

        if free_locations:
            self.food = random.choice(list(free_locations))
        else:
            self.food = None

    def print_state(self):
        print("Snake Position:", self.snake)
        print("Food Position:", self.food)

    def play_step(self):
        self.handle_events()
        self.move()
        self.print_state()
        self.snake.insert(0, self.head)
        game_over = self.is_collision()
        if game_over:
            return True, self.score
        self.check_food_collision()
        self.update_ui()
        self.clock.tick(self.speed)
        return False, self.score

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.change_direction(event.key)

    def change_direction(self, key):
        if key == pygame.K_LEFT and self.direction != Direction.opposite(
            Direction.LEFT
        ):
            self.direction = Direction.LEFT
        elif key == pygame.K_RIGHT and self.direction != Direction.opposite(
            Direction.RIGHT
        ):
            self.direction = Direction.RIGHT
        elif key == pygame.K_UP and self.direction != Direction.opposite(Direction.UP):
            self.direction = Direction.UP
        elif key == pygame.K_DOWN and self.direction != Direction.opposite(
            Direction.DOWN
        ):
            self.direction = Direction.DOWN

    def is_collision(self):
        hit_boundary = (
            self.head.x < 0
            or self.head.x >= self.width
            or self.head.y < 0
            or self.head.y >= self.height
        )

        if self.head in self.snake[1:]:
            self_collision = True
        else:
            self_collision = False

        if hit_boundary or self_collision:
            return True
        else:
            False

    def check_food_collision(self):
        if self.head == self.food:
            self.score += 1
            self.speed = START_SPEED + self.score // 5

            self.place_food()
        else:
            self.snake.pop()

    def update_ui(self):
        self.display.fill(self.colors["background"])
        for pt in self.snake:
            pygame.draw.rect(
                self.display,
                self.colors["snake"],
                pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE),
            )
        pygame.draw.rect(
            self.display,
            self.colors["food"],
            pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE),
        )
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.display.blit(score_text, [0, 0])
        direction_text = font.render(
            f"Direction: {self.direction}", True, (255, 255, 255)
        )

        self.display.blit(direction_text, [0, 20])

        pygame.display.flip()

    def move(self):
        x = self.head.x
        y = self.head.y

        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)


if __name__ == "__main__":
    game = SnakeGame()
    while True:
        game_over, score = game.play_step()
        if game_over:
            print("Final Score", score)
            break
    pygame.quit()
