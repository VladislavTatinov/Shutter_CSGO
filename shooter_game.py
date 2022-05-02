from pygame import *
from random import *


img_back = '1587484087_3-p-foni-cs-go-5.jpg'
img_hero = 'saldat.png'
img_enemy = 'sobak.png'
img_enemy2 = 'luchkp.png'
font.init()
font2 = font.SysFont('Arial', 36)
font3 = font.SysFont('Arial',190)

score = 0
lost = 0

mixer.init()
mixer.music.load('sanf.mp3')
mixer.music.play()

img_bullet = 'kiberbull.png'

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 1050:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1



class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed

        if self.rect.y < 0:
            self.kill()

win_width = 1200
win_height = 700
display.set_caption('Shooter')
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

ship = Player(img_hero, 5, win_height - 100, 150, 100, 30)

monsters = sprite.Group()
for i in range(1, 5):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 100, randint(1, 5))
    monsters.add(monster)

monsters2 = sprite.Group()
for i in range(1, 3):
    monster = Enemy(img_enemy2, randint(80, win_width - 80), -40, 150, 100, randint(1, 5))
    monsters2.add(monster)
bullets = sprite.Group()
finish = False
life = 50
run = True 
lose = font3.render('Ты проиграл!', 1, (255, 0, 0))        
win = font3.render('Ты выиграл!', 1, (255, 0, 0))
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                # fire_sound.play()
                ship.fire()

    if not finish:
        window.blit(background,(0, 0))
        
        ship.update()

        ship.reset()

        

        text = font2.render('Счет: ' + str(score), 1, (255, 0, 0))
        window.blit(text, (10, 20))

        text_lose = font2.render('Пропущено: ' + str(lost), 1, (255, 0, 0))
        window.blit(text_lose, (10, 50))

        ser = font2.render('Жизни: ' + str(life), 1, (255, 0, 0))
        window.blit(ser, (10, 80))


     

        if sprite.spritecollide(ship, monsters, False) :
            if lost > 10:
                finish = True
                window.blit(lose, (200, 200))
            if life == 0:
                finish = True
                window.blit(lose, (200, 200))
            
            life = life - 1



        if score >= 10:
            finish = True
            window.blit(win, (100, 100))


        monsters.update()
        monsters2.update()

        monsters.draw(window)
        monsters2.draw(window)

        bullets.update()
        bullets.draw(window)
        
        collides = sprite.groupcollide(monsters, bullets, True, True)

        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)


        display.update()

    time.delay(26)