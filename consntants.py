import pygame


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
    'v': 'v',
    'V': 'V',
    '9': '9',
}  # всякие существующие ячейки. вся информация о ячейках прописана в файле cells_inf
BUTTON_INITIALIZER = {
    'q': ['w', 'e'],
    'a': ['s', 'd'],
    'z': ['x', 'c'],
}  # все инициализаторы различных кнопок


gamer_dead = [False, False]

pygame.init()

pygame.mixer.music.load('music//music.mp3')
pygame.mixer.music.play(-1)

screen = pygame.display.set_mode((WIDTH, HEIGHT))  # игровая площадь
screen.fill((255, 255, 255))
wave_surface = pygame.Surface((DELTA, DELTA), pygame.SRCALPHA)  # поверхность, по которой колеблются волны
