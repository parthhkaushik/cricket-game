import pygame
from settings import *


# SPRITES

class BATSMAN(pygame.sprite.Sprite):

    """
        SPRITE DESCRIPTION 
        a single sprite for the player
    """
    def __init__(self):
        super().__init__()
        self.animation_state = "start"
        self.get_frames("batsman", "start")

        # class vaiables
        self.sign = 1        
        self.t = 0
        self.key_pressed = False

    """ 
        get the correct images for the animation as frames
        anomations have either 4 or 5 frames 
    """
    def get_frames(self, player, action):

        # dictionary containing frames
        self.frames = {}
        self.frame_index = 0

        # taking all the frames in a dictionary
        c = 0
        while True:
            try:
                file = f'graphics/{player}/{action}/frame-{c+1}.png'
                frame = pygame.image.load(file).convert_alpha()
                frame = pygame.transform.scale(frame, (225,197))
                self.frames[c] = frame
                c+=1
            except: break

        # animation order
        self.image = self.frames[int(self.frame_index)]  
        self.rect = self.image.get_rect(midbottom=pitch_mid_point)

    """
        check player input
    """
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.animation_state == "waiting":
            self.get_frames("batsman", "straight-loft")
            self.animation_state = "shot" 
            self.sign = 1

    """
        get frames according to the animation playing
        to ensure correct order of frames 
    """
    def animation(self):

        if self.animation_state == "start":
            if self.frame_index < 1: self.frame_index += 0.01
            elif 1 <= self.frame_index < 3: self.frame_index += 0.2 
            elif self.frame_index >= 3: 
                self.get_frames("batsman", "waiting")
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
                self.get_frames("batsman", "start")
                self.animation_state = "start"
                self.key_pressed = False
            
            elif self.frame_index >= len(self.frames)-1: 
                self.sign = 0
                self.t += 1

            # time delay after last frame
            if self.t >= 150: 
                self.sign = -1
                self.t = 0

            # updating the frame
            self.frame_index += self.sign*0.25

        # updating the image 
        self.image = self.frames[int(self.frame_index)]  
        self.rect = self.image.get_rect(midbottom=pitch_mid_point)

    """
        to update the sprite
        60 frames per second
        1 frame - 1.66 second
    """
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
