import pygame


pygame.init()

FPS = 60
WIDTH = 1000  # ширина экрана
HEIGHT = 700  # высота экрана
DELTA = 20  # все игровое пространство разбито на некие клеточки, которые определяют цифры из файлов уровней.
# ширина этих клеточек есть "ширина" одной цифры. иначе говоря, декартовая система координат скрина из пайгема
# была расширена в DELTA раз
GAME_IS_OVER = False  # состояние, проиграли лы вы или нет
SET_TIME = 0  # начало отсчета с момента поражения
FONT = pygame.font.Font(None, 50)  # шрифт текста
FILE_NAME = 'levels//lvl1.txt'
CONNECTION = False  # переменная, говорящая о том, удержана ли кнопка мыши или нет.
PAUSE = False  # переменная, говорящая о том, активировано ли окно паузы или нет
LEVEL_CHOICE = True  # переменная, говорящая о том, выбирается ли уровень или нет
LEVELS_FILE = 'levels//levels_coordinates.JSON'
FILES_NAME = [
    'levels//lvl1.txt',
    'levels//lvl2.txt'
]

gamer1_keys = [pygame.K_a, pygame.K_w, pygame.K_d]  # массив клавиш, определяющих движение превого игрока
gamer2_keys = [pygame.K_LEFT, pygame.K_UP, pygame.K_RIGHT]  # массив клавиш, определяющих движение второго игрока
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
fences = [[], [], []]  # массив из ограды
gates = []  # массив из ворот
decorations = []  # массив из декоратинвых элементов

screen = pygame.display.set_mode((WIDTH, HEIGHT))  # игровая площадь
screen.fill((255, 255, 255))
wave_surface = pygame.Surface((DELTA, DELTA), pygame.SRCALPHA)  # поверхность, по которой колеблются волны
