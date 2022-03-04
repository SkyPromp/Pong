import pygame
import pygame as pg
import time
import math

pg.init()
DISPLAY = pg.display.set_mode((1000, 1000))
pg.display.set_caption("Hardcode button masher")
font = pg.font.Font('freesansbold.ttf', 32)
CLOCK = pg.time.Clock()

running = True

r = 500
k = 500
start = time.time()
radius = 20
exp = 1.01
clickcount = 0
t = 0


def hatMan(r, k):
    pg.draw.ellipse(DISPLAY, 255, (r - 10, k - 5, 5, 5))
    pg.draw.ellipse(DISPLAY, 255, (r + 5, k - 5, 5, 5))
    pg.draw.line(DISPLAY, 255, (r - 5, k + 7), (r + 5, k + 7), 4)
    pg.draw.polygon(DISPLAY, 255, ((r, k - 20 - radius), (r - radius, k - radius), (r + radius, k - radius)), 5)
    pg.draw.circle(DISPLAY, 255, (r, k), radius, 5)


while running:
    t += 4
    exp = math.log10(t)*2
    DISPLAY.fill((255, 255, 255))
    events = pg.event.get()

    for event in events:
        if event.type == pg.MOUSEBUTTONDOWN:
            clickcount += 1

            if k - 60 >= radius:
                k -= 60
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                r -= 60
            if event.key == pg.K_RIGHT:
                r += 60
                if r > DISPLAY.get_size()[0] - radius:
                    r = DISPLAY.get_size()[0] - radius - 60
            if event.key == pg.K_UP:
                clickcount += 1

                if k - 60 >= radius + 20:
                    k -= 60
                else:
                    k = radius + 20
            if event.key == pg.K_q:
                running = False
    if k <= DISPLAY.get_size()[1] - radius:
        k += 3 * exp

    else:
        timespan = time.time() - start
        if timespan > 1:
            print(clickcount)
            print(timespan)
            print("Your cps is:", clickcount / timespan)
            clickcount = 0

        exp = 1
        clickcount = 0
        start = time.time()

    r = abs(r)
    hatMan(r, k)

    text = font.render(str(clickcount), True, (0, 0, 0), (255, 255, 255))
    textRect = text.get_rect().topleft
    DISPLAY.blit(text, textRect)
    textSpeed = font.render(f"v = {exp:.2f}", True, (0, 0, 0), (255, 255, 255))
    textRectSpeed = textSpeed.get_rect().topright
    DISPLAY.blit(textSpeed, textRectSpeed)

    pg.display.update()
    CLOCK.tick(30)

pygame.quit()
