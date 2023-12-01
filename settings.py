import pygame

# display
screen_width, screen_height = 800, 600
scoreboard_height = 40

# user events
THROW_BALL = pygame.USEREVENT +1

# cricket pitch
pitch_top_point = (screen_width/2 + 30, screen_height/2.85)
over_the_wicket = screen_width/2 - 100

# ball-bowler
ball_release_pt = (325,250)

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