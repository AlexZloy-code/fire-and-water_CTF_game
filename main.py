import pygame
from random import randint

FPS = 60

WIDTH = 1000  # задает ширину экрана
HEIGHT = 700  # задает высоту экрана
DELTA = 20  # все игровое пространство разбито на некие клеточки, которые определяют цифры из файлов уровней.
# ширина этих клеточек есть "ширина" одной цифры
gamer1_keys = [pygame.K_a, pygame.K_w, pygame.K_d]  # массив клавиш, определяющих движение превого игрока
gamer2_keys = [pygame.K_LEFT, pygame.K_UP, pygame.K_RIGHT]  # массив клавиш, определяющих движение второго игрока
CELLS = {
    '0': '0',
    '1': '1',
    'B': 'B',
    'G': 'G',
    'P': 'P',
    '9': '9'
}  # всякие существующие ячейки. вся информация о ячейках прописана в файле cells_inf
BUTTON_INITIALIZER = {
    'q': ['w', 'e'],
    'a': ['s', 'd'],
    'z': ['x', 'c'],
}  # все инициализаторы различных кнопок

gamer_dead = [False, False]

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))  # игровая площадь
screen.fill((255, 255, 255))
wave_surface = pygame.Surface((DELTA, DELTA), pygame.SRCALPHA)  # поверхность, по которой колеблются волны


class Draw:

    def __init__(self):
        """
        все изобржаения, использующиеся в игре
        self.wall - текступа непроходимого блока (стены)
        self.background - фон
        self.wave_blue - текстура голубой жидкости
        self.wave_green - текстура зеленой жидкости
        self.wave_pink - текстура розовой жидкости
        self.character_images - массив текстур всех персонажей
        """

        self.wall = pygame.image.load('pictures//wall//wall.jpg')
        self.background = pygame.image.load('pictures//backgrounds//background1.jpg')
        self.wave_blue = pygame.image.load('pictures//waves//blue.png')
        self.wave_green = pygame.image.load('pictures//waves//green.png')
        self.wave_pink = pygame.image.load('pictures//waves//pink.png')
        self.character_images = [
            pygame.image.load('pictures//characters//ch1_down.png'),
            pygame.image.load('pictures//characters//ch1_stay.png'),
            pygame.image.load('pictures//characters//ch1_up.png'),
            pygame.image.load('pictures//characters//ch2_down.png'),
            pygame.image.load('pictures//characters//ch2_stay.png'),
            pygame.image.load('pictures//characters//ch2_up.png')
        ]
        self.buttons = [
            pygame.image.load('pictures//buttons//button_1.png'),
            pygame.image.load('pictures//buttons//button_2.png'),
            pygame.image.load('pictures//buttons//button_3.png'),
        ]
        self.stuffs = [
            pygame.image.load('pictures//elements//el_1.png'),
            pygame.image.load('pictures//elements//el_2.png'),
            pygame.image.load('pictures//elements//el_3.png'),
            pygame.image.load('pictures//elements//el_4.png'),
            pygame.image.load('pictures//elements//el_5.png'),
            pygame.image.load('pictures//elements//snowman.png')
        ]

    def draw_cells(self, file_massive, count, but):
        """ отрисовывает каждую ячейку файла в pygame.screen"""

        # переменная для смещения волны во времени
        dx = - ((pygame.time.get_ticks() // 10) % 20)

        # обновление wave_surface прозрачный цветом
        wave_surface.fill(0)
        if count == len(players) - 1:
            for line_count, string in enumerate(file_massive):
                for letter_count, letter in enumerate(string):
                    if letter == CELLS['1']:  # отрисовывает все стены или полы
                        screen.blit(self.wall, (DELTA * letter_count, DELTA * line_count))
                    elif letter == CELLS['B']:  # отрисовывает голубую жидкость
                        wave_surface.blit(self.wave_blue, (dx, 0))
                        screen.blit(wave_surface, (DELTA * letter_count, DELTA * line_count))
                    elif letter == CELLS['G']:  # отрисовывает зеленую жидкость
                        wave_surface.blit(self.wave_green, (dx, 0))
                        screen.blit(wave_surface, (DELTA * letter_count, DELTA * line_count))
                    elif letter == CELLS['P']:  # отрисовывает розовую жидкость
                        wave_surface.blit(self.wave_pink, (dx, 0))
                        screen.blit(wave_surface, (DELTA * letter_count, DELTA * line_count))
                    elif letter == but.letter and not but.pushed:  # отрисовывает кнопки
                        for key_number, key in enumerate(BUTTON_INITIALIZER):
                            if but.letter == key:
                                screen.blit(self.buttons[key_number], (but.x_file * DELTA, but.y_file * DELTA + DELTA / 2))

    def draw_background(self):
        """ рисует фон """

        screen.blit(self.background, (0, 0))

    def draw_character(self, count, inf):
        """
        рисует персонажа
        inf = [vy, x, y]
        """

        if inf[0] > 0:  # отрисовка поднимающегося персонажа
            player_surface = self.character_images[0 + count * 3]
        elif inf[0] == 0:  # отрисовка стоящего персонажа
            player_surface = self.character_images[1 + count * 3]
        else:  # отрисовка падающего персонажа
            player_surface = self.character_images[2 + count * 3]
        screen.blit(player_surface, (inf[1], inf[2]))

    def draw_element(self, decoration):
        """ рисует каждый декоративный элемент """

        player_surface = self.stuffs[decoration.decoration_number]
        screen.blit(player_surface, (decoration.x * DELTA, decoration.y * DELTA))


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
        self.fences = [
            pygame.image.load('pictures//fences//fence_1.png'),
            pygame.image.load('pictures//fences//fence_2.png'),
            pygame.image.load('pictures//fences//fence_3.png'),
        ]

    def player_initializer(self, symbols, stuff):
        """ создает персонажей """

        global players
        y_file = -1  # y_file - координата объекта по y - 1
        for string in self.storage:
            y_file += 1
            x_file = -1  # x_file - координата объекта по x - 1
            for letter in string:
                x_file += 1
                for symbol in symbols:  # ищет все объекты, перебирает каждый символ-инициализатор
                    if letter == symbol:
                        x = x_file * DELTA
                        y = y_file * DELTA
                        obj = stuff(x, y)
                        players.append(obj)

    def button_fence_initializer(self, symbols, obj_button, obj_fence):
        """ создает кнопки и баррикады """

        global buttons, fences
        buttons = [[], [], []]
        fences = [[], [], []]
        y_file = -1  # y_file - координата ограды по y - 1
        for string in self.storage:
            y_file += 1
            x_file = -1  # x_file - координата ограды по x - 1
            for letter in string:
                x_file += 1
                for symbol_count, symbol in enumerate(symbols):  # ищет все ограждения, перебирает каждый
                    # символ-инициализатор

                    # проверка кнопки
                    if letter == symbol:
                        x = x_file * DELTA
                        y = y_file * DELTA
                        obj = obj_button(x, y, symbol)
                        buttons[symbol_count].append(obj)

                    # проверка баррикады
                    for element in symbols[symbol]:
                        if letter == element:
                            x = x_file * DELTA
                            y = y_file * DELTA
                            obj = obj_fence(x, y, element)
                            fences[symbol_count].append(obj)

    def element_initializer(self, obj_decoration):
        """ инициализирует каждый декоративынй элемент """

        global decorations
        y_file = -1  # y_file - координата ограды по y - 1
        for string in self.storage:
            y_file += 1
            x_file = -1  # x_file - координата ограды по x - 1
            for letter in string:
                x_file += 1
                if letter == '1':
                    element_number = randint(0, 24)
                    if element_number < 5:
                        obj = obj_decoration(x_file, y_file, element_number)
                        decorations.append(obj)
                    if y_file > 1 and self.storage[y_file - 1][x_file] == '0' and element_number == 5:
                        obj = obj_decoration(x_file, y_file - 1, element_number)
                        decorations.append(obj)

    def draw_fence(self, obj_fence, obj_button):
        """ отрисовывает баррикады, описывает поведение баррикад """

        if obj_button.pushed:
            if obj_fence.letter == BUTTON_INITIALIZER[obj_button.letter][0]:
                for height in range(3):
                    self.storage[obj_fence.y // DELTA + height] = \
                        self.storage[obj_fence.y // DELTA + height][:obj_fence.x // DELTA] + '0' + \
                        self.storage[obj_fence.y // DELTA + height][obj_fence.x // DELTA + 1:]
            elif obj_fence.letter == BUTTON_INITIALIZER[obj_button.letter][1]:
                for length in range(3):
                    self.storage[obj_fence.y // DELTA] = \
                        self.storage[obj_fence.y // DELTA][:obj_fence.x // DELTA + length] + '0' + \
                        self.storage[obj_fence.y // DELTA][obj_fence.x // DELTA + length + 1:]
            pass
        else:
            if obj_fence.letter == BUTTON_INITIALIZER[obj_button.letter][0]:
                for key_number, key in enumerate(BUTTON_INITIALIZER):
                    if obj_button.letter == key:
                        screen.blit(self.fences[key_number], (obj_fence.x, obj_fence.y))
                for height in range(3):
                    self.storage[obj_fence.y // DELTA + height] = \
                        self.storage[obj_fence.y // DELTA + height][:obj_fence.x // DELTA] + '1' + \
                        self.storage[obj_fence.y // DELTA + height][obj_fence.x // DELTA + 1:]
            elif obj_fence.letter == BUTTON_INITIALIZER[obj_button.letter][1]:
                for key_number, key in enumerate(BUTTON_INITIALIZER):
                    if obj_button.letter == key:
                        screen.blit(pygame.transform.rotate(self.fences[key_number], 90), (obj_fence.x, obj_fence.y))
                for length in range(3):
                    self.storage[obj_fence.y // DELTA] = \
                        self.storage[obj_fence.y // DELTA][:obj_fence.x // DELTA + length] + '1' + \
                        self.storage[obj_fence.y // DELTA][obj_fence.x // DELTA + length + 1:]

    def collision(self, obj, champ_number, but):
        """ функция говорит о дозволенных движениях персонажа по оси Оу"""

        if champ_number == 0:
            but.pushed = False
        obj.north, obj.south, obj.west, obj.east, obj.alive = False, False, False, False, True

        # проверяет разрешаемые направление движения по оси Оy
        for degree in range(2):  # degree - степень: 0 - возможности прыгнуть вверх, 1 - возможности упасть вниз
            if obj.y_file == len(self.storage) * degree - 3 * degree:  # если персонаж на нулевой строке, то
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
                    y_check = obj.y_file + 1 - 2 * (-1) ** degree  # y_check - номер просматриваемой строки
                else:
                    y_check = obj.y_file - 1 + 3 * degree
                for cell_number in range(length):  # перебирает каждыю ячейку на возможность свободно передвигаться
                    # cell_number - порядок выбранной ячейки

                    # проверяет, не столкнулся ли персонаж с нежелаемой для него жидкостью или с непропускаемой ячейкой
                    if degree == 1 and champ_number == 0 and\
                            self.storage[y_check - 1][obj.x_file + cell_number] == CELLS['P']:
                        obj.alive = False
                        break
                    elif degree == 1 and champ_number == 1 and\
                            self.storage[y_check - 1][obj.x_file + cell_number] == CELLS['G']:
                        obj.alive = False
                        break
                    elif degree == 1 and self.storage[y_check - 1][obj.x_file + cell_number] == CELLS['B']:
                        obj.alive = False
                        break
                    elif self.storage[y_check][obj.x_file + cell_number] == CELLS['1']:
                        break
                    elif self.storage[y_check][obj.x_file + cell_number] != CELLS['1']:
                        count += 1
                if count == length:
                    if degree == 0:
                        obj.north = True
                    else:
                        obj.south = True

        # проверяет разрешаемые направление движения по оси Ох
        for degree in range(2):  # degree - степень: 0 - возможность побежать влево, 1 - возможность побежать вправо
            if obj.x_file == len(self.storage[obj.y_file]) * degree - 3 * degree:  # если персонаж на нулевом столбце,
                # то он не побежит влево, если персонаж на последнем столбце, то он не побежит вправо нужно отметить,
                # что касаясь правой границы функция выдает True

                pass
            else:
                count = 0  # кол-во файловых ячеек, которые позволяют свободно передвигаться
                if obj.y % DELTA > 0:  # проверяет, персонаж находится в 2 или 3 вертикалльных ячейках
                    height = 3  # length - кол-во "свободных" ячеек
                else:
                    height = 2
                if obj.x % DELTA > 0:  # в зависимости от "жирноты" по оси Ох переменная x_check имееть свою формулу
                    if degree == 1:
                        x_check = obj.x_file + 3
                    else:
                        x_check = obj.x_file - 1  # x_check - номер просматриваемой строки
                else:
                    if degree == 1:
                        x_check = obj.x_file + 2
                    else:
                        x_check = obj.x_file - 1

                # если персонаж столкнулся с кнопкой, то кнопка нажимается
                for button_position_check in range(obj.x_file, obj.x_file + 3):
                    if self.storage[obj.y_file + 2][button_position_check] == but.letter:
                        but.pushed = True

                for cell_number in range(height):  # перебирает каждыю ячейку на возможность свободно передвигаться
                    # cell_number - порядок выбранной ячейки

                    if self.storage[obj.y_file + cell_number][x_check] == CELLS['1']:
                        break
                    elif self.storage[obj.y_file + cell_number][x_check] != CELLS['1']:
                        count += 1
                if count == height:
                    if degree == 0:
                        obj.west = True
                    else:
                        obj.east = True


class Button:

    def __init__(self, x, y, letter):
        """
        информация о каждой кнопке
        self.pushed - показатель, говорящий нажата ли кнопка или нет
        self.letter - инициализатор кнопки
        self.x_file, self.y_file - файловые координаты кнопки
        """

        self.pushed = False
        self.letter = letter
        self.x_file = x // DELTA
        self.y_file = y // DELTA

    def inf(self):
        """ возвращает информацию: нажата ли кнопка или нет """

        return self.pushed


class Fence:

    def __init__(self, x, y, letter):
        """
        информация о каждой баррикаде
        self.letter - символ-индетификатор баррикады: (w, e, s, d, x, c)
        self.x, self.y - координаты левого правого угла
        """

        self.letter = letter
        self.x = x
        self.y = y


class Decoration:

    def __init__(self, x_file, y_file, decoration_number):
        """
        информация о каждом декоратовном элементе
        self.x_file, self.y_file - координата левого правого угла
        """

        self.x = x_file
        self.y = y_file
        self.decoration_number = decoration_number


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


finished = False
clock = pygame.time.Clock()

players = []  # массив из игроков
buttons = []  # массив из кнопок
fences = []  # массив из ограды
decorations = []  # массив из декоратинвых элементов
map = Map('lvl1.txt')  # передает классу Map информацию об уровне
draw = Draw()  # класс отрисовки

# инициализирует кнопки и персонажей
map.player_initializer(CELLS['9'], Player)
map.button_fence_initializer(BUTTON_INITIALIZER, Button, Fence)
map.element_initializer(Decoration)

while not finished:

    clock.tick(FPS)
    draw.draw_background()  # рисует фон

    # рисует на screen и в файле баррикады
    for list_count, list in enumerate(buttons):  # перебирает каждый список из buttons. в каждом списке свой символ
        for button in list:  # перебирает все кнопки с одинаковым символом-индетификатором
            for fence in fences[list_count]:  # перебирает каждую баррикаду из списка. в списке все привязаны к одной
                # кнопке

                map.draw_fence(fence, button)

    # проверяет дозволенные направление движения
    for count_player, player in enumerate(players):
        for list in buttons:  # перебирает каждый список из buttons
            for button in list:
                map.collision(player, count_player, button)

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

    # безпрерывная анимация, зарисовка персонажей, проверка, попал ли персонаж в смертельную жидкость, нажатие кнопки
    for count_player, player in enumerate(players):

        # проверка на нажатие кнопки
        for list_count in buttons:  # перебирает каждый список из buttons
            for button in list_count:
                map.collision(player, count_player, button)

        # перемещает персонаж
        player.move()

        # проверяет, столкнулся ли персонаж с жидкостью
        inform = player.inf()
        if not inform[3]:
            gamer_dead[count_player] = True
        else:
            draw.draw_character(count_player, inform)
            
        # зарисовывает каждую ячейку
        for list in buttons:  # перебирает каждый список из buttons
            for button in list:
                draw.draw_cells(map.load_map('lvl1.txt'), count_player, button)  # зарисовка каждой игровой ячейки

    for decoration in decorations:
        draw.draw_element(decoration)

    pygame.display.update()
    screen.fill((255, 255, 255))

pygame.quit()
