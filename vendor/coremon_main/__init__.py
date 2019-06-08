"""
Cogmonger engine, 'cgm_engine' for short
VERSION 0.0.2
designed & coded by Thomas Iwaszko
contact: thomas@gaudia-tech.com
(c) 2019
"""
import pygame
from pygame import constants

from ._defs import EngineEvTypes, enum_for_custom_event_types
from ._events import EventManager, EventReceiver, CgmEvent, EventDispatcher, CogObject
from .structures import BaseGameState


PygameBridge = constants
screen = None
DEFAULT_CAPTION = 'Made with coremonger engine'
DEFAULT_SCREEN_SIZE = (1024, 768)


def init(scr_size=None, caption=None):
    pygame.init()

    if caption:
        pygame.display.set_caption(caption)
    else:
        pygame.display.set_caption(DEFAULT_CAPTION)

    global screen
    if scr_size:
        screen = pygame.display.set_mode(scr_size)
    else:
        screen = pygame.display.set_mode(DEFAULT_SCREEN_SIZE)

def cleanup():
    global  screen
    del screen
    pygame.quit()
