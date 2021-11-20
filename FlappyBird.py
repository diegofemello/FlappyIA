import pygame
import os
import random

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800

IMG_PIPE = pygame.transform.scale2x(pygame.image.load(
    os.path.join('assets', 'images', 'pipe.png')))

IMG_FLOOR = pygame.transform.scale2x(pygame.image.load(
    os.path.join('assets', 'images', 'base.png')))

IMG_BG = pygame.transform.scale2x(pygame.image.load(
    os.path.join('assets', 'images', 'bg.png')))

IMG_BIRD = [
    pygame.transform.scale2x(pygame.image.load(
        os.path.join('assets', 'images', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(
        os.path.join('assets', 'images', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(
        os.path.join('assets', 'images', 'bird3.png'))),
]

pygame.font.init()
FONT_POINTS = pygame.font.SysFont('comicsans', 30)


class Bird:
    IMGS = IMG_BIRD
    # Animações da rotação
    MAX_ROTATION = 25
    VEL_ROTATION = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.vel = 0
        self.height = self.y
        self.time = 0
        self.img_count = 0
        self.img = self.IMGS[0]

    # Calculo para o pulo do pássaro
    def jump(self):
        self.vel = -10.5
        self.time = 0
        self.height = self.y

    # Calcular o deslocamento (S = so + vot + at²/2)
    def move(self):
        self.time += 1
        displacement = 1.5 * (self.time**2) + self.vel * self.time

        # Restringir o deslocamento
        if displacement > 16:
            displacement = 16
        elif displacement < 0:
            displacement -= 2

        self.y += displacement

        # o angulo do pássaro
        if displacement < 0 or self.y < (self.height + 50):
            if self.angle < self.MAX_ROTATION:
                self.angle += self.MAX_ROTATION
        else:
            if self.angle > -90:
                self.angle -= self.VEL_ROTATION

    # Desenhar o pássaro
    def draw(self, screen):
        # Definir a imagem do passáro
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        # Se o passaro estiver caindo não bater asas
        if self.angle <= -90:
            self.image = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        # Desenhar a imagem do passáro
        rotated_img = pygame.transform.rotate(self.img, self.angle)
        pos_center_img = self.img.get_rect(topleft=(self.x, self.y)).center
        rectangle = rotated_img.get_rect(center=pos_center_img)
        screen.blit(rotated_img, rectangle.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe:
    DISTANCE = 200
    VELOCITY = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top_position = 0
        self.base_position = 0
        self.PIPE_TOP = pygame.transform.flip(IMG_PIPE, False, True)
        self.PIPE_BASE = IMG_PIPE
        self.passed = False
        self.height_definiton()

    # Definir a altura do cano
    def height_definiton(self):
        self.height = random.randrange(50, SCREEN_HEIGHT-250)
        self.top_position = self.height - self.PIPE_TOP.get_height()
        self.base_position = self.height + self.DISTANCE

    # Mover o cano
    def move(self):
        self.x -= self.VELOCITY

    # Desenhar o cano
    def draw(self, screen):
        screen.blit(self.PIPE_TOP, (self.x, self.top_position))
        screen.blit(self.PIPE_BASE, (self.x, self.base_position))

    def colide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        base_mask = pygame.mask.from_surface(self.PIPE_BASE)

        top_distance = (self.x - bird.x, self.top_position - round(bird.y))
        base_distance = (self.x - bird.x, self.base_position - round(bird.y))

        top_point = bird_mask.overlap(top_mask, top_distance)
        base_point = bird_mask.overlap(base_mask, base_distance)

        if top_point or base_point:
            return True
        else:
            return False


class Floor:
    VELOCITY = 5
    WIDTH = IMG_FLOOR.get_width()
    IMAGE = IMG_FLOOR

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VELOCITY
        self.x2 -= self.VELOCITY

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, screen):
        screen.blit(self.IMAGE, (self.x1, self.y))
        screen.blit(self.IMAGE, (self.x2, self.y))


def draw_screen(screen, birds, pipes, floor, points):
    screen.blit(IMG_BG, (0, 0))
    for bird in birds:
        bird.draw(screen)
    for pipe in pipes:
        pipe.draw(screen)
    text = FONT_POINTS.render(f'Pontuação: {points}', 1, (255, 255, 255))
    screen.blit(text, (SCREEN_WIDTH - 10 - text.get_width(), 10))
    floor.draw(screen)

    pygame.display.update()


def main():
    birds = [Bird(SCREEN_WIDTH/2.2, SCREEN_HEIGHT/2.2)]
    floor = Floor(SCREEN_HEIGHT - 50)
    pipes = [Pipe(SCREEN_HEIGHT - 100)]
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    points = 0
    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for bird in birds:
                        bird.jump()

        for bird in birds:
            bird.move()
        floor.move()

        add_pipe = False
        remove_pipe = []

        for pipe in pipes:
            for i, bird in enumerate(birds):
                if pipe.colide(bird):
                    birds.pop(i)
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True
            pipe.move()

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                remove_pipe.append(pipe)

        if add_pipe:
            points += 1
            pipes.append(Pipe(SCREEN_WIDTH + 100))
        for pipe in remove_pipe:
            pipes.remove(pipe)

        for i, bird in enumerate(birds):
            if (bird.y + bird.img.get_height() >= floor.y or bird.y < 0):
                birds.pop(i)

        draw_screen(screen, birds, pipes, floor, points)


if __name__ == '__main__':
    main()
