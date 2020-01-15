import pygame
import random
from Engine.Engine import Engine
from Engine.Config import get_screenrect
from Engine.Text import text_surface

class GameManager:
    def __init__(self, engine):
        self.engine = engine
        self.game = Game(self)

    def update(self, dt):
        self.game.update(dt)

    def draw(self, canvas):
        self.game.draw(canvas)

    def handle_event(self, event):
        self.game.handle_event(event)

class Block:
    def __init__(self, rect):
        self.rect = rect
        self.status = "fresh"
        self.border = 3

    def hit(self):
        if self.status == "fresh":
            self.status = "hit_once"
        elif self.status == "hit_once":
            self.status = "killed"

    def draw(self, canvas):
        if self.status == "fresh":
            color = (200, 0, 0)
        elif self.status == "hit_once":
            color = (100, 0, 0)
        pygame.draw.rect(canvas, color, self.rect, self.border)

class Game:
    def __init__(self, engine):
        self.engine = engine
        self.player_pos = None
        self.screen_rect = None
        self.player_width = 50
        self.player_speed = 0.35
        self.keys_pressed = {pygame.K_RIGHT: False, pygame.K_LEFT: False}

        self.ball_pos = None
        self.ball_radius = 10
        self.ball_velocity = None
        self.ball_speed = 10

        self.blocks = []
        self.state = "start"
        self.setup()

    def setup(self):
        self.screen_rect = get_screenrect()
        self.player_pos = [20, self.screen_rect.height - 40]
        self.setup_ball()
        self.setup_blocks()

    def setup_ball(self):
        self.ball_pos = [self.screen_rect.width // 2, self.screen_rect.height - 80]
        rand_x = random.random()
        rand_y = random.random()
        self.ball_velocity = pygame.math.Vector2(-rand_x, -rand_y)

    def setup_blocks(self):
        rows = 5
        cols = 8
        block_width = 90
        block_height = 30
        padding = 8
        self.blocks = []
        x_offset = 10
        y_offset = 10
        for row in range(rows):
            for col in range(cols):
                x = col * block_width + (col * padding)
                y = row * block_height + (row * padding)
                self.blocks.append(Block(pygame.Rect(x + x_offset, y + y_offset, block_width, block_height)))
            
    def update(self, dt):
        if self.keys_pressed[pygame.K_LEFT]:
            self.player_pos[0] -= self.player_speed * dt
            if self.player_pos[0] < 0:
                self.player_pos[0] = 0
        elif self.keys_pressed[pygame.K_RIGHT]:
            self.player_pos[0] += self.player_speed * dt
            if self.player_pos[0] + self.player_width > self.screen_rect.width:
                self.player_pos[0] = self.screen_rect.width - self.player_width

        if self.state == "playing":
            self.ball_pos[0] += int(self.ball_velocity.x * self.ball_speed)
            self.ball_pos[1] += int(self.ball_velocity.y * self.ball_speed)
            if self.ball_pos[0] < 0:
                self.ball_pos[0] = 1
                self.ball_velocity[0] *= -1
            elif self.ball_pos[0] > self.screen_rect.width:
                self.ball_pos[0] = self.screen_rect.width - 1
                self.ball_velocity[0] *= -1
            if self.ball_pos[1] < 0:
                self.ball_pos[1] = 0
                self.ball_velocity[1] *= -1
            if self.check_collisions():
                self.ball_velocity[0] *= -1
                self.ball_velocity[1] *= -1

            if self.ball_pos[1] > self.screen_rect.height:
                # we went offscreen, place new ball
                self.state = "start"
                self.setup_ball()


    def check_collisions(self):
        print("Checking Collisions", self.ball_pos)
        for block in self.blocks:
            if block.rect.collidepoint(self.ball_pos):
                block.hit()
                return True
        return False


    def draw(self, canvas):
        pygame.draw.rect(canvas, (0, 0, 200), (self.player_pos[0], self.player_pos[1], self.player_width, 15))
        pygame.draw.circle(canvas, (0, 200, 0), self.ball_pos, self.ball_radius)
        left_key = text_surface("Left Key: {}".format(self.keys_pressed[pygame.K_LEFT]), color=(255, 255, 255), font_size=24)
        right_key = text_surface("Right Key: {}".format(self.keys_pressed[pygame.K_RIGHT]), color=(255, 255, 255), font_size=24)
        ball_vel = text_surface("Ball Velocity: {}".format(self.ball_velocity), color=(255, 255, 255), font_size=24)

        for block in self.blocks:
            #pygame.draw.rect(canvas, (255, 255, 255), block.rect, 2)
            block.draw(canvas)

        # canvas.blit(left_key, (20, 20))
        # canvas.blit(right_key, (20, 50))
        # canvas.blit(ball_vel, (20, 70))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in self.keys_pressed.keys():
                self.keys_pressed[event.key] = True
        elif event.type == pygame.KEYUP:
            if event.key in self.keys_pressed.keys():
                self.keys_pressed[event.key] = False
            if event.key == pygame.K_SPACE:
                if self.state == "start":
                    self.state = "playing"

if __name__ == '__main__':
    e = Engine(Game)
    e.game_loop()
