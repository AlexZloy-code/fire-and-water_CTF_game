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
        self.north = False  # состояние возможности прыгнуть вверх
        self.south = False  # состояние возможности упасть вниз
        self.west = False  # состояние возможности убежать влево
        self.east = False  # состояние возможности убежать вправо

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
        self.x_file = self.x // 20
        self.y_file = self.y // 20

    def check_possible_movements(self, input_filename):
        """ функция проверяет возможность движения по всем направлениям """
        self.north = False
        self.south = False
        self.west = False
        self.east = False

        with open(input_filename, 'r') as input_file:
            file_massive = input_file.readlines()  # file_massive - массив строк
            # вида [line0, line1, ..., line(len(file_massive) - 1)]

            for lien_number in range(len(file_massive)):  # убирает /n в конце каждой строки
                file_massive[lien_number] = file_massive[lien_number].rstrip()

            # далее цикл проверяет, куда может двинуться по вертикали персонаж в данный момент времени
            for degree in range(2):  # degree - степень. 0 - возможности прыгнуть вверх, 1 - возможности упасть вниз
                if self.y_file == (len(file_massive) - 1) * degree - 2 * degree:  # если персонаж на нулевой строке, то
                    # он не прыгнет вверх, если персонаж на последней строке, то он не упадет вниз
                    # нужно отметить, что касаяюсь нижней границы функция выдает True
                    pass
                else:
                    line = file_massive[self.y_file - (-1) ** degree].rstrip()  # предыдущая/последующая строка
                    count = 0  # кол-во файловых ячеек, которые позволяют свободно передвигаться
                    if self.x % 20 > 0:  # проверяет, персонаж находится в 2 или 3 горизонтальных ячейках
                        length = 3  # length - кол-во "свободных" ячеек
                    else:
                        length = 2
                    for i in range(length):  # перебирает каждыю ячейку на возможность свободно передвигаться
                        if line[self.x_file + i] == '1':
                            break
                        elif line[self.x_file + i] == '0' or line[self.x_file + i] == '9':
                            count += 1
                    if count == length:
                        if degree == 0:
                            self.north = True
                        else:
                            self.south = True

            # далее цикл проверяет, куда может двинуться по горизонтали персонаж в данный момент времени
            for degree in range(2):  # degree - степень. 0 - возможности побежать влево, 1 - возможности побежать вправо
                if self.x_file == (len(file_massive[self.y_file]) - 1) * degree - 2 * degree:  # если персонаж на
                    # нулевой строке, то он не пойдет налево, если персонаж на последней строке, то он не пойдет направо

                    pass
                else:
                    count = 0
                    if self.y % 20 > 0:  # проверяет, персонаж находится в 2 или 3 вертикальных ячейках
                        height = 3  # height - кол-во "свободных" ячеек
                    else:
                        height = 2
                    for i in range(height):  # перебирает каждыю ячейку на возможность свободно передвигаться
                        x_check = (self.x_file + 1) - (-2) ** degree + 1 * (degree - 1)  # единая формула для ячеек
                        if file_massive[self.y_file + i][x_check] == '1':
                            break
                        elif file_massive[self.y_file + i][x_check] == '0' or \
                        file_massive[self.y_file + i][x_check] == '9':
                            count += 1
                    if count == height:
                        if degree == 0:
                            self.west = True
                        else:
                            self.east = True


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
