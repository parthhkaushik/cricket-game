import pygame
from module import get_frames
from settings import *

class BATSMAN(pygame.sprite.Sprite):
    shot = "stroke"
    direction = "straight"
    t_player_input = 0
    delivery_played = False
    key_pressed = False
    display_runs = False

    """
        SPRITE DESCRIPTION 
        batsman sprite for the player
    """
    def __init__(self):
        super().__init__()

        # class vaiables
        self.sign = 1        
        self.t = 0

        self.animation_state = "start"
        self.update_frames("start")

    """ 
        get the correct images for the animation as frames
        animations have either 4 or 5 frames 
    """
    def update_frames(self, action):

        # dictionary containing frames
        self.frames = get_frames("batsman",action,scale=(225,197))
        self.frame_index = 0

        # animation order
        self.image = self.frames[int(self.frame_index)]  
        self.rect = self.image.get_rect(midbottom=pitch_top_point)

    """
        check player input
    """
    def player_input(self):
        keys = pygame.key.get_pressed()
        if self.animation_state == "waiting":
            if keys[pygame.K_LEFT]:
                BATSMAN.direction = "left"
                BATSMAN.t_player_input = pygame.time.get_ticks()
                self.sign = 1
                BATSMAN.key_pressed = True
            elif keys[pygame.K_DOWN]:
                BATSMAN.direction = "straight"
                BATSMAN.t_player_input = pygame.time.get_ticks()
                self.sign = 1
                BATSMAN.key_pressed = True
            elif keys[pygame.K_RIGHT]:
                BATSMAN.direction = "right"
                BATSMAN.t_player_input = pygame.time.get_ticks()
                self.sign = 1
                BATSMAN.key_pressed = True
                
    
    """
    """
    def play_shot(self):
        self.update_frames(BATSMAN.direction + "-" + BATSMAN.shot)
        self.animation_state = "shot" 
        
            
    """
        get frames according to the animation playing
        to ensure correct order of frames 
    """
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

            if self.sign == -1: 
                self.update_frames("start")
                self.animation_state = "start"
            
            elif self.frame_index >= len(self.frames)-1: 
                self.sign = 0
                self.t += 1
                BATSMAN.delivery_played = True
            
            # time delay after last frame
            if self.t >= 300: 
                self.sign = -1
                self.t = 0
                BATSMAN.delivery_played = False
                BATSMAN.display_runs = False
            elif self.t >= 120:
                BATSMAN.display_runs = True

            # updating the frame
            self.frame_index += self.sign*0.25

        # updating the image 
        self.image = self.frames[int(self.frame_index)]  
        self.rect = self.image.get_rect(midbottom=pitch_top_point)

    """
        to update the sprite
        60 frames per second
        1 frame - 1.66 second
    """
    def update(self):
        self.animation()
        self.player_input()
            


class NON_STRIKER(pygame.sprite.Sprite):

    can_move = False

    def __init__(self):
        super().__init__()
        self.pos = (screen_width/2+160,475)
        self.t = 0
        self.update_frames()

    def update_frames(self):
        self.frames = get_frames("batsman","non-striker",(115,220))
        self.frame_index = 0
        
        self.image = self.frames[int(self.frame_index)]  
        self.rect = self.image.get_rect(midbottom=self.pos)
    
    def animation(self):
        if NON_STRIKER.can_move:
            
            if self.frame_index >= len(self.frames)-1:
                self.t += 1
                # time delay after last frame
                if self.t >= 150:
                    self.t = 0
                    self.update_frames()
                    NON_STRIKER.can_move = False
            
            else: self.frame_index += 0.1

            self.image = self.frames[int(self.frame_index)]  
            self.rect = self.image.get_rect(midbottom=self.pos)

    def update(self):
        self.animation()
