import pygame
from pygame.draw import *

FPS = 60

WIDTH = 1000  # задает ширину экрана
HEIGHT = 700  # задает высоту экрана
delta = 20  # все игровое пространство разбито на некие клеточки, которые определяют цифры из файлов уровней.
# ширина этих клеточек есть "ширина" одной цифры
gamer_existence = False  # существование игрока. переменная существует для того, чтобы один раз создать
# персонажа по координатам, ибо дальше код игры будет определять координаты персонажа в файле
gamer1_keys = [pygame.K_a, pygame.K_w, pygame.K_d]  # массив клавиш, определяющих движение превого игрока
gamer2_keys = [pygame.K_LEFT, pygame.K_UP, pygame.K_RIGHT]  # массив клавиш, определяющих движение второго игрока

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))  # игровая площадь
screen.fill((255, 255, 255))


class Player:

    def __init__(self):
        """ информация о каждом персонаже """

        self.x = 0  # положение верхнего левого угла player_surface в игровой области
        self.y = 0  # положение верхнего левого угла player_surface в игровой области
        self.vx = 0  # скорость персонажа по оси Ох, направленной вправо
        self.vy = 0  # скорость персонажа по оси Оу, направленной вниз
        self.x_file = 0  # положение верхнего левого угла player_surface в файле
        self.y_file = 0  # положение верхнего левого угла player_surface в файле

    def coordinate_input(self, input_filename, player_number):
        """ функция записывает координаты игрока в базу данных """

        with open(input_filename, 'r') as input_file:
            y_file = -1  # y_file - координата игрока по y - 1
            number = 0  # номер игрока
            for line in input_file:
                y_file += 1
                x_file = -1  # x_file - координата игрока по x - 1
                for letter in line:
                    x_file += 1
                    if letter == '9':  # 9 - цифра-индетификатор игрока
                        number += 1
                        if number == player_number:
                            self.x = x_file * delta
                            self.y = y_file * delta
                            self.x_file = x_file
                            self.y_file = y_file

    def draw(self):
        """ рисует поверхность и персонажа на этой поверхности """

        player_surface = pygame.Surface((40, 40), pygame.SRCALPHA)
        player_surface.fill(0)
        circle(
            player_surface,
            (0, 0, 0),
            (20, 20),
            20
        )
        screen.blit(player_surface, (self.x, self.y))

    def move(self, k):
        """ задает движение персонажа """

        if k == 0 or k == 3:
            self.x -= 3
        elif k == 1 or k == 4:
            self.y -= 3
        else:
            self.x += 3


finished = False
clock = pygame.time.Clock()
players = [Player() for _ in range(2)]  # массив из двух игроков

while not finished:

    clock.tick(FPS)

    # спавнит персонажей на поле
    if not gamer_existence:
        for count_player, Player in enumerate(players):
            Player.coordinate_input('lvl1.txt',  count_player + 1)
            gamer_existence = True

    # обработчик событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.KEYDOWN:
            # по нажатию кнопки w или ARROW_UP персонаж прыгает
            for motion_number, motion in enumerate(gamer1_keys + gamer2_keys):
                if event.key == motion and motion_number == 1:
                    players[motion_number // 3].move(motion_number)
                if event.key == motion and motion_number == 4:
                    players[motion_number // 3].move(motion_number)

    # непрерывное управление персонажами по оси Ох
    for motion_number, motion in enumerate(gamer1_keys + gamer2_keys):
        if pygame.key.get_pressed()[motion] and (motion_number % 3 != 1):
            players[motion_number // 3].move(motion_number)

    # зарисовка персонажей
    for count_player, Player in enumerate(players):
        Player.draw()

    pygame.display.update()
    screen.fill((255, 255, 255))

pygame.quit()
