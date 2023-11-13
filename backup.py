import pygame
from settings import *

class BATSMAN(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.animation_state = "start"

        # start animation images
        batsman_start_1 = pygame.image.load('graphics/batsman/start/frame-1.png').convert_alpha()
        batsman_start_2 = pygame.image.load('graphics/batsman/start/frame-2.png').convert_alpha()
        batsman_start_3 = pygame.image.load('graphics/batsman/start/frame-3.png').convert_alpha()
        batsman_start_4 = pygame.image.load('graphics/batsman/start/frame-4.png').convert_alpha()

        # start animation images - transformed
        batsman_start_1 = pygame.transform.scale(batsman_start_1, (260,180))
        batsman_start_2 = pygame.transform.scale(batsman_start_2, (260,180))
        batsman_start_3 = pygame.transform.scale(batsman_start_3, (260,180))
        batsman_start_4 = pygame.transform.scale(batsman_start_4, (260,180))
        
        # waiting animation images
        batsman_waiting_1 = pygame.image.load('graphics/batsman/waiting/frame-1.png').convert_alpha()
        batsman_waiting_2 = pygame.image.load('graphics/batsman/waiting/frame-2.png').convert_alpha()
        batsman_waiting_3 = pygame.image.load('graphics/batsman/waiting/frame-3.png').convert_alpha()

        # waiting animation images - transformed
        batsman_waiting_1 = pygame.transform.scale(batsman_waiting_1, (260,180))
        batsman_waiting_2 = pygame.transform.scale(batsman_waiting_2, (260,180))
        batsman_waiting_3 = pygame.transform.scale(batsman_waiting_3, (260,180))

        # start animation order
        self.batsman = [
            batsman_start_1, batsman_start_2, batsman_start_3, 
            batsman_start_4, batsman_waiting_2, batsman_waiting_3]
        self.player_index = 0
		
        self.image = self.batsman[self.player_index]  
        self.rect = self.image.get_rect(midbottom=pitch_mid_point)

    def animation(self):

        if self.animation_state == "start":
            if self.player_index < 1: self.player_index += 0.01
            elif 1 <= self.player_index < 4: self.player_index += 0.2 
            elif self.player_index >= 4: self.animation_state = "waiting"

        elif self.animation_state == "waiting":
            self.player_index += 0.02
            if self.player_index >= len(self.batsman): self.player_index = 4
        
        self.image = self.batsman[int(self.player_index)]

    def update(self):
        self.animation()


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
