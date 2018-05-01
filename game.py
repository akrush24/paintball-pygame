#!/usr/bin/python3.5
import pygame
from random import randint
import time

pygame.init()
DELAY = 20 # время ожилания перед обновлением в цикле

screen_width = 900
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))
win = False
pygame.display.set_caption("paintball") # название окна

widht = 70; height = 15 # размер доски
speed = 20 # скорость передвижения доски
x = screen_width/2; y = screen_height-height-15 # стартовая позиция доски

ball = {'xrevers':False, 'yrevers':True, 'x':int(x+widht/2), 'y':int(y), 'speed':5}
game = 0 # 0 игра не запущена, 1 игра идет, 2 игра проиграна, 3 игра выиграна
barrier=[] # массив барьеров

# генерируем препятствия
def get_barriers():
    y = 5 # отступ по Y от первого блока
    ROWS = 6 # число строк с барьерами
    for row in range(ROWS):
        i = 1; x = 5;
        for i in range(8):
            barrier.append({'status':True,'color':{'r':randint(10, 255),'g':randint(10, 255),'b':randint(10, 255)},'x':x,'y':y})
            x += 112
            i += 1
        y += 30
    return barrier

barrier = get_barriers() # наполняем массив с препятствиями

run = True
while run:

    pygame.time.delay(DELAY) # скорость обнолвения игры
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game == 0:
                    game = 1
                elif game == 2: # Если мы проиграли и нажали пробел то игра начинается за ново
                    game = 1
                elif game == 3: # Если мы выиграли и нажали пробел то игра начинается за ново
                    game = 1
                    barrier = get_barriers()
            if event.key == pygame.K_ESCAPE:
                run = False

    # отслеживаем нажатые кнопки
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and x > 15:
        x -= speed
    if keys[pygame.K_RIGHT] and x < screen_width - widht - 15:
        x += speed

    #if keys[pygame.K_UP] and y > 15:
    #    y -= speed
    #if keys[pygame.K_DOWN] and y < screen_height - height - 15:
    #    y += speed

    #if keys[pygame.K_PLUS] or keys[pygame.K_KP_PLUS]:
    #    speed = speed + 1
    #if keys[pygame.K_MINUS] and speed > 5:
    #    speed = speed - 1

    if game == 1 or game == 0:
        screen.fill((0,0,0))# зарисовываем все черным цветом
    elif game == 3:
        screen.fill((0,200,0))
    elif game == 2:
        screen.fill((250,0,0))

    # выводим статистику
    text = 'speed:'+str(speed)+'; x:'+str(x)+'; y:'+str(y)
    myfont = pygame.font.SysFont('Comic Sans MS', 20)
    textsurface = myfont.render(text, True, (255, 0, 0))
    #screen.blit(textsurface,(0,0))

    # рисуем доску
    #pygame.draw.rect(screen, (0,0,255), (x, y, widht, height))
    pygame.draw.ellipse(screen, (0,0,255), (x, y, widht, height))

    if ball['y'] >= screen_height - 10: # шарик падает сниз, игра начинается сначала
        game = 2
        barrier = get_barriers()
        x = screen_width/2;
        y = screen_height-height-15
        ball = {'xrevers':False, 'yrevers':True, 'x':int(x+widht/2), 'y':int(y), 'speed':5}

    if ball['y'] + 5 >= y and (ball['x'] + 5 >= x and ball['x'] + 5 <= x+widht): ball['yrevers'] = True # отскок от доски
    if ball['x'] >= screen_width - 10 and not ball['xrevers']: ball['xrevers'] = True # отскок от правой графице, по X
    if ball['y'] <= 10 and ball['yrevers']: ball['yrevers'] = False # отскок от верхний графице по Y
    if ball['x'] <= 10 and ball['xrevers']: ball['xrevers'] = False # отскок от левой графице, по X

    if game == 1: # шарик летает
        if ball['xrevers']:
            ball['x'] -= ball['speed']
        else:
            ball['x'] += ball['speed']

        if ball['yrevers']:
            ball['y'] -= ball['speed']
        else:
            ball['y'] += ball['speed']
    else: # просто перемещяем доску с шариком на ней, шарик не летает
        ball['x'] = int(x+widht/2)
        ball['y'] = int(y)
    # рисуем шарик
    pygame.draw.circle(screen, (255,255,255), (int(ball['x']), int(ball['y'])), 6)

    # рисуем препятствия
    i = 1; h = 5; activ = 0
    for i in range(len(barrier)):
        if barrier[i]['status']:
            activ += 1
            pygame.draw.rect(screen, (barrier[i]['color']['r'],barrier[i]['color']['g'],barrier[i]['color']['b']), (barrier[i]['x'], barrier[i]['y'], 107, 25))
            if ball['y']+3 <= barrier[i]['y']+25 and ( ball['x']+3 >= barrier[i]['x'] and ball['x']+3 <= barrier[i]['x']+107 ):
                ball['yrevers'] = False
                barrier[i]['status'] = False

            elif ( ball['y']+3 <= barrier[i]['y'] and ball['y']+3 >= barrier[i]['y']+25 ) and ( ball['x']+3 >= barrier[i]['x'] and ball['x']+3 <= barrier[i]['x']+107 ):
                ball['yrevers'] = True # отскакиваем по Y
                barrier[i]['status'] = False


            h = h + 110
            i += 1
    if activ == 0:
        game = 3

    pygame.display.update()

pygame.quit()
