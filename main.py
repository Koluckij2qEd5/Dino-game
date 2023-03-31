import pygame
from random import randint, choice
import pickle

pygame.init()

# окно и фпс
WIDTH, HEIGHT = 1000, 400
FPS = 60

# иницализация игры
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Dino game')
pygame.display.set_icon(pygame.image.load('картикни/иконка/icon.png'))
clock = pygame.time.Clock()

def scoresSave():
    '''экспорт рекорда'''
    global scoresBest
    if scores > scoresBest:
        file = open('рекорд/scores.dat', 'wb')
        pickle.dump(scores, file)
        file.close()
        scoresBest = scores

def scoresLoad():
    '''импорт рекорда'''
    global scoresBest
    try:
        file = open('рекорд/scores.dat', 'rb')
        scoresBest = pickle.load(file)
        file.close()
    except:
        pass
# главный спрайт
imgSprite = pygame.image.load('картикни/sprites.png').convert_alpha()

# все спрайты
imgBG = imgSprite.subsurface(2, 104, 2400, 26)
imgDinoStand = [pygame.image.load('картикни/объекты/dino3.png').convert_alpha(),
                pygame.image.load('картикни/объекты/dino4.png').convert_alpha()]
imgDinoSit = [pygame.image.load('картикни/объекты/dino6.png').convert_alpha(),
              pygame.image.load('картикни/объекты/dino7.png').convert_alpha()]
imgDinoLose = [pygame.image.load('картикни/объекты/dino5.1.png').convert_alpha()]
imgCactus = [imgSprite.subsurface(446, 2, 34, 70),
             imgSprite.subsurface(480, 2, 68, 70),
             imgSprite.subsurface(512, 2, 102, 70),
             imgSprite.subsurface(512, 2, 68, 70),
             imgSprite.subsurface(652, 2, 50, 100),
             imgSprite.subsurface(752, 2, 98, 100),
             imgSprite.subsurface(750, 2, 102, 100)]
imgPter = [imgSprite.subsurface(260, 0, 92, 82),
           imgSprite.subsurface(352, 0, 92, 82)]
imgRestart = imgSprite.subsurface(2, 2, 72, 64)

# звуки
sndJump = pygame.mixer.Sound('музыка/jump.wav')
sndLevelUp = pygame.mixer.Sound('музыка/levelup.wav')
sndGameOver = pygame.mixer.Sound('музыка/gameover.wav')

# шрифт
fontScorces = pygame.font.Font('шрифты/technofosiano.ttf', 30) #none

# переменные
py, sy = 380, 0  # 180
isStand = False # прыжок
speed = 10 # скорость объектов
frame = 0 # смена кадров у картинок
scores = 0
scoresBest = 0
level = 0 # каждые 100 очков звук
day = 0
night = 255
bgs = [pygame.Rect(0, HEIGHT - 50, 2400, 26)] # задний фон
objects = [] # объекты
timer = 0 # для создание слева на право

# главный конструктор объектов
class Obj():
    '''создание класса объктов'''

    def __init__(self):
        objects.append(self) # добвление всех объектов в список

        # создание птеродактилей
        if randint(0, 4) == 0 and scores > 500:
            self.image = imgPter
            self.speed = 3
            py = HEIGHT - 30 - randint(0, 2) * 50
        # создание кактусов
        else:
            self.image = [choice(imgCactus)]
            self.speed = 0
            py = HEIGHT - 20

        # создание прямоугольноков по объектам сверху
        self.rect = self.image[0].get_rect(bottomleft = (WIDTH, py))
        self.frame = 0

    def update(self):
        '''обновление игры'''
        global speed, timer, sy
        self.rect.x -= speed + self.speed
        self.frame = (self.frame + 0.1) % len(self.image)

        if self.rect.colliderect(dinoRect) and speed !=0:
            speed = 0
            timer = 60
            sy = -10
            sndGameOver.play()

        # объеты которые уже не видно стираються
        self.rect.right < 0 and objects.remove(self)

    def draw(self):
        '''отрисовка объектов'''
        window.blit(self.image[int(self.frame)], self.rect)

scoresLoad()

play = True
while play:
    # главнй цикл игры
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False

    keys = pygame.key.get_pressed()
    b1, b2, b3 = pygame.mouse.get_pressed()
    pressJump = keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP] or b1 # клавиши для прыжка
    pressSit = keys[pygame.K_LCTRL] or keys[pygame.K_s] or keys[pygame.K_DOWN] or b3 # клавиши для приседания

    # рестарт игры
    if speed == 0 and timer == 0:
        # рестарт с мышкой
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if rect.collidepoint(pygame.mouse.get_pos()):
                scoresSave()
                py, sy = 380, 0
                isStand = False
                speed = 10
                frame = 0
                scores = 0
                objects = []
        # рестарт c space и с enter
        if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
            scoresSave()
            py, sy = 380, 0
            isStand = False
            speed = 10
            frame = 0
            scores = 0
            objects = []

    if pressJump and isStand and speed > 0:
        sy = -22
        sndJump.play()

    # приседание
    if isStand:
        frame = (frame + speed / 35) % 2

    py += sy
    sy = (sy + 1) * 0.97

    isStand = False
    #прыжок
    if py > HEIGHT - 20:
        py, sy, isStand = HEIGHT - 20, 0, True

    # застывший dino
    if speed == 0:
        dinoimg = imgDinoLose[0]

    # присед dino
    elif pressSit:
        dinoimg = imgDinoSit[int(frame)]

    # стоит dino
    else:
        dinoimg = imgDinoStand[int(frame)]

    # данные для отрисовки dino
    dw, dh = dinoimg.get_width(), dinoimg.get_height()
    dinoRect = pygame.Rect(80, py - dh, dw, dh)

    # работа с задним фоном
    for i in range(len(bgs) - 1, -1, -1):
        bg = bgs[i]
        bg.x -=speed
        bg.right < 0 and bgs.pop(i)
    if bgs[-1].right < WIDTH:
        bgs.append(pygame.Rect(bgs[-1].right, HEIGHT-50, 2400, 26))
    for obj in objects:
        obj.update()
    if timer > 0:
        timer -=1
    elif speed > 0:
        timer = randint(100, 150)
        Obj()

    # расчет счёта
    scores += speed / 50

    # левел для звука
    if scores // 100  > level:
        level = scores // 100
        sndLevelUp.play()

    # каждые 100 очков + 1 к скорости
    if speed > 0:
        speed = 10 + scores // 100

    d = 255 # белый

    # работа со сменой днем и ночью
    if scores > 600:
        for i in range(1):
            night = night - 0.3
            d = night
            if night < 10:
                d = 0
                break
    if scores > 1000:
        for i in range(1):
            day = day + 0.3
            d = day
            if day > 250:
                d = 255
                break
    if scores > 1600:
        for i in range(1):
            night = night - 0.3
            d = night
            if night < 10:
                d = 0
                break
    if scores > 2000:
        for i in range(1):
            day = day + 0.3
            d = day
            if day > 250:
                d = 255
                break
    if scores > 2600:
        for i in range(1):
            night = night - 0.3
            d = night
            if night < 10:
                d = 0
                break
    if scores > 3000:
        for i in range(1):
            day = day + 0.3
            d = day
            if day > 250:
                d = 255
                break
    if scores > 3600:
        for i in range(1):
            night = night - 0.3
            d = night
            if night < 10:
                d = 0
                break
    if scores > 4000:
        for i in range(1):
            day = day + 0.3
            d = day
            if day > 250:
                d = 255
                break
    if scores > 4600:
        for i in range(1):
            night = night - 0.3
            d = night
            if night < 10:
                d = 0
                break
    if scores > 5000:
        for i in range(1):
            day = day + 0.3
            d = day
            if day > 250:
                d = 255
                break

    # заливка фона
    window.fill((d, d, d))

    # отрисовка спрайтов/объектов
    for bg in bgs:
        window.blit(imgBG, bg)
    for obj in objects:
        obj.draw()

    # отрисовка dino
    window.blit(dinoimg, dinoRect)

    # отрисовка счета
    text = fontScorces.render('scores: ' + str(int(scores)), 0, 'gray40')
    window.blit(text, (WIDTH - 250, 10))

    # отрисока рекорда
    text = fontScorces.render('record: ' + str(int(scoresBest)), 0, 'gray40')
    window.blit(text, (30, 10))

    # отрисовка кнопки
    if speed == 0:
        rect = imgRestart.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        window.blit(imgRestart, rect)

    pygame.display.update()
    clock.tick(FPS)
scoresSave()
pygame.quit()
