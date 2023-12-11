import pygame
from module import TEXT
from settings import *

class TIMING_BAR():
    # class vairables
    p = {"x":screen_width-220, "y":50}
    s = {"w":210, "h":10}
    txt_pos = [(screen_width-200,65),(screen_width-110,65),(screen_width-30,65)]

    # displaying the timing bar
    def blit(self,target):
        rect = pygame.Rect(TIMING_BAR.p["x"],TIMING_BAR.p["y"],TIMING_BAR.s["w"],TIMING_BAR.s["h"])
        pygame.draw.rect(target,colors["hex"]["charcoal"],rect)
        TEXT().blit("EARLY",target,TIMING_BAR.txt_pos[0],12,color=colors["rgb"]["white"])
        TEXT().blit("PERFECT",target,TIMING_BAR.txt_pos[1],12,color=colors["rgb"]["white"])
        TEXT().blit("LATE",target,TIMING_BAR.txt_pos[2],12,color=colors["rgb"]["white"])

    # updating the timing
    def update(self,target,timing,sign=0):
        if timing == 3:
            color = colors["hex"]["lime_green"]
            x,y = screen_width-120,50
        elif timing == 2:
            color = colors["hex"]["yellow"]
            x,y = screen_width-abs(sign*240-150),50
        elif timing == 1:
            color = colors["hex"]["dark_orange"]
            x,y = screen_width-abs(sign*250-180),50
        else:
            color = colors["hex"]["brick_red"]
            x,y = screen_width-abs(sign*250-210),50

        rect = pygame.Rect(x,y,20,10)
        pygame.draw.rect(target,color,rect)