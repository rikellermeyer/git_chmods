#!/usr/bin/env python3

import pygame
import subprocess
import random

# make fighter class

simonisms = ['S H I T', 'Oof', 'great form', 'Yikes', 'wanker',
             'buy me a drink first', 'bloody hell']

class Fighter():
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps):
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.image_offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0 # 0 = idle, 1 = run, 2 = jump, 3 = attack1, 4 = attack 2, 5 = hit, 6 = death
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.hit = False
        self.health = 100
        self.alive = True

    def load_images(self, sprite_sheet, animation_steps):
        #extract images from spritesheet
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_image_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_image_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_image_list)

        return animation_list
    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
        surface.blit(img, (self.rect.x - (self.image_offset[0] * self.image_scale), self.rect.y - (self.image_offset[1] * self.image_scale)))

    def move(self, screen_width, screen_height, surface, target):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        #get keypresses
        key = pygame.key.get_pressed()

        #can only perform other actions if only not attacking
        if self.attacking == False and self.alive == True:
            #check player 1 controls
            if self.player == 1:
            #movement
                if key[pygame.K_a]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_d]:
                    dx = SPEED
                    self.running = True

                #jumping
                if key[pygame.K_w] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True

                #attacks
                if key[pygame.K_r] or key[pygame.K_t]:
                    self.attack(surface, target)

                    #which attack type is used
                    if key[pygame.K_r]:
                        self.attack_type = 1
                    if key[pygame.K_t]:
                        self.attack_type = 2

            #check player 2 controls
            if self.player == 2:
            #movement
                if key[pygame.K_LEFT]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_RIGHT]:
                    dx = SPEED
                    self.running = True

                #jumping
                if key[pygame.K_UP] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True

                #attacks
                if key[pygame.K_KP1] or key[pygame.K_KP2]:
                    self.attack(surface, target)

                    #which attack type is used
                    if key[pygame.K_KP1]:
                        self.attack_type = 1
                    if key[pygame.K_KP2]:
                        self.attack_type = 2

            # apply gravity
            self.vel_y += GRAVITY
            dy += self.vel_y

            #make player stay on screen
            if self.rect.left + dx < 0:
                dx = -self.rect.left
            if self.rect.right + dx > screen_width:
                dx = screen_width - self.rect.right
            if self.rect.bottom + dy > screen_height - 45:
                self.vel_y = 0
                self.jump = False
                dy = screen_height - 45 - self.rect.bottom

            #make players face each other
            if target.rect.centerx > self.rect.centerx:
                self.flip = False
            else:
                self.flip = True

            #apply attack cooldown
            if self.attack_cooldown > 0:
                self.attack_cooldown -= 1

            # update player position
            self.rect.x += dx
            self.rect.y += dy

        #handle animation updates
    def update(self):
        #print(self.hit, self.attacking, self.health, self.jump, self.running, self.action)
        #check what action is being performed
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6) #death
        elif self.hit == True:
            self.update_action(5)
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(3) # attack 1
            elif self.attack_type == 2:
                self.update_action(4) # attack 2
        elif self.jump == True:
            self.update_action(2) #jump
        elif self.running == True:
            self.update_action(1) # run
        else:
            self.update_action(0) #idle

        animation_cooldown = 50
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
            #check if player is alive
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                #check if an attack was executed
                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.attack_cooldown = 20
                #check if damage was take
                if self.action == 5:
                    self.hit = False
                    #if player in middle of attack, stop
                    self.attacking = False
                    self.attack_cooldown = 20

        #define attack method
    def attack(self, surface, target):
        if self.attack_cooldown == 0:
            self.attacking = True
            attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height) #makes attack surface 2x the player
            if attacking_rect.colliderect(target.rect):
                voice_cmd = f'say -v Daniel "{random.choice(simonisms)}"'
                subprocess.Popen(voice_cmd, shell=True)
                target.health -= 10
                target.hit = True

            pygame.draw.rect(surface, (0, 255, 0), attacking_rect)

    def update_action(self, new_action):
        #check if new action is different than previous
        if new_action != self.action:
            self.action = new_action
            #update animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()



