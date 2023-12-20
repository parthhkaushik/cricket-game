import pygame, random
from assets.scripts.settings import *


""" batsman sprite for the player """

class Batsman(pygame.sprite.Sprite):
    
    # class vaiables
    shot, direction = "stroke", "straight"
    t_player_input = 0
    delivery_played = False
    key_pressed = False
    non_striker_can_move = False
    next_ball_event = False

    def __init__(self, non_striker=False):
        super().__init__()
        self.non_striker = non_striker
        
        if non_striker:
            self.pos = (screen_width/2+160,475)
            self.t = 0
            self.animation_state = "non-striker"
            self.update_frames("non-striker",(115,220))
        
        else:
            self.pos = pitch_top_point
            self.sign, self.t = 1, 0
            self.animation_state = "start"
            self.update_frames("start")

    
    # methods

    def update_frames(self, action, scale=(225,197)):

        # dictionary containing frames
        self.frames = get_frames("batsman",action,scale)
        self.frame_index = 0

        # animation order
        self.image = self.frames[int(self.frame_index)]  
        self.rect = self.image.get_rect(midbottom=self.pos)


    def player_input(self):
        keys = pygame.key.get_pressed()
        if self.animation_state == "waiting":
            if keys[pygame.K_LEFT] or keys[pygame.K_DOWN] or keys[pygame.K_RIGHT]:
                Batsman.t_player_input = pygame.time.get_ticks()
                self.sign = 1
                Batsman.key_pressed = True
                
                if keys[pygame.K_LEFT]:
                    Batsman.direction = "left"
                elif keys[pygame.K_DOWN]:
                    Batsman.direction = "straight"
                elif keys[pygame.K_RIGHT]:
                    Batsman.direction = "right"
                
    
    def play_shot(self):
        self.update_frames(Batsman.direction + "-" + Batsman.shot)
        self.animation_state = "shot" 
        
            
    def animation(self):

        # if the batsman is non striker
        if self.animation_state == "non-striker":

            if Batsman.non_striker_can_move:
                
                if self.frame_index <= len(self.frames)-1:
                    self.frame_index += 0.1

        # when the batsman is starting the over
        elif self.animation_state == "start":

            if self.frame_index < 1: self.frame_index += 0.01
            elif 1 <= self.frame_index < 3: self.frame_index += 0.2 
            elif self.frame_index >= 3: 
                self.update_frames("waiting")
                self.animation_state = "waiting"

        # when the batsman is waiting for the ball
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

        # when the batsman is playing shot
        elif self.animation_state == "shot":
            
            if self.frame_index >= len(self.frames)-1: 
                self.sign = 0
                self.t += 1
                Batsman.delivery_played = True

            # updating the frame
            self.frame_index += self.sign*0.25

        # updating the image 
        self.image = self.frames[int(self.frame_index)]  
        self.rect = self.image.get_rect(midbottom=self.pos)


    """ update sprite """
    def update(self):
        self.animation()
        if not self.non_striker: self.player_input()

        if Batsman.next_ball_event:
            if self.non_striker:
                Batsman.non_striker_can_move = False
                self.frame_index = 0
                Batsman.next_ball_event = False 
            else:
                self.sign, self.t = -1, 0
                self.update_frames("start")
                self.animation_state = "start"
                Batsman.delivery_played = False    
            




""" bowler sprite for the computer """

class Bowler(pygame.sprite.Sprite):

    # class variables
    flag, t_ball_released = 0, 0

    def __init__(self):
        super().__init__()  
        self.pos = (over_the_wicket, screen_height-40)      
        self.t1,self.t2 = 0,0
        self.animation_state = "fast"
        self.update_frames("fast")


    # methods

    def throw_ball(self):
        if int(self.frame_index) == 19:
            if not Bowler.flag:
                pygame.event.post(pygame.event.Event(throw_ball_event))
                Bowler.t_ball_released = pygame.time.get_ticks()
                Bowler.flag = 1

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
                    Bowler.flag = 0

            else: self.frame_index += 0.25
        
        # updating the image 
        self.image = self.frames[int(self.frame_index)]  
        self.rect = self.image.get_rect(midbottom=self.pos)


    """ update sprite """
    def update(self):
        self.animation()
        self.throw_ball()





""" ball sprite """

class Ball(pygame.sprite.Sprite):

    # class variables
    delivery_played = False
    direction, shot = "straight", "stroke"
    runs_scored = 0
    point, circle_pos = None, None

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/images/ground/white-ball.png")
        self.image = pygame.transform.scale(self.image,(8,8))
        self.sound = pygame.mixer.Sound('assets/audio/ball hitting bat.mp3')
        self.rect = self.image.get_rect(midbottom=ball_release_pt)


    # methods

    def select_pos(self):
        """ select the direction of the ball """

        Ball.point = random.choice(ball_points)
        Ball.circle_pos = Ball.point["circle_pos"]
        Ball.direction = Ball.point["shot_dir"]


    def update(self):
        """ update the position of the ball """
        
        hit_pos = shots[Ball.direction+"-"+Ball.shot]["hit_pos"]
            
        if self.rect.y >= Ball.point["length"]:
            self.rect.x += Ball.point["dx"][0]
            self.rect.y -= Ball.point["dy"][0]
        
        else:
            self.rect.x += Ball.point["dx"][1]
            self.rect.y -= Ball.point["dy"][1]

        if Ball.delivery_played:

            if Ball.runs_scored == "Bowled":
                if self.rect.y <= 145:
                    Ball.delivery_played = False
                    self.kill()
                    
                    self.sound.set_volume(0.15)
                    self.sound.play()

            elif self.rect.y <= hit_pos and Ball.runs_scored not in [0,"Bowled","Caught"]:
                Ball.delivery_played = False
                self.kill()
                self.sound.set_volume(0.15)
                self.sound.play()

            elif self.rect.y <= 0:
                Ball.delivery_played = False
                self.kill()

        else:
            if Ball.direction == "straight":
                if self.rect.y <= 140:
                    self.kill()          