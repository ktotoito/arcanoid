import pygame
import sys
from random import randint
import pygame as pg
import time

BLOCK_SIZE = 60
game_over = False
pygame.font.init()
font_style = pygame.font.SysFont(None, 50)
balls = []
col = 0
pg.init()
volume = 0.5
music = True

# вывод музыки
# причем при music.play  песня будет играть фоном указанное количество раз
pg.mixer.music.load('music.mp3')
pg.mixer.music.play(99999)
pg.mixer.music.set_volume(volume)
# volume отвечает за уровень громкости
sound1 = pg.mixer.Sound('shoot.mp3')
sound2 = pg.mixer.Sound('Game over.mp3')
# размеры игрового поля
size = width, height = 420, 600
pygame.display.set_caption("Balls and blocks")
all_rects = []

fps = 100
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
move = pygame.USEREVENT
pygame.time.set_timer(move, 2)
pygame.init()
# изображение шарика который играет роль мышки и прицела
arrow = pygame.image.load("data/arrow.png")
r = arrow.get_rect()
pygame.mouse.set_visible(False)
dis = pygame.display.set_mode((width, width))

for i in range(0, height, BLOCK_SIZE):
    row = []
    for j in range(0, width, BLOCK_SIZE):
        rect = pygame.Rect(j, i, BLOCK_SIZE - 1, BLOCK_SIZE - 1)
        row.append([rect, 'black'])
    all_rects.append(row)

sc = pygame.display.set_mode((width, height))
background = pg.Surface((420, 700))

sc.blit(background, (0, 0))
pg.display.update()
# будущие координаты шаров при стрельбе
x2 = width
y2 = height

surf = pygame.Surface((35, 35))
pygame.draw.circle(surf, 'white', (10, 10), 10)
sc.blit(surf, (0, 0))
pygame.display.update()


class Ball:
    def __init__(self, x, y, v):
        self.x = x
        self.y = y
        self.dx = -v
        self.dy = -v
        # dх отвечает за направление движение вдоль оси ох
        # нужно сделать 3 варианта dx = v/ -v/ 0
        # то есть движение вправо влево и  вертикально вверх
        # В этой же классе и функции move нужно реализовать изменение
        # напрвления(скорости) полета шаров при касании с блоками

    def move(self, w, h):
        # изменение направления полета шаров при столкновении со стенками
        self.x += self.dx
        self.y += self.dy
        if self.x < 0:
            self.dx *= -1
            self.x *= -1
        if self.x > w:
            self.dx *= -1
            self.x = w - self.x % w
        if self.y < 0:
            self.dy *= -1
            self.y *= -1
        if self.y > h:
            self.dy *= -1
            self.y = h - self.y % h
        if self.y == h:
            self.dy = 0
            self.dx = 0
            self.y = h + 10

    # def draw(self):
    #   pygame.draw.circle(screen, pygame.Color('white'),
    #              (self.x, self.y), 10, 0)


def message(msg, color):
    # вывод надписи game over
    # нужно переделать функцию что бы выводилась
    # программа Game over из раздела спрайты
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [width / 8, height / 2])


n = 0
# игровой цикл
while not game_over:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()

        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_LEFT:
        #         self.dx = -1
        #     elif event.key == pygame.K_RIGHT:
        #         self.dx = 1
        #     elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
        #         self.dx = 0

        elif event.type == pygame.MOUSEMOTION:
            # замены мышки красным шаром которым можно пользоваться как прицелом
            r.topleft = event.pos

        elif event.type == pygame.MOUSEBUTTONUP and balls == []:
            # стрельба идет только 1 шаром поэтому идет проверка
            # если если список пуст то в него добавляется шар
            # если в нем есть даже один шар то функция не будет
            # работать пока необнулится
            a = [event.pos[0], 500]
            balls.append(Ball(*a, 1))

        elif balls and event.type == move:
            for b in balls:
                b.move(width, height)
                # координаты шара которым ведется стрельба
                x2 = b.x
                y2 = b.y
                if b.y == 590:
                    # проверка на то находится ли шар на нижнем ребре
                    # или еще в полете
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


        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                sound1.play()
            elif event.button == 3:
                sound2.play()






        elif event.type == pygame.MOUSEBUTTONDOWN and balls == []:
            if event.button == 1:
                sound1.play()
                # при стрельбе издается соответствующий звук
            if event.button == 1:
                # если нажата ЛКМ
                n += 1
                for i in range(4):
                    # появление блоков после каждого нажатия
                    # а соответственно и хода
                    for row in all_rects:
                        for item in row:
                            rect, color = item
                            if rect.collidepoint(randint(0, 420), 58 * n):
                                # наполняет случайные клетки "строчки" поля
                                if color == 'black':
                                    # случайными цветами
                                    item[1] = (randint(0, 255), randint(0, 255), randint(0, 255))

        if n == 10:
            # если блоки спустились до нижнего ребра, то игра проиграна
            # и звучит соответствующая мелодия
            if event.button == 1:
                sound2.play()
            game_over = True

    screen.fill(pygame.Color("black"))

    for row in all_rects:
        for item in row:
            rect, color = item
            pygame.draw.rect(sc, color, rect)
    pygame.display.flip()
    # выделение координат положения стрелки
    replaced_text = ((str(r).replace('<rect(', '')).replace(')>', '')).split(", ")
    x1, y1 = int(replaced_text[0]), int(replaced_text[1])
    background.blit(sc, (x2, y2))
    # наложение стрелки мыши и игрового шара
    # поверх клетчатого поля
    sc.blit(arrow, (x1, y1))
    sc.blit(surf, (x2, y2))
    pg.display.update()
    pg.time.delay(30)
message("You lost! Game over.", 'red')
pygame.display.update()
time.sleep(3)