import pygame


pygame.init()

FPS = 60
WIDTH = 1000  # ширина экрана
HEIGHT = 700  # высота экрана
# все игровое пространство разбито на некие клеточки, которые определяют цифры из файлов уровней.
DELTA = 20
# ширина этих клеточек есть "ширина" одной цифры. иначе говоря, декартовая система координат скрина из пайгема
# была расширена в DELTA раз
GAME_IS_OVER = False  # состояние, проиграли лы вы или нет
SET_TIME = 0  # начало отсчета с момента поражения
FONT = pygame.font.Font(None, 50)  # шрифт текста
# переменная, говорящая о том, удержана ли кнопка мыши или нет.
CONNECTION = False
PAUSE = False  # переменная, говорящая о том, активировано ли окно паузы или нет
LEVEL_CHOICE = True  # переменная, говорящая о том, выбирается ли уровень или нет
# название файла, в котором написаны координаты снежинок, которые
LEVELS_FILE = 'levels//levels_coordinates.JSON'
# вызывают свой уровень
FILES_NAME = [
    'levels//lvl1.txt',
    'levels//lvl2.txt',
    'levels//lvl3.txt',
    'levels//lvl4.txt',
    'levels//lvl5.txt',
    'levels//lvl6.txt',
    'levels//lvl7.txt',
    'levels//lvl8.txt',
    'levels//lvl9.txt',
    'levels//lvl10.txt',
    'levels//lvl11.txt',
    'levels//lvl12.txt',
    'levels//lvl13.txt',
    'levels//lvl14.txt',
    'levels//lvl15.txt',
    'levels//lvl16.txt',
    'levels//lvl17.txt',
    'levels//lvl18.txt',
    'levels//lvl19.txt',
    'levels//lvl20.txt',
    'levels//lvl21.txt',
    'levels//lvl22.txt',
    'levels//lvl23.txt',
    'levels//lvl24.txt',
    'levels//lvl25.txt',
    'levels//lvl26.txt',
    'levels//lvl27.txt',
    'levels//lvl28.txt',
    'levels//lvl29.txt',
    'levels//lvl30.txt',
    'levels//lvl31.txt',
    'levels//lvl32.txt',
    'levels//lvl33.txt',
    'levels//lvl34.txt',
    'levels//lvl35.txt',
    'levels//lvl36.txt',
    'levels//lvl37.txt',
    'levels//lvl38.txt'
]  # названия всех уровней

# массив клавиш, определяющих движение превого игрока
gamer1_keys = [pygame.K_a, pygame.K_w, pygame.K_d]
# массив клавиш, определяющих движение второго игрока
gamer2_keys = [pygame.K_LEFT, pygame.K_UP, pygame.K_RIGHT]
CELLS = {
    '0': '0',
    '1': '1',
    'B': 'B',
    'G': 'G',
    'P': 'P',
    'v': 'v',
    'V': 'V',
    '9': '9',
}  # все существующие ячейки. вся информация о ячейках прописана в файле cells_inf
BUTTON_INITIALIZER = {
    'q': ['w', 'e'],
    'a': ['s', 'd'],
    'z': ['x', 'c'],
}  # все инициализаторы различных кнопок
players = []  # массив из игроков
buttons = [[], [], []]  # массив из кнопок
button_massive = []
fences = [[], [], []]  # массив из ограды
fence_massive = []
gates = []  # массив из ворот
decorations = []  # массив из декоратинвых элементов

LEVELS_DICT = {
    '1': ['2'],
    '2': ['3'],
    '3': ['4', '5'],
    '4': [],
    '5': ['6'],
    '6': ['7', '11'],
    '7': ['8', '10'],
    '8': ['9'],
    '9': [],
    '10': [],
    '11': ['12'],
    '12': ['13', '21', '32'],
    '13': ['14'],
    '14': ['15'],
    '15': ['16', '18'],
    '16': [],
    '17': [],
    '18': ['19'],
    '19': ['20'],
    '20': [],
    '21': ['22', '30'],
    '22': ['24', '29'],
    '23': [],
    '24': ['25'],
    '25': [],
    '26': [],
    '27': ['26', '28'],
    '28': [],
    '29': ['27'],
    '30': ['31'],
    '31': [],
    '32': ['33'],
    '33': ['34'],
    '34': ['35', '23'],
    '35': ['36'],
    '36': ['37', '38'],
    '37': ['17'],
    '38': []
}

screen = pygame.display.set_mode((WIDTH, HEIGHT))  # игровая площадь
screen.fill((255, 255, 255))
# поверхность, по которой колеблются волны
wave_surface = pygame.Surface((DELTA, DELTA), pygame.SRCALPHA)
