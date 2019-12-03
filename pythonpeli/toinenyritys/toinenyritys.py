import pygame
import random
import time
#import keyboard

WIDTH = 1270
HEIGHT = 720
FPS = 30

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Matiaksen peli")
clock = pygame.time.Clock()
#<<<<<<< HEAD
counter = 0
score = 0


#=======
#pygame.display.set_caption("jaakko on gei")
#>>>>>>> 9aad2c00641988ef09586c5a7e9b7e3ea070f352
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        #self.rect = self.image.load('player.png')
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_UP]:
            self.speedy = -8
        if keystate[pygame.K_DOWN]:
            self.speedy = 8
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.y > HEIGHT - 40:
            self.rect.y = HEIGHT - 40
        if self.rect.y < 0:
            self.rect.y = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 2)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 3)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((8, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        self.speedx = 0 # ampuu sivulle
        global counter

        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_n]:
            counter += 1
            
            #self.speedx = 10
            #self.speedy = 0
        if counter == 1:
                self.speedx = 10
                self.speedy = 0
                pygame.sprite.Sprite.__init__(self)
                self.image = pygame.Surface((20, 8))
                self.image.fill(YELLOW)
                self.rect = self.image.get_rect()
                self.rect.bottom = y + 20
                self.rect.centerx = x
        if counter == 2:
                self.speedx = 0
                self.speedy = 10
                self.rect.bottom = y + 20
        if counter == 3:
                self.speedx = -10
                self.speedy = 0
                pygame.sprite.Sprite.__init__(self)
                self.image = pygame.Surface((20, 8))
                self.image.fill(YELLOW)
                self.rect = self.image.get_rect()
                self.rect.bottom = y + 20
                self.rect.centerx = x
        if counter == 4:
                counter = 0
        #print(counter)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx # ampuu sivulle
        #self.speedy = -10



        # kill if it moves off the screen
        if self.rect.bottom < 0:
            self.kill()
        if self.rect.top < 0:
            self.kill()
        if self.rect.left < 0:
            self.kill()
        if self.rect.right > WIDTH:
            self.kill()

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
        

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Update
    all_sprites.update()

    # check to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

    if hits:
        score = score + 1
        print(score)

    # check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(player, mobs, False)
    if hits:
        print(":'(")
        #draw_text(screen, str(score), 18, WIDTH / 2, HEIGHT / 2)
        running = False
        print("Final score: ", score)
        if score > 50:
            print("Good job :)")

    # Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()