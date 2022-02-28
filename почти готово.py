import sys
from random import randint
import pygame as pg
import time
import sqlite3

BLOCK_SIZE = 60
game_over = False
pg.font.init()
font_style = pg.font.SysFont(None, 25)
balls = []
volume = 0.2
music = True
pg.init()

width, height = 420, 600
pg.mixer.music.load('LHS-RLD10.mp3')
pg.mixer.music.play(99999)
pg.mixer.music.set_volume(volume)
# volume отвечает за уровень громкости
sound1 = pg.mixer.Sound('shoot.mp3')
sound2 = pg.mixer.Sound('Game over.mp3')
sound2.set_volume(volume)
pg.display.set_caption("Balls and blocks")
all_rects = []
fps = 100
screen = pg.display.set_mode((width, height))
clock = pg.time.Clock()
move = pg.USEREVENT
pg.time.set_timer(move, 2)
pg.init()
arrow = pg.image.load("arrow1.png")
r = arrow.get_rect()
pg.mouse.set_visible(False)
dis = pg.display.set_mode((width, width))
color_list = ["black"] * 70
img = pg.image.load('112.jpg').convert()
for i in range(0, height, BLOCK_SIZE):
    for j in range(0, width, BLOCK_SIZE):
        rect = pg.Rect(j, i, BLOCK_SIZE - 1, BLOCK_SIZE - 1)
        all_rects.append(rect)

sc = pg.display.set_mode((width, height))
background = pg.Surface((420, 600))

sc.blit(background, (0, 0))
x2 = 210
y2 = 590
ball_radius = 10
ball_rect = int(ball_radius * 2)
ball = pg.Rect(x2, y2, ball_rect, ball_rect)


con = sqlite3.connect('records')
cur = con.cursor()

result = cur.execute("""
SELECT счёт from the_best_score """).fetchall()


class Ball:
    def __init__(self, obj, x, y, v, t):
        self.obj = obj
        self.x = x
        self.y = y
        self.dx = -v * t
        self.dy = -v
        # dх отвечает за направление движение вдоль оси ох
        # нужно сделать 3 варианта dx = v/ -v/ 0
        # то есть движение вправо влево и  вертикально вверх

    def move(self, block=None):
        if self.obj.centerx < ball_radius or self.obj.centerx > width - ball_radius:
            self.dx = -self.dx
        # collision top
        if self.obj.centery < ball_radius:
            self.dy = -self.dy
        if block:
            if self.dx > 0:
                delta_x = self.obj.right - block.left
            else:
                delta_x = block.right - self.obj.left
            if self.dy > 0:
                delta_y = self.obj.bottom - block.top
            else:
                delta_y = block.bottom - self.obj.top

            if abs(delta_x - delta_y) < 10:
                self.dx = -self.dx
                self.dy = -self.dy
            elif delta_x > delta_y:
                self.dy = -self.dy
            elif delta_y > delta_x:
                self.dx = -self.dx

        self.x += self.dx
        self.y += self.dy

image = pg.image.load("game_over1.jpg")

gameover = pg.sprite.Sprite()
gameover.image = pg.Surface((420, 600))
gameover.image = image
gameover.rect = gameover.image.get_rect()
gameover.rect.x = 0
gameover.rect.y = 0

pg.display.update()


def message(msg, color, k):
    m = result[0][0]
    if k > m:
        m = k
    mesg = font_style.render('The best score: {}'.format(m), True, color)
    mesg2 = font_style.render(msg, True, color)
    sc.blit(mesg, (270, 5))
    sc.blit(mesg2, (342, 25))


k = 0
n = 0
d = 0
while not game_over:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()

        elif event.type == pg.MOUSEMOTION:
            r.topleft = event.pos

        elif balls and event.type == move:
            for b in balls:
                b.move()
                x2 = b.x
                y2 = b.y
                ball.x = x2
                ball.y = y2
                if b.y == 590:
                    balls = []

        elif event.type == pg.KEYUP:

            # при нажатии на кнопку 1 музыка ставится либо на паузу либо включается
            if event.key == pg.K_1:
                if music == True:
                    pg.mixer.music.pause()
                    music = False
                else:
                    pg.mixer.music.unpause()
                    music = True
            # при нажатии на кнопку 2 громкость увеличивается
            # а при нажатии на 3 громкость уменьшается
            elif event.key == pg.K_2 and volume < 1:
                volume += 0.1
                pg.mixer.music.set_volume(volume)
            elif event.key == pg.K_3 and volume > 0:
                volume -= 0.1
                pg.mixer.music.set_volume(volume)

        elif event.type == pg.KEYDOWN and balls == []:
            KEY = 2
            if event.key == pg.K_LEFT:
                KEY = 1
            elif event.key == pg.K_RIGHT:
                KEY = -1
            elif event.key == pg.K_UP:
                KEY = 0
            if KEY != 2 and n < 10:
                pos = pg.mouse.get_pos()
                a = [pos[0], 590, 1]
                balls.append(Ball(ball, *a, KEY))
                sound1.play()

                n += 1
                for i in range(5):
                    for g, rect in enumerate(all_rects[7 * (n - 1):7 * n]):
                        if rect.collidepoint(randint(0, 420), 58 * n):

                            if color_list[g + 7 * (n - 1)] == "black":
                                color_list[g + 7 * (n - 1)] = (randint(0, 255), randint(0, 255), randint(0, 255))

    screen.fill(pg.Color("black"))

    hit_index = ball.collidelist(all_rects)
    if hit_index != -1:
        if color_list[hit_index] != (0, 0, 0) and color_list[hit_index] != 'black':
            hit_rect = all_rects[hit_index]
            for b in balls:
                b.move(hit_rect)
            color_list[hit_index] = (0, 0, 0)
            d = 1

    sc.blit(img, (0, 0))
    if n < 10:

        for i, rect in enumerate(all_rects):
            if color_list[i] != (0, 0, 0) and color_list[i] != 'black':
                pg.draw.rect(sc, color_list[i], rect)

        replaced_text = ((str(r).replace('<rect(', '')).replace(')>', '')).split(", ")
        x1, y1 = int(replaced_text[0]), int(replaced_text[1])
        background.blit(sc, (x2, y2))
        sc.blit(arrow, (x1, y1))

        pg.draw.circle(sc, pg.Color('red'), (x2, y2), ball_radius)

        if hit_index != -1:
            if d:
                k += 1
                d = 0
            message(f'Score: {k}', 'red', k)
        pg.display.flip()

    else:
        sc.blit(gameover.image, (0, -100))
        pg.mouse.set_visible(True)
        if gameover.rect.bottom >= height:
            game_over = True
            pg.mixer.music.stop()
            sound2.play()

    pg.display.flip()
    pg.display.update()
    pg.time.delay(30)

if k > result[0][0]:
    cur.execute("""UPDATE the_best_score
        SET счёт = {}""".format(k)).fetchall()
con.commit()
con.close()
pg.display.update()
time.sleep(3)
