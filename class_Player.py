from consntants import *


class Player:

    def __init__(self, x, y):
        """
        информация о каждом персонаже
        self.x - положение верхнего левого угла player_surface в игровой области
        self.y - положение верхнего левого угла player_surface в игровой области
        self.vx - скорость персонажа по оси Ох, направленной вправо
        self.vy - скорость персонажа по оси Оу, направленной вниз
        self.a - ускорение персонажа по оси Оу, направленное вниз
        self.x_file - положение верхнего левого угла player_surface в файле
        self.y_file - положение верхнего левого угла player_surface в файле
        self.north - состояние возможности прыгнуть вверх
        self.south - состояние возможности упасть вниз
        self.west - состояние возможности убежать влево
        self.east - состояние возможности убежать вправо
        """

        self.x = x
        self.y = y
        self.vx = 4
        self.vy = 0
        self.a = 1
        self.x_file = 0
        self.y_file = 0
        self.north = False
        self.south = False
        self.west = False
        self.east = False
        self.alive = True

    def set_possibility(self, abilities):
        """ записивыет данные о дозволенном движении перонажа"""

        self.north = abilities['north']
        self.south = abilities['south']
        self.west = abilities['west']
        self.east = abilities['east']

    def inf(self):
        """ возвращает информацию, чтобы потом правильно нарисовать картинку """

        return self.vy, self.x, self.y, self.alive

    def to_make_it_move(self, k):
        """
        функция, которая заставляет перемещать персонаж по оси Оx и прыгать по оси Оy
        k - номер абстрактного списка [left, up, right]
        """

        # далее в условиях прописаны длинные формулы. они учитывают несколько багов
        if k == 0 and self.west or k == 0 and\
                not self.west and self.x > self.x_file * DELTA + self.vx and self.x % DELTA > 0:  # если путь
            # свободен или около свободен, то есть позволяет приблизиться к стенке несмотря на False

            self.x -= self.vx
        elif k == 1 and self.north and self.vy == 0 and not self.south or \
                (k == 1 and self.y > self.y_file * DELTA - self.vy and self.vy == 0 and not self.south):
            # условие осуществления прыжка, позволяет приблизиться к потолку несмотря на False

            self.vy = -13
        elif k == 2 and self.east or k == 2 and\
                not self.east and self.x < (self.x_file + 1) * DELTA - self.vx and self.x % DELTA > 0:  # если
            # путь свободен или около свободен, то есть позволяет приблизиться к стенке несмотря на False

            self.x += self.vx

    def move(self):
        """ функция, которая отвечает за непрерывное движение персонажа по оси Оу и за вычисление новых координат"""

        if self.south and self.vy >= 0:
            self.y += self.vy
            self.vy += 1
        elif not self.south and self.vy >= 0:
            self.vy = 0
            self.y -= self.y % DELTA
            self.y += DELTA - 1
        elif self.north and self.vy < 0:
            self.y += self.vy
            self.vy += self.a
        elif not self.north and self.vy < 0:
            if self.y > self.y_file * DELTA - self.vy:
                self.y += self.vy
            else:
                self.vy = -self.vy

        # высчитываение нового положение персонажа в карте
        self.x_file = self.x // DELTA
        self.y_file = self.y // DELTA
