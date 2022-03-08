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

colors_dict = ['firebrick', 'gold', 'coral', 'hotpink', 'mediumturquoise', 'limegreen']

game_is_started = False
levels = {'level_1': 0, 'level_2': 0, 'level_infinity': 0}
game_win = False

width, height = 420, 600
pg.mixer.music.load('LHS-RLD10.mp3')
# pg.mixer.music.play(99999)
pg.mixer.music.set_volume(volume)
# volume отвечает за уровень громкости
sound1 = pg.mixer.Sound('shoot.mp3')
sound2 = pg.mixer.Sound('Game over.mp3')
sound2.set_volume(volume)
pg.display.set_caption("Balls and blocks")
block_list = []
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
color_list = [""] * 70

img = pg.image.load('112.jpg').convert()
img2 = pg.image.load('menu1.png').convert()
for i in range(0, height, BLOCK_SIZE):
    for j in range(0, width, BLOCK_SIZE):
        rect = pg.Rect(j, i, BLOCK_SIZE - 1, BLOCK_SIZE - 1)
        block_list.append(rect)

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


class Menu:
    pass


image1 = pg.image.load('win.png')
win = pg.sprite.Sprite()
win.image = pg.Surface((420, 600))
win.image = image1
win.rect = win.image.get_rect()
win.rect.x = 0
win.rect.y = 0


class Button(pg.sprite.Sprite):

    def __init__(self, img, y, level, *group):
        super().__init__(*group)
        self.image = pg.Surface((66, 218))
        self.image = pg.image.load(img)
        self.rect = self.image.get_rect()
        self.rect.x = 101
        self.rect.y = y
        self.level = level

    def update(self, *args):
        if args and args[0].type == pg.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            global game_is_started
            global levels
            game_is_started = True
            levels[self.level] = 1


all_sprites = pg.sprite.Group()
Button('button1.png', 350, 'level_1', all_sprites)
Button('button2.png', 426, 'level_2', all_sprites)
Button('infinity.png', 502, 'level_infinity', all_sprites)


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

result = cur.execute("""
SELECT счёт from the_best_score""").fetchall()
result1 = cur.execute("""
SELECT num_of_wins from the_best_score""").fetchall()


def message(msg, x, y, color, font_style1=font_style):
    mesg2 = font_style1.render(msg, True, color)
    sc.blit(mesg2, (x, y))


def painter(colors, blocks, dict_of_colors, n1=0, n_max=10000000):
    global game_win
    if not any(colors[63:]) and (any(colors[:7]) or n1 > n_max):
        lister = colors.copy()
        colors.clear()
        colors = lister[63:]
        colors.extend(lister[:63])
        lister.clear()
    if n1 <= n_max:
        for le in range(5):
            for g, rect1 in enumerate(blocks[:7]):
                if rect1.collidepoint(randint(0, 420), 58):
                    # if randint(0, 1):

                    if colors[g] == "":
                        colors[g] = dict_of_colors[randint(0, 5)]
    if not any(colors) and n1 >= n_max:
        game_win = True
    return colors


k = 0
n = 0
d = 0
while not game_over:
    if game_is_started:
        pg.mouse.set_visible(False)
        if not any(color_list[63:]):
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()

                elif event.type == pg.MOUSEMOTION:
                    r.topleft = event.pos

                elif balls and event.type == move:
                    for b in balls:
                        b.move()
                        x2 = b.x + 15
                        y2 = b.y
                        ball.x = x2
                        ball.y = y2
                        if b.y >= 590:
                            balls = []

                elif event.type == pg.KEYUP:

                    # при нажатии на кнопку 1 музыка ставится либо на паузу либо включается
                    if event.key == pg.K_1:
                        if music:
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
                    if KEY != 2 and not any(color_list[63:]):
                        pos = pg.mouse.get_pos()
                        a = [pos[0], 590, 1]
                        balls.append(Ball(ball, *a, KEY))
                        sound1.play()

                        n += 1

                        # if n % 2 == 1:
                        if levels['level_infinity']:
                            color_list = painter(color_list, block_list, colors_dict).copy()
                        elif levels['level_1']:
                            color_list = painter(color_list, block_list, colors_dict, n, 5).copy()
                        elif levels['level_2']:
                            color_list = painter(color_list, block_list, colors_dict, n, 15).copy()

        hit_index = ball.collidelist(block_list)
        if hit_index != -1:
            if color_list[hit_index] != '':
                hit_rect = block_list[hit_index]
                for b in balls:
                    b.move(hit_rect)
                color_list[hit_index] = ''
                d = 1
        screen.fill(pg.Color("black"))

        sc.blit(img, (0, 0))
        if not any(color_list[63:]) and not game_win:

            for i, rect in enumerate(block_list):
                if color_list[i] != (0, 0, 0) and color_list[i] != '':
                    pg.draw.rect(sc, color_list[i], rect)

            replaced_text = ((str(r).replace('<rect(', '')).replace(')>', '')).split(", ")
            x1, y1 = int(replaced_text[0]), int(replaced_text[1])
            background.blit(sc, (x2, y2))
            sc.blit(arrow, (x1, y1))

            pg.draw.circle(sc, pg.Color('snow'), (x2, y2), ball_radius)

            if hit_index != -1:
                if d:
                    k += 1
                    d = 0
                message(f'Score: {k}', 342, 25, 'snow')
            pg.display.flip()

        else:
            if not game_win:
                sound2.play()
            else:
                cur.execute("""UPDATE the_best_score
                    SET num_of_wins = {} WHERE номер = {}""".format(k, list(levels.values()).index(1) + 1)).fetchall()
            pg.mixer.music.stop()
            if k > result[list(levels.values()).index(1)][0]:
                cur.execute("""UPDATE the_best_score
                    SET счёт = {} WHERE номер = {}""".format(k, list(levels.values()).index(1) + 1)).fetchall()
                # game_over = True
            while True:
                if not game_win:
                    sc.blit(gameover.image, (0, -100))
                else:
                    sc.blit(win.image, (0, 0))
                pg.mouse.set_visible(True)
                # message(f'Your score: {k}', 500, 100, 'snow')
                # # message('Press space to restart the game', 550, 100, 'snow', pg.font.SysFont(None, 30))
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        sys.exit()

                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_SPACE:
                            game_is_started = False
                            n = 0
                            color_list.clear()
                            color_list = [''] * 70
                            k = 0
                            result = cur.execute("""
                            SELECT счёт from the_best_score""").fetchall()
                            levels['level_infinity'] = 0
                            levels['level_1'] = 0
                            levels['level_2'] = 0
                pg.display.flip()
                if not game_is_started:
                    break
    else:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            all_sprites.update(event)

        pg.mouse.set_visible(True)
        screen.fill(pg.Color("black"))
        sc.blit(img2, (0, 0))
        message('Best scores', 40, 210, 'snow', pg.font.SysFont(None, 40))
        message(f'1st LEVEL: {result[0][0]}', 40, 250, 'gray', pg.font.SysFont(None, 30))
        message(f'2nd LEVEL: {result[1][0]}', 40, 280, 'gray', pg.font.SysFont(None, 30))
        message(f'INFINITY: {result[2][0]}', 40, 310, 'gray', pg.font.SysFont(None, 30))
        message('Number of wins', 220, 212, 'snow', pg.font.SysFont(None, 33))
        message(f'1st LEVEL: {result1[0][0]}', 220, 250, 'gray', pg.font.SysFont(None, 30))
        message(f'2nd LEVEL: {result1[1][0]}', 220, 280, 'gray', pg.font.SysFont(None, 30))
        all_sprites.draw(sc)

    pg.display.flip()
    pg.display.update()
    clock.tick(fps)

con.commit()
con.close()
pg.display.update()
time.sleep(3)
