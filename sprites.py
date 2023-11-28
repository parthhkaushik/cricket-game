import pygame, random
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


# USER EVENTS
THROW_BALL = pygame.USEREVENT +1


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
        self.points = [
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