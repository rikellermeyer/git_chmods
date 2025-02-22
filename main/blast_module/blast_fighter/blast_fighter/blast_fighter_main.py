#!/usr/bin/env python3

import pygame
import subprocess
import sys
import time

from pygame.surface import Surface, SurfaceType

from fighters import Fighter

pygame.init()

# create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen: Surface | SurfaceType = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Blast Brawl')

# set framerate
clock = pygame.time.Clock()
FPS = 60

#define colors
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

#define game variables
#intro_count = 3
#last_count_update = pygame.time.get_ticks()
score = [0, 0] #player score
round_over = False
ROUND_OVER_COOLDOWN = 2000
end_str = 'FATALITY'

#define fighter variables
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [108, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]
WARRIOR_SIZE = 150
WARRIOR_SCALE = 3.5
WARRIOR_OFFSET = [66, 45]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]

# load background image
bg_image = pygame.image.load('/Users/student/PycharmProjects/pythonProject/git_chmods/main/blast_module/blast_fighter/assets/images/background/8pixel_lab.jpg').convert_alpha()

#load spritesheets
wizard_sheet = pygame.image.load('/Users/student/PycharmProjects/pythonProject/git_chmods/main/blast_module/blast_fighter/assets/images/wizard/Wizard_fin.png').convert_alpha()
warrior_sheet = pygame.image.load('/Users/student/PycharmProjects/pythonProject/git_chmods/main/blast_module/blast_fighter/assets/images/warrior/warrior.png').convert_alpha()


#define number of steps in each animation
WIZARD_ANIMATION_STEPS = [8, 8, 2, 8, 8, 3, 7]
WARRIOR_ANIMATION_STEPS = [8, 6, 4, 6, 6, 3, 7]

#define fonts
count_font = pygame.font.Font('/Users/student/PycharmProjects/pythonProject/git_chmods/main/blast_module/blast_fighter/assets/images/Font/Turok.ttf', 80)
health_bar_font = pygame.font.Font('/Users/student/PycharmProjects/pythonProject/git_chmods/main/blast_module/blast_fighter/assets/images/Font/Turok.ttf', 30)
end_font = pygame.font.Font('/Users/student/PycharmProjects/pythonProject/git_chmods/main/blast_module/blast_fighter/assets/images/Font/Turok.ttf', 80)

#function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# add a fxn for drawing background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

#fxn for drawing health
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 3, y - 3, 406, 36))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))


# create 2 instances of fighters
fighter_1 = Fighter(1, 200, 1, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS)
fighter_2 = Fighter(2, 700, 375, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS)

# create game loop
count = 0
run = True
while run:

    #set framerate
    clock.tick(FPS)

    # draw background
    draw_bg()

    #draw health bar
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 580, 20)

    #move fighters
    fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2)
    fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1)

    #update countdown
    #if intro_count <= 0:
     #   fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2)
      #  fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1)
    #else:
        #display count timer
     #   draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH /2, SCREEN_HEIGHT / 3)
        #update count timer
      #  if (pygame.time.get_ticks() - last_count_update) >= 1000:
       #     intro_count -= 1
        #    last_count_update = pygame.time.get_ticks()


    #update fighters
    fighter_1.update()
    fighter_2.update()

    # draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    #check for player dead
    if round_over == False:
        if fighter_1.alive == False:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif fighter_2.alive == False:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
        draw_text(end_str, end_font, RED, SCREEN_WIDTH/3, SCREEN_HEIGHT/3)
    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # update display
    pygame.display.update()

    if not count:
        voice_cmd = 'say -v Daniel "hello, this is Simon, ' \
                   + 'the wizard of Cold Spring Harbor Laboratory. ' \
                  + 'Prepare for me to BLAST your ass."'
        subprocess.Popen(voice_cmd, shell=True)
        count += 1

# exit pygame
pygame.quit()
