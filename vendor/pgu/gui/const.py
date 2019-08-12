"""Constants.

From pygame:
    QUIT
    MOUSEBUTTONDOWN
    MOUSEBUTTONUP
    MOUSEMOTION
    KEYDOWN

PGU specific:
    ENTER
    EXIT
    BLUR
    FOCUS
    CLICK
    CHANGE
    OPEN
    CLOSE
    INIT

Other:
    NOATTR

"""
import pygame
#from pygame.locals import QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, KEYDOWN

_k = 387129
ENTER, EXIT, BLUR, FOCUS, CLICK, CHANGE, OPEN, CLOSE, INIT, ACTIVATE = range(_k, _k+10)


class NOATTR: 
    pass
