import pygame, random
from settings import *
from scoreboard import *

# importing sprites
from sprites.ball import *
from sprites.batsman import *
from sprites.bowler import *


# intialise pygame
pygame.init()

screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()

icon = pygame.image.load("graphics/logo.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Cricket 2023")





class Game():

    # variables
    next_ball_event = False
    dt,dr = 0,0
    total_overs = ""
    runs_scored = 0
    show_circle = False
    six_count = 0
    
    # images
    pitch = pygame.image.load('graphics/background.jpg')
    pitch = pygame.transform.scale(pitch,(screen_width,screen_height))

    logo = pygame.image.load("graphics/cricket'23.png")
    logo = pygame.transform.scale(logo,(180,30))
    pause = pygame.image.load("graphics/pause.png")
    pause = pygame.transform.scale(pause,(80,30))

    umpire = pygame.image.load("graphics/umpire.png")
    umpire = pygame.transform.scale(umpire,(80,215))
    
    wickets = pygame.image.load("graphics/wickets-1.png")
    wickets = pygame.transform.scale(wickets,(64,80))

    circle = pygame.image.load("graphics/target.png")
    circle = pygame.transform.scale(circle,(30,15))

    # sprites
    all_sprites = pygame.sprite.Group()
    all_sprites.add(BATSMAN(),NON_STRIKER(),BOWLER())
    ball = pygame.sprite.GroupSingle()

    def setup():
        pass

    def run(self, target):

        target.blit(Game.pitch,(0,0))
        target.blit(Game.wickets,(screen_width/2-25,105))

        # other objects
        target.blit(Game.pause,(screen_width-80-10,10))
        blit_alpha(target, Game.logo, (10,10), 128)

        # player and computer sprites
        Game.all_sprites.draw(target)
        for sprite in Game.all_sprites.sprites():
            sprite.update()
        target.blit(Game.umpire,umpire_pos)
        
        if Game.show_circle: target.blit(Game.circle,BALL.circle_pos)

        Game.ball.draw(target)
        Game.ball.update()
                
        # displaying the sccoreboard
        SCOREBOARD().blit(target, Game.total_overs) 

        Game.dt += 1
        if Game.dt >= 420:
            if not BATSMAN.delivery_played: Game.check_wicket()
            Game.display_runs(Game.runs_scored,target) 

        if Game.next_ball_event:
            BATSMAN.next_ball_event = True
            BOWLER.next_ball_event = True
            NON_STRIKER.next_ball_event = True
            Game.dt = 0
            SCOREBOARD().update(Game.runs_scored, Game.six_count)
            Game.next_ball_event = False
            Game.show_circle = False

        if BATSMAN.key_pressed:
            Game.check_runs_scored()
            Game.all_sprites.sprites()[0].play_shot()
            BALL.shot = BATSMAN.shot
            BALL.delivery_played = True
            BATSMAN.key_pressed = False 
                

    """ methods """

    def match_type(self, match_type):
        if match_type == "exhibition":
            Game.total_overs = "5"
            SCOREBOARD.target_runs = None
        else:
            Game.total_overs = "10"
            if match_type == "easy":
                SCOREBOARD.target_runs = random.randint(75,120)
            elif match_type == "hard":
                SCOREBOARD.target_runs = random.randint(190,250)

    def check_runs_scored():
        Game.dr = BATSMAN.t_player_input-BOWLER.t_ball_released

        # checking the player input
        if BATSMAN.direction == BALL.direction:

            if 100 <= Game.dr <= 400:
                Game.runs_scored = 6
                BATSMAN.shot = "loft"
                Game.six_count += 1

            elif 0 <= Game.dr <= 410:
                Game.runs_scored = "Catch-Out"
                BATSMAN.shot = "loft"

            elif 0 <= Game.dr <= 475:
                Game.runs_scored = 4
                BATSMAN.shot = "stroke"

            elif 0 <= Game.dr <= 550:
                Game.runs_scored = random.choice([1,1,1,2,2,3])
                BATSMAN.shot = "stroke"
            
            else: Game.check_wicket()

        else: Game.check_wicket() 
        BALL.runs_scored = Game.runs_scored


    def check_wicket():

        if BALL.direction != "straight":

            if -220 <= Game.dr <= 220 and BATSMAN.direction == BALL.direction:
                Game.runs_scored = "Caught"
            else: 
                Game.runs_scored = 0
                BALL.delivery_played = True
        
        else: 
            Game.runs_scored = "Bowled"
            BATSMAN.shot = "stroke"


    def display_runs(runs,target):
    
        rect = pygame.Rect(screen_width/2-100,screen_height/2-125,200,250)
        pygame.draw.rect(target,"#343434",rect)
        rect = pygame.Rect(screen_width/2-100,screen_height/2-90,200,180)
        pygame.draw.rect(target,"#B22222",rect)

        # displaying text by checking the runs scored
        if runs == 0:
            TEXT().blit("DOT",target,(screen_width/2,screen_height/2-30),50,"Action_Man")
            TEXT().blit("BALL",target,(screen_width/2,screen_height/2+30),50,"Action_Man")
        
        elif runs in ["Bowled","Catch-Out","Caught"]:
            match runs:
                case "Bowled":
                    TEXT().blit("BOWLED",target,(screen_width/2,screen_height/2),50,"Action_Man")
                case "Catch-Out":
                    TEXT().blit("CATCH",target,(screen_width/2,screen_height/2-30),50,"Action_Man")
                    TEXT().blit("OUT",target,(screen_width/2,screen_height/2+30),50,"Action_Man")
                case "Caught":
                    TEXT().blit("CAUGHT",target,(screen_width/2,screen_height/2),50,"Action_Man")

        else:
            match runs:
                case 6: txt = "SIX"
                case 4: txt = "FOUR"
                case 3: txt = "TRIPLE"
                case 2: txt = "DOUBLE"
                case 1: txt = "SINGLE"
            TEXT().blit(str(runs),target,(screen_width/2,screen_height/2-20),132)
            TEXT().blit(txt,target,(screen_width/2,screen_height/2+60),50,"Action_Man")


class Main(object):

    def __init__(self):
        self.running = True

        self.img1 = pygame.image.load("graphics/start-screen.png")
        self.img1 = pygame.transform.scale(self.img1,(screen_width,screen_height))

        self.img2 = pygame.image.load("graphics/home-screen.png")
        self.img2 = pygame.transform.scale(self.img2,(screen_width,screen_height))

        self.menu1 = pygame.image.load("graphics/menu-1.png")
        self.menu1 = pygame.transform.scale(self.menu1,(360,128))
        self.menu2 = pygame.image.load("graphics/menu-2.png")
        self.menu2 = pygame.transform.scale(self.menu2,(360,128))
        self.menu3 = pygame.image.load("graphics/menu-3.png")
        self.menu3 = pygame.transform.scale(self.menu3,(360,128))

        self.bg_music = pygame.mixer.Sound('audio\My Type - Saint Motel.mp3')
        self.bg_music.set_volume(0.25)
        self.bg_music_playing = False
        
        
        # variables
        Main.dt = 0
        Main.game_state = "start"
        Main.match_type = None
        Main.flag = 0

    def run(self):
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN])
        while self.running:

            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if Main.game_state == "home":
                        x, y = event.pos
                        if screen.blit(self.menu1,(18,154)).collidepoint(x, y):
                            Main.match_type = "exhibition"
                            Main.game_state = "game"
                        elif screen.blit(self.menu2,(18,300)).collidepoint(x, y):
                            Main.match_type = "easy"
                            Main.game_state = "game"
                        elif screen.blit(self.menu3,(18,448)).collidepoint(x, y):
                            Main.match_type = "hard"
                            Main.game_state = "game"
                        
                    elif Main.game_state == "game":
                        x, y = event.pos
                        if screen.blit(Game.pause,(screen_width-80-10,10)).collidepoint(x, y):
                            Main.game_state = "pause"


                if event.type == pygame.KEYDOWN:

                    if Main.game_state == "start" and not PROGRESS_BAR.loading: 
                        Main.game_state = "home"

                    elif event.key == pygame.K_SPACE and Main.game_state == "pause":
                        Main.game_state = "game"


                if event.type == throw_ball_event:
                    BALL().select_pos() 
                    Game.ball.add(BALL())
                    NON_STRIKER.can_move = True
                    Game.show_circle = True

                if event.type == next_ball_event:
                    Game.next_ball_event = True

                if event.type == game_won_event:
                    Main.game_state = "won"

                elif event.type == game_lost_event:
                    Main.game_state = "lost"

                elif event.type == exhibition_event:
                    Main.game_state = "end"

            # main game
            if Main.game_state == "game":

                if self.bg_music_playing:
                    self.bg_music.stop()
                    self.bg_music_playing = False

                if not Main.flag: 
                    Game().match_type(Main.match_type)
                    Main.flag = 1
                self.music_paused = False
                Game().run(screen)

            elif Main.game_state == "pause":
                # pause screen
                img = pygame.image.load("graphics/pause-screen.png")
                img = pygame.transform.scale(img,(screen_width,screen_height))
                screen.blit(img,(0,0))
                
            elif Main.game_state == "start":
                # start screen
                screen.blit(self.img1,(0,0))

                # message
                PROGRESS_BAR().load(screen,(205,screen_height-50),(380,15))
                if not PROGRESS_BAR.loading:
                    message = "PRESS ANY KEY TO CONTINUE"
                    pos = (screen_width/2,screen_height-50)
                    TEXT().blit(message,screen,pos,bounce=True)  
                    if not self.bg_music_playing:
                        self.bg_music.play(loops=-1)
                        self.bg_music_playing = True

            elif Main.game_state == "home":
                # start screen
                screen.blit(self.img2,(0,0))
                
                # statistics
                with open("data/userdata.txt","r") as f:
                    lines = f.readlines()
                    for i in range(len(lines)):
                        pos = (screen_width-200,screen_height-160+30*i)
                        TEXT().blit(lines[i],screen,pos,size=25,color=(255,255,255))

                screen.blit(self.menu1,(18,154))
                screen.blit(self.menu2,(18,300))
                screen.blit(self.menu3,(18,448))
            
            else:
                img = pygame.image.load(f"graphics/{Main.game_state}.png")
                img = pygame.transform.scale(img,(screen_width,screen_height))
                screen.blit(img,(0,0))
                


            # updating display
            pygame.display.update()

Main().run()
pygame.quit()