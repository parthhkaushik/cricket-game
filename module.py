import pygame
from settings import *


target_runs = 200
current_runs = "100/2"
current_overs = "5.1"

# scoreboard

class SCOREBOARD():
    def display_score(self,target):
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

        rect = pygame.Rect(screen_width-220,10,120,30)
        pygame.draw.rect(target,"#343434",rect)

        # text 
        TEXT().blit("AUS",target,(35,screen_height-15),16,color=(255,255,255))
        TEXT().blit("VS",target,(80,screen_height-15),16,color=(255,255,255))
        TEXT().blit(f"IND {current_runs}",target,(160,screen_height-15),16,color=(255,255,255))
        TEXT().blit(current_overs,target,(240,screen_height-15),16,color=(255,255,255))
        TEXT().blit("10",target,(280,screen_height-15),16,color=(255,255,255))
        TEXT().blit(f"TARGET : {target_runs}",target,(screen_width-160,25),16,color=(255,255,255))


    def update(self):
        pass



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
            pygame.draw.rect(target,"Orange",rect2)
        if PROGRESS_BAR.ds >= size[0]:
            PROGRESS_BAR.loading = False



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


def display_runs(runs,target):
    """
        Display the runs scored on that ball
    """
    rect1 = pygame.Rect(screen_width/2-100,screen_height/2-125,200,250)
    pygame.draw.rect(target,"#343434",rect1)
    rect2 = pygame.Rect(screen_width/2-100,screen_height/2-90,200,180)
    pygame.draw.rect(target,"#B22222",rect2)

    if runs == 0:
        TEXT().blit("DOT",target,(screen_width/2,screen_height/2-30),50,"Action_Man")
        TEXT().blit("BALL",target,(screen_width/2,screen_height/2+30),50,"Action_Man")
    
    elif  runs in ["Bowled","Catch-Out","Caught"]:
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
        


class TIMING_BAR():
    # class vairables
    p = {"x":screen_width-220, "y":50}
    s = {"w":210, "h":10}
    txt_pos = [(screen_width-200,65),(screen_width-110,65),(screen_width-30,65)]

    # displaying the timing bar
    def blit(self,target):
        rect = pygame.Rect(TIMING_BAR.p["x"],TIMING_BAR.p["y"],TIMING_BAR.s["w"],TIMING_BAR.s["h"])
        pygame.draw.rect(target,colors["hex"]["charcoal"],rect)
        TEXT().blit("EARLY",target,TIMING_BAR.txt_pos[0],12,color=colors["rgb"]["white"])
        TEXT().blit("PERFECT",target,TIMING_BAR.txt_pos[1],12,color=colors["rgb"]["white"])
        TEXT().blit("LATE",target,TIMING_BAR.txt_pos[2],12,color=colors["rgb"]["white"])

    # updating the timing
    def update(self,target,timing,sign=0):
        if timing == 3:
            color = colors["hex"]["lime_green"]
            x,y = screen_width-120,50
        elif timing == 2:
            color = colors["hex"]["yellow"]
            x,y = screen_width-abs(sign*240-150),50
        elif timing == 1:
            color = colors["hex"]["dark_orange"]
            x,y = screen_width-abs(sign*250-180),50
        else:
            color = colors["hex"]["brick_red"]
            x,y = screen_width-abs(sign*250-210),50

        rect = pygame.Rect(x,y,20,10)
        pygame.draw.rect(target,color,rect)