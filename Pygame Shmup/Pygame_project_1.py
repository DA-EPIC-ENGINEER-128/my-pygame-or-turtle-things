import os
import random

import pygame

WIDTH = 1396
HEIGHT = 856
FPS = 60

white = (255, 255, 255)
black = (0, 0, 0)
gray = (60, 60, 60)

# folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "images (assets)")

dead = False


class Player(pygame.sprite.Sprite):
    # player sprite
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .9 / 2)
        # pygame.draw.circle(self.image, gray, self.rect.center, self.radius)
        self.rect.centerx = int(WIDTH / 2)
        self.rect.bottom = HEIGHT - 10
        self.x_speed = 0

    def update(self):
        self.x_speed = 0
        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_a]:
            self.x_speed = -7
        if key_state[pygame.K_d]:
            self.x_speed = 7
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        self.rect.x += self.x_speed

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2)
        # pygame.draw.circle(self.image, gray, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.y_speed = random.randrange(1, 8)
        self.x_speed = random.randrange(-4, 4)

    def update(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        if self.rect.top > HEIGHT + 10 or self.rect.left < -105 or self.rect.right > WIDTH + 105:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.y_speed = random.randrange(1, 8)
        if dead:
            self.image = pygame.transform.scale(enemy_death, (40, 56))
            self.rect = self.image.get_rect()
            self.image.set_colorkey(black)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.y_speed = -10

    def update(self):
        self.rect.y += self.y_speed
        if self.rect.bottom < 0:
            self.kill()


pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Alien Invaders Pygame Edition.")
clock = pygame.time.Clock()

back = pygame.image.load(os.path.join(img_folder, "back1.png")).convert()
back_rect = back.get_rect()
player_img = pygame.image.load(os.path.join(img_folder, "ship.png")).convert()
bullet_img = pygame.image.load(os.path.join(img_folder, "Bullet.png")).convert()
enemy_img = pygame.image.load(os.path.join(img_folder, "enemy_ship.png")).convert()
enemy_death = pygame.image.load(os.path.join(img_folder, "p1_jump.png")).convert()

# SPRITES
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

running = True

while running:
    # EVENTS
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.shoot()

    # DRAWING/RENDERING
    screen.fill(gray)
    screen.blit(back, back_rect)
    all_sprites.draw(screen)
    # UPDATES
    pygame.display.update()
    all_sprites.update()

    # COLLISIONS
    hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
    if hits:
        running = False

    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
        dead = True
