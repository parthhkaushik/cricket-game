import pygame, random
from module import *
from settings import *

# VARIABLES
t_ball_released = 0

# USER EVENTS
THROW_BALL = pygame.USEREVENT +1


class BOWLER(pygame.sprite.Sprite):

    """
        SPRITE DESCRIPTION 
        bowler sprite for the computer
    """
    def __init__(self):
        super().__init__()  

        # class variables
        self.pos = (over_the_wicket, screen_height-40)      
        self.t = 0
        self.wait = True

        self.animation_state = "fast"
        self.update_frames("fast")

    """ 
        get the correct images for the animation as frames
        bowling animations have around 30 frames
    """
    def update_frames(self, action):

        # dictionary containing frames
        self.frames = get_frames("bowler",action,(355,400))
        self.frame_index = 0

        # animation order
        self.image = self.frames[int(self.frame_index)]  
        self.rect = self.image.get_rect(midbottom=self.pos)

    """
        get frames according to the animation playing
        to ensure correct order of frames 
    """
    def animation(self):
        
        if self.wait:
            self.t +=1
            if self.t >= 300:
                self.t = 0
                self.wait = False

        else:
            if self.frame_index >= len(self.frames)-1: 
                self.t += 1
                
                # time delay after last frame
                if self.t >= 180: 
                    self.wait = True
                    self.frame_index = 0
                    self.t = 0
                
            else: self.frame_index += 0.25
        
        # updating the image 
        self.image = self.frames[int(self.frame_index)]  
        self.rect = self.image.get_rect(midbottom=self.pos)

    """
    """
    def throw_ball(self):
        if int(self.frame_index) == 19:
            pygame.event.post(pygame.event.Event(THROW_BALL))
            global t_ball_released
            t_ball_released = pygame.time.get_ticks()
            print(t_ball_released)

    """
        to update the sprite
        60 frames per second
        1 frame - 1.66 second
    """
    def update(self):
        self.animation()
        self.throw_ball()


class BALL(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("graphics/white-ball.png")
        self.image = pygame.transform.scale(self.image,(8,8))
        self.rect = self.image.get_rect(midbottom=ball_release_pt)
        
        self.points = [{"dx":(3.5,-0.5),"dy":(2,3),"length":210,"shot_dir":"straight-1"}]
        points = [
            {"dx":(1.5,-0.5),"dy":(1,3),"length":210,"shot_dir":"straight-1"},
            {"dx":(3.5,0),"dy":(1,3),"length":215,"shot_dir":"right-1"},
            {"dx":(1.5,0),"dy":(1.5,3),"length":225,"shot_dir":"left-1"}
            ]
        self.d = random.choice(self.points)
    
    def update(self):
        
        if self.rect.y >= self.d["length"]:
            self.rect.x += self.d["dx"][0]
            self.rect.y -= self.d["dy"][0]
        else:
            self.rect.x += self.d["dx"][1]
            self.rect.y -= self.d["dy"][1]

        if self.rect.y <= 175:
            self.d = random.choice(self.points)
            self.kill()