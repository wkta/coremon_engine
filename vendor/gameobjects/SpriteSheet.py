import pygame
from pygame.locals import QUIT


class SpriteSheet:
    def __init__(self, pygame_img, sprite_size, colorkey=None, upscaling=True, flip_horz=False):
        """
        charge en mémoire une image représentant une planche de sprites
        """
        self.taille_sprite = list(sprite_size)
        if upscaling:
            self.taille_sprite[0] *= 2
            self.taille_sprite[1] *= 2

        rezz = pygame_img.convert()
        if flip_horz:
            rezz = pygame.transform.flip(rezz, True, False)
        if upscaling:
            rezz = pygame.transform.scale(
                rezz,
                (rezz.get_width() * 2, rezz.get_height() * 2)
            )
        self.planche = rezz

        self.nb_col = int(self.planche.get_width() / self.taille_sprite[0])
        assert self.nb_col > 0
        self.nb_lig = int(self.planche.get_height() / self.taille_sprite[1])
        self.colorkey = colorkey

        self.cache = dict()  # association indice <> image
    
    def __extrais_vignette(self, boite4pts):
        """Loads image from a given (x,y, x+offset,y+offset)"""
        x_offset = boite4pts[2] - boite4pts[0]
        y_offset = boite4pts[3] - boite4pts[1]
        img_res = pygame.Surface((x_offset, y_offset))  # surface de destination, vide
        img_res.blit(self.planche, (0, 0), boite4pts)  # copie pixels de planche VERS coords (0, 0) dans img_res
        if self.colorkey is not None:
            img_res.set_colorkey(self.colorkey)
        return img_res

    def getSpriteCount(self):
        return self.nb_lig * self.nb_col

    def getSpriteNo(self, indice_planche):
        if indice_planche in self.cache:
            return self.cache[indice_planche]

        boite_adhoc = [0, 0, 0, 0]
        i = indice_planche % self.nb_col
        j = int(indice_planche / self.nb_col)
        # print(i,j)

        boite_adhoc[0] = i * self.taille_sprite[0]
        boite_adhoc[1] = j * self.taille_sprite[1]

        boite_adhoc[2] = (i + 1) * self.taille_sprite[0]

        boite_adhoc[3] = (j + 1) * self.taille_sprite[1]
        # print(str(boite_adhoc))

        res = self.__extrais_vignette(boite_adhoc)
        self.cache[indice_planche] = res
        return res

    def getStrip(self, li_indices):
        res = [self.getSpriteNo(ind) for ind in li_indices]
        return res


# --- tests
if __name__ == '__main__':
    pygame.init()
    cl = pygame.time.Clock()
    window = pygame.display.set_mode((250, 200))
    pygame.display.set_caption('test planche sprites')
    game_running = True
    bg_color = pygame.color.Color('pink')

    planche = PlancheSprites('../assets/pedro_planche.png', (48, 72), pygame.color.Color('blue'))
    nb_sprites = planche.getSpriteCount()
    print(str(nb_sprites))
    K = 30  # nb iterations avant de passer au sprite suivant
    iter_countdown = K
    current_spr_no = 0

    tmp_sprite = planche.getSpriteNo(current_spr_no)
    print(str(tmp_sprite.get_size()))
    while game_running:
        event_list = pygame.event.get()
        for ev in event_list:
            if ev.type == QUIT:
                game_running = False
                break

        # logique de jeu

        iter_countdown -= 1
        if iter_countdown == 0:
            iter_countdown = K
            current_spr_no = (current_spr_no + 1) % nb_sprites
            print('nouveau sprite: ' + str(current_spr_no))
            tmp_sprite = planche.getSpriteNo(current_spr_no)
            print(str(tmp_sprite.get_size()))
        # affichage
        window.fill(bg_color)
        window.blit(tmp_sprite, (0, 0))
        pygame.display.flip()
        cl.tick(30)

    pygame.quit()
