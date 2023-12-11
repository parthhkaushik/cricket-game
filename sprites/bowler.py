import pygame
from settings import *


""" bowler sprite for the computer """

class BOWLER(pygame.sprite.Sprite):

    flag = 0
    t_ball_released = 0

    def __init__(self):
        super().__init__()  

        # class variables
        self.pos = (over_the_wicket, screen_height-40)      
        self.t1,self.t2 = 0,0
        self.wait = True

        self.animation_state = "fast"
        self.update_frames("fast")


    """ methods """ 

    def throw_ball(self):
        if int(self.frame_index) == 19:
            if not BOWLER.flag:
                pygame.event.post(pygame.event.Event(throw_ball_event))
                BOWLER.t_ball_released = pygame.time.get_ticks()
                BOWLER.flag = 1


    def update_frames(self, action):

        # dictionary containing frames
        self.frames = get_frames("bowler",action,(355,400))
        self.frame_index = 0

        # animation order
        self.image = self.frames[int(self.frame_index)]  
        self.rect = self.image.get_rect(midbottom=self.pos)


    def animation(self):
              
        # time delay before bowling
        if self.t1 <= 240: self.t1 +=1
        else:
            
            if self.frame_index >= len(self.frames)-1: 
                
                if self.t2 <= 240: self.t2 += 1
                else:
                    pygame.event.post(pygame.event.Event(next_ball_event))
                    self.frame_index = 0
                    self.t1,self.t2 = 0,0
                    BOWLER.flag = 0
                    BOWLER.next_ball_event = False
                
            else: self.frame_index += 0.25
        
        # updating the image 
        self.image = self.frames[int(self.frame_index)]  
        self.rect = self.image.get_rect(midbottom=self.pos)


    """ update sprite """
    def update(self):
        self.animation()
        self.throw_ball()