import pygame
from random import randint
import os

pygame.init()

# pygame.mixer.music.set_volume(0.05)
# pygame.mixer.music.load(
#     os.path.join('assets', 'sounds', 'background_music.mp3'))
# pygame.mixer.music.play(-1)

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

collision_sound = pygame.mixer.Sound(os.path.join(
    'assets', 'sounds', 'smw_coin.wav'))

IMG_APPLE = pygame.transform.scale(
    pygame.image.load(os.path.join('assets', 'images', 'apple.png')),
    (20, 20)
)

IMG_SNAKE = pygame.transform.scale(
    pygame.image.load(os.path.join('assets', 'images', 'snake.png')),
    (20, 20)
)

IMG_HEAD = pygame.transform.scale(
    pygame.image.load(os.path.join('assets', 'images', 'bird1.png')),
    (20, 20)
)


IMG_GAME_OVER = pygame.transform.scale(
    pygame.image.load(os.path.join('assets', 'images', 'game_over.png')),
    (SCREEN_WIDTH/1.5, 120))


x_snake = int(SCREEN_WIDTH / 2)
y_snake = int(SCREEN_HEIGHT / 2)

velocity = 10
x_control = velocity
y_control = 0

apple_x = randint(0, SCREEN_WIDTH-50)
apple_y = randint(0, SCREEN_HEIGHT-50)

points = 0

FONT_POINTS = pygame.font.SysFont('arial', 20, True, True)

screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

snake_list = []
initially_snake_length = 5


def grow_snake(snake_list):
    head = IMG_HEAD

    if y_control == 0:
        if x_control < 0:
            head = pygame.transform.rotate(IMG_HEAD, 180)
    elif x_control == 0:
        if y_control > 0:
            head = pygame.transform.rotate(IMG_HEAD, 270)
        elif y_control < 0:
            head = pygame.transform.rotate(IMG_HEAD, 90)

    for XandY in snake_list:
        if XandY == snake_list[0]:
            pygame.draw.rect(
                screen, (0, 255, 0), (XandY[0], XandY[1], 20, 20))
        elif XandY != snake_list[len(snake_list)-1]:
            screen.blit(IMG_SNAKE, (XandY[0], XandY[1]))
        else:
            screen.blit(head, (XandY[0], XandY[1]))


def restart_game():
    global points, initially_snake_length,  x_control, y_control
    global snake_list, head_list, x_snake, y_snake

    points = 0
    initially_snake_length = 5
    x_snake = int(SCREEN_WIDTH / 2)
    y_snake = int(SCREEN_HEIGHT / 2)
    head_list = []
    snake_list = []
    x_control = 10
    y_control = 0


def game_over(screen, points, running):
    screen.fill((0, 0, 0))
    game_over = IMG_GAME_OVER.get_rect(
        center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    game_over.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    screen.blit(IMG_GAME_OVER, game_over)

    text = FONT_POINTS.render(f'Pontuação: {points}', 1, (255, 255, 255))
    screen.blit(text, (SCREEN_WIDTH - 10 - text.get_width(), 10))

    formated_text = FONT_POINTS.render(
        'Pressione [Spaço] para reiniciar', True, (255, 255, 255))
    rect_text = formated_text.get_rect()
    rect_text.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/1.5)
    screen.blit(formated_text, rect_text)

    pygame.display.update()
    pygame.time.delay(1000)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return running


running = True
while running:

    clock.tick(30)
    screen.fill((15, 15, 15))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

            elif event.key == pygame.K_w:
                if y_control != velocity:
                    y_control -= velocity
                    x_control = 0
            elif event.key == pygame.K_s:
                if y_control != -velocity:
                    y_control += velocity
                    x_control = 0
            elif event.key == pygame.K_d:
                if x_control != -velocity:
                    x_control += velocity
                    y_control = 0
            elif event.key == pygame.K_a:
                if x_control != velocity:
                    x_control -= velocity
                    y_control = 0

    x_snake += x_control
    y_snake += y_control

    snake = pygame.draw.rect(screen, (15, 15, 15), (x_snake, y_snake, 20, 20))
    apple = screen.blit(IMG_APPLE, (apple_x, apple_y))

    if snake.colliderect(apple):
        apple_x = randint(0, SCREEN_WIDTH-50)
        apple_y = randint(0, SCREEN_HEIGHT-50)
        points += 1
        collision_sound.play()
        initially_snake_length += 1

    # Game over ao colidir com a parede
    # if (snake.y >= SCREEN_HEIGHT or snake.y <= 0
    #         or snake.x >= SCREEN_WIDTH or snake.x <= 0):
    #     if(game_over(screen, points, running)):
    #         restart_game()

    # Permitindo atravessar paredes
    if x_snake > SCREEN_WIDTH:
        x_snake = 0
    if x_snake < 0:
        x_snake = SCREEN_WIDTH
    if y_snake > SCREEN_HEIGHT:
        y_snake = 0
    if y_snake < 0:
        y_snake = SCREEN_HEIGHT

    head_list = []
    head_list.append(x_snake)
    head_list.append(y_snake)

    snake_list.append(head_list)

    if snake_list.count(head_list) > 1:
        if(game_over(screen, points, running)):
            restart_game()

    grow_snake(snake_list)

    if len(snake_list) > initially_snake_length:
        del snake_list[0]

    text = FONT_POINTS.render(f'Pontuação: {points}', True, (255, 255, 255))
    screen.blit(text, (SCREEN_WIDTH - 10 - text.get_width(), 10))

    pygame.display.update()
