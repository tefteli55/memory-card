#Создай собственный Шутер!

from pygame import *
from random import randint

#фон сцены
background = transform.scale(image.load('dom.jpg'), (700,500))

#создaй окно игры
window = display.set_mode((700, 500))
display.set_caption('Шутер')

#Подключение музыки
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

#работа со шрифтами
font.init()
#font1 = font.Font(None, 36)
font1 = font.SysFont('Arial', 36)

#класс спрайтав
class GameSprite(sprite.Sprite):
    def __init__(self, img, x,y, w,h, speed):
        super().__init__()
        self.image = transform.scale(image.load(img),(w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def collidepoint(self, x, y):
        return self.rect.collidepoint(x,y)

#класс плэйера
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x>10:  
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x<700-10-self.rect.width:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.y, 20, 30, 20)
        bullets.add(bullet)




#класс свинюшэк
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 500 - self.rect.height:
            self.rect.x = randint(10, 700-10-self.rect.width)
            self.rect.y = -self.rect.height
            self.speed = randint(2,3)
            lost += 1

#класс пуле
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

#танчеке, свинке
hero = Player('tank.png', 300,400, 60,100, 13)

bullets = sprite.Group()

enemy_count = 6
enemyes = sprite.Group()
for i in range(enemy_count):
    enemy = Enemy('svinka.png', randint(10, 700-10-90), -40, 90, 60, randint(2,5))
    enemyes.add(enemy)

button = GameSprite('play.png', 300, 200, 100, 50, 0)



#цикл
game = True
finish = True
menu = True
lost = 0
score = 0
clock = time.Clock()
FPS = 40
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                hero.fire()

    if menu:
        window.blit(background, (0,0))
        button.reset()
        pressed = mouse.get_pressed()
        pos = mouse.get_pos()
        if pressed[0]: 
            if button.collidepoint(pos[0], pos[1]):
                menu = False
                finish = False

    if not finish:
        window.blit(background, (0,0))

        hero.update()
        hero.reset()

        enemyes.update()
        enemyes.draw(window)

        bullets.update()
        bullets.draw(window)

        lost_enemy = font1.render('Пропущено: '+str(lost), 1, (255, 255, 255))
        window.blit(lost_enemy, (10,10))

        score_enemy = font1.render('Убито: '+str(score), 1, (255, 255, 255))
        window.blit(score_enemy, (10,40))

        sprite_list = sprite.groupcollide(
            enemyes, bullets, True, True
        )
        for i in range(len(sprite_list)):
            score += 1
            enemy = Enemy('svinka.png', randint(10, 700-10-90), -40, 90, 60, randint(2,5))
            enemyes.add(enemy)

        if score >30:
            finish = True
            text_win = font1.render('YOU WIN', 1, (255,255,255))
            window.blit(text_win, (300,200))

        sprite_list = sprite.spritecollide(hero, enemyes, True)
        if lost>=10 or len(sprite_list)>0:
            finish = True
            text_lose = font1.render('YOU LOSE', 1, (255,255,255))
            window.blit(text_lose, (300,200))


    clock.tick(FPS)
    display.update()

    

