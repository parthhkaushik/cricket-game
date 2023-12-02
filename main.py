from time import sleep
from game import *

class MAIN():
    run = True

    screen = pygame.display.set_mode((screen_width,screen_height))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Cricket 2023")

    img = pygame.image.load("graphics/home-screen.png")
    img = pygame.transform.scale(img,(screen_width,screen_height))

    pause_screen = pygame.image.load("graphics/pause-screen.png")
    pause_screen = pygame.transform.scale(pause_screen,(screen_width,screen_height))
    
    # variables
    dt = 0
    game_state = "home"

    def RUN(self):
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN])
        while MAIN.run:
            MAIN.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == throw_ball_event:
                    BALL().select_pos() 
                    GAME.ball.add(BALL())
                    NON_STRIKER.can_move = True
                    GAME.show_circle = True
                if event.type == pygame.KEYDOWN:
                    if MAIN.game_state == "home": MAIN.game_state = "game"
                    if event.key == pygame.K_SPACE and MAIN.game_state == "pause":
                        MAIN.game_state = "game"

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if MAIN.screen.blit(GAME.pause,(screen_width-80-10,10)).collidepoint(x, y):
                        MAIN.game_state = "pause"

                if event.type == next_ball_event:
                    GAME.next_ball_event = True
        
            if MAIN.game_state == "game":
                GAME().RUN(MAIN.screen)

            elif MAIN.game_state == "pause":
                # pause screen
                MAIN.screen.blit(MAIN.pause_screen,(0,0))
                
            elif MAIN.game_state == "home":
                # home screen
                MAIN.screen.blit(MAIN.img,(0,0))

                # message
                PROGRESS_BAR().load(MAIN.screen,(175,screen_height-30),(450,10))
                if not PROGRESS_BAR.loading:
                    message = "PRESS ANY KEY TO CONTINUE"
                    pos = (screen_width/2+15,screen_height-30)
                    TEXT().blit(message,MAIN.screen,pos,bounce=True)   
                    
            # updating display
            pygame.display.update()

MAIN().RUN()