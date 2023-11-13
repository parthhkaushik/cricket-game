import pygame
from settings import *
from time import sleep

class BATSMAN(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.animation_state = "start"
        self.get_frames("batsman", "start")
        self.sign = 1        
        self.t = 0
        self.key_pressed = False

    def get_frames(self, player, action):

        self.frame_1 = pygame.image.load(f'graphics/{player}/{action}/frame-1.png').convert_alpha()
        self.frame_2 = pygame.image.load(f'graphics/{player}/{action}/frame-2.png').convert_alpha()
        self.frame_3 = pygame.image.load(f'graphics/{player}/{action}/frame-3.png').convert_alpha()
        self.frame_4 = pygame.image.load(f'graphics/{player}/{action}/frame-4.png').convert_alpha()
        try: self.frame_5 = pygame.image.load(f'graphics/{player}/{action}/frame-5.png').convert_alpha()
        except: self.frame_5 = ""

        self.frame_1 = pygame.transform.scale(self.frame_1, (260,180))
        self.frame_2 = pygame.transform.scale(self.frame_2, (260,180))
        self.frame_3 = pygame.transform.scale(self.frame_3, (260,180))
        self.frame_4 = pygame.transform.scale(self.frame_4, (260,180))
        if self.frame_5 != "": self.frame_5 = pygame.transform.scale(self.frame_5, (260,180))

        # start animation order
        self.player_index = 0
        self.batsman = [self.frame_1, self.frame_2, self.frame_3, self.frame_4, self.frame_5]
        self.image = self.batsman[int(self.player_index)]  
        self.rect = self.image.get_rect(midbottom=pitch_mid_point)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.key_pressed = True

    def animation(self):

        if self.animation_state == "start":
            if self.player_index < 1: self.player_index += 0.01
            elif 1 <= self.player_index < 3: self.player_index += 0.2 
            elif self.player_index >= 3: 
                self.get_frames("batsman", "waiting")
                self.animation_state = "waiting"

        elif self.animation_state == "waiting":
            
            if self.player_index <= 0: 
                self.sign = 1
            elif self.player_index >= 2.5: 
                self.sign = 0
                self.t += 1

            if self.t >= 90: 
                self.sign = -1
                self.t = 0
            
            if self.key_pressed and int(self.player_index) == 0:
                self.get_frames("batsman", "straight-stroke")
                self.animation_state = "shot" 
                self.sign = 1

            self.player_index += self.sign * 0.2

        elif self.animation_state == "shot":

            if self.sign == -1: 
                self.get_frames("batsman", "start")
                self.animation_state = "start"
                self.key_pressed = False

            elif self.player_index >= 4.5: 
                self.sign = 0
                self.t += 1

            if self.t >= 120: 
                self.sign = -1
                self.t = 0

            self.player_index += self.sign*0.2
                
        self.image = self.batsman[int(self.player_index)]  
        self.rect = self.image.get_rect(midbottom=pitch_mid_point)
               
    def update(self):
        self.animation()
        self.player_input()


class BOWLER(pygame.sprite.Sprite):
    def __init__(self, type):
        pass

    def update(self):
        pass


class BALL(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("graphics/cricket-ball.png")
        self.image = pygame.transform.scale(self.image, (12,12))
        self.rect = self.image.get_rect(midbottom=(375,380))
    
    def update(self):
        if self.rect.y >= 250:
            self.rect.y += -5
            self.rect.x += 0.5
        else:
            self.rect.y += -5
            self.rect.x -= 0.5

        if self.rect.y <= 175:
            self.kill()
