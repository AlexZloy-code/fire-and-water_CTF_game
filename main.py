import pygame

FPS = 60

WIDTH = 1000  # задает ширину экрана
HEIGHT = 700  # задает высоту экрана
DELTA = 20  # все игровое пространство разбито на некие клеточки, которые определяют цифры из файлов уровней.
# ширина этих клеточек есть "ширина" одной цифры
CELLS = {
    '0': '0',
    '1': '1',
    'B': 'B',
    'G': 'G',
    'P': 'P',
    '9': '9'
}  # всякие существующие ячейки. вся информация о ячейках прописана
# в файле cells_inf
COUNT_PLAYERS = 2  # задает кол-во персонажей от 0 до 2

RED = (219, 96, 94)
gamer_existence = False  # существование игрока. переменная существует для того, чтобы один раз создать
# персонажа по координатам, ибо дальше код игры будет определять координаты персонажа в файле
character_images = [
    pygame.image.load('pictures//characters//ch1_down.png'),
    pygame.image.load('pictures//characters//ch1_stay.png'),
    pygame.image.load('pictures//characters//ch1_up.png'),
    pygame.image.load('pictures//characters//ch2_down.png'),
    pygame.image.load('pictures//characters//ch2_stay.png'),
    pygame.image.load('pictures//characters//ch2_up.png')
]  # массив изображений персонажа

gamer1_keys = [pygame.K_a, pygame.K_w, pygame.K_d]  # массив клавиш, определяющих движение превого игрока
gamer2_keys = [pygame.K_LEFT, pygame.K_UP, pygame.K_RIGHT]  # массив клавиш, определяющих движение второго игрока

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))  # игровая площадь
screen.fill((255, 255, 255))


class Draw:

    def __init__(self):
        """
        все изобржаения, использующиеся в игре
        self.wall - текступа непроходимого блока (стены)
        self.background - фон
        self.wave_blue - текстура голубой жидкости
        self.wave_green - текстура зеленой жидкости
        self.wave_pink - текстура розовой жидкости
        """

        self.wall = pygame.image.load('pictures//wall//nigga.jpg')
        self.background = pygame.image.load('pictures//background.jpg')
        self.wave_blue = pygame.image.load('pictures//waves//blue.png')
        self.wave_green = pygame.image.load('pictures//waves//green.png')
        self.wave_pink = pygame.image.load('pictures//waves//pink.png')

    def draw_cells(self, file_massive):
        """ отрисовывает каждую ячейку файла в pygame.screen"""

        for line_count, string in enumerate(file_massive):
            for letter_count, letter in enumerate(string):
                if letter == CELLS['1']:  # отрисовывает все стены или полы
                    screen.blit(self.wall, (DELTA * letter_count, DELTA * line_count))
                elif letter == CELLS['B']:  # отрисовывает голубую жидкость
                    screen.blit(self.wave_blue, (DELTA * letter_count, DELTA * line_count))
                elif letter == CELLS['G']:  # отрисовывает зеленую жидкость
                    screen.blit(self.wave_green, (DELTA * letter_count, DELTA * line_count))
                elif letter == CELLS['P']:  # отрисовывает розовую жидкость
                    screen.blit(self.wave_pink, (DELTA * letter_count, DELTA * line_count))

    def draw_background(self):
        """ рисует фон """

        screen.blit(self.background, (0, 0))

    @staticmethod
    def draw_character(count, inf):
        """
        рисует персонажа
        inf = [vy, x, y]
        """

        if inf[0] > 0:  # отрисовка поднимающегося персонажа
            player_surface = character_images[0 + count * 3]
        elif inf[0] == 0:  # отрисовка стоящего персонажа
            player_surface = character_images[1 + count * 3]
        else:  # отрисовка падающего персонажа
            player_surface = character_images[2 + count * 3]
        screen.blit(player_surface, (inf[1], inf[2]))


class Map:

    @staticmethod
    def load_map(input_filename):
        """ выписывает всю информацию об уровне в массив """

        with open(input_filename, 'r') as input_file:
            file_massive = input_file.readlines()  # массив строк
            for lines_count in range(len(file_massive)):
                file_massive[lines_count] = file_massive[lines_count].rstrip()  # удаляет в каждой строке '/n'
        return file_massive

    def __init__(self, input_filename):
        """
        информация о классе
        self.storage - массив строк
        """

        self.storage = self.load_map(input_filename)

    @staticmethod
    def to_map_coordinates(obj):
        """ возвращает координаты персонажа в файле (уровне). type: integer """

        return obj.x // DELTA, obj.y // DELTA

    def coordinate(self, player_number):
        """ функция считывает координаты игрока из карты """

        y_file = -1  # y_file - координата игрока по y - 1
        number = -1  # номер игрока
        for string in self.storage:
            y_file += 1
            x_file = -1  # x_file - координата игрока по x - 1
            for letter in string:
                x_file += 1
                if letter == CELLS['9']:  # ищет всех персонажей
                    number += 1
                    if number == player_number:
                        x_champion = x_file * DELTA
                        y_champion = y_file * DELTA

                        return x_champion, y_champion

    def collision(self, obj, champ_number):
        """ функция говорит о дозволенных движениях персонажа по оси Оу"""

        res = {
            "north": False,
            "south": False,
            "west": False,
            "east": False,
            "alive": True
        }  # массив, который превращается в результат по окончании функции

        x, y = self.to_map_coordinates(obj)  # файловые координаты персонажа в целых числах

        # проверяет разрешаемые направление движения по оси Ох
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

                    # проверяет, не столкнулся ли персонаж с нежелаемой для него жидкостью или с непропускаемой ячейкой
                    if degree == 1 and champ_number == 0 and self.storage[y_check - 1][x + cell_number] == CELLS['P']:
                        res["alive"] = False
                        break
                    elif degree == 1 and champ_number == 1 and self.storage[y_check - 1][x + cell_number] == CELLS['G']:
                        res["alive"] = False
                        break
                    elif degree == 1 and self.storage[y_check - 1][x + cell_number] == CELLS['B']:
                        res["alive"] = False
                        break
                    elif self.storage[y_check][x + cell_number] != CELLS['1']:
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

                    if self.storage[y + cell_number][x_check] == CELLS['1']:
                        break
                    elif self.storage[y + cell_number][x_check] != CELLS['1']:
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
        self.vx = 0
        self.vy = 0
        self.x_file = 0
        self.y_file = 0
        self.north = False
        self.south = False
        self.west = False
        self.east = False

    def set_possibility(self, abilities):
        """ записивыет данные о дозволенном движении перонажа"""

        self.north = abilities['north']
        self.south = abilities['south']
        self.west = abilities['west']
        self.east = abilities['east']

    def coordinate_input(self, data):
        """ функция записывает координаты игрока в базу данных """

        self.x, self.y = data

    def inf(self):
        """ возвращает информацию, чтобы потом правильно нарисовать картинку """

        return self.vy, self.x, self.y

    def to_make_it_move(self, k):
        """
        функция, которая заставляет перемещать персонаж по оси Оx и прыгать по оси Оy
        k - номер абстрактного списка [left, up, right]
        """

        # далее в условиях прописаны длинные формулы. они учитывают несколько багов
        if k == 0 and self.west or k == 0 and\
                not self.west and self.x > self.x_file * DELTA + self.vx and self.x % DELTA > 0:  # если путь
            # свободен или около свободен, то есть позволяет приблизиться к стенке несмотря на False

            self.vx = -4
            self.x += self.vx
        elif k == 1 and self.north and self.vy == 0 and not self.south or \
                (k == 1 and self.y > self.y_file * DELTA - self.vy and self.vy == 0 and not self.south):
            # условие осуществления прыжка, позволяет приблизиться к потолку несмотря на False

            self.vy = -13
        elif k == 2 and self.east or k == 2 and\
                not self.east and self.x < (self.x_file + 1) * DELTA - self.vx and self.x % DELTA > 0:  # если
            # путь свободен или около свободен, то есть позволяет приблизиться к стенке несмотря на False

            self.vx = 4
            self.x += self.vx

        self.vx = 0

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
            self.vy += 1
        elif not self.north and self.vy < 0:
            if self.y > self.y_file * DELTA - self.vy:
                self.y += self.vy
            else:
                self.vy = -self.vy

        # высчитываение нового положение персонажа в карте
        self.x_file = self.x // DELTA
        self.y_file = self.y // DELTA


def check_possible_movements(count_player):
    """ возвращает инфорацию о дозволенных движениях"""

    oy_abilities = map.collision(player, count_player)
    player.set_possibility(oy_abilities)


finished = False
clock = pygame.time.Clock()

players = [Player() for _ in range(COUNT_PLAYERS)]  # массив из двух игроков
map = Map('lvl1.txt')  # передает классу Map информацию об уровне
draw = Draw()

while not finished:

    clock.tick(FPS)
    draw.draw_background()  # рисует фон

    # спавнит персонажей на поле
    if not gamer_existence:
        for count_player, player in enumerate(players):
            player.coordinate_input(map.coordinate(count_player))
        gamer_existence = True

    # проверяет дозволенные направление движения
    for count_player, player in enumerate(players):
        check_possible_movements(count_player)

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

    # безпрерывная анимация, зарисовка персонажей, проверка, попал ли персонаж в смертельную жидкость
    for count_player, player in enumerate(players):
        check_possible_movements(count_player)
        player.move()
        inform = player.inf()
        draw.draw_character(count_player, inform)
        if not map.collision(player, count_player)['alive']:
            print('u dead inside')

    draw.draw_cells(map.load_map('lvl1.txt'))  # зарисовка каждой игровой ячейки

    pygame.display.update()
    screen.fill((255, 255, 255))

pygame.quit()
