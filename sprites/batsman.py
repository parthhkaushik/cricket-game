import pygame
from module import get_frames
from settings import *


""" batsman sprite for the player """

class BATSMAN(pygame.sprite.Sprite):
    
    shot = "stroke"
    direction = "straight"
    t_player_input = 0
    delivery_played = False
    key_pressed = False
    next_ball_event = False

    def __init__(self):
        super().__init__()

        # class vaiables
        self.sign = 1        
        self.t = 0

        self.animation_state = "start"
        self.update_frames("start")

    
    """ methods"""

    def update_frames(self, action):

        # dictionary containing frames
        self.frames = get_frames("batsman",action,scale=(225,197))
        self.frame_index = 0

        # animation order
        self.image = self.frames[int(self.frame_index)]  
        self.rect = self.image.get_rect(midbottom=pitch_top_point)


    def player_input(self):
        keys = pygame.key.get_pressed()
        if self.animation_state == "waiting":
            if keys[pygame.K_LEFT] or keys[pygame.K_DOWN] or keys[pygame.K_RIGHT]:
                BATSMAN.t_player_input = pygame.time.get_ticks()
                self.sign = 1
                BATSMAN.key_pressed = True
                
                if keys[pygame.K_LEFT]:
                    BATSMAN.direction = "left"
                elif keys[pygame.K_DOWN]:
                    BATSMAN.direction = "straight"
                elif keys[pygame.K_RIGHT]:
                    BATSMAN.direction = "right"
                
    
    def play_shot(self):
        self.update_frames(BATSMAN.direction + "-" + BATSMAN.shot)
        self.animation_state = "shot" 
        
            
    def animation(self):

        if self.animation_state == "start":
            if self.frame_index < 1: self.frame_index += 0.01
            elif 1 <= self.frame_index < 3: self.frame_index += 0.2 
            elif self.frame_index >= 3: 
                self.update_frames("waiting")
                self.animation_state = "waiting"

        elif self.animation_state == "waiting":

            if self.frame_index <= 0: 
                self.sign = 1

            elif self.frame_index >= 2: 
                self.sign = 0
                self.t += 1

            # time delay after frame-3              
            if self.t >= 90: 
                self.sign = -1
                self.t = 0
                
            # updating the frame
            self.frame_index += self.sign * 0.2

        elif self.animation_state == "shot":
            
            if self.frame_index >= len(self.frames)-1: 
                self.sign = 0
                self.t += 1
                BATSMAN.delivery_played = True

            # updating the frame
            self.frame_index += self.sign*0.25

        # updating the image 
        self.image = self.frames[int(self.frame_index)]  
        self.rect = self.image.get_rect(midbottom=pitch_top_point)


    """ update sprite """
    def update(self):
        self.animation()
        self.player_input()

        if BATSMAN.next_ball_event:
            self.sign, self.t = -1, 0
            self.update_frames("start")
            self.animation_state = "start"
            BATSMAN.delivery_played = False
            BATSMAN.next_ball_event = False
            