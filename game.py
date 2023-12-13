import pygame, random
from settings import *

# importing sprites
from sprites.batsman import *
from sprites.bowler import *
from sprites.ball import *


class SCOREBOARD():

    target_runs = 1
    current_runs = "0/0"
    current_overs = "0.0"
    runs_in_over = []
    six_count = 0
    balls_left = 60
    runs_left = 0

    def blit(self,target,total_overs,team):
        scoreboard = pygame.Rect(0,screen_height-scoreboard_height,screen_width,scoreboard_height)
        pygame.draw.rect(target,"#343434",scoreboard)
        
        # rectangles
        rect = pygame.Rect(10,screen_height-scoreboard_height+5,50,scoreboard_height-5)
        pygame.draw.rect(target,"#ff8c00",rect)
        rect = pygame.Rect(100,screen_height-scoreboard_height+5,120,scoreboard_height-5)
        pygame.draw.rect(target,"#B22222",rect)
        rect = pygame.Rect(260,screen_height-scoreboard_height+5,40,scoreboard_height-5)
        pygame.draw.rect(target,"#ff8c00",rect)
        for i in range(6):
            rect = pygame.Rect(600+i*32,screen_height-scoreboard_height+5,30,scoreboard_height-5)
            pygame.draw.rect(target,"#ff8c00",rect)
        
        # runs in over
        pos = (615+16*(len(SCOREBOARD.runs_in_over)-1),screen_height-15)
        TEXT().blit("     ".join(SCOREBOARD.runs_in_over),target,pos,16,color=(255,255,255))
        
        # target
        rect = pygame.Rect(screen_width-220,10,120,30)
        pygame.draw.rect(target,"#343434",rect)

        # text 
        TEXT().blit("VS",target,(80,screen_height-15),16,color=(255,255,255))
        s = f"ALL {SCOREBOARD.current_runs}"
        TEXT().blit(s,target,(160,screen_height-15),16,color=(255,255,255))
        TEXT().blit(SCOREBOARD.current_overs,target,(240,screen_height-15),16,color=(255,255,255))
        TEXT().blit(total_overs,target,(280,screen_height-15),16,color=(255,255,255))
        if SCOREBOARD.target_runs == None: 
            TEXT().blit("OPP",target,(35,screen_height-15),16,color=(255,255,255))
            txt1 = "NO TARGET"
            with open("data/userdata.txt","r") as f:
                lines = f.readlines()
                txt2 = "YOUR PREVIOUS HIGHSCORE IS " + lines[2].split()[4]
        else: 
            txt1 = f"TARGET : {SCOREBOARD.target_runs}"
            txt2 = "NEED " + str(SCOREBOARD.runs_left) + " RUNS OFF " + str(SCOREBOARD.balls_left) + " BALLS"
            TEXT().blit(team,target,(35,screen_height-15),16,color=(255,255,255))

        TEXT().blit(txt1,target,(screen_width-160,25),16,color=(255,255,255))
        TEXT().blit(txt2,target,(450,screen_height-15),16,color=(255,255,255))
        


    def update(self, runs_scored, six_count):
        # current runs
        if runs_scored in ["Bowled","Catch-Out","Caught"]:
            SCOREBOARD.current_runs = SCOREBOARD.current_runs[:-1]+str(int(SCOREBOARD.current_runs[-1])+1)
            SCOREBOARD.runs_in_over.append("W")               
        else:
            SCOREBOARD.current_runs = str(int(SCOREBOARD.current_runs[:-2])+runs_scored)+SCOREBOARD.current_runs[-2:]
            SCOREBOARD.runs_in_over.append(str(runs_scored))
        
        SCOREBOARD.six_count = six_count

        # over update
        SCOREBOARD.current_overs = str(round(float(SCOREBOARD.current_overs)+0.1,1))
        if SCOREBOARD.current_overs[-1] == "6":
            SCOREBOARD.current_overs = str(round(float(SCOREBOARD.current_overs)))+".0"
            SCOREBOARD.runs_in_over = []
        SCOREBOARD.balls_left -= 1
        if runs_scored in [1,2,3,4,6]: SCOREBOARD.runs_left -= runs_scored
        SCOREBOARD.check_win_loss()
    
    def check_win_loss():
        if SCOREBOARD.target_runs != None:
            # win conditin check
            if int(SCOREBOARD.current_runs[:-2]) >= SCOREBOARD.target_runs:
                pygame.event.post(pygame.event.Event(game_won_event))
                update_stats(won=True, six_count=SCOREBOARD.six_count)

            # loose conditin check
            elif SCOREBOARD.current_overs == "10.0" and int(SCOREBOARD.current_runs[:-2]) <= SCOREBOARD.target_runs:
                pygame.event.post(pygame.event.Event(game_lost_event))
                update_stats(won=False, six_count=SCOREBOARD.six_count)
            elif SCOREBOARD.current_runs[len(SCOREBOARD.current_runs)-2:] == "10":
                pygame.event.post(pygame.event.Event(game_lost_event))
                update_stats(won=False, six_count=SCOREBOARD.six_count) 

        elif Game.matchtype == "quickmatch":
            if SCOREBOARD.current_overs == "5.0":
                pygame.event.post(pygame.event.Event(quickmatch_event))
                update_hs(int(SCOREBOARD.current_runs[:-2]))


class Game():

    next_ball_event = False
    dt,dr = 0,0
    total_overs = ""
    runs_scored = 0
    show_circle = False
    six_count = 0
    sound_playing = False
    team = None
    
    # images
    pitch = pygame.image.load('graphics/background.jpg')
    pitch = pygame.transform.scale(pitch,(screen_width,screen_height))

    logo = pygame.image.load("graphics/cricket'23.png")
    logo = pygame.transform.scale(logo,(180,30))
    pause = pygame.image.load("graphics/buttons/pause.png")
    pause = pygame.transform.scale(pause,(80,30))

    umpire = pygame.image.load("graphics/umpire.png")
    umpire = pygame.transform.scale(umpire,(80,215))
    
    wickets = pygame.image.load("graphics/wickets-1.png")
    wickets = pygame.transform.scale(wickets,(64,80))

    circle = pygame.image.load("graphics/target.png")
    circle = pygame.transform.scale(circle,(30,15))

    all_sprites = pygame.sprite.Group()
    ball = pygame.sprite.GroupSingle()

    def setup(self):

        Game.next_ball_event = False
        Game.dt,Game.dr = 0,0
        Game.total_overs = ""
        Game.runs_scored = 0
        Game.show_circle = False
        Game.six_count = 0
        Game.sound_playing = False
        Game.team = None

        Game.all_sprites.add(BATSMAN(),NON_STRIKER(),BOWLER())

        Game.sound_playing = False
        Game.dt = 0
        Game.next_ball_event = False
        Game.show_circle = False
        
        # scoreboard
        SCOREBOARD.target_runs = 1
        SCOREBOARD.current_runs = "0/0"
        SCOREBOARD.current_overs = "0.0"
        SCOREBOARD.runs_in_over = []
        SCOREBOARD.six_count = 0
        SCOREBOARD.balls_left = 60
        SCOREBOARD.runs_left = 0

        # Batsman
        NON_STRIKER.next_ball_event = True
        NON_STRIKER.can_move = False
        BATSMAN.shot = "stroke"
        BATSMAN.direction = "straight"
        BATSMAN.t_player_input = 0
        BATSMAN.delivery_played = False
        BATSMAN.key_pressed = False
        BATSMAN.next_ball_event = False

        # Bowler
        BOWLER.flag = 0
        BOWLER.t_ball_released = 0

        # Ball
        BALL.delivery_played = False
        BALL.shot = "stroke"
        BALL.direction = "straight"
        BALL.runs_scored = 0
        BALL.circle_pos = None
        BALL.point = None

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
        if Game.matchtype != "practice": 
            SCOREBOARD().blit(target, Game.total_overs, Game.team)
        else:
            scoreboard = pygame.Rect(0,screen_height-scoreboard_height,screen_width,scoreboard_height)
            pygame.draw.rect(target,"#343434",scoreboard)
            TEXT().blit("PRACTICE",target,(150,screen_height-15),16,color=(255,255,255))
            TEXT().blit("SESSION",target,(screen_width-150,screen_height-15),16,color=(255,255,255))

        Game.dt += 1
        if Game.dt >= 420:
            if not BATSMAN.delivery_played: Game.check_wicket()
            Game.display_runs(Game.runs_scored,target) 

        if Game.next_ball_event:
            Game.sound_playing = False
            BATSMAN.next_ball_event = True
            NON_STRIKER.next_ball_event = True
            Game.dt = 0
            if Game.matchtype != "practice":
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


    def match_type(self, match_type, team):
        Game.matchtype = match_type
        if match_type == "quickmatch":
            Game.total_overs = "5"
            SCOREBOARD.target_runs = None
        else:
            Game.total_overs = "10"
            Game.team = team
            if match_type == "very easy":
                SCOREBOARD.target_runs = random.randint(49,79)
            elif match_type == "easy":
                SCOREBOARD.target_runs = random.randint(80,99)
            elif match_type == "medium":
                SCOREBOARD.target_runs = random.randint(100,149)
            elif match_type == "hard":
                SCOREBOARD.target_runs = random.randint(150,199)
            elif match_type == "very hard":
                SCOREBOARD.target_runs = random.randint(200,250)
            SCOREBOARD.runs_left = SCOREBOARD.target_runs


    def check_runs_scored():
        Game.dr = BATSMAN.t_player_input-BOWLER.t_ball_released

        # checking the player input
        if BATSMAN.direction == BALL.direction:

            if 100 <= Game.dr <= 400:
                Game.runs_scored, BATSMAN.shot = 6, "loft"
                Game.six_count += 1

            elif 0 <= Game.dr <= 410:
                Game.runs_scored, BATSMAN.shot = "Catch-Out", "loft"

            elif 0 <= Game.dr <= 475:
                Game.runs_scored, BATSMAN.shot = 4, "stroke"

            elif 0 <= Game.dr <= 550:
                Game.runs_scored = random.choice([1,1,1,2,2,3])
                BATSMAN.shot = "stroke"            

            else: Game.check_wicket()

        else: Game.check_wicket() 
        BALL.runs_scored = Game.runs_scored


    def check_wicket():        

        if BALL.direction != "straight":

            if BATSMAN.direction == BALL.direction:
                if -220 <= Game.dr <= 220: Game.runs_scored = "Caught"
            else: Game.runs_scored, BALL.delivery_played = 0, True
        
        else: Game.runs_scored, BATSMAN.shot = "Bowled", "stroke"


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

            if not Game.sound_playing:   
                sound = pygame.mixer.Sound(f'audio\\commentator\\{runs}.mp3')
                sound.play()
                Game.sound_playing = True

        else:
            match runs:
                case 6: txt = "SIX"
                case 4: txt = "FOUR"
                case 3: txt = "TRIPLE"
                case 2: txt = "DOUBLE"
                case 1: txt = "SINGLE"
            TEXT().blit(str(runs),target,(screen_width/2,screen_height/2-20),132)
            TEXT().blit(txt,target,(screen_width/2,screen_height/2+60),50,"Action_Man")

            if not Game.sound_playing:
                sound = pygame.mixer.Sound(f'audio\\commentator\\{txt.lower()}.mp3')
                sound.play()
                Game.sound_playing = True