import random
import time
import pygame

pygame.init()
fpsClock = pygame.time.Clock()
pygame.display.set_caption('Avoid Asteroids')

asteroidtimer = 10
asteroids = [[20, 0, 0]]

screen_width = 1280
screen_heigth = 720
screen = pygame.display.set_mode((screen_width, screen_heigth))

spaceshipimg = pygame.image.load('./img/spaceship.png')
asteroid0 = pygame.image.load('./img/asteroid00.png')
asteroid1 = pygame.image.load('./img/asteroid01.png')
asteroid2 = pygame.image.load('./img/asteroid02.png')
asteroidimgs = (asteroid0,asteroid1,asteroid2)
gameover = pygame.image.load('./img/gameover.jpg')
background = pygame.image.load('./img/background.jpg')
getbackground = pygame.image.load('./img/getbackground.jpg')

backgroundmusic = pygame.mixer.Sound('./audio/backgroundmusic.wav')
boomsound = pygame.mixer.Sound('./audio/boom.wav')


def text(arg, x, y, size):
    font = pygame.font.Font(None, size)
    text = font.render('Score: ' + str(arg).zfill(6), True, (0,0,0))
    textRect = text.get_rect()
    textRect.centerx = x
    textRect.centery = y
    screen.blit(text, textRect)


def high(arg, x, y, size):
    font = pygame.font.Font(None, size)
    text = font.render('High: ' + str(arg).zfill(6), True, (0,0,0))
    textRect = text.get_rect()
    textRect.centerx = x
    textRect.centery = y
    screen.blit(text, textRect)


def music(x, y, size):
    font = pygame.font.Font(None, size)
    text = font.render('>> TheFatRat - Unity'.zfill(6), True, (0,0,0))
    textRect = text.get_rect()
    textRect.centerx = x
    textRect.centery = y
    screen.blit(text, textRect)


def gethighscore(size, color):
    font = pygame.font.Font(None, size)
    text = font.render('HighScore!!!'.zfill(6), True, color)
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery
    screen.blit(text, textRect)


def gameoverscreen():
    high(highscore, 1125, 50, 60)
    text(score, 1115, 110, 60)


while 1:
    score = 0
    FPS = 60

    try:
        with open('./highscore.txt', 'r') as f:
            pass
    except:
        with open('./highscore.txt', 'w') as f:
            f.write('0')
    finally:
        try:
            with open('./highscore.txt', 'r') as f:
                highscore = int(f.readline())
        except:
            with open('./highscore.txt', 'w') as f:
                f.write('0')
        finally:
            with open('./highscore.txt', 'r') as f:
                highscore = int(f.readline())

    backgroundmusic.play()

    background1_y = 0
    background2_y = -screen_heigth

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                exit(0)

        background1_y += 1
        background2_y += 1

        if background1_y == screen_heigth:
            background1_y = -screen_heigth
        if background2_y == screen_heigth:
            background2_y = -screen_heigth

        screen.blit(background, (0, background1_y))
        screen.blit(background, (0, background2_y))

        music(1218, 5, 18)
        text(score, 780, 20, 30)
        high(highscore, 500, 20, 30)

        position = pygame.mouse.get_pos()
        spaceshippos = (position[0], position[1])
        screen.blit(spaceshipimg, spaceshippos)
        spaceshiprect = pygame.Rect(spaceshipimg.get_rect())
        spaceshiprect.left = spaceshippos[0]
        spaceshiprect.top = spaceshippos[1]

        asteroidtimer -= 40
        if asteroidtimer <= 0:
            asteroids.append([random.randint(5, 1275), 0, random.randint(0, 2)])
            asteroidtimer = random.randint(50, 200)

        index = 0
        for stone in asteroids:
            stone[1] += 20
            if stone[1] > 720:
                asteroids.pop(index)
                score += 1

            stonerect = pygame.Rect(asteroidimgs[stone[2]].get_rect())
            stonerect.left = stone[0]
            stonerect.top = stone[1]
            if stonerect.colliderect(spaceshiprect):
                backgroundmusic.stop()
                boomsound.play()
                asteroids.pop(index)
                run = False
            screen.blit(asteroidimgs[stone[2]], (stone[0], stone[1]))
            index += 1

        fpsClock.tick(FPS)
        pygame.display.flip()

    sleep = 1.4
    hightof = False
    with open('./highscore.txt', 'r') as f:
        line = f.readline()
        if int(line) < score:
            highscore = score
            with open('./highscore.txt', 'w') as f:
                f.write(str(score))
                hightof = True
    screen.blit(gameover, (0, 0))
    gameoverscreen()
    if hightof:
        screen.blit(getbackground, (0, screen.get_rect().centery-150))
        gethighscore(300, (255,0,0))
        sleep = 2.5
    pygame.display.flip()
    asteroids.clear()
    key_event = pygame.key.get_pressed()
    time.sleep(sleep)
    boomsound.stop()
