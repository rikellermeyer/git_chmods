import pygame
import config


class Player:

    def __init__(self, x_position, y_position):
        self.position = [x_position, y_position]
        print('player created')
        self.image = pygame.image.load("/Users/student/PycharmProjects/pythonProject/git_chmods/main/overworld_files/images/player.png")
        self.image = pygame.transform.scale(self.image, (config.SCALE, config.SCALE))
        self.rect = pygame.Rect(self.position[0] * config.SCALE, self.position[1] * config.SCALE, config.SCALE, config.SCALE)

    def update(self):
        print('player updated')

    def render(self, screen):
        screen.blit(self.image, self.rect)



    def update_position(self, new_position):
        self.position[0] = new_position[0]
        self.position[1] = new_position[1]
        self.rect = pygame.Rect(self.position[0] * config.SCALE, self.position[1] * config.SCALE, config.SCALE, config.SCALE)


class NPC:

    def __init__(self, x_position, y_position, image_file):
        self.position = [x_position, y_position]
        print('NPC created')
        self.image = pygame.image.load(image_file)
        self.image = pygame.transform.scale(self.image, (config.SCALE, config.SCALE))
        self.rect = pygame.Rect(self.position[0] * config.SCALE, self.position[1] * config.SCALE, config.SCALE, config.SCALE)

    def update(self):
        print('player updated')

    def render(self, screen):
        screen.blit(self.image, self.rect)



    def update_position(self, new_position):
        self.position[0] = new_position[0]
        self.position[1] = new_position[1]
        self.rect = pygame.Rect(self.position[0] * config.SCALE, self.position[1] * config.SCALE, config.SCALE, config.SCALE)

