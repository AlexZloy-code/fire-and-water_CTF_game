from program_files.constants import *
import json


class Draw:

    def __init__(self):
        """
        все изобржаения, использующиеся в игре
        self.wall - текступа непроходимого блока (стены)
        self.background - фон
        self.wave_blue, self.wave_green, self.wave_pink - текстурки голубой, зеленой и розовой жидкости
        self.character_images - массив текстур всех персонажей
        self.button_images - массив текстур всех кнопок
        self.decoration_images - массив текстур всех декораций
        self.gate_images - массив текстур всех врат
        self.fence_images - массив текстур всех баррикад
        self.menu_images - массив текстур интерфейса
        """

        self.wall = pygame.image.load('pictures//wall//wall.jpg')
        self.background = pygame.image.load('pictures//backgrounds//background1.jpg')
        self.level_background = pygame.image.load('pictures//menu//background.png')
        self.snowflakes = [
            pygame.image.load('pictures//menu//not_activated.png'),
            pygame.image.load('pictures//menu//activated.png')
        ]
        self.wave_blue = pygame.image.load('pictures//waves//blue.png')
        self.wave_green = pygame.image.load('pictures//waves//green.png')
        self.wave_pink = pygame.image.load('pictures//waves//pink.png')
        self.pause_button = pygame.image.load('pictures//menu//pause_button.png')
        self.character_images = [
            pygame.image.load('pictures//characters//ch1_down.png'),
            pygame.image.load('pictures//characters//ch1_stay.png'),
            pygame.image.load('pictures//characters//ch1_up.png'),
            pygame.image.load('pictures//characters//ch2_down.png'),
            pygame.image.load('pictures//characters//ch2_stay.png'),
            pygame.image.load('pictures//characters//ch2_up.png')
        ]
        self.button_images = [
            pygame.image.load('pictures//buttons//button_1.png'),
            pygame.image.load('pictures//buttons//button_2.png'),
            pygame.image.load('pictures//buttons//button_3.png'),
        ]
        self.decoration_images = [
            pygame.image.load('pictures//elements//el_1.png'),
            pygame.image.load('pictures//elements//el_2.png'),
            pygame.image.load('pictures//elements//el_3.png'),
            pygame.image.load('pictures//elements//el_4.png'),
            pygame.image.load('pictures//elements//el_5.png'),
            pygame.image.load('pictures//elements//snowman.png')
        ]
        self.gate_images = [
            pygame.image.load('pictures//gates//gate_1.png'),
            pygame.image.load('pictures//gates//gate_2.png'),
            pygame.image.load('pictures//gates//lattice.png')
        ]
        self.fence_images = [
            pygame.image.load('pictures//fences//fence_1.png'),
            pygame.image.load('pictures//fences//fence_2.png'),
            pygame.image.load('pictures//fences//fence_3.png'),
        ]
        self.menu_images = [
            pygame.image.load('pictures//menu//lose_background.png'),
            pygame.image.load('pictures//menu//win_background.png'),
            pygame.image.load('pictures//menu//pause_background.png')
        ]
        self.music_interface_images = [
            pygame.image.load('pictures//menu//bar.png'),
            pygame.image.load('pictures//menu//music_ball.png')
        ]

    def draw_cells(self, file_massive, obj_player, count, obj_but, obj_gate, gates):
        """
        отрисовывает каждую ячейку файла в pygame.screen
        данные на вход:
        file_massive - массив строк из текстового документа
        obj_player - класс игрок Player
        count - упорядоченный номер игрока из глобального массива players
        obj_but - класс кнопка Button
        obj_gate - класс врат Gate
        gates - массив элементов Gate
        """

        # переменная для смещения волны во времени
        dx = - ((pygame.time.get_ticks() // 10) % 20)

        # обновление wave_surface прозрачный цветом
        wave_surface.fill(0)
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
                elif letter == obj_but.letter and (not obj_but.pushed[0] and not obj_but.pushed[1]):  # отрисовывает
                    # кнопки

                    for key_number, key in enumerate(BUTTON_INITIALIZER):
                        if obj_but.letter == key:
                            screen.blit(
                                self.button_images[key_number],
                                (obj_but.x_file * DELTA, obj_but.y_file * DELTA + DELTA / 2))
                elif letter == obj_gate.letter:  # отрисовывает врата
                    self.draw_gates(obj_player, obj_gate, count, gates)

    def draw_background(self):
        """ рисует фон """

        screen.blit(self.background, (0, 0))

    def draw_level_background(self, filename):
        """ рисует фон со всеми уровнями """

        screen.blit(self.level_background, (0, 0))
        with open(filename, 'r') as file:
            loaded = json.load(file)
        for level in loaded['levels']:
            if level['activated']:
                screen.blit(self.snowflakes[1], (level['x'], level['y']))
            else:
                screen.blit(self.snowflakes[0], (level['x'], level['y']))

    def draw_pause_button(self):
        """ рисует кнопку паузы """

        screen.blit(self.pause_button, (WIDTH // 2 - 40, 0))

    def draw_character(self, count, inf):
        """
        отрисовка персонажа
        данные на вход:
        count - упорядоченный номер игрока из глобального массива players
        inf = [vy, x, y] - данные о персонаже
        """

        if inf[0] > 0:  # отрисовка поднимающегося персонажа
            player_surface = self.character_images[0 + count * 3]
        elif inf[0] == 0:  # отрисовка стоящего персонажа
            player_surface = self.character_images[1 + count * 3]
        else:  # отрисовка падающего персонажа
            player_surface = self.character_images[2 + count * 3]
        screen.blit(player_surface, (inf[1], inf[2]))

    def draw_element(self, obj_decoration):
        """
        отрисовка каждого декоративного элемента
        данные на вход:
        obj_decoration - класс декорации Decoration
        """

        player_surface = self.decoration_images[obj_decoration.decoration_number]
        screen.blit(player_surface, (obj_decoration.x * DELTA, obj_decoration.y * DELTA))

    def draw_fence(self, obj_fence, key_number, angle):
        """
        отрисовывает баррикаду
        данные на вход:
        obj_fence - класс баррикады Fence
        key_number - номер [0, 1, 2] кнопки, к которой привязана баррикада.
        angle - угол поворота картинки баррикады. при angle = 0 смотрит вертикально вниз, angle = 90 - горизонтально
        вправо
        """

        if key_number == 'no_image_number':
            pass
        elif angle == 0:
            screen.blit(self.fence_images[key_number], (obj_fence.x, obj_fence.y))
        elif angle == 90:
            screen.blit(pygame.transform.rotate(self.fence_images[key_number], angle), (obj_fence.x, obj_fence.y))

    def draw_gates(self, obj_player, obj_gate, count, gates):
        """
        отрисовка врат, отвечает за динамику решеток
        данные на вход:
        obj_player - класс игрок Player
        obj_gate - класс врат Gate
        count - упорядоченный номер игрока из глобального массива players
        gates - массив элементов Gate
        """

        if obj_gate == gates[count]:

            # создает поверхность врат без решетки
            if obj_gate.letter == 'V':
                gate_surface = self.gate_images[0]
            else:
                gate_surface = self.gate_images[1]

            # отвечает за динамику решетки
            if obj_gate.x - 10 < obj_player.x < obj_gate.x + 40 and obj_gate.y + 60 > obj_player.y > obj_gate.y:
                if obj_gate.y_lattice > -60:
                    obj_gate.y_lattice -= 1
            else:
                if obj_gate.y_lattice < 0:
                    obj_gate.y_lattice += 1

            # отображает все поверхности на игровое окно
            lattice_surface = pygame.Surface((40, 60), pygame.SRCALPHA)  # поверхность для изображения решетки,
            # по которой будет скользить изображение

            lattice_surface.blit(self.gate_images[2], (0, obj_gate.y_lattice))
            screen.blit(gate_surface, (obj_gate.x, obj_gate.y - 10))
            screen.blit(lattice_surface, (obj_gate.x + 11, obj_gate.y))

    def draw_win_or_lose_menu(self, obj_menu, time, win, PAUSE):
        """
        отрисовка окна поражения
        obj_menu - класс менюшки Menu
        time - временной промежуток, в котором работает менюшка
        win - True/False. True - если оба персонажа достигли своих врат и игра требует побудную менюшку, False - если
        какой-то персонаж умер, возвращает менюшку поражения
        PAUSE - True/False. True - пазуа, False - нет паузы
        """

        if obj_menu.y < 100:
            obj_menu.y += time // 10  # координаты окна меню
            obj_menu.retry_y = obj_menu.y + 200  # координаты кнопки retry
            obj_menu.back_to_menu_y = obj_menu.retry_y + 50  # координаты кнопки back_to_menu
            if PAUSE:
                obj_menu.contin_y = obj_menu.retry_y - 50  # координаты кнопки continue

        if win:  # если оба персонажа достигли своих врат и игра требует победную менюшку
            screen.blit(self.menu_images[1], (obj_menu.x, obj_menu.y))
        elif not win and not PAUSE:  # если какой-то персонаж умер, возвращает менюшку поражения
            screen.blit(self.menu_images[0], (obj_menu.x, obj_menu.y))
        elif PAUSE:  # если пауза
            screen.blit(self.menu_images[2], (obj_menu.x, obj_menu.y))
        screen.blit(obj_menu.retry_surface, (obj_menu.retry_x, obj_menu.retry_y))
        screen.blit(obj_menu.back_to_menu_surface, (obj_menu.back_to_menu_x, obj_menu.back_to_menu_y))
        if PAUSE:
            screen.blit(obj_menu.contin_surface, (obj_menu.contin_x, obj_menu.contin_y))

    def draw_music_interface(self, obj_music):
        """
        рисует slider и полосу прокрути
        данные на вход:
        obj_music - класс музыки Music
        """

        obj_music.music_interface_surface.fill(0)  # обновляет surface
        obj_music.music_interface_surface.blit(
            self.music_interface_images[0],
            (obj_music.bar_x, obj_music.bar_y)
        )  # рисует полосу прокрутки
        obj_music.music_interface_surface.blit(
            self.music_interface_images[1],
            (obj_music.slider_x, obj_music.slider_y)
        )  # рисует слайдер
        screen.blit(
            obj_music.music_interface_surface,
            (obj_music.music_interface_surface_x, obj_music.music_interface_surface_y)
        )
