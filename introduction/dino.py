import pygame
from pygame.sprite import Sprite
import os

sprites_path = os.path.join('assets', 'sprites')
sounds_path = os.path.join('assets', 'sounds')
pygame.init()

clock = pygame.time.Clock()
clock.tick(2)

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

DARK = (15, 15, 15)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption("Dino - Game")

venu = pygame.image.load(
    os.path.join(sprites_path, 'sprite-ven.png')).convert_alpha()


class Dino(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.dino_img = []
        for i in range(167):
            img = venu.subsurface((0, 71*i), (86, 71))
            img = pygame.transform.scale(img, (86*1.5, 71*1.5))
            self.dino_img.append(img)

        self.index_list = 0
        self.image = self.dino_img[self.index_list]
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

    def update(self):
        if self.index_list > 166:
            self.index_list = 0
        self.index_list += 0.7
        self.image = self.dino_img[int(self.index_list)]

    def attack(self):
        self.animate = True


all_sprites = pygame.sprite.Group()
dino = Dino()
all_sprites.add(dino)

background_image = pygame.image.load("assets/images/tumblr.gif")
background_image = pygame.transform.scale(
    background_image, (SCREEN_WIDTH, SCREEN_HEIGHT+30))

clock = pygame.time.Clock()

while True:
    clock.tick(30)
    screen.fill(DARK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            dino.attack()
    screen.blit(background_image, (0, 0))
    all_sprites.draw(screen)
    all_sprites.update()

    pygame.display.flip()
