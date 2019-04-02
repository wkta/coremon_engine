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


def init(scr_size=None):
    global screen
    pygame.init()
    default_scr_size = (640, 480)
    arg = default_scr_size if (scr_size is None) else scr_size
    screen = pygame.display.set_mode(arg)
