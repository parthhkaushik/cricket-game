import pygame, random
from settings import *


""" ball sprite """

class BALL(pygame.sprite.Sprite):

    delivery_played = False
    shot = "stroke"
    direction = "straight"
    runs_scored = 0
    circle_pos = None
    point = None

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("graphics/white-ball.png")
        self.image = pygame.transform.scale(self.image,(8,8))
        self.rect = self.image.get_rect(midbottom=ball_release_pt)


    """ methods """

    def select_pos(self):
        self.points = [
            {"dx":(3.5,-0.5),"dy":(1,3),"length":222,"shot_dir":"straight", "circle_pos":(392,220)},
            {"dx":(6,0),"dy":(1,3),"length":225,"shot_dir":"right", "circle_pos":(418,222)},
            {"dx":(3,-0.5),"dy":(1,3),"length":225,"shot_dir":"left", "circle_pos":(360,222)}
            ]
        BALL.point = random.choice(self.points)
        BALL.direction = BALL.point["shot_dir"]
        BALL.circle_pos = BALL.point["circle_pos"]

    def move(self):
        hit_pos = shots[BALL.direction+"-"+BALL.shot]["hit_pos"]
            
        if self.rect.y >= BALL.point["length"]:
            self.rect.x += BALL.point["dx"][0]
            self.rect.y -= BALL.point["dy"][0]
        
        else:
            self.rect.x += BALL.point["dx"][1]
            self.rect.y -= BALL.point["dy"][1]

        if BALL.delivery_played:

            if BALL.runs_scored == "Bowled":
                if self.rect.y <= 145:
                    BALL.delivery_played = False
                    self.kill()

            elif self.rect.y <= hit_pos:
                BALL.delivery_played = False
                self.kill()

            elif self.rect.y <= 0:
                BALL.delivery_played = False
                self.kill()
        
        else:
            
            if self.rect.y <= 140:
                if BALL.direction == "straight":
                    self.kill()

    """ update sprite """
    def update(self): 
        self.move()