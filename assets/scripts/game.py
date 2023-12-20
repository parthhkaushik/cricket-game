import pygame, random
from assets.scripts.settings import *
from assets.scripts.sprites import *



""" scoreboard class """

class Scoreboard():

    # class variables
    target_runs, runs_left = 1, 0
    current_runs, current_overs = "0/0", "0.0"
    runs_in_over = []
    six_count, balls_left = 0, 60
    txt1 = ""
    current_batsmen = [1,2]
    batsman_on_strike = 0


    # methods 

    def blit(self,target,total_overs,team):
        """ blit/draw the scoreboard on the screen """
        
        scoreboard = pygame.Rect(0,screen_height-scoreboard_height,screen_width,scoreboard_height)
        pygame.draw.rect(target,colors['hex']['charcoal'],scoreboard)
        
        # rectangles
        rect = pygame.Rect(10,screen_height-scoreboard_height+5,120,scoreboard_height-5)
        pygame.draw.rect(target,colors['hex']['brick_red'],rect)
        rect = pygame.Rect(170,screen_height-scoreboard_height+5,40,scoreboard_height-5)
        pygame.draw.rect(target,colors['hex']['dark_orange'],rect)
        for i in range(6):
            rect = pygame.Rect(600+i*32,screen_height-scoreboard_height+5,30,scoreboard_height-5)
            pygame.draw.rect(target,colors['hex']['dark_orange'],rect)
        
        # runs in over
        pos = (615+16*(len(Scoreboard.runs_in_over)-1),screen_height-15)
        TEXT().blit("     ".join(Scoreboard.runs_in_over),target,pos,16,color=(255,255,255))
        
        # target runs
        rect = pygame.Rect(screen_width-220,10,120,30)
        pygame.draw.rect(target,colors['hex']['charcoal'],rect)

        # text 
        s = f"ALL {Scoreboard.current_runs}"
        TEXT().blit(s,target,(70,screen_height-15),16,color=(255,255,255))
        TEXT().blit(Scoreboard.current_overs,target,(150,screen_height-15),16,color=(255,255,255))
        TEXT().blit(total_overs,target,(190,screen_height-15),16,color=(255,255,255))

        TEXT().blit(Scoreboard.txt1,target,(screen_width-160,25),16,color=(255,255,255))
        
        batsman1_runs = Game.scorecard[Scoreboard.current_batsmen[0]-1][1]
        batsman1_balls = Game.scorecard[Scoreboard.current_batsmen[0]-1][2]
        batsman1 = f"{Game.batsman1[0]} {batsman1_runs} ({batsman1_balls})" 
        TEXT().blit(batsman1,target,(320,screen_height-15),16,color=(255,255,255))

        batsman2_runs = Game.scorecard[Scoreboard.current_batsmen[1]-1][1]
        batsman2_balls = Game.scorecard[Scoreboard.current_batsmen[1]-1][2]
        batsman2 = f"{Game.batsman2[0]} {batsman2_runs} ({batsman2_balls})"
        TEXT().blit(batsman2,target,(480,screen_height-15),16,color=(255,255,255))


    def update(self, runs_scored):
        """ update the screoboard """

        # balls played
        Game.scorecard[Scoreboard.current_batsmen[Scoreboard.batsman_on_strike]-1][2] += 1

        # current runs
        if runs_scored in ["Bowled","Catch-Out","Caught"]:
            Scoreboard.current_runs = Scoreboard.current_runs[:-1]+str(int(Scoreboard.current_runs[-1])+1)
            Scoreboard.runs_in_over.append("W")
            Game.scorecard[Scoreboard.current_batsmen[Scoreboard.batsman_on_strike]-1][4] = runs_scored.upper()

            # change the batsman on strike   
            file = "assets/data/players.csv"
            out = int(Scoreboard.current_runs[-1])
            if Scoreboard.batsman_on_strike == 0:
                Game.batsman1 = next_batsman(file,out)
                Scoreboard.current_batsmen[0] = out+2
            else:
                Game.batsman2 = next_batsman(file,out)
                Scoreboard.current_batsmen[1] = out+2
        else:
            Scoreboard.current_runs = str(int(Scoreboard.current_runs[:-2])+runs_scored)+Scoreboard.current_runs[-2:]
            Scoreboard.runs_in_over.append(str(runs_scored))

            Scoreboard.runs_left -= runs_scored
            Game.scorecard[Scoreboard.current_batsmen[Scoreboard.batsman_on_strike]-1][1] += runs_scored

            if runs_scored in [1,3]:
                if Scoreboard.batsman_on_strike == 0:
                    Scoreboard.batsman_on_strike = 1
                else:
                    Scoreboard.batsman_on_strike = 0
    
        # over update
        Scoreboard.current_overs = str(round(float(Scoreboard.current_overs)+0.1,1))
        Scoreboard.balls_left -= 1            

        # check over completed
        if Scoreboard.current_overs[-1] == "6":
            Scoreboard.current_overs = str(round(float(Scoreboard.current_overs)))+".0"
            Scoreboard.runs_in_over = []
            if Scoreboard.batsman_on_strike == 0:
                Scoreboard.batsman_on_strike = 1
            else:
                Scoreboard.batsman_on_strike = 0

        # checking for win or loss
        ch = check_win_loss(Scoreboard.target_runs,Scoreboard.current_runs, Scoreboard.current_overs, Game.matchtype)
        
        if ch == "won":
            pygame.event.post(pygame.event.Event(game_won_event))
            update_stats(won=True, six_count=Scoreboard.six_count)
        
        elif ch == "lost":
            pygame.event.post(pygame.event.Event(game_lost_event))
            update_stats(won=False, six_count=Scoreboard.six_count)
        
        elif ch == "quickmatch ended":
            pygame.event.post(pygame.event.Event(quickmatch_event))
            update_hs(int(Scoreboard.current_runs[:-2]))


class Game():

    # class variables
    next_ball_event = False
    dt,dr = 0,0
    total_overs, runs_scored = "", 0
    show_circle = False
    team = 0, None
    sound_playing = False
    batsman1, batsman2 = "",""
    scorecard = []

    # images
    pitch = pygame.image.load('assets/images/ground/background.jpg')
    pitch = pygame.transform.scale(pitch,(screen_width,screen_height))

    logo = pygame.image.load("assets/icons/cricketgame.png")
    logo = pygame.transform.scale(logo,(180,30))
    pause = pygame.image.load("assets/images/buttons/pause.png")
    pause = pygame.transform.scale(pause,(80,30))

    umpire = pygame.image.load("assets/images/ground/umpire.png")
    umpire = pygame.transform.scale(umpire,(80,215))
    
    wickets = pygame.image.load("assets/images/ground/wickets-1.png")
    wickets = pygame.transform.scale(wickets,(64,80))

    circle = pygame.image.load("assets/images/ground/target.png")
    circle = pygame.transform.scale(circle,(30,15))

    all_sprites = pygame.sprite.Group()
    ball = pygame.sprite.GroupSingle()


    # methods 

    def setup(self):
        """ set all the necessary variables to default """

        Game.next_ball_event = False
        Game.dt,Game.dr = 0,0
        Game.total_overs = ""
        Game.runs_scored = 0
        Game.show_circle = False
        Game.sound_playing = False
        Game.team, Game.scorecard = None, []
        Game.batsman1,Game.batsman2="",""

        Game.all_sprites.add(Batsman(),Batsman(non_striker=True),Bowler())

        Game.sound_playing = False
        Game.dt = 0
        Game.next_ball_event = False
        Game.show_circle = False
        
        # scoreboard
        Scoreboard.target_runs = 1
        Scoreboard.current_runs = "0/0"
        Scoreboard.current_overs = "0.0"
        Scoreboard.runs_in_over = []
        Scoreboard.six_count = 0
        Scoreboard.balls_left = 60
        Scoreboard.runs_left = 0
        Scoreboard.current_batsmen = [1,2]
        Scoreboard.batsman_on_strike = 0
        Scoreboard.txt1 = ""


        # Batsman
        Batsman.non_striker_can_move = False
        Batsman.shot = "stroke"
        Batsman.direction = "straight"
        Batsman.t_player_input = 0
        Batsman.delivery_played = False
        Batsman.key_pressed = False
        Batsman.next_ball_event = False

        # Bowler
        Bowler.flag = 0
        Bowler.t_ball_released = 0

        # Ball
        Ball.delivery_played = False
        Ball.shot = "stroke"
        Ball.direction = "straight"
        Ball.runs_scored = 0
        Ball.circle_pos = None
        Ball.point = None


    def run(self, target):
        """ main cricket game code """

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
        
        if Game.show_circle: target.blit(Game.circle,Ball.circle_pos)

        Game.ball.draw(target)
        Game.ball.update()
                
        # displaying the sccoreboard   
        if Game.matchtype != "practice": 
            Scoreboard().blit(target, Game.total_overs, Game.team)
        else:
            scoreboard = pygame.Rect(0,screen_height-scoreboard_height,screen_width,scoreboard_height)
            pygame.draw.rect(target,"#343434",scoreboard)
            TEXT().blit("PRACTICE",target,(150,screen_height-15),16,color=(255,255,255))
            TEXT().blit("SESSION",target,(screen_width-150,screen_height-15),16,color=(255,255,255))

        Game.dt += 1
        if Game.dt >= 420:
            if not Batsman.delivery_played: Game.check_wicket()
            Game.display_runs(Game.runs_scored,target) 

        if Game.next_ball_event:
            Game.sound_playing = False
            Batsman.next_ball_event = True
            Game.dt = 0
            if Game.matchtype != "practice":
                Scoreboard().update(Game.runs_scored)
            Game.next_ball_event = False
            Game.show_circle = False

        if Batsman.key_pressed:
            Game.check_runs_scored()
            Game.all_sprites.sprites()[0].play_shot()
            Ball.shot = Batsman.shot
            Ball.delivery_played = True
            Batsman.key_pressed = False 
        

    def match_type(self, match_type, team):
        """ setup the game requirements according to the user """

        Game.matchtype = match_type
        if match_type == "quickmatch":
            Game.total_overs = "5"
            Scoreboard.target_runs = None
            Scoreboard.txt1 = "NO TARGET"
        else:
            Game.total_overs = "10"
            Game.team = team
            if match_type == "very easy":
                Scoreboard.target_runs = random.randint(49,79)
            elif match_type == "easy":
                Scoreboard.target_runs = random.randint(80,99)
            elif match_type == "medium":
                Scoreboard.target_runs = random.randint(100,149)
            elif match_type == "hard":
                Scoreboard.target_runs = random.randint(150,199)
            elif match_type == "very hard":
                Scoreboard.target_runs = random.randint(200,250)
            Scoreboard.runs_left = Scoreboard.target_runs
            Scoreboard.txt1 = f"{team} {Scoreboard.target_runs}/" + str(random.randint(0,10))
        
        Game.scorecard = get_scorecard("assets/data/players.csv")
        Game.batsman1, Game.batsman2 = next_batsman("assets/data/players.csv")


    def check_runs_scored():
        """ check the runs scored accoding to the timing """

        Game.dr = Batsman.t_player_input-Bowler.t_ball_released

        # checking the player input
        if Batsman.direction == Ball.direction:

            if Scoreboard.batsman_on_strike == 0:
                ch = 5 * int(Game.batsman1[1])-2
            else:
                ch = 5 * int(Game.batsman2[1])-2

            if 100 <= Game.dr <= 400+ch:
                Game.runs_scored, Batsman.shot = 6, "loft"
                Scoreboard.six_count += 1
                Game.scorecard[Scoreboard.current_batsmen[Scoreboard.batsman_on_strike]-1][3] += 1

            elif 0 <= Game.dr <= 410+ch:
                Game.runs_scored, Batsman.shot = "Catch-Out", "loft"

            elif 0 <= Game.dr <= 475+ch:
                Game.runs_scored, Batsman.shot = 4, "stroke"

            elif 0 <= Game.dr <= 550+ch:
                Game.runs_scored = random.choice([1,1,1,2,2,3])
                Batsman.shot = "stroke"            

            else: Game.check_wicket()

        else: Game.check_wicket() 
        Ball.runs_scored = Game.runs_scored


    def check_wicket():    
        """ check wether its a wicket """    

        if Ball.direction != "straight":

            if Batsman.direction == Ball.direction:
                if -220 <= Game.dr <= 220: Game.runs_scored = "Caught"
            else: Game.runs_scored, Ball.delivery_played = 0, True
        
        else: Game.runs_scored, Batsman.shot = "Bowled", "stroke"


    def display_runs(runs,target):
        """ display the runs scored on that ball """
    
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
                sound = pygame.mixer.Sound(f'assets/audio/commentator/{runs}.mp3')
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
                sound = pygame.mixer.Sound(f'assets/audio/commentator/{txt.lower()}.mp3')
                sound.play()
                Game.sound_playing = True