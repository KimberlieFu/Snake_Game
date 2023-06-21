# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 15:19:25 2018

@author: zou

"""

#importing modules - pygame, random, numpy
import pygame, random

import numpy as np

#creating class Settings consisting of height, width and rect_len
class Settings:
    def __init__(self):
        self.width = 28
        self.height = 28
        self.rect_len = 15

#creating Snake class defining the figure/body snake, snake's position, score which can be seen in the game.
class Snake:
    '''
    __init__ : initilization of the objects of Snake class
    initialize : reset the values of snake's position, starting point and score
    blit_body : blits the snake's body to the screen
    blit_head : blits the snake's head to the screen
    blit_tail : blits the snake's tail to the screen
    blit : blits the whole body of snake in order - head, body, tail to the screen
    update : updating the position of snake
    '''
    def __init__(self):

        self.image_up = pygame.image.load('snakeskin/headUp.png')
        self.image_down = pygame.image.load('snakeskin/headDown.png')
        self.image_left = pygame.image.load('snakeskin/headLeft.png')
        self.image_right = pygame.image.load('snakeskin/headRight.png')

        self.tail_up = pygame.image.load('snakeskin/tailUp.png')
        self.tail_down = pygame.image.load('snakeskin/tailDown.png')
        self.tail_left = pygame.image.load('snakeskin/tailLeft.png')
        self.tail_right = pygame.image.load('snakeskin/tailRight.png')

        self.image_body = pygame.image.load('snakeskin/body.png')

        self.facing = "right"
        self.initialize()

    def initialize(self):
        self.position = [6, 6]
        self.segments = [[6 - i, 6] for i in range(3)]
        self.score = 0

    def blit_body(self, x, y, screen):
        screen.blit(self.image_body, (x, y))

    def blit_head(self, x, y, screen):
        if self.facing == "up":
            screen.blit(self.image_up, (x, y))
        elif self.facing == "down":
            screen.blit(self.image_down, (x, y))
        elif self.facing == "left":
            screen.blit(self.image_left, (x, y))
        else:
            screen.blit(self.image_right, (x, y))

    def blit_tail(self, x, y, screen):
        tail_direction = [self.segments[-2][i] - self.segments[-1][i] for i in range(2)]

        if tail_direction == [0, -1]:
            screen.blit(self.tail_up, (x, y))
        elif tail_direction == [0, 1]:
            screen.blit(self.tail_down, (x, y))
        elif tail_direction == [-1, 0]:
            screen.blit(self.tail_left, (x, y))
        else:
            screen.blit(self.tail_right, (x, y))

    def blit(self, rect_len, screen):
        self.blit_head(self.segments[0][0]*rect_len, self.segments[0][1]*rect_len, screen)
        for position in self.segments[1:-1]:
            self.blit_body(position[0]*rect_len, position[1]*rect_len, screen)
        self.blit_tail(self.segments[-1][0]*rect_len, self.segments[-1][1]*rect_len, screen)

    def update(self):
            if self.facing == 'right':
                self.position[0] += 1
            if self.facing == 'left':
                self.position[0] -= 1
            if self.facing == 'up':
                self.position[1] -= 1
            if self.facing == 'down':
                self.position[1] += 1
            self.segments.insert(0, list(self.position) )


#Creating Strawberry class to define random food items which moves to random places seen in the game.
class Strawberry():
    '''
    __init__ : initilization of the objects of Strawberry class
    random_pos : randomly selects the food item out of the 6 files and randomly positions them on the screen
    blit : blits the food item image to the screen
    initialize : starting position
    '''
    def __init__(self, settings):
        self.settings = settings
        self.style = str(random.randint(1, 6))
        self.image = pygame.image.load('foodPNG/fruit' + str(self.style) + '.png')
        self.image_bomb = pygame.image.load('foodPNG/Bomb.png')
        self.initialize()

    def random_pos(self, snake):
        self.style = str(random.randint(1, 6))
        self.image = pygame.image.load('foodPNG/fruit' + str(self.style) + '.png')
        self.position[0] = random.randint(0, self.settings.width-1)
        self.position[1] = random.randint(0, self.settings.height-1)

        self.position[0] = random.randint(9, 19)
        self.position[1] = random.randint(9,19)

        if self.position in snake.segments:
            self.random_pos(snake)

    def blit(self, screen):
        screen.blit(self.image, [p * self.settings.rect_len for p in self.position])

    def initialize(self):
        self.position = [10, 10]


#Creating Bomb class to define bomb item on the screen and move it to random places.
class Bomb():
    '''
    __init__ : initilization of the objects of Bomb class
    random_pos_bomb : randomly positions the bomb image on the screen
    blit_bomb : blits the bomb image to the screen
    initialize : starting position
    '''
    def __init__(self, settings):
        self.settings = settings
        self.image_bomb = pygame.image.load('foodPNG/Bomb.png')
        self.initialize()

    def random_pos_bomb(self, snake):
        self.image_bomb = pygame.image.load('foodPNG/Bomb.png')
        self.position[0] = random.randint(0, self.settings.width-3)
        self.position[1] = random.randint(0, self.settings.height-3)

        self.position[0] = random.randint(9, 19)
        self.position[1] = random.randint(9, 19)
        if self.position in snake.segments:
            self.random_pos_bomb(snake)


    def blit_bomb(self, screen):
        screen.blit(self.image_bomb, [p * self.settings.rect_len for p in self.position])

    def initialize(self):
        self.position = [22, 10]

#Creating Game class specifying how the game will work in 3 different difficulty levels, ends the game and displays Score on top left side of the window.
class Game:
    """
    Connecting the other classes - Settings, Snake, Strawberry, Bomb so as to get the game function properly.
    restart_game : restarts the game.
    current_state : returns the current state.
    direction_to_int : returns the direction.
    do_move_easy, do_move_med, do_move_hard : moving the snake in a direction given by the user in the game and increasing the score if it successfully eats the food items.
    game_end : returning the value of 'end' which is either True or False.
    blit_score : updating the score displayed on the screen/window.
    """
    def __init__(self):
        self.settings = Settings()
        self.snake = Snake()
        self.strawberry = Strawberry(self.settings)
        self.move_dict = {0 : 'up',
                          1 : 'down',
                          2 : 'left',
                          3 : 'right'}
        self.bomb = Bomb(self.settings)

    def restart_game(self):
        self.snake.initialize()
        if self.snake.segments[0] in self.snake.segments[1:]:
            self.snake.segments[0] not in self.snake.segments[1:]
            self.snake.initialize()
        self.strawberry.initialize()
        self.bomb.initialize()

    def current_state(self):
        state = np.zeros((self.settings.width+2, self.settings.height+2, 2))
        expand = [[0, 1], [0, -1], [-1, 0], [1, 0], [0, 2], [0, -2], [-2, 0], [2, 0]]

        for position in self.snake.segments:
            state[position[1], position[0], 0] = 1

        state[:, :, 1] = -0.5

        state[self.strawberry.position[1], self.strawberry.position[0], 1] = 0.5
        for d in expand:
            state[self.strawberry.position[1]+d[0], self.strawberry.position[0]+d[1], 1] = 0.5
        return state

    def direction_to_int(self, direction):
        direction_dict = {value : key for key,value in self.move_dict.items()}
        return direction_dict[direction]

    def do_move(self, move):
        move_dict = self.move_dict

        change_direction = move_dict[move]

        if change_direction == 'right' and not self.snake.facing == 'left':
            self.snake.facing = change_direction
        if change_direction == 'left' and not self.snake.facing == 'right':
            self.snake.facing = change_direction
        if change_direction == 'up' and not self.snake.facing == 'down':
            self.snake.facing = change_direction
        if change_direction == 'down' and not self.snake.facing == 'up':
            self.snake.facing = change_direction

        self.snake.update()

        if self.snake.position == self.strawberry.position:
            eat_sound = pygame.mixer.Sound('sound/eatSound.wav')
            pygame.mixer.Sound.play(eat_sound)
            self.strawberry.random_pos(self.snake)
            reward = 1
            self.snake.score += 1
            self.bomb.random_pos_bomb(self.snake)
            if self.strawberry.position == self.bomb.position:
                self.bomb.random_pos_bomb(self.snake)
        else:
            self.snake.segments.pop()
            reward = 0

        if self.game_end():
            return -1

        return reward

    def game_end(self):
        end = False
        if self.snake.position == self.bomb.position:
            end=True
        if self.snake.position[0] >= self.settings.width or self.snake.position[0] < 0:
            end = True
        if self.snake.position[1] >= self.settings.height or self.snake.position[1] < 0:
            end = True
        if self.snake.segments[0] in self.snake.segments[1:]:
            end = True

        return end

    def blit_score(self, color, screen):
        font = pygame.font.SysFont(None, 25)
        text = font.render('Score: ' + str(self.snake.score), True, color)
        screen.blit(text, (0, 0))
