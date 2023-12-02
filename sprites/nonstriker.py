import pygame
from module import get_frames
from settings import *


""" non striker sprite """

class NON_STRIKER(pygame.sprite.Sprite):

    next_ball_event = False
    can_move = False

    def __init__(self):
        super().__init__()
        self.pos = (screen_width/2+160,475)
        self.t = 0

        self.frames = get_frames("batsman","non-striker",(115,220))
        self.frame_index = 0

        self.image = self.frames[int(self.frame_index)]  
        self.rect = self.image.get_rect(midbottom=self.pos)


    """ methods """

    def animation(self):
        if NON_STRIKER.can_move:
            
            if self.frame_index <= len(self.frames)-1:
                self.frame_index += 0.1

        self.image = self.frames[int(self.frame_index)]  
        self.rect = self.image.get_rect(midbottom=self.pos)


    def update(self): 
        self.animation()
        if NON_STRIKER.next_ball_event:
            self.frame_index = 0
            NON_STRIKER.can_move = False
            NON_STRIKER.next_ball_event = False