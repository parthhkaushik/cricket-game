import pygame
from pygame.locals import FULLSCREEN,DOUBLEBUF

# importing other files
from assets.scripts.game import *
from assets.scripts.settings import *

# initialise pygame
pygame.init()

flags = FULLSCREEN | DOUBLEBUF
screen = pygame.display.set_mode((screen_width,screen_height), flags, 16)
clock = pygame.time.Clock()

icon = pygame.image.load("assets/icons/logo.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Cricket '23")

# variables
dt = 0
game_state = "start"
match_type = None
flag = 0
team = None
match_result = None

# functions
def return_to_mainmenu():
    global game_state
    game_state = "game-select"
    global flag
    flag = 0
    crowd.stop()
    global crowd_noise_playing
    crowd_noise_playing = False
    music.play(loops=-1)
    global music_playing
    music_playing = True
    Game.all_sprites.empty()
    Game.ball.empty()


# background images
start_bg = pygame.image.load("assets/images/background/start-screen.png").convert()
start_bg = pygame.transform.scale(start_bg,(screen_width,screen_height))

game_select_bg = pygame.image.load("assets/images/background/menu-1.png").convert()
game_select_bg = pygame.transform.scale(game_select_bg,(screen_width,screen_height))

team_select_bg = pygame.image.load("assets/images/background/menu-2.png").convert()
team_select_bg = pygame.transform.scale(team_select_bg,(screen_width,screen_height))

pause_bg = pygame.image.load("assets/images/background/pause-screen.png").convert()
pause_bg = pygame.transform.scale(pause_bg,(screen_width,screen_height))

help_bg = pygame.image.load("assets/images/background/help-screen.png").convert()
help_bg = pygame.transform.scale(help_bg,(screen_width,screen_height))   

scorecard_bg = pygame.image.load("assets/images/background/scorecard.png").convert()
scorecard_bg = pygame.transform.scale(scorecard_bg,(screen_width,screen_height))   

# buttons images
exit_img = pygame.image.load("assets/images/buttons/exit.jpg").convert()
exit_img = pygame.transform.scale(exit_img,(80,30))
back_img = pygame.image.load("assets/images/buttons/back.jpg").convert()
back_img = pygame.transform.scale(back_img,(80,30))
cont_img = pygame.image.load("assets/images/buttons/continue.jpg").convert()
cont_img = pygame.transform.scale(cont_img,(175,55))
help_img = pygame.image.load("assets/images/buttons/help.jpg").convert()
help_img = pygame.transform.scale(help_img,(175,55))
menu_img = pygame.image.load("assets/images/buttons/quit.jpg").convert()
menu_img = pygame.transform.scale(menu_img,(175,55))
scorecard_img = pygame.image.load("assets/images/buttons/scorecard.png").convert()
scorecard_img = pygame.transform.scale(scorecard_img,(175,55))
 
# sounds
crowd = pygame.mixer.Sound('assets/audio/crowd noise.mp3')
crowd.set_volume(0.15)
crowd_noise_playing = False

# music
music = pygame.mixer.Sound('assets/audio/music (My Type).mp3')
music.set_volume(0.25)
music_playing = False

# menu-1 images
button1 = pygame.image.load("assets/images/buttons/worldcup.png").convert()
button1 = pygame.transform.scale(button1,(373,128))
button2 = pygame.image.load("assets/images/buttons/quickmatch.png").convert()
button2 = pygame.transform.scale(button2,(373,128))
button3 = pygame.image.load("assets/images/buttons/practice.png").convert()
button3 = pygame.transform.scale(button3,(373,128))

# menu-2 images
team1 = pygame.image.load("assets/images/buttons/win.png").convert()
team1 = pygame.transform.scale(team1,(373,128))
team2 = pygame.image.load("assets/images/buttons/eng.png").convert()
team2 = pygame.transform.scale(team2,(373,128))
team3 = pygame.image.load("assets/images/buttons/pak.png").convert()
team3 = pygame.transform.scale(team3,(373,128))
team4 = pygame.image.load("assets/images/buttons/nz.png").convert()
team4 = pygame.transform.scale(team4,(373,128))
team5 = pygame.image.load("assets/images/buttons/ind.png").convert()
team5 = pygame.transform.scale(team5,(373,128))
team6 = pygame.image.load("assets/images/buttons/aus.png").convert()
team6 = pygame.transform.scale(team6,(373,128))


# event loop
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN])
def check_events():
    for event in pygame.event.get():
        global running, match_type, game_state, team, match_result
        if event.type == pygame.QUIT: running = False
        
        # checking for userevents
            
        if event.type == throw_ball_event:
            Ball().select_pos() 
            Game.ball.add(Ball())
            Batsman.non_striker_can_move = True
            Game.show_circle = True

        elif event.type == next_ball_event:
            Game.next_ball_event = True
            crowd.set_volume(0.15)

        elif event.type == game_won_event: 
            game_state = "break"
            match_result = "won"

        elif event.type == game_lost_event: 
            game_state = "break"
            match_result = "lost"

        elif event.type == quickmatch_event: 
            game_state = "break"
            match_result = "end"


        # checking for a button click
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            # if game mode select screen is open
            if game_state == "game-select":
                x, y = event.pos

                # game mode buttons
                if screen.blit(button2,(18,300)).collidepoint(x, y):
                    game_state, match_type, team = "wait", "quickmatch", "OPP" 
                elif screen.blit(button1,(18,154)).collidepoint(x, y):
                    game_state = "team-select"
                elif screen.blit(button3,(18,448)).collidepoint(x, y):
                    game_state, match_type, team = "wait", "practice", "OPP"

                # quit button
                elif screen.blit(exit_img, (screen_width-100, 88)).collidepoint(x, y):
                    running = False
            
            # if team/difficulty select screen is open
            elif game_state == "team-select":
                x, y = event.pos

                # team buttons
                if screen.blit(team1,(18,154)).collidepoint(x, y):
                    game_state, match_type, team = "wait", "very easy", "WIN"
                elif screen.blit(team2,(410,154)).collidepoint(x, y):
                    game_state, match_type, team = "wait", "easy", "ENG"
                elif screen.blit(team3,(18,300)).collidepoint(x, y):
                    game_state, match_type, team = "wait", "medium", "PAK"
                elif screen.blit(team4,(410,300)).collidepoint(x, y):
                    game_state, match_type, team = "wait", "medium", "NZ"
                elif screen.blit(team5,(18,448)).collidepoint(x, y):
                    game_state, match_type, team = "wait", "hard", "IND"
                elif screen.blit(team6,(410,448)).collidepoint(x, y):
                    game_state, match_type, team = "wait", "very hard", "AUS"

                # back button
                elif screen.blit(back_img, (screen_width-100, 88)).collidepoint(x, y):
                    game_state = "game-select"
            
            # if the cricket game is active
            elif game_state == "game":
                x, y = event.pos

                # pause button
                if screen.blit(Game.pause,(screen_width-80-10,10)).collidepoint(x, y):
                    game_state = "pause"

            # if the game is paused
            elif game_state == "pause":
                x, y = event.pos

                # pause screen buttons
                if screen.blit(cont_img, (160, 240)).collidepoint(x, y):
                    game_state = "game"
                elif screen.blit(help_img, (160, 340)).collidepoint(x, y):
                    game_state = "help"
                elif screen.blit(scorecard_img, (460, 240)).collidepoint(x, y):
                    game_state = "scorecard"
                elif screen.blit(menu_img, (460, 340)).collidepoint(x, y):
                    return_to_mainmenu()
            
            # if the help/controls screen is open
            elif game_state == "help":
                x, y = event.pos

                # back button
                if screen.blit(back_img,(screen_width-80-30,screen_height-50)).collidepoint(x, y):
                    game_state = "pause"
                
            elif game_state == "scorecard":
                x, y = event.pos

                # back button
                if screen.blit(back_img,(screen_width-80-30,screen_height-50)).collidepoint(x, y):
                    game_state = "pause"
        

        # checking for a key press
        elif event.type == pygame.KEYDOWN:
            
            # start screen
            if game_state == "start" and not PROGRESS_BAR.loading: 
                game_state = "game-select"
            
            # wait screen (help screen)
            elif game_state == "wait": game_state = "game"

            # scorecard (after match is over)
            elif game_state == "break": 
                game_state = match_result

            # results screen
            elif game_state in ["end","won","lost"]: return_to_mainmenu()


# main game loop
running = True
while running:
    # checking for the events
    check_events()


    # checking the game state
    if game_state == "start":

        # start screen
        screen.blit(start_bg,(0,0))

        # message
        PROGRESS_BAR().load(screen,(205,screen_height-50),(380,15))
        if not PROGRESS_BAR.loading:
            # you can start the game when the progress has completed loading
            message = "PRESS ANY KEY TO CONTINUE"
            pos = (screen_width/2,screen_height-50)
            TEXT().blit(message,screen,pos,bounce=True)  
            if not music_playing:
                music.play(loops=-1)
                music_playing = True
          
                
    # if the game select screen is open
    elif game_state == "game-select":
        # start screen
        screen.blit(game_select_bg,(0,0))
        screen.blit(exit_img, (screen_width-100, 88))
        
        # statistics
        with open("assets/data/userdata.txt","r") as f:
            lines = f.readlines()
            for i in range(len(lines)):
                pos = (screen_width-200,screen_height-162+32*i)
                TEXT().blit(lines[i],screen,pos,size=23,color=(255,255,255))

        screen.blit(button1,(18,154))
        screen.blit(button2,(18,300))
        screen.blit(button3,(18,448))
    

    # if the team/difficulty select screen is open
    elif game_state == "team-select":
        # start screen
        screen.blit(team_select_bg,(0,0))
        screen.blit(back_img, (screen_width-100, 88))

        screen.blit(team1,(18,154))
        screen.blit(team3,(18,300))
        screen.blit(team5,(18,448))

        screen.blit(team2,(410,154))
        screen.blit(team4,(410,300))
        screen.blit(team6,(410,448))


    # if the wait sceen/ help screen is open
    elif game_state == "wait":
        screen.blit(help_bg,(0,0))

        # message
        message = "PRESS ANY KEY TO CONTINUE"
        pos = (screen_width/2,screen_height-50)
        TEXT().blit(message,screen,pos,bounce=True)  

        if music_playing:
            music.stop()
            music_playing = False
    
    
    # if the cricket game is active
    elif game_state == "game":

        if Game.runs_scored != 0 and Ball.delivery_played:
            crowd.set_volume(0.4)

        if not crowd_noise_playing:
            crowd.play(loops=-1)
            crowd_noise_playing = True

        if not flag: 
            Game().setup()
            Game().match_type(match_type, team)
            flag = 1
        Game().run(screen)


    # if the game is paused
    elif game_state == "pause":
        screen.blit(pause_bg,(0,0))
        screen.blit(cont_img, (160, 240))
        screen.blit(scorecard_img, (460, 240))
        screen.blit(help_img, (160, 340))
        screen.blit(menu_img, (460, 340))

    # if the scorecard is open
    elif game_state == "scorecard" or game_state == "break":
        screen.blit(scorecard_bg,(0,0))

        if game_state == "scorecard":
            screen.blit(back_img, (screen_width-80-30, screen_height-50))
        else:
            # message
            message = "PRESS ANY KEY TO CONTINUE"
            pos = (screen_width/2,screen_height-50)
            TEXT().blit(message,screen,pos)

        for i in range(len(Game.scorecard)):
            TEXT().blit(Game.scorecard[i][0],screen,(112,240+22*i),size=15,align="left") 
            if str(Game.scorecard[i][2]) == "0": continue
            pos = (screen_width-270,240+22*i)
            TEXT().blit(str(Game.scorecard[i][1]),screen,pos,size=15)    
            pos = (screen_width-195,240+22*i)
            TEXT().blit(str(Game.scorecard[i][2]),screen,pos,size=15)    
            pos = (screen_width-125,240+22*i)
            TEXT().blit(str(Game.scorecard[i][3]),screen,pos,size=15) 
            pos = (screen_width-310,240+22*i)
            TEXT().blit(str(Game.scorecard[i][4]),screen,pos,size=15,align="right")

        pos = (screen_width-160,screen_height-98)
        TEXT().blit(Scoreboard.current_runs,screen,pos,20,color=(255,255,255))
        pos = (screen_width-270,screen_height-98)
        TEXT().blit(Scoreboard.current_overs,screen,pos,20,color=(255,255,255))


    # if the help/controls screen is open
    elif game_state == "help":
        screen.blit(help_bg,(0,0))
        screen.blit(back_img, (screen_width-80-30, screen_height-50))

    
    else:
        img = pygame.image.load(f"assets/images/background/{game_state}.png").convert()
        img = pygame.transform.scale(img,(screen_width,screen_height))
        screen.blit(img,(0,0))

        # message
        message = "PRESS ANY KEY TO CONTINUE"
        pos = (screen_width/2,screen_height-50)
        TEXT().blit(message,screen,pos,bounce=True)
                

    # 60 frames/second
    clock.tick(60)
    # updating display
    pygame.display.update()