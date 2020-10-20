
import pygame
import random


WIDTH = 1600
HEIGHT = 900
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Helicopter Game")
clock = pygame.time.Clock()
picture = [pygame.image.load('separated_frames/helicopter_1.png'),
           pygame.image.load('separated_frames/helicopter_2.png'),
           pygame.image.load('separated_frames/helicopter_3.png'),
           pygame.image.load('separated_frames/helicopter_4.png'),
           pygame.image.load('separated_frames/helicopter_5.png'),
           pygame.image.load('separated_frames/helicopter_6.png'),
           pygame.image.load('separated_frames/helicopter_7.png'),
           pygame.image.load('separated_frames/helicopter_8.png')]
helicopter_sound = pygame.mixer.Sound('helicopter.wav')
helicopter_sound.set_volume(0.008)
explosion = pygame.mixer.Sound('explosion.wav')
explosion.set_volume(0.1)
font_name = pygame.font.match_font('arialw')


def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)
def Welcome_Exit_Screen():
    draw_text(screen, 'Press any key to start ', 50, WIDTH / 2 + 200, HEIGHT / 3)
    draw_text(screen, 'Press or hold "W" to go up ', 50, WIDTH / 2 + 200, HEIGHT / 2)
    pygame.display.flip()
    pause = True
    while pause:
        clock.tick(FPS)
        for event1 in pygame.event.get():
             if event1.type == pygame.KEYDOWN:
                pause = False
             if event1.type == pygame.QUIT:
                pygame.quit()


class Helicopter(pygame.sprite.Sprite):
    def __init__(self, picture):
        super().__init__()
        self.index = 0
        self.image = picture[self.index]
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 2
        self.height = self.rect.h
        self.width = self.rect.w
        self.score = 0
        self.vel = 0
        self.acc = 0
        self.friction = -0.2

    def update(self):
        self.score += 1
        self.index += 1
        if self.index >= len(picture):
            self.index = 0
        self.image = picture[self.index]

        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_w]:
            self.acc = -1.2
            helicopter_sound.play(0,-1,10)

        else:
            self.acc = 1.2
            self.image = pygame.transform.rotate(self.image, 355)
        self.acc += self.vel * self.friction
        self.vel += self.acc
        self.rect.y += self.vel + 0.5 * self.acc


class OBSTACLES(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('obstacle.png')
        self.rect = self.image.get_rect()
        self.height = self.rect.h
        self.rect.x = x
        self.rect.y = random.randrange(150, HEIGHT - self.height - 150)
        self.speedx = 10

    def update(self):
        self.rect.x -= self.speedx
        if self.rect.x < 10:
            self.rect.x = WIDTH
            self.rect.y = random.randrange(150, HEIGHT - self.height - 150)


class BOT(pygame.sprite.Sprite):
    def __init__(self, x=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('obstacle.png')
        self.rect = self.image.get_rect()
        self.width = self.rect.w
        self.rect.x = x
        self.rect.y = random.randint(HEIGHT - 140, HEIGHT - 50)
        self.y = self.rect.y
        self.pace = 5

    def update(self):
        self.rect.x -= self.pace * 2
        if self.rect.x <= -(self.pace * 10):
            self.rect.x = WIDTH
            self.rect.y = random.randint(HEIGHT - 140, HEIGHT - 50)

class TOP(pygame.sprite.Sprite):
    def __init__(self, x=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('obstacle.png')
        self.rect = self.image.get_rect()
        self.width = self.rect.w
        self.rect.x = x
        self.rect.y = random.randint(-100, 0)
        self.y = self.rect.y
        self.pace = 5

    def update(self):
        self.rect.x -= self.pace * 2
        if self.rect.x <= -(self.pace * 10):
            self.rect.x = WIDTH
            self.rect.y = random.randint(-100, 0)


def GameOver():
    helicopter_sound.stop()
    explosion.play()
    score = helicopter.score
    h = helicopter.height
    w = helicopter.width
    x = int(helicopter.rect.x + w / 2)
    y = int(helicopter.rect.y + h / 2)
    pygame.draw.circle(screen, RED, (x, y), 100, 5)
    print(score)
Run = True
exit = True
# Game loop
while exit:
    if Run:

        Run = False
        Welcome_Exit_Screen()
        backgroundlist = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900,
                          950, 1000, 1050, 1100, 1150, 1200,1250,1300,1350,1400,1450,1500,1550,1600]
        obstacle_list = [WIDTH / 3 + WIDTH,WIDTH * 2 / 3 + WIDTH, WIDTH + WIDTH]
        helicopter = Helicopter(picture)
        background = pygame.sprite.Group()
        for i in obstacle_list:
            ob = OBSTACLES(i)
            background.add(ob)
        for i in backgroundlist:
            bt = BOT(i)
            tp = TOP(i)
            background.add(bt)
            background.add(tp)
        all_sprites = pygame.sprite.Group()
        all_sprites.add(helicopter)
        pygame.time.wait(250)

    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            exit = False

    # Update
    all_sprites.update()
    background.update()

    # Draw / render
    screen.fill(BLACK)
    background.draw(screen)
    all_sprites.draw(screen)
    # collision
    collide = pygame.sprite.groupcollide(all_sprites, background, '', '')
    if collide:
        GameOver()
        Run = True

    pygame.display.update()

pygame.quit()
