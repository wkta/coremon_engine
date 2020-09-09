import pygame


class GameMod:

    def __init__(self):
        self.invaders, self.colors, self.shots = [], [] ,[]
        
        for x in range(15, 300, 15):
            for y in range(10, 100, 15):
                self.invaders.append(pygame.Rect(x, y, 7, 7))
                self.colors.append(((x * 0.7) % 256, (y * 2.4) % 256))
