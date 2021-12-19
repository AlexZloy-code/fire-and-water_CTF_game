import json
from program_files.constants import *


def choose_level():

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True, ''
        if event.type == pygame.MOUSEBUTTONDOWN:
            with open(LEVELS_FILE, 'r') as file:
                loaded = json.load(file)
            for level in loaded['levels']:
                x = level['x']
                y = level['y']
                size = 60
                if x <= event.pos[0] <= x + size and y <= event.pos[1] <= y + size:
                    return False, level['level']

    pygame.display.update()

    return False, ''
