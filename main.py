from game import *

class MAIN():
    run = True

    screen = pygame.display.set_mode((screen_width,screen_height))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Cricket 2023")

    img = pygame.image.load("graphics/home-screen.png")
    img = pygame.transform.scale(img,(screen_width,screen_height))
    
    # variables
    dt = 0
    game_active = True

    def RUN(self):
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, THROW_BALL])
        while MAIN.run:
            MAIN.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == THROW_BALL:
                    GAME.ball.add(BALL())
                    NON_STRIKER.can_move = True                 
                if event.type == pygame.KEYDOWN and not MAIN.game_active:
                    MAIN.game_active = True
        
            if MAIN.game_active:
                GAME().RUN(MAIN.screen)
                
            else:
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