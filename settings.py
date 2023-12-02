from pygame import USEREVENT,time

# display
screen_width, screen_height = 800, 600
scoreboard_height = 40

# user events
next_ball_event = USEREVENT +1
throw_ball_event = USEREVENT +2
game_won_event = USEREVENT +3
game_lost_event = USEREVENT +4

# cricket pitch
umpire_pos = (screen_width/2-35,340)
pitch_top_point = (screen_width/2 + 30, screen_height/2.85)
over_the_wicket = screen_width/2 - 100

# ball-bowler
ball_release_pt = (325,250)

# shots
shots = {
    "straight-loft":{"name":"lofted-straight","hit_pos":160},
    "straight-stroke":{"name":"straight-drive","hit_pos":155},
    "left-loft":{"name":"reverse_sweep","hit_pos":135},
    "left-stroke":{"name":"cover-drive","hit_pos":140},
    "right-loft":{"name":"pull-shot","hit_pos":90},
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