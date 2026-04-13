from pygame import *
from random import randint

lost = 0
score = 0

class GameSprite(sprite.Sprite):
  def __init__(self, player_image, player_x, player_y, width, height, player_speed):
    super().__init__()
    self.image = transform.scale(image.load(player_image), (width, height))
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
        if keys[K_RIGHT] and self.rect.x < win_width - 65:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 10)
        bullets.add(bullet)

class Enemy(GameSprite): 
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(60, 640)
            self.rect.y = 0
            lost += 1

class Asteroids(GameSprite): 
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(60, 640)
            self.rect.y = 0

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

win_width = 700
win_height = 500
display.set_caption('Shooter')
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
mixer.music.set_volume(0.2)
shoot = mixer.Sound('fire.ogg')

font.init()
font_1 = font.Font(None, 50)
font_2 = font.Font(None, 70)
font_3 = font.Font(None, 60)
win = font_2.render('You win!', True, (255, 215, 0))
lose = font_2.render('You lose!', True, (255, 0, 0))
retry = font_3.render('Пробел - повторить', True, (150, 200, 50))

ship = Player('rocket.png', 5, 430, 60, 60, 8)
finish = False
run = True

monsters = sprite.Group()
for _ in range(5):
    monster = Enemy('ufo.png', randint(60, 640), -40, 65, 65, randint(1,5))
    monsters.add(monster)

asteroids = sprite.Group()
for _ n range(7):
    asteroid = Asteroids('asteroid.png', randint(60, 640), -40, 20, 20, randint(10,25))
    asteroids.add(asteroid)

bullets = sprite.Group()

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
                if e.key == K_SPACE:
                    ship.fire()
                    shoot.play()

    if not finish:
        window.blit(background,(0,0))

        text = font_1.render(f'Счет: {score}', 1, (255,255,255))
        window.blit(text, (10, 20))
        text_lose = font_1.render(f'Пропущено: {lost}', 1, (255,255,255))
        window.blit(text_lose, (10, 50))
        
        ship.update()
        ship.reset()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        asteroids.update()
        asteroids.draw(window)

        collides = sprite.groupcollide(bullets, monsters, True, True)
        for collide in collides:
            monster = Enemy('ufo.png', randint(60, 640), -40, 65, 65, randint(1,5))
            monsters.add(monster)
            score += 1

        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False) or lost >= 3:
            finish = True
            window.blit(lose, (240, 225))
            window.blit(retry, (180, 275))
        
        if score >= 10:
            finish = True
            window.blit(win, (240, 225))
            window.blit(retry, (180, 275))

        display.update()
    else:
        wait = True
        while wait:
            for e in event.get():
                if e.type == QUIT:
                    run = False
                    wait = False
                elif e.type == KEYDOWN:
                    if e.key == K_SPACE:
                        finish = False
                        wait = False
        lost = 0
        score = 0
        for bullet in bullets:
            bullet.kill()
        for monster in monsters:
            monster.kill()
        for _ in range(5):
            monster = Enemy('ufo.png', randint(60, 640), -40, 65, 65, randint(1,5))
            monsters.add(monster)

    time.delay(30)