import pygame
from settings import *

# FUNCTIONS

def get_frames(player,action,scale=None):
    # taking all the frames in a dictionary
    frames, c = {}, 0
    while True:
        try:
            file = f'graphics/{player}/{action}/frame-{c+1}.png'
            frame = pygame.image.load(file).convert_alpha()
            if scale != None:
                frame = pygame.transform.scale(frame, scale)
            frames[c] = frame
            c+=1
        except: break
    return frames


# SPRITES

class BATSMAN(pygame.sprite.Sprite):

    """
        SPRITE DESCRIPTION 
        a single batsman sprite for the player
    """
    def __init__(self):
        super().__init__()

        # class vaiables
        self.sign = 1        
        self.t = 0
        self.key_pressed = False

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
        if keys[pygame.K_SPACE] and self.animation_state == "waiting":
            self.update_frames("straight-loft")
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
        self.rect = self.image.get_rect(midbottom=pitch_top_point)

    """
        to update the sprite
        60 frames per second
        1 frame - 1.66 second
    """
    def update(self):
        self.animation()
        self.player_input()



class BOWLER(pygame.sprite.Sprite):

    """
        SPRITE DESCRIPTION 
        a single bowler sprite for the computer
    """
    def __init__(self):
        super().__init__()  

        # class variables
        self.pos = (over_the_wicket, screen_height)      
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
        to update the sprite
        60 frames per second
        1 frame - 1.66 second
    """
    def update(self):
        self.animation()



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
