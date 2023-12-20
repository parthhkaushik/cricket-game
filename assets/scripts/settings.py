import pygame,csv

# display
screen_width, screen_height = 800, 600
scoreboard_height = 40

# user events
next_ball_event = pygame.USEREVENT +1
throw_ball_event = pygame.USEREVENT +2
game_won_event = pygame.USEREVENT +3
game_lost_event = pygame.USEREVENT +4
quickmatch_event = pygame.USEREVENT +5

# cricket pitch
umpire_pos = (screen_width/2-35,340)
pitch_top_point = (screen_width/2 + 30, screen_height/2.85)
over_the_wicket = screen_width/2 - 100

# ball-bowler
ball_release_pt = (325,250)


# functions  
 
def blit_alpha(target, source, location, opacity):
    """ 
        It is used for adjusting the opacity of the surfaces 
    """
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)        
    target.blit(temp, location)


def get_frames(player,action,scale=None):
    """ 
        Importing all the frames from the folders in a dictionary 
    """
    frames, c = {}, 0
    while True:
        try:
            file = f'assets/images/{player}/{action}/frame-{c+1}.png'
            frame = pygame.image.load(file)
            if scale != None:
                frame = pygame.transform.scale(frame, scale)
            frames[c] = frame
            c+=1
        except: break
    return frames


def check_win_loss(target, score, over, matchtype):
    """ 
        check wether the game has ended or not 
    """
    # if world cup match
    if target != None:
        # win conditin check
        if int(score[:-2]) >= target:
            return "won"

        # loose conditin check
        elif over == "10.0" and int(score[:-2]) <= target:
            return "lost"
        elif score[len(score)-2:] == "10":
            return "lost"
        
    # if quick match
    elif matchtype == "quickmatch" and over == "5.0":
            return "quickmatch ended"
            

def update_stats(won,six_count):
    """ 
        update the stats in the text file userdata.txt 
    """
    with open("assets/data/userdata.txt", "r+") as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if i == 0:
                lines[i] = f"TOTAL MATCHES PLAYED : {int(lines[i].split()[4])+1}\n"
            elif i == 1 and won:
                lines[i] = f"TOTAL WINS : {int(lines[i].split()[3])+1}\n"
            elif i == 3:
                lines[i] = f"SIX COUNTER : {int(lines[i].split()[3])+six_count}"
        f.seek(0)
        f.writelines(lines)


def update_hs(runs):
    """ 
        update the highscore in the text file userdata.txt 
    """
    with open("assets/data/userdata.txt","r+") as f:
        lines = f.readlines()
        if runs >= int(lines[2].split()[4]):
            lines[2] = f"QUICK MATCH HIGHSCORE : {runs}\n"
            f.seek(0)
            f.writelines(lines)
            pygame.event.post(pygame.event.Event(quickmatch_event))


def get_scorecard(file):
    scorecard = []
    with open(file,"r",newline="") as f:
        lines = csv.reader(f)
        for line in lines:
            # player, runs, balls, 6s, status
            c = [line[0],0,0,0,"NOT-OUT"]
            scorecard.append(c)
    return scorecard


def next_batsman(file,out=0):
    with open(file,"r",newline="") as f:
        lines = csv.reader(f)
        c = 0
        if out == 0:
            openers = []
            for line in lines:
                openers.append(line)
                if c == 1: return openers
                c+=1
        for line in lines:
            if c-out == 1: return line
            c+=1



# shots
shots = {
    "straight-loft":{"name":"advance-straight-drive","hit_pos":160},
    "straight-stroke":{"name":"straight-drive","hit_pos":155},
    "left-loft":{"name":"reverse_sweep","hit_pos":135},
    "left-stroke":{"name":"cover-drive","hit_pos":140},
    "right-loft":{"name":"pull-shot","hit_pos":80},
    "right-stroke":{"name":"on-drive","hit_pos":145},
}

# color codes
colors = {
    "hex":{
        "charcoal":"#343434",
        "brick_red":"#B22222",
        "dark_orange":"#ff8c00",
        "lime_green":"#32cd32",
        "yellow":"#ffd700"
        },
    "rgb":{
        "white":(255,255,255)
    }
}

# ball hit points
ball_points = [
    {"dx":(3.5,-0.5),"dy":(1,3),"length":222,"shot_dir":"straight", "circle_pos":(392,220)},
    {"dx":(5,0.5),"dy":(1,3.5),"length":225,"shot_dir":"right", "circle_pos":(418,222)},
    {"dx":(3,-0.5),"dy":(1,3),"length":225,"shot_dir":"left", "circle_pos":(360,222)}
]



# objects
class TEXT():
    ds, sign = 0, 1
    def blit(self,text,target,pos,size=20,font="Aller",bold=False,color=(0,0,0),bounce=False,align="center"):
        if bounce:
            if TEXT.ds >= 2.75: TEXT.sign = -1
            elif TEXT.ds == 0: TEXT.sign = 1
            TEXT.ds += TEXT.sign*0.125
        if bold:
            font = pygame.font.Font(f"assets/fonts/{font}-Bold.ttf",(size+int(TEXT.ds)))
        else:
            font = pygame.font.Font(f"assets/fonts/{font}-Regular.ttf",(size+int(TEXT.ds)))
        txt = font.render(text,False,color)
        if align == "center": txt_rect = txt.get_rect(center = pos)
        elif align == "right": txt_rect = txt.get_rect(midright = pos)
        else: txt_rect = txt.get_rect(midleft=pos)
        target.blit(txt,txt_rect)
    
class PROGRESS_BAR():
    ds, loading = 0, True
    def load(self,target,pos,size):
        if PROGRESS_BAR.loading:
            rect1 = pygame.Rect(pos[0],pos[1],size[0],size[1])
            pygame.draw.rect(target,"Black",rect1)
            rect2 = pygame.Rect(pos[0],pos[1],int(PROGRESS_BAR.ds),size[1])
            PROGRESS_BAR.ds += 1.5
            pygame.draw.rect(target,"Dark Orange",rect2)
        if PROGRESS_BAR.ds >= size[0]:
            PROGRESS_BAR.loading = False