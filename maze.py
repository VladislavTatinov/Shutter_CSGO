from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (70, 70))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
      

class Enemy(GameSprite):
    def update(self):
        if self.rect.x <= 180:
            self.side = 'right'
        if self.rect.x >= win_width - 195:
            self.side = 'left'
        if self.side == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height

        self.image = Surface((self.width, self.height))
        self.image.fill((self.color_1, self.color_2, self.color_3))

        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    # final = GameSprite('treasure.png', win_width - 120, win_height - 80, 0)

w1 = Wall(139, 0, 255, 205, 110, 10, 350)
w2 = Wall(139, 0, 255, 205, 480, 290, 10)
w3 = Wall(139, 0, 255, 300, 20, 10, 350)
w4 = Wall(139, 0, 255, 400, 10, 10, 390)
w5 = Wall(139, 0, 255, 600, 10, 15, 400)
w6 = Wall(139, 0, 255, 500, 200, 10, 300)

game = True
finish = False
clock = time.Clock()
FPS = 120


mixer.init()
mixer.music.load('main.mp3')
mixer.music.play()

money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')

            
    
win_width = 800
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Maze')
background = transform.scale(image.load('9.jpg'), (win_width, win_height))

player = Player('among-us-6044191_1280.png', 3, 300, 10)
monster = Enemy('Amogus.png', 650, 240, 20)
final = GameSprite('treasure.png', win_width - 120, win_height - 80, 0)

game = True

font.init()
font = font.Font(None, 70)
win = font.render('Успех!', True, (255, 215, 0))
lose = font.render('Потрачено', True, (180, 0, 0))


while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if finish != True:
        window.blit(background, (0, 0))
        player.reset()
        monster.reset()

        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()
        w4.draw_wall()
        w5.draw_wall()
        w6.draw_wall()
        final.reset()

        #Проигрыш
        if sprite.collide_rect(player, monster) or sprite.collide_rect(player, w1) \
        or sprite.collide_rect(player, w2) or sprite.collide_rect(player, w3):
            finish = True
            mixer.music.stop()
            window.blit(lose, (200, 200))
            kick.play()

        #Выигрыш
        if sprite.collide_rect(player, final):
            finish = True
            window.blit(win, (200, 200))
            money.play()


        monster.update()
        player.update()
        display.update()
        time.Clock().tick(60)