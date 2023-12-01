import pygame, random
from module import *
from settings import *

class BOWLER(pygame.sprite.Sprite):
    t_ball_released = 0

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
            BOWLER.t_ball_released = pygame.time.get_ticks()

    """
        to update the sprite
        60 frames per second
        1 frame - 1.66 second
    """
    def update(self):
        self.animation()
        self.throw_ball()


class BALL(pygame.sprite.Sprite):
    delivery_played = False
    shot="loft"
    direction = "straight"

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("graphics/white-ball.png")
        self.image = pygame.transform.scale(self.image,(8,8))
        self.rect = self.image.get_rect(midbottom=ball_release_pt)
        BALL.rebound = False
        
        self.points = [{"dx":(4.5,-0.5),"dy":(2,3),"length":210,"shot_dir":"straight"}]
        points = [
            {"dx":(4.5,-0.5),"dy":(2,3),"length":210,"shot_dir":"straight"},
            {"dx":(6,1),"dy":(1,6),"length":230,"shot_dir":"right"},
            {"dx":(3,0.5),"dy":(2,4),"length":220,"shot_dir":"left"}
            ]
        self.d = random.choice(self.points)
        BALL.direction = self.d["shot_dir"]
    
    def move(self):
        hit_pos = shots[BALL.direction+"-"+BALL.shot]["hit_pos"]
            
        if self.rect.y >= self.d["length"]:
            self.rect.x += self.d["dx"][0]
            self.rect.y -= self.d["dy"][0]
        
        else:
            self.rect.x += self.d["dx"][1]
            self.rect.y -= self.d["dy"][1]

        if BALL.delivery_played:

            if self.rect.y <= hit_pos:
                self.d = random.choice(self.points)
                BALL.delivery_played = False
                self.kill()

            elif self.rect.y <= 0:
                self.d = random.choice(self.points)
                BALL.delivery_played = False
                self.kill()
        
        else:
            
            if self.rect.y <= 140:
                if BALL.direction == "straight":
                    self.d = random.choice(self.points)
                    self.kill()

    def update(self):
        if BALL.rebound:
            self.rect.x += 1.5
            self.rect.y += 4
        else: self.move()