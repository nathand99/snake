import pygame as pg
from pygame.locals import *
import sys
import time
import random

#initialize global variables
score = -1 # starts -1 here then incremented to 0 when the game starts
high_score = 0
width = 800
height = 800
white = (255, 255, 255)
line_color = (10, 10, 10)
line_width = 2
heading = "RIGHT"
squares = 16 # use a multiple of 8 only - to avoid division errors later
speed = 250 # number of ms between snake moves

# the board is a squares x sqaures array
board = [ [ None for y in range(squares) ] for x in range(squares) ] # this is actually never used - neat way to make a 2d array
# snake array holds tiles that form the snake. The head is the first element
snake = [] 
# co-ordinates of the apple (first position hardcoded)
apple_start = (8,5)
apple_co = apple_start

#initialisation
pg.init()
fps = 60
CLOCK = pg.time.Clock()
# intialise window/screen
screen = pg.display.set_mode(size=(width, height+100),flags=pg.RESIZABLE)
pg.display.set_caption("SNAKE")

snake_img = pg.image.load('snake.png')
snake_img = pg.transform.scale(snake_img, (width, height + 100))

apple_img = pg.image.load('apple.png')
apple_img = pg.transform.scale(apple_img, (width / squares - 2 * line_width, height / squares - 2 * line_width))

BITE_SOUND = pg.mixer.Sound('bite.wav')
BITE_SOUND.set_volume(0.2)

# function that starts the game
def game_opening():
    global snake
    #screen.blit(snake_img,(0,0)) # blit draws an image on top of another image. We put the opening_img on top of the screen
    #pg.display.update() # after you do anything you need to update the display
    #time.sleep(1)
    screen.fill(white) # fill screen with white which removes the opening_img
    # draw in sqaures
    for i in range(squares + 1):
        pg.draw.line(screen, line_color, (width / squares * i, 0), (width/  squares * i, height), width=line_width) # line(surface, color, start_pos, end_pos)
        pg.draw.line(screen, line_color, (0, height / squares * i), (width, height / squares * i), width=line_width)
    # default snake is hardcoded as 3 tiles
    snake = [(2,5), (1,5), (0,5)]
    colour_snake()
    (x, y) = apple_co
    screen.blit(apple_img,(x * width / squares + line_width, y * height / squares + line_width))
    # update score
    update_score()
    #wait()

# colours in the tiles that the snake is on red
def colour_snake():
    for (x, y) in snake:
        screen.fill((255, 0, 0), ((x * (width / squares) + line_width), (y * (height / squares) + line_width), width / squares - line_width, height / squares - line_width)) # make the black box that the status text goes in

# colours in the tile given white
def erase_snake(z):
    (x, y) = z
    screen.fill((255, 255, 255), ((x * (width / squares) + line_width), (y * (height / squares) + line_width), width / squares - line_width, height / squares - line_width)) # make the black box that the status text goes in

# snake moves 1 place. If move is illegal -> return True
def snake_move():
    global snake, apple_co
    (x, y) = snake[0]
    # give new head
    if heading == "UP":
        new_tile = (x, (y - 1))
    elif heading == "DOWN":
        new_tile = (x, (y + 1))
    elif heading == "RIGHT":
        new_tile = ((x + 1), y)
    elif heading == "LEFT":
        new_tile = ((x - 1), y)     
    if illegal_move(new_tile):
        return True
    # if we moved onto an apple - dont cut the tail and make a new apple
    if new_tile == apple_co:
        BITE_SOUND.play()
        snake = [new_tile] + snake
        apple()
        update_score()
    # no apple, cut tail
    else:
        erase_snake(snake[-1])
        snake = [new_tile] + snake[:-1]
    colour_snake()

# generate new apple
def apple():
    global apple_co
    while (True):
        x = random.randint(0, squares - 1)
        y = random.randint(0, squares - 1)
        if (x, y) in snake:
            continue
        else:
            break
    apple_co = (x, y)
    screen.blit(apple_img,(x * width / squares + line_width, y * height / squares + line_width))
    
# checks if move is illegal or not. If illegal -> return True
def illegal_move(new_tile):
    if new_tile in snake:
        return True
    (x, y) = new_tile
    if x >= squares or y >= squares:
        return True
    elif x < 0 or y < 0:
        return True

# update the score on the bottom of the screen 
def update_score():
    global score
    score += 1
    font = pg.font.Font(None, 50) #Font(filename, size)
    # creates a new Surface with the specified text rendered on it
    text = font.render("Score: " + str(score), 1, (255, 255, 255)) #render(text, antialias, color, background=None) -> Surface
    # copy the rendered score onto the board
    screen.fill((0, 0, 0), (0, height, width, 100)) # make the black box that the status text goes in
    text_rect = text.get_rect(center=(width/2, height + 100 - 50), left=10)
    screen.blit(text, text_rect)
    text2 = font.render("Best: " + str(high_score), 1, (255, 255, 255))
    text_rect2 = text2.get_rect(center=(width/2, height + 100 - 50), right=width - 10)
    screen.blit(text2, text_rect2)
    pg.display.update()

# YOU LOST!
def game_over():
    font = pg.font.Font(None, 70) #Font(filename, size)
    # creates a new Surface with the specified text rendered on it
    text = font.render("GAME OVER! Score: " + str(score), 1, (255, 255, 255)) #render(text, antialias, color, background=None) -> Surface
    # copy the rendered score onto the board
    screen.fill((0, 0, 0), (0, height / 2, width, 100)) # make the black box that the status text goes in
    text_rect = text.get_rect(center=(width/2, (height + 100) / 2))
    screen.blit(text, text_rect)
    pg.display.update()
    wait()

# reset global variables back to default values
def reset_game():
    global score, heading, apple_co, high_score
    if score > high_score:
        high_score = score
    score = -1
    heading = "RIGHT"
    apple_co = apple_start
    game_opening()

# returns when there is user input
def wait():
    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
                return
###########################################################
# game loop
game_opening()
wait()
# create an event that runs every "speed" milliseconds (default 250)
MOVEEVENT, t = pg.USEREVENT+1, speed
pg.time.set_timer(MOVEEVENT, t)
# run the game loop forever
while(True):
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        # change heading according to arrow input. Not allowed to move in the opposite direction that the snake is facing. WASD also allowed
        elif event.type == pg.KEYDOWN: #or event.type == pg.KEYUP:
            if event.key == K_UP or event.key == K_w:
                if heading == "DOWN":
                    continue
                heading = "UP"
            elif event.key == K_DOWN or event.key == K_s:
                if heading == "UP":
                    continue
                heading = "DOWN"
            elif event.key == K_RIGHT or event.key == K_d:
                if heading == "LEFT":
                    continue
                heading = "RIGHT"
            elif event.key == K_LEFT or event.key == K_a:
                if heading == "RIGHT":
                    continue
                heading = "LEFT"
            # press p to pause
            elif event.key == K_p:
                wait()
        # every 250ms snake moves
        elif event.type == MOVEEVENT:
            ret = snake_move()  
            # snake_move returns something when there is an illegal move - game over
            if ret is not None:
                game_over()
                reset_game()
    #time.sleep(1)
    pg.display.update()
    CLOCK.tick(fps)