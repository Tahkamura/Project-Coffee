import pygame
from pygame.locals import *
import random
import time
import concurrent.futures
import logging
import queue
import threading
import socket
import sys

WIDTH = 1920
HEIGHT = 1080
#FPS = 30

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# initialize pygame and create window
#pygame.init()
#pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
#screen = pygame.display.get_surface()
#w,h = screen.get_width(),screen.get_height()
#screen = pygame.display.set_mode((w,h),flags^FULLSCREEN,bits)
pygame.display.set_caption("Matiaksen peli ")
clock = pygame.time.Clock()
counter = 0
score = 0

global data
data = ""
global data2
data2 = ""
lock = threading.Lock()
global nuq
nuq = 0.002

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT/2
        self.speedx = 0
        self.speedy = 0

    def update(self):
        #self.speedx = 0
        #self.speedy = 0
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
        if self.rect.right > WIDTH-200:
            self.rect.right = WIDTH-200
        if self.rect.left < 200:
            self.rect.left = 200
        if self.rect.y > HEIGHT -80:
            self.rect.y = HEIGHT-80
        if self.rect.y < 80:
            self.rect.y = 80

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
  
class Gamerun(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        global data
        global nuq
        global counter
        global data2
        running = True
        while running:
            lock.acquire()
            print("Ykkosthreadin data:", data2)
            while data2.find("Sormi 1") is not -1:
                player.shoot()
                data2 = ""
                break
            while data2.find("Vasen") is not -1:
                player.speedx = -4
                break
            while data2.find("Oikea") is not -1:
                player.speedx = 4
                break
            while data2.find("Ylos") is not -1:
                player.speedy = -4
                break
            while data2.find("Alas") is not -1:
                player.speedy = 4
                break
            while data2.find("Sormi 2") is not -1:
                counter += 1
                data2 = ""
                break
            if counter == 4:
                counter = 0
            while data2.find("XNada") is not -1:
                player.speedx = 0
                break
            while data2.find("YNada") is not -1:
                player.speedy = 0
                break
            # keep loop running at the right speed
            #clock.tick(FPS)
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

            # check to see if a mob hit the player
            hits = pygame.sprite.spritecollide(player, mobs, False)
            if hits:
                print(":'(")
                running = False
                print("Final score: ", score)
                #screen.display.close()
                
               
                
                pygame.quit()
                thread1._Thread_stop()
                
               
               

            # Draw / render
            screen.fill(BLACK)
            all_sprites.draw(screen)
            # *after* drawing everything, flip the display
            pygame.display.flip()
            lock.release()
            time.sleep(nuq)
        pygame.quit()

class Yhteys(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print ('Starting Thread')
        global data
        global nuq
        global data2

        TCP_IP = '192.168.43.195' #127.0.0.1
        TCP_PORT = 5005
        BUFFER_SIZE = 20  # Normally 1024, but we want fast response

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((TCP_IP, TCP_PORT))
        s.listen(1)

        conn, addr = s.accept()
        print ('Connection address:', addr)
        while 1:
            #lock.acquire()
            data = conn.recv(BUFFER_SIZE)
            data2 = data.decode('utf-8')
            #print (data2)
            conn.send(data)  # echo
            #lock.release()
            time.sleep(nuq)
        #conn.close()

class shoot (threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)
   def run(self):
      global data
      muuttuja = 2
      print ("Starting schoolshooting ")
      while 1:
          if muuttuja == 1:
              lock.acquire()
              data = "bam"
              muuttuja = 2
              lock.release()
              #time.sleep(0.2)
          if muuttuja == 2:
              lock.acquire()
              data = "vasen"
              muuttuja = 3
              lock.release()
              #time.sleep(0.2)
          if muuttuja == 3:
              lock.acquire()
              data = "oikea"
              muuttuja = 4
              lock.release()
              #time.sleep(0.2)
          if muuttuja == 4:
              lock.acquire()
              data = "ylos"
              muuttuja = 5
              lock.release()
          if muuttuja == 5:
              lock.acquire()
              data = "alas"
              muuttuja = 6
              lock.release()
          if muuttuja == 6:
              lock.acquire()
              data = "vaihto"
              muuttuja = 1
              lock.release()

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
thread1 = Gamerun(1, "Thread-1", 1)
thread2 = Yhteys(2, "Thread-2", 2)
thread3 = shoot()
all_sprites.add(player)
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

# Game loop
#running = True

def main():

    WIDTH = 1920
    HEIGHT = 1080
    FPS = 30

    # colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.get_surface()
    pygame.display.set_mode((WIDTH,HEIGHT), pygame.FULLSCREEN)
    #screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Matiaksen peli ")
    clock = pygame.time.Clock()
    counter = 0
    score = 0
    thread1.start()
    thread2.start()
    #thread3.start()
    

    

if __name__ == "__main__":
    main()

    
#pygame.quit()