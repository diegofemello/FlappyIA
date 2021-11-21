import pygame
from pygame.sprite import Sprite
import os

pygame.init()

clock = pygame.time.Clock()
clock.tick(2)

SCREEN_HEIGHT = 480
SCREEN_WIDTH = 640

DARK = (15, 15, 15)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption("Sprites")


bg_image = pygame.image.load(
    os.path.join('assets', 'sprites', 'pantanosprite.png')).convert_alpha()


class Character(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.sprites = []
        for i in range(1, 10):
            self.sprites.append(pygame.image.load(
                f"assets/sprites/frog/attack_{i}.png"))
        self.actual_sprite = 0
        self.image = self.sprites[self.actual_sprite]

        self.image = pygame.transform.scale(self.image, (128*3, 64*3))

        self.rect = self.image.get_rect()
        self.rect.topleft = (210, 80)

        self.animate = False

    def update(self):
        if self.animate:
            self.actual_sprite += 0.6
            if self.actual_sprite >= len(self.sprites):
                self.actual_sprite = 0
                self.animate = False
            self.image = self.sprites[int(self.actual_sprite)]
            self.image = pygame.transform.scale(self.image, (128*3, 64*3))

    def attack(self):
        self.animate = True


class Background(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.background = []
        for i in range(20):
            img = bg_image.subsurface((0, 400*i), (640, 400))
            img = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT+25))
            self.background.append(img)

        self.index_list = 0
        self.image = self.background[self.index_list]
        self.rect = self.image.get_rect()

    def update(self):
        if self.index_list > 19:
            self.index_list = 0
        self.index_list += 0.3
        self.image = self.background[int(self.index_list)]


all_sprites = pygame.sprite.Group()
character = Character()
bg = Background()
all_sprites.add(bg)

all_sprites.add(character)
clock = pygame.time.Clock()

while True:
    clock.tick(30)
    screen.fill(DARK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            character.attack()
    all_sprites.draw(screen)
    all_sprites.update()

    pygame.display.flip()
