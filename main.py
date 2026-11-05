import random
import sys
import pygame
from pygame.locals import *

FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 289

SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT)) # screen initialized
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}

PLAYER_ROOT = "assets/sprites/"
PLAYER_COLORS = {'B': "bluebird", 'R': "redbird", 'Y': "yellowbird"}
PLAYER_MODIFIERS = ["-downflap.png", "-midflap.png", "-upflap.png"]
BACKGROUND_ROOT = "assets/sprites/background-"
BACKGROUND_LIGHT = ["day.png", "night.png"]
PIPE_ROOT = "assets/sprites/pipe-"
PIPE_COLORS = {'G': "green.png", 'R': "red.png"}
BASE = "assets/sprites/base.png"
MESSAGE = "assets/sprites/message.png"
GAMEOVER = "assets/sprites/gameover.png"
CAPTION = "Gesture Controlled Flappy Bird Game"

if __name__ == '__main__':
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption(CAPTION)
    GAME_SPRITES['NUMBERS'] = [pygame.image.load(f"assets/sprites/{i}.png").convert_alpha() for i in range(10)]
    GAME_SPRITES['MESSAGE'] = pygame.image.load(MESSAGE).convert_alpha()
    GAME_SPRITES['BASE'] = pygame.image.load(BASE).convert_alpha()
    GAME_SPRITES['GAMEOVER'] = pygame.image.load(GAMEOVER)
    pipe_col = "G" # choices: "G", "R"
    GAME_SPRITES['PIPE'] = (
        pygame.transform.rotate(pygame.image.load(PIPE_ROOT + PIPE_COLORS[pipe_col]).convert_alpha(), 180),
        pygame.image.load(PIPE_ROOT + PIPE_COLORS[pipe_col]).convert_alpha()
    )
    bird_col = "B" # choices: "B", "R", "Y"
    GAME_SPRITES['PLAYER'] = [pygame.image.load(PLAYER_ROOT + PLAYER_COLORS[bird_col] + PLAYER_MODIFIERS[i]).convert_alpha() for i in range(3)]
    GAME_SPRITES['BG_LIGHT'] = [pygame.image.load(BACKGROUND_ROOT + BACKGROUND_LIGHT[i]).convert() for i in range(2)]

    GAME_SOUNDS['die'] = pygame.mixer.Sound("assets/audio/die.wav")
    GAME_SOUNDS['hit'] = pygame.mixer.Sound("assets/audio/hit.wav")
    GAME_SOUNDS['point'] = pygame.mixer.Sound("assets/audio/point.wav")
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound("assets/audio/swoosh.wav")
    GAME_SOUNDS['wing'] = pygame.mixer.Sound("assets/audio/wing.wav")


def welcome_screen():
    pass

def main_game():
    pass


    while True:
        welcome_screen() # executes until button pressed
        main_game()