import json
from program_files.constants import *


def choose_level():
    """ функция выбора уровня """

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True, ''
        if event.type == pygame.MOUSEBUTTONDOWN:
            with open(LEVELS_FILE, 'r') as file:  # открывается файл, в котором хранятся координаты снежинок,
                # определяющие загрузку уровня

                loaded = json.load(file)  # массив данных json файла
            for level in loaded['levels']:
                x = level['x']
                y = level['y']
                size = 60  # размер снежинки равне size x size
                if x <= event.pos[0] <= x + size and y <= event.pos[1] <= y + size:  # если курсор попал по снежинке
                    return False, level['level']  # возвращает finished = False, название уровня

    pygame.display.update()

    return False, ''  # возвращает finished = True, пустой уровень
