import pygame
from pygame.draw import *

FPS = 60

WIDTH = 1000  # задает ширину экрана
HEIGHT = 700  # задает высоту экрана
DELTA = 20  # все игровое пространство разбито на некие клеточки, которые определяют цифры из файлов уровней.
# ширина этих клеточек есть "ширина" одной цифры

gamer_existence = False  # существование игрока. переменная существует для того, чтобы один раз создать
# персонажа по координатам, ибо дальше код игры будет определять координаты персонажа в файле

gamer1_keys = [pygame.K_a, pygame.K_w, pygame.K_d]  # массив клавиш, определяющих движение превого игрока
gamer2_keys = [pygame.K_LEFT, pygame.K_UP, pygame.K_RIGHT]  # массив клавиш, определяющих движение второго игрока

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))  # игровая площадь
screen.fill((255, 255, 255))


class Map:

    @staticmethod
    def _load_map(input_filename):
        with open(input_filename, 'r') as input_file:
            file_massive = input_file.readlines()
            for lines_count in range(len(file_massive)):
                file_massive[lines_count] = file_massive[lines_count].rstrip()
        return file_massive

    def __init__(self, input_filename):
        self.storage = self._load_map(input_filename)

    @staticmethod
    def to_map_coordinates(obj):
        return obj.x // DELTA, obj.y // DELTA

    def collision(self, obj):
        """ функция говорит о дозволенных движениях персонажа по оси Оу"""

        res = {"north": False, "south": False, "west": False, "east": False}  # массив, который превращается в
        # результат по окончании функции

        x, y = self.to_map_coordinates(obj)  # файловые координаты персонажа в целых числах
        for degree in range(2):  # degree - степень: 0 - возможности прыгнуть вверх, 1 - возможности упасть вниз
            if y == len(self.storage) * degree - 3 * degree:  # если персонаж на нулевой строке, то
                # он не прыгнет вверх, если персонаж на последней строке, то он не упадет вниз
                # нужно отметить, что касаяюсь нижней границы функция выдает True

                pass
            else:
                count = 0  # кол-во файловых ячеек, которые позволяют свободно передвигаться
                if obj.x % DELTA > 0:  # проверяет, персонаж находится в 2 или 3 горизонтальных ячейках
                    length = 3  # length - кол-во "свободных" ячеек
                else:
                    length = 2
                if obj.y % DELTA > 0:  # в зависимости от "жирноты" по оси Оу переменная y_check имееть свою формулу
                    y_check = y + 1 - 2 * (-1) ** degree  # y_check - номер просматриваемой строки
                else:
                    y_check = y - 1 + 3 * degree
                for cell_number in range(length):  # перебирает каждыю ячейку на возможность свободно передвигаться
                    # cell_number - порядок выбранной ячейки

                    if self.storage[y_check][x + cell_number] == '1':
                        break
                    elif self.storage[y_check][x + cell_number] == '0' or self.storage[y_check][x + cell_number] == '9':
                        count += 1
                if count == length:
                    if degree == 0:
                        res["north"] = True
                    else:
                        res["south"] = True

        # проверяет разрешаемые направление движения по оси Ох
        for degree in range(2):  # degree - степень: 0 - возможность побежать влево, 1 - возможность побежать вправо
            if x == len(self.storage[y]) * degree - 3 * degree:  # если персонаж на нулевом столбце, то
                # он не побежит влево, если персонаж на последнем столбце, то он не побежит вправо
                # нужно отметить, что касаясь правой границы функция выдает True

                pass
            else:
                count = 0  # кол-во файловых ячеек, которые позволяют свободно передвигаться
                if obj.y % DELTA > 0:  # проверяет, персонаж находится в 2 или 3 вертикалльных ячейках
                    height = 3  # length - кол-во "свободных" ячеек
                else:
                    height = 2
                if obj.x % DELTA > 0:  # в зависимости от "жирноты" по оси Ох переменная x_check имееть свою формулу
                    x_check = x + 1 - 2 * (-1) ** degree  # x_check - номер просматриваемой строки
                else:
                    x_check = x - 1 + 3 * degree
                for cell_number in range(height):  # перебирает каждыю ячейку на возможность свободно передвигаться
                    # cell_number - порядок выбранной ячейки

                    if self.storage[y + cell_number][x_check] == '1':
                        break
                    elif self.storage[y + cell_number][x_check] == '0' or self.storage[y + cell_number][x_check] == '9':
                        count += 1
                if count == height:
                    if degree == 0:
                        res["west"] = True
                    else:
                        res["east"] = True

        return res


class Player:

    def __init__(self):
        """
        информация о каждом персонаже
        self.x - положение верхнего левого угла player_surface в игровой области
        self.y - положение верхнего левого угла player_surface в игровой области
        self.vx - скорость персонажа по оси Ох, направленной вправо
        self.vy - скорость персонажа по оси Оу, направленной вниз
        self.x_file - положение верхнего левого угла player_surface в файле
        self.y_file - положение верхнего левого угла player_surface в файле
        self.north - состояние возможности прыгнуть вверх
        self.south - состояние возможности упасть вниз
        self.west - состояние возможности убежать влево
        self.east - состояние возможности убежать вправо
        """

        self.x = 0
        self.y = 0
        self.vx = 3
        self.vy = 0
        self.x_file = 0
        self.y_file = 0
        self.north = False
        self.south = False
        self.west = False
        self.east = False

    def set_possibility(self, abilities):
        self.north = abilities["north"]
        self.south = abilities["south"]
        self.west = abilities['west']
        self.east = abilities['east']

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
                            self.x = x_file * DELTA
                            self.y = y_file * DELTA

    def draw(self):
        """ рисует поверхность и персонажа на этой поверхности """

        player_rect = pygame.Surface((40, 40), pygame.SRCALPHA)
        player_rect.fill(0)
        circle(
            player_rect,
            (0, 0, 0),
            (20, 20),
            20
        )
        screen.blit(player_rect, (self.x, self.y))

    def to_make_it_move(self, k):
        """
        функция, которая заставляет перемещать персонаж по оси Оx и прыгать по оси Оy
        k - номер абстрактного списка [left, up, right]
        """

        if k == 0 and self.west or k == 0 and not self.west and self.x > self.x_file * DELTA + self.vx:  # если путь
            # свободен или около свободен

            self.x -= self.vx
        elif k == 1 and self.north and self.vy == 0:
            self.vy = -15
        elif k == 2 and self.east or k == 2 and not self.east and self.x < (self.x_file + 1) * DELTA - self.vx:  # если
            # путь свободен или около свободен

            self.x += self.vx

    def move(self):
        """ функция, которая отвечает за непрерывное движение персонажа по оси Оу"""

        if self.south and self.vy >= 0:
            self.y += self.vy
            self.vy += 1
        elif not self.south and self.vy > 0:
            self.vy = 0
            self.y -= self.y % DELTA
            self.y += DELTA - 1
        elif self.north and self.vy < 0:
            self.y += self.vy
            self.vy += 1
        elif not self.north and self.vy < 0:
            self.vy = -self.vy

        # высчитываение нового положение персонажа в карте
        self.x_file = self.x // DELTA
        self.y_file = self.y // DELTA


def check_possible_movements(lvl_handler, checked_player):
    oy_abilities = lvl_handler.collision(checked_player)
    checked_player.set_possibility(oy_abilities)


finished = False
clock = pygame.time.Clock()
players = [Player() for _ in range(2)]  # массив из двух игроков
Map = Map('lvl1.txt')  # предает классу Map информацию об уровне

while not finished:

    clock.tick(FPS)
    # спавнит персонажей на поле
    if not gamer_existence:
        for count_player, Player in enumerate(players):
            Player.coordinate_input('lvl1.txt',  count_player + 1)
            gamer_existence = True

    # проверяет разрешаемые направление движения
    for player in players:
        check_possible_movements(Map, player)

    # обработчик событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.KEYDOWN:
            for motion_number, motion in enumerate(gamer1_keys + gamer2_keys):  # по нажатию кнопки w или ARROW_UP
                # персонаж прыгает. motion - кнопка из списка (gamer1_keys + gamer2_keys), motion_number - его номер

                if event.key == motion and motion_number == 1:
                    players[motion_number // 3].to_make_it_move(motion_number % 3)
                if event.key == motion and motion_number == 4:
                    players[motion_number // 3].to_make_it_move(motion_number % 3)

    # непрерывное управление персонажами по оси Ох
    for motion_number, motion in enumerate(gamer1_keys + gamer2_keys):
        if pygame.key.get_pressed()[motion] and (motion_number % 3 != 1):
            players[motion_number // 3].to_make_it_move(motion_number % 3)

    # безпрерывная анимация и зарисовка персонажей
    for count_player, Player in enumerate(players):
        Player.move()
        Player.draw()

    pygame.display.update()
    screen.fill((255, 255, 255))

pygame.quit()
