import pygame
import pygame as pg
import random
import math


class Palet:
    def __init__(self, r, c, height, width, speed, screen_height):
        self.__r = r
        self.__c = c
        self.__height = height
        self.__width = width
        self.__speed = speed
        self.__screen_height = screen_height

    def __repr__(self):
        return f"Palet({self.__r}, {self.__c}, {self.__height}, {self.__width}, {self.__speed}, {self.__screen_height})"

    def down(self):  # TODO: smooth palet movement
        new_y = self.__r + self.__speed
        if self.__screen_height - self.__height > new_y:  # Slightly sinks into the border
            self.__r = new_y
        else:
            self.__r = self.__screen_height - self.__height  # Slightly sinks into the border

    def up(self): # TODO: smooth palet movement
        new_y = self.__r - self.__speed
        if new_y > 0:
            self.__r = new_y
        else:
            self.__r = 0

    def draw(self, screen):
        pg.draw.rect(screen, (255, 255, 255), pg.Rect(self.__c, self.__r, self.__width,
                                                      self.__height))  # c = side to side


class Ball:
    def __init__(self, radius, r, c, speed, screen_height, screen_width, palet_width, angle=(random.random() * 2 * math.pi)):
        self.__radius = radius
        self.__r = r
        self.__c = c
        self.__speed = speed
        self.__screen_height = screen_height
        self.__screen_width = screen_width
        self.__angle = angle
        self.__wait = 0
        self.__palet_width = palet_width

    def next(self, screen):  # TODO: smooth ball movement
        self.__c += math.cos(self.__angle) * self.__speed
        self.__r += math.sin(self.__angle) * self.__speed

        if self.__c < self.__radius:  # hits top
            self.__angle = math.pi - self.__angle

        elif self.__c >= self.__screen_height - self.__radius:  # hits bottom
            self.__angle = math.pi - self.__angle

        if self.__r < self.__radius:  # hits left
            self.reset()

            return 0, 1

        elif self.__r >= self.__screen_width - self.__radius:  # hits right
            self.reset()

            return 1, 0

        self.__wait += 1
        try:
            color = screen.get_at((round(self.__r) - self.__radius, round(self.__c)))
            if str(color) == str((255, 255, 255, 255)) and self.__wait > 0:
                self.__angle *= -1
                self.__wait = - (self.__palet_width / self.__speed) - 2

            color = screen.get_at((round(self.__r) + self.__radius, round(self.__c)))
            if str(color) == str((255, 255, 255, 255)) and self.__wait > 0:
                self.__angle *= -1
                self.__wait = - (self.__palet_width / self.__speed) - 2

        finally:
            # returns score to be added to player wasd, player arrows
            return 0, 0

    def reset(self):
        self.__r = self.__screen_width // 2
        self.__c = self.__screen_height // 2
        self.__angle = random.random() * 2 * math.pi
        while abs(math.cos(self.__angle)) > 0.9:
            self.__angle = random.random() * 2 * math.pi

    def draw(self, screen):
        pg.draw.circle(screen, (255, 255, 255), (self.__r, self.__c), self.__radius, 5)


def main():
    pg.init()
    CLOCK = pg.time.Clock()
    DISPLAY = pg.display.set_mode((858, 525))
    dheight = DISPLAY.get_size()[1]
    dwidth = DISPLAY.get_size()[0]
    pg.display.set_caption("Pong")
    font = pg.font.Font('freesansbold.ttf', 32)
    background = None

    pygame.mixer.music.load('song.mp3')
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)

    try:
        background = pygame.image.load("background.jpg")
    except FileNotFoundError:
        pass

    running = True
    fps = 30

    palet_speed = 10
    palet_height = 100
    palet_width = 20
    palet_wall_distance = 50
    wasd = Palet(dheight // 2 - palet_height // 2, palet_wall_distance, palet_height, palet_width, palet_speed, dheight)
    arrows = Palet((DISPLAY.get_size()[1] // 2) - palet_height // 2, dwidth - palet_wall_distance - 1 - palet_width,
                   palet_height, palet_width, palet_speed, dheight)

    wasdup = False
    wasddown = False
    arrowsup = False
    arrowsdown = False

    ballradius = 10
    ballspeed = 10
    ball = Ball(ballradius, dwidth // 2, dheight // 2, ballspeed, dheight, dwidth, palet_width)

    wasdscore = 0
    arrowsscore = 0

    while running:
        try:
            DISPLAY.blit(background, (0, 0))
        except TypeError:
            DISPLAY.fill((0, 0, 0))

        events = pg.event.get()
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_DOWN:
                    arrowsdown = True

                if event.key == pg.K_UP:
                    arrowsup = True

                if event.key == pg.K_z:  # AZERTY
                    wasdup = True

                # if event.key == pg.K_w:  # QWERTY
                #     wasdup = True

                if event.key == pg.K_s:
                    wasddown = True

                if event.key == pg.K_p:
                    running = False
                    print(wasdscore, arrowsscore)

            if event.type == pg.KEYUP:
                if event.key == pg.K_DOWN:
                    arrowsdown = False

                if event.key == pg.K_UP:
                    arrowsup = False

                if event.key == pg.K_z:  # AZERTY
                    wasdup = False

                # if event.key == pg.K_w:  # QWERTY
                #     wasdup = False

                if event.key == pg.K_s:
                    wasddown = False

        if wasddown:
            wasd.down()
        elif wasdup:
            wasd.up()
        if arrowsdown:
            arrows.down()
        elif arrowsup:
            arrows.up()

        wasd.draw(DISPLAY)
        arrows.draw(DISPLAY)

        wasdscoreadder, arrowsscoreadder = ball.next(DISPLAY)
        wasdscore += wasdscoreadder
        arrowsscore += arrowsscoreadder
        text = font.render(str(wasdscore), True, (254, 254, 254))  # May not be white because of ball collision system
        DISPLAY.blit(text, (5, 5))
        text = font.render(str(arrowsscore), True, (254, 254, 254))  # May not be white because of ball collision system
        DISPLAY.blit(text, (dwidth - text.get_rect().width - 5, 5))

        ball.draw(DISPLAY)

        pg.display.update()
        CLOCK.tick(fps)


if __name__ == "__main__":
    main()
    pygame.quit()
