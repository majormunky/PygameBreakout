from __future__ import absolute_import
import pygame
from Engine.Text import text_surface


class ImageMenuWidget:
    def __init__(self, game, list_items, x, y):
        self.x = x
        self.y = y
        self.list_items = list_items
        self.game = game
        self.current_item = 0
        self.second_selection = None
        self.second_selection_color = (100, 100, 100)
        self.text_color = (255, 255, 255)
        self.active = True
        self.menu_type = "normal"
        self.state = "normal"
        self.disabled_items = []

    def handle_normal_menu_key(self, key):
        # get a quick reference to our current index
        new_item = self.current_item

        # we are only worried about up and down keys
        # this just checks the index against the list and will wrap
        # the index around if we go up or down too far
        if key == pygame.K_UP:
            if self.current_item == 0:
                new_item = len(self.list_items) - 1
            else:
                new_item -= 1
        elif key == pygame.K_DOWN:
            if self.current_item == len(self.list_items) - 1:
                new_item = 0
            else:
                new_item += 1

        # now that we have our item, make sure it isn't the one we
        # are currently at and check that its not disabled
        if new_item != self.current_item:
            if self.list_items[new_item] not in self.disabled_items:
                # then set it
                self.current_item = new_item
                self.current_item.update_data()

    def update_data(self):
        pass

    def handle_swapping_menu_key(self, key):
        new_item = self.second_selection

        if key == pygame.K_UP:
            if self.second_selection == 0:
                new_item = len(self.list_items) - 1
            else:
                new_item -= 1
            if new_item == self.current_item:
                if new_item == 0:
                    new_item = len(self.list_items) - 1
                else:
                    new_item -= 1

        elif key == pygame.K_DOWN:
            if self.second_selection == len(self.list_items) - 1:
                new_item = 0
            else:
                new_item += 1
            if new_item == self.current_item:
                if new_item == len(self.list_items) - 1:
                    new_item = 0
                else:
                    new_item += 1

        if new_item != self.second_selection:
                if self.list_items[new_item] not in self.disabled_items:
                    self.second_selection = new_item

    def handle_key(self, key):
        if self.state == "normal":
            self.handle_normal_menu_key(key)
        elif self.state == "controlling_second_selection":
            if key == pygame.K_ESCAPE:
                self.state = "normal"
                self.second_selection = None
                return
            self.handle_swapping_menu_key(key)

        if self.menu_type == "swapping":
            if self.state == "controlling_second_selection":
                if key == pygame.K_RETURN:
                    print(f"Need to swap {self.current_item} with {self.second_selection}.")
                    self.game.swap_characters(self.current_item, self.second_selection)

            elif self.state == "normal":
                if key == pygame.K_RETURN:
                    self.second_selection = self.current_item + 1
                    self.state = "controlling_second_selection"
                    if self.second_selection > len(self.list_items):
                        self.second_selection = 0

    def get_current_item(self):
        return self.list_items[self.current_item]

    def get_current_index(self):
        return self.current_item

    def draw(self, canvas):
        for index, item in enumerate(self.list_items):
            my = self.y + (index * (self.list_items[index].get_height() * 2))
            canvas.blit(self.list_items[index], (self.x, my))
            if self.current_item == index and self.active:
                pygame.draw.rect(canvas, self.text_color, (self.x - 20, my + 5, 10, 10))
            if self.second_selection is not None and self.second_selection == index and self.active:
                pygame.draw.rect(canvas, self.second_selection_color, (self.x - 20, my + 15, 10, 10))


class MenuWidget:
    def __init__(self, list_items, x, y, font_size=20, text_color = (0, 0, 0), disabled_color = (200, 200, 200), font_face="Helvetica"):
        self.x = x
        self.y = y
        self.font_face = font_face
        self.font_size = font_size
        self.list_items = list_items
        self.disabled_items = []
        self.item_images = {}
        self.current_item = 0
        self.second_selection = 0
        self.text_color = text_color
        self.disabled_color = disabled_color
        self.second_selection_color = (100, 100, 100)
        self.menu_height = 0
        self.active = True
        self.state = "normal"
        self.menu_type = "normal"
        self.render_images()

    # def update_items(self, item_list):
    #     self.list_items = [x.name for x in item_list]
    #     self.render_images()

    def disable_item(self, menu_name):
        if menu_name in self.list_items:
            self.disabled_items.append(menu_name)
        self.render_images()

    def render_images(self):
        self.menu_height = 0
        self.item_images = {}
        for item in self.list_items:
            if item in self.disabled_items:
                color = self.disabled_color
            else:
                color = self.text_color
            self.item_images[item] = text_surface(item, self.font_size, color, font_face=self.font_face)
            self.menu_height += self.item_images[item].get_rect().height

    def handle_key(self, key):
        print("handling key")
        new_item = self.current_item
        if key == pygame.K_UP:
            if self.current_item == 0:
                new_item = len(self.list_items) - 1
            else:
                new_item -= 1
        elif key == pygame.K_DOWN:
            if self.current_item == len(self.list_items) - 1:
                new_item = 0
            else:
                new_item += 1

        if self.menu_type == "swapping":
            if key == pygame.K_RETURN:
                print("We Detected RETURN!")

        if new_item != self.current_item:
            if self.list_items[new_item] not in self.disabled_items:
                self.current_item = new_item

    def get_current_item(self):
        return self.list_items[self.current_item]

    def get_current_index(self):
        return self.current_item

    def draw(self, canvas):

        for index, item in enumerate(self.list_items):
            my = self.y + (index * (self.item_images[item].get_height() * 2))
            canvas.blit(self.item_images[item], (self.x, my))
            if self.current_item == index and self.active:
                pygame.draw.rect(canvas, self.text_color, (self.x - 20, my + 5, 10, 10))