from random import randint
from program_files.constants import *


class Map:

    @staticmethod
    def load_map(input_filename):
        """
        выписывает всю информацию об уровне в массив
        входные данные:
        input_filename - имя текстового файла, в котором хранится уровень
        """

        with open(input_filename, 'r') as input_file:
            file_massive = input_file.readlines()  # массив строк
            for lines_count in range(len(file_massive)):
                file_massive[lines_count] = file_massive[lines_count].rstrip()  # удаляет в каждой строке '/n'
        return file_massive

    def get_file(self):
        """ возвращает массив строк уровня """

        return self.storage_const

    def __init__(self, input_filename):
        """
        информация о классе
        self.storage - массив строк
        входные данные:
        input_filename - имя текстового файла, в котором хранится уровень
        """

        self.storage_const = self.load_map(input_filename)
        self.storage = self.load_map(input_filename)

    def player_initializer(self, symbols, obj_player, players):
        """
        помещает в массив персонажей всех персонажей
        входные данные:
        symbols - массив символов-инициализаторов (в данном случае он один и равно '9')
        obj_player - класс игрок Player
        players - массив элемента класса Player
        """

        y_file = -1  # y_file - координата объекта по y
        for string in self.storage:
            y_file += 1
            x_file = -1  # x_file - координата объекта по x
            for letter in string:
                x_file += 1
                for symbol in symbols:  # ищет всех персонажей, перебирает каждый символ-инициализатор
                    if letter == symbol:
                        x = x_file * DELTA
                        y = y_file * DELTA
                        obj = obj_player(x, y)
                        players.append(obj)

    def button_fence_initializer(self, symbols, obj_button, buttons, obj_fence, fences):
        """
        помещает в массив класса соответствующий объект: button, fence, door
        """

        y_file = -1  # y_file - координата объекта по y
        for string in self.storage:
            y_file += 1
            x_file = -1  # x_file - координата объекта по x
            for letter in string:
                x_file += 1

                for symbol_count, symbol in enumerate(symbols):  # ищет все объекты, перебирает каждый
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

    def gate_initializer(self, obj_gate, gates):
        """ помещает в массив класса соответствующий объект: button, fence, door """

        y_file = -1  # y_file - координата объекта по y
        for string in self.storage:
            y_file += 1
            x_file = -1  # x_file - координата объекта по x
            for letter in string:
                x_file += 1

                # проверка врат
                if letter == CELLS['v'] and len(gates) == 0 or letter == CELLS['V'] and len(gates) == 1:
                    x = x_file * DELTA
                    y = y_file * DELTA
                    obj = obj_gate(x, y, letter)
                    gates.append(obj)
        if len(gates) < 2:  # рекурсия сделано специально, чтобы первыми вратами заиницилизировались зеленые врата 'v'
            self.gate_initializer(obj_gate, gates)

    def decoration_initializer(self, obj_decoration, decorations):
        """ помещает в массив декорации каждую декорацию """

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

    def treatment_fence(self, obj_fence, obj_button):
        """
        работа с баррикадами. если нажата кнопка, то соответствующей баррикады в файле как бы не существует, если
        кнопка отжата, то в файл в соответствующую ячейку передается значение 1, а также возвращает числовое значение
        key_number (характеризует номер картинки) и angle (угол поворота)
        """

        if obj_button.pushed[0] or obj_button.pushed[1]:  # если кнопка не нажата
            if obj_fence.letter == BUTTON_INITIALIZER[obj_button.letter][0]:  # вертикальная баррикада
                for height in range(3):  # меняет ячейки на '0', чтобы можно было спокойно ходить
                    self.storage[obj_fence.y // DELTA + height] = \
                        self.storage[obj_fence.y // DELTA + height][:obj_fence.x // DELTA] + '0' + \
                        self.storage[obj_fence.y // DELTA + height][obj_fence.x // DELTA + 1:]
            elif obj_fence.letter == BUTTON_INITIALIZER[obj_button.letter][1]:  # горизонтальная баррикада
                for length in range(3):  # меняет ячейки на '0', чтобы можно было спокойно ходить
                    self.storage[obj_fence.y // DELTA] = \
                        self.storage[obj_fence.y // DELTA][:obj_fence.x // DELTA + length] + '0' + \
                        self.storage[obj_fence.y // DELTA][obj_fence.x // DELTA + length + 1:]
            pass
        else:  # если кнопка нажата
            if obj_fence.letter == BUTTON_INITIALIZER[obj_button.letter][0]:  # вертикальная баррикада
                for height in range(3):  # меняет ячейки на '1', чтобы нельзя было ходить
                    self.storage[obj_fence.y // DELTA + height] = \
                        self.storage[obj_fence.y // DELTA + height][:obj_fence.x // DELTA] + '1' + \
                        self.storage[obj_fence.y // DELTA + height][obj_fence.x // DELTA + 1:]
                for key_number, key in enumerate(BUTTON_INITIALIZER):
                    if obj_button.letter == key:
                        return key_number, 0  # возвращает номер кнопки, к которой привязана баррикада, возвращает угол
            elif obj_fence.letter == BUTTON_INITIALIZER[obj_button.letter][1]:  # горизонтальная баррикада
                for length in range(3):  # меняет ячейки на '1', чтобы нельзя было ходить
                    self.storage[obj_fence.y // DELTA] = \
                        self.storage[obj_fence.y // DELTA][:obj_fence.x // DELTA + length] + '1' + \
                        self.storage[obj_fence.y // DELTA][obj_fence.x // DELTA + length + 1:]
                for key_number, key in enumerate(BUTTON_INITIALIZER):
                    if obj_button.letter == key:
                        return key_number, 90  # возвращает номер кнопки, к которой привязана баррикада, возвращает угол
        return 'no_image_number', 'no_angle'  # возвращает "пустое значение", чтобы функция
        # draw_fences ничего не рисовала

    def collision(self, obj, champ_number, but):
        """ взаоимдействие персонажа с каждой ячейкой из файла"""

        but.pushed[champ_number] = False
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
                        but.pushed[champ_number] = True

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
