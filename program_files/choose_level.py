import json
from program_files.constants import *


def choose_level():
    """ функция выбора уровня """

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True, ''
        if event.type == pygame.MOUSEBUTTONDOWN:
            # открывается файл, в котором хранятся координаты снежинок,
            with open(LEVELS_FILE, 'r') as file:
                # определяющие загрузку уровня

                loaded = json.load(file)  # массив данных json файла
            for level in loaded['levels']:
                if not level['hide']:
                    x = level['x']
                    y = level['y']
                    size = 60  # размер снежинки равне size x size
                    # если курсор попал по снежинке
                    if x <= event.pos[0] <= x + size and y <= event.pos[1] <= y + size:
                        # возвращает finished = False, название уровня
                        return False, level['level']

    pygame.display.update()

    return False, ''  # возвращает finished = True, пустой уровень
