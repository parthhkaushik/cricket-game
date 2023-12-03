import pygame
from sys import exit
from game import *

# intialise pygame
pygame.init()

screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()

icon = pygame.image.load("graphics/logo.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Cricket 2023")


class MAIN(object):

    def __init__(self):
        self.running = True

        self.img1 = pygame.image.load("graphics/start-screen.png")
        self.img1 = pygame.transform.scale(self.img1,(screen_width,screen_height))

        self.img2 = pygame.image.load("graphics/home-screen.png")
        self.img2 = pygame.transform.scale(self.img2,(screen_width,screen_height))

        self.menu1 = pygame.image.load("graphics/menu-1.png")
        self.menu1 = pygame.transform.scale(self.menu1,(300,105))
        self.menu2 = pygame.image.load("graphics/menu-2.png")
        self.menu2 = pygame.transform.scale(self.menu2,(300,105))
        self.menu3 = pygame.image.load("graphics/menu-3.png")
        self.menu3 = pygame.transform.scale(self.menu3,(300,105))
        
        
        # variables
        MAIN.dt = 0
        MAIN.game_state = "start"
        MAIN.flag = 0

    def RUN(self):
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN])
        while self.running:

            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if MAIN.game_state == "home":
                        x, y = event.pos
                        if screen.blit(self.menu1,(110,100)).collidepoint(x, y):
                            MAIN.game_state = "exhibition"
                        elif screen.blit(self.menu2,(110,240)).collidepoint(x, y):
                            MAIN.game_state = "easy"
                        elif screen.blit(self.menu3,(110,380)).collidepoint(x, y):
                            MAIN.game_state = "hard"
                        
                    elif MAIN.game_state in ["exhibition", "easy", "hard"]:
                        x, y = event.pos
                        if screen.blit(GAME.pause,(screen_width-80-10,10)).collidepoint(x, y):
                            MAIN.old_game_state = MAIN.game_state
                            MAIN.game_state = "pause"


                if event.type == pygame.KEYDOWN:

                    if MAIN.game_state == "start" and not PROGRESS_BAR.loading: 
                        MAIN.game_state = "home"

                    elif event.key == pygame.K_SPACE and MAIN.game_state == "pause":
                        MAIN.game_state = MAIN.old_game_state


                if event.type == throw_ball_event:
                    BALL().select_pos() 
                    GAME.ball.add(BALL())
                    NON_STRIKER.can_move = True
                    GAME.show_circle = True

                if event.type == next_ball_event:
                    GAME.next_ball_event = True

                if event.type == game_won_event:
                    MAIN.game_state = "won"

                elif event.type == game_lost_event:
                    MAIN.game_state = "lost"

                elif event.type == exhibition_event:
                    MAIN.game_state = "end"
            

            # main game
            if MAIN.game_state in ["exhibition", "easy", "hard"]:

                if not MAIN.flag:
                    GAME().match_type(MAIN.game_state)
                    MAIN.flag = 1
                GAME().RUN(screen)

            elif MAIN.game_state == "pause":
                # pause screen
                img = pygame.image.load("graphics/pause-screen.png")
                img = pygame.transform.scale(img,(screen_width,screen_height))
                screen.blit(img,(0,0))
                
            elif MAIN.game_state == "start":
                # start screen
                screen.blit(self.img1,(0,0))

                # message
                PROGRESS_BAR().load(screen,(175,screen_height-30),(450,10))
                if not PROGRESS_BAR.loading:
                    message = "PRESS ANY KEY TO CONTINUE"
                    pos = (screen_width/2+15,screen_height-30)
                    TEXT().blit(message,screen,pos,bounce=True)  

            elif MAIN.game_state == "home":
                # start screen
                screen.blit(self.img2,(0,0))
                
                # statistics
                with open("data/userdata.txt","r") as f:
                    lines = f.readlines()
                    for i in range(len(lines)):
                        pos = (screen_width-175,screen_height-130+16*i)
                        TEXT().blit(lines[i],screen,pos,size=16)

                screen.blit(self.menu1,(110,100))
                screen.blit(self.menu2,(110,240))
                screen.blit(self.menu3,(110,380))
            
            else:
                img = pygame.image.load(f"graphics/{MAIN.game_state}.png")
                img = pygame.transform.scale(img,(screen_width,screen_height))
                screen.blit(img,(0,0))
                


            # updating display
            pygame.display.update()

m = MAIN()
m.RUN()
