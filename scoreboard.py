import pygame
from settings import *

def update_stats(won,six_count):
    with open("data/userdata.txt", "r+") as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if i == 0:
                lines[i] = f"TOTAL MATCHES PLAYED : {int(lines[i].split()[4])+1}\n"
            elif i == 1 and won:
                lines[i] = f"TOTAL WINS : {int(lines[i].split()[3])+1}\n"
            elif i == 3:
                lines[i] = f"SIX COUNTER : {int(lines[i].split()[3])+six_count}\n"
        f.seek(0)
        f.writelines(lines)


def update_hs(runs):
    with open("data/userdata.txt","r+") as f:
        lines = f.readlines()
        if runs >= int(lines[2].split()[4]):
            lines[3] = f"EXHIBITION HIGH SCORE : {int(SCOREBOARD.current_runs[:-2])}"
            f.seek(0)
            f.writelines(lines)
            pygame.event.post(pygame.event.Event(exhibition_event))


class SCOREBOARD():

    target_runs = 1
    current_runs = "0/0"
    current_overs = "0.0"
    runs_in_over = []
    six_count = 0

    def blit(self,target,total_overs):
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
        
        TEXT().blit("     ".join(SCOREBOARD.runs_in_over),target,(615+16*(len(SCOREBOARD.runs_in_over)-1),screen_height-15),16,color=(255,255,255))
        
        rect = pygame.Rect(screen_width-220,10,120,30)
        pygame.draw.rect(target,"#343434",rect)

        # text 
        TEXT().blit("AUS",target,(35,screen_height-15),16,color=(255,255,255))
        TEXT().blit("VS",target,(80,screen_height-15),16,color=(255,255,255))
        TEXT().blit(f"IND {SCOREBOARD.current_runs}",target,(160,screen_height-15),16,color=(255,255,255))
        TEXT().blit(SCOREBOARD.current_overs,target,(240,screen_height-15),16,color=(255,255,255))
        TEXT().blit(total_overs,target,(280,screen_height-15),16,color=(255,255,255))
        if SCOREBOARD.target_runs == None: txt = "NO TARGET"
        else: txt = f"TARGET : {SCOREBOARD.target_runs}"
        TEXT().blit(txt,target,(screen_width-160,25),16,color=(255,255,255))


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
        SCOREBOARD.check_win_loss()
    
    def check_win_loss():

        if SCOREBOARD.target_runs != None:

            # win conditin check
            if int(SCOREBOARD.current_runs[:-2]) > SCOREBOARD.target_runs:
                pygame.event.post(pygame.event.Event(game_won_event))
                update_stats(won=True, six_count=SCOREBOARD.six_count)


            # loose conditin check
            elif SCOREBOARD.current_overs == "10.0" and int(SCOREBOARD.current_runs[:-2]) <= SCOREBOARD.target_runs:
                pygame.event.post(pygame.event.Event(game_lost_event))
                update_stats(won=False, six_count=SCOREBOARD.six_count)

            elif SCOREBOARD.current_runs[len(SCOREBOARD.current_runs)-2:] == "10":
                pygame.event.post(pygame.event.Event(game_lost_event))
                update_stats(won=False, six_count=SCOREBOARD.six_count)
            
            

        else:
            if SCOREBOARD.current_overs == "5.0":
                pygame.event.post(pygame.event.Event(exhibition_event))
                update_hs(int(SCOREBOARD.current_runs[:-2]))
