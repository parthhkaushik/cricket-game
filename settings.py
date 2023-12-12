from pygame import USEREVENT
import pygame

# display
screen_width, screen_height = 800, 600
scoreboard_height = 40

# user events
next_ball_event = USEREVENT +1
throw_ball_event = USEREVENT +2
game_won_event = USEREVENT +3
game_lost_event = USEREVENT +4
quickmatch_event = USEREVENT +5

# cricket pitch
umpire_pos = (screen_width/2-35,340)
pitch_top_point = (screen_width/2 + 30, screen_height/2.85)
over_the_wicket = screen_width/2 - 100

# ball-bowler
ball_release_pt = (325,250)

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
            file = f'graphics/{player}/{action}/frame-{c+1}.png'
            frame = pygame.image.load(file)
            if scale != None:
                frame = pygame.transform.scale(frame, scale)
            frames[c] = frame
            c+=1
        except: break
    return frames

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
            lines[3] = f"QUICK MATCH HIGH SCORE : {runs}"
            f.seek(0)
            f.writelines(lines)
            pygame.event.post(pygame.event.Event(quickmatch_event))
      

# objects
class TEXT():
    ds = 0
    sign = 1
    def blit(self,text,target,pos,size=20,font="Aller",bold=False,color=(0,0,0),bounce=False):
        if bounce:
            if TEXT.ds >= 2.75: TEXT.sign = -1
            elif TEXT.ds == 0: TEXT.sign = 1
            TEXT.ds += TEXT.sign*0.125
        if bold:
            font = pygame.font.Font(f"fonts/{font}-Bold.ttf",(size+int(TEXT.ds)))
        else:
            font = pygame.font.Font(f"fonts/{font}-Regular.ttf",(size+int(TEXT.ds)))
        txt = font.render(text,False,color)
        txt_rect = txt.get_rect(center = pos)
        target.blit(txt,txt_rect)
    
class PROGRESS_BAR():
    ds = 0
    loading = True
    def load(self,target,pos,size):
        if PROGRESS_BAR.loading:
            rect1 = pygame.Rect(pos[0],pos[1],size[0],size[1])
            pygame.draw.rect(target,"Black",rect1)
            rect2 = pygame.Rect(pos[0],pos[1],int(PROGRESS_BAR.ds),size[1])
            PROGRESS_BAR.ds += 1.5
            pygame.draw.rect(target,"Dark Orange",rect2)
        if PROGRESS_BAR.ds >= size[0]:
            PROGRESS_BAR.loading = False