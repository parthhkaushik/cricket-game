import pygame

# importing other files
from game import *
from settings import *

# initialise pygame
pygame.init()

screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()

icon = pygame.image.load("graphics/logo.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Cricket '23")

# music
music = pygame.mixer.Sound('audio\\music (My Type).mp3')
music.set_volume(0.25)
music_playing = False  

# sounds
crowd = pygame.mixer.Sound('audio\\crowd noise.mp3')
crowd.set_volume(0.15)
crowd_noise_playing = False

# images
start_img = pygame.image.load("graphics/start-screen.png")
start_img = pygame.transform.scale(start_img,(screen_width,screen_height))

menu1_bg = pygame.image.load("graphics/menu/bg1.png")
menu1_bg = pygame.transform.scale(menu1_bg,(screen_width,screen_height))

menu2_bg = pygame.image.load("graphics/menu/bg2.png")
menu2_bg = pygame.transform.scale(menu2_bg,(screen_width,screen_height))

button1 = pygame.transform.scale(pygame.image.load("graphics/menu/worldcup.png"),(373,128))
button2 = pygame.transform.scale(pygame.image.load("graphics/menu/quickmatch.png"),(373,128))
button3 = pygame.transform.scale(pygame.image.load("graphics/menu/practice.png"),(373,128))    

back = pygame.transform.scale(pygame.image.load("graphics/back.jpg"),(80,30))
cont = pygame.transform.scale(pygame.image.load("graphics/continue.jpg"),(175,55))
help = pygame.transform.scale(pygame.image.load("graphics/help.jpg"),(175,55))
menu = pygame.transform.scale(pygame.image.load("graphics/quit.jpg"),(175,55))

team1 = pygame.transform.scale(pygame.image.load("graphics/menu/win.png"),(373,128))
team2 = pygame.transform.scale(pygame.image.load("graphics/menu/eng.png"),(373,128))
team3 = pygame.transform.scale(pygame.image.load("graphics/menu/pak.png"),(373,128))
team4 = pygame.transform.scale(pygame.image.load("graphics/menu/nz.png"),(373,128))
team5 = pygame.transform.scale(pygame.image.load("graphics/menu/ind.png"),(373,128))
team6 = pygame.transform.scale(pygame.image.load("graphics/menu/aus.png"),(373,128))
        
# variables
dt = 0
game_state = "start"
match_type = None
flag = 0
team = None

running = True
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN])


def check_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            global running, match_type, game_state, team
            running = False
        
        # checking for events
        if event.type == pygame.MOUSEBUTTONDOWN:

            if game_state == "menu1":
                x, y = event.pos
                if screen.blit(button2,(18,300)).collidepoint(x, y):
                    game_state, match_type, team = "game", "quickmatch", "" 
                elif screen.blit(button1,(18,154)).collidepoint(x, y):
                    game_state = "menu2"
                elif screen.blit(button3,(18,448)).collidepoint(x, y):
                    game_state, match_type, team = "game", "practice", ""
            
            elif game_state == "menu2":
                x, y = event.pos
                if screen.blit(team1,(18,154)).collidepoint(x, y):
                    game_state, match_type, team = "game", "very easy", "WIN"
                elif screen.blit(team2,(410,154)).collidepoint(x, y):
                    game_state, match_type, team = "game", "easy", "ENG"
                elif screen.blit(team3,(18,300)).collidepoint(x, y):
                    game_state, match_type, team = "game", "medium", "PAK"
                elif screen.blit(team4,(410,300)).collidepoint(x, y):
                    game_state, match_type, team = "game", "medium", "NZ"
                elif screen.blit(team5,(18,448)).collidepoint(x, y):
                    game_state, match_type, team = "game", "hard", "IND"
                elif screen.blit(team6,(410,448)).collidepoint(x, y):
                    game_state, match_type, team = "game", "very hard", "AUS"
                
                elif screen.blit(back, (screen_width-100, 88)).collidepoint(x, y):
                    game_state = "menu1"
                    
                        
            elif game_state == "game":
                x, y = event.pos
                if screen.blit(Game.pause,(screen_width-80-10,10)).collidepoint(x, y):
                    game_state = "pause"

            elif game_state == "pause":
                x, y = event.pos
                if screen.blit(cont, (160, 240)).collidepoint(x, y):
                    game_state = "game"
                elif screen.blit(help, (460, 240)).collidepoint(x, y):
                    game_state = "help"
                elif screen.blit(menu, (160, 340)).collidepoint(x, y):
                    game_state = "menu1"
                    global flag, crowd_noise_playing, music_playing
                    flag = 0
                    crowd.stop()
                    crowd_noise_playing = False
                    music.play(loops=-1)
                    music_playing = True
                    Game.all_sprites.empty()
                    Game.ball.empty()
            
            elif game_state == "help":
                x, y = event.pos
                if screen.blit(back,(screen_width-80-30,screen_height-50)).collidepoint(x, y):
                    game_state = "pause"
            
        elif event.type == pygame.KEYDOWN:
            if game_state == "start" and not PROGRESS_BAR.loading: game_state = "menu1"
                    
        
        # checking for userevents
        if event.type == throw_ball_event:
            BALL().select_pos() 
            Game.ball.add(BALL())
            NON_STRIKER.can_move = True
            Game.show_circle = True

        elif event.type == next_ball_event:
            Game.next_ball_event = True
            crowd.set_volume(0.15)

        elif event.type == game_won_event:
            game_state = "won"

        elif event.type == game_lost_event:
            game_state = "lost"

        elif event.type == quickmatch_event:
            game_state = "end"


# main game loop
while running:
    check_events()

    # main game
    if game_state == "game":

        if Game.runs_scored != 0 and BALL.delivery_played:
            crowd.set_volume(0.4)

        if music_playing:
            music.stop()
            music_playing = False

        if not crowd_noise_playing:
            crowd.play(loops=-1)
            crowd_noise_playing = True

        if not flag: 
            Game().setup()
            Game().match_type(match_type, team)
            flag = 1
        Game().run(screen)

    elif game_state == "pause":
        # pause screen
        img = pygame.image.load("graphics/pause-screen.png")
        img = pygame.transform.scale(img,(screen_width,screen_height))
        screen.blit(img,(0,0))

        screen.blit(cont, (160, 240))
        screen.blit(help, (460, 240))
        screen.blit(menu, (160, 340))
    
    elif game_state == "help":
        # pause screen
        img = pygame.image.load("graphics/help-screen.png")
        img = pygame.transform.scale(img,(screen_width,screen_height))
        screen.blit(img,(0,0))
        screen.blit(back, (screen_width-80-30, screen_height-50))
                
    elif game_state == "start":
        # start screen
        screen.blit(start_img,(0,0))

        # message
        PROGRESS_BAR().load(screen,(205,screen_height-50),(380,15))
        if not PROGRESS_BAR.loading:
            message = "PRESS ANY KEY TO CONTINUE"
            pos = (screen_width/2,screen_height-50)
            TEXT().blit(message,screen,pos,bounce=True)  
            if not music_playing:
                music.play(loops=-1)
                music_playing = True

    elif game_state == "menu1":
        # start screen
        screen.blit(menu1_bg,(0,0))
                
        # statistics
        with open("data/userdata.txt","r") as f:
            lines = f.readlines()
            for i in range(len(lines)):
                pos = (screen_width-200,screen_height-160+30*i)
                TEXT().blit(lines[i],screen,pos,size=24,color=(255,255,255))

        screen.blit(button1,(18,154))
        screen.blit(button2,(18,300))
        screen.blit(button3,(18,448))
    
    elif game_state == "menu2":
        # start screen
        screen.blit(menu2_bg,(0,0))
        screen.blit(back, (screen_width-100, 88))

        screen.blit(team1,(18,154))
        screen.blit(team3,(18,300))
        screen.blit(team5,(18,448))

        screen.blit(team2,(410,154))
        screen.blit(team4,(410,300))
        screen.blit(team6,(410,448))

    else:
        img = pygame.image.load(f"graphics/{game_state}.png")
        img = pygame.transform.scale(img,(screen_width,screen_height))
        screen.blit(img,(0,0))
                
    # 60 frames per second
    clock.tick(60)
    # updating display
    pygame.display.update()