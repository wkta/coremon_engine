#!/usr/bin/env python
#
#Copyright 2006 DR0ID <dr0id@bluewin.ch> http://mypage.bluewin.ch/DR0ID
#
#
#

"""
#TODO: documentation!
"""

__author__    = "$Author: DR0ID $"
__version__   = "$Revision: 154 $"
__date__      = "$Date: 2007-04-10 17:39:49 +0200 (Di, 10 Apr 2007) $"
__license__   = ''
__copyright__ = "DR0ID (c) 2007"


import pygame

class Text(object):
    """
    
    """
    
    def __init__(self, text, font, position):
        """
        
        """
        
        self.text = text
        self.position = position
        
        size = font.size(text)
        rect = pygame.Rect((0,0),size)
        self.image = pygame.Surface(rect.size).convert()
        self.image.fill((0,0,0))
        self.image.set_colorkey((0,0,0))
        
        txtimg = font.render(text, 1, (255, 255, 255), (0, 0, 0))
        xpos = (rect.width-size[0])/2
        ypos = (rect.height-size[1])/2
        self.image.blit(txtimg, (xpos, ypos))