import pygame
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

class Game:
    def __init__(self, manager):
        self.manager = manager
        self.player_pos = None
        self.screen_rect = None
        self.player_width = 50
        self.player_speed = 2
        self.left_key_down = False
        self.right_key_down = False
        self.setup()

    def setup(self):
        self.screen_rect = get_screenrect()
        self.player_pos = [20, self.screen_rect.height - 40]

    def update(self, dt):
        if self.left_key_down and self.right_key_down:
            return
        if self.left_key_down:
            self.player_pos[0] -= self.player_speed * dt
            if self.player_pos[0] < 0:
                self.player_pos[0] = 0
        elif self.right_key_down:
            self.player_pos[0] += self.player_speed * dt
            if self.player_pos[0] + self.player_width > self.screen_rect.width:
                self.player_pos[0] = self.screen_rect.width - self.player_width

    def draw(self, canvas):
        pygame.draw.rect(canvas, (0, 0, 200), (self.player_pos[0], self.player_pos[1], self.player_width, 15))
        left_key = text_surface("Left Key: {}".format(self.left_key_down), color=(255, 255, 255), font_size=24)
        right_key = text_surface("Right Key: {}".format(self.right_key_down), color=(255, 255, 255), font_size=24)
        canvas.blit(left_key, (20, 20))
        canvas.blit(right_key, (20, 50))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.left_key_down = True
            elif event.key == pygame.K_RIGHT:
                self.right_key_down = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.left_key_down = False
            elif event.key == pygame.K_RIGHT:
                self.right_key_down = False

if __name__ == '__main__':
    e = Engine(GameManager)
    e.game_loop()
