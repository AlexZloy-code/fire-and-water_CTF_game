from consntants import *


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
        self.gates = [
            pygame.image.load('pictures//gates//gate_1.png'),
            pygame.image.load('pictures//gates//gate_2.png'),
            pygame.image.load('pictures//gates//lattice.png')
        ]

    def draw_cells(self, file_massive, obj_player, count, obj_but, obj_gate, gates):
        """ отрисовывает каждую ячейку файла в pygame.screen"""

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
                                self.buttons[key_number],
                                (obj_but.x_file * DELTA, obj_but.y_file * DELTA + DELTA / 2))
                elif letter == obj_gate.letter:
                    self.draw_gates(obj_player, obj_gate, count, gates)

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

    def draw_element(self, element):
        """ рисует каждый декоративный элемент """

        player_surface = self.stuffs[element.decoration_number]
        screen.blit(player_surface, (element.x * DELTA, element.y * DELTA))

    def draw_gates(self, obj_player, obj_gate, count, gates):
        """ рисует врата и отвечает за динамику решеток """

        if obj_gate == gates[count]:
            # создает поверхность врат без решетки
            if obj_gate.letter == 'V':
                gate_surface = self.gates[0]
            else:
                gate_surface = self.gates[1]

            # создает поверхность решетки
            if obj_gate.x - 10 < obj_player.x < obj_gate.x + 40 and\
                    obj_gate.y + 60 > obj_player.y > obj_gate.y:
                if obj_gate.y_lattice >= -60:
                    obj_gate.y_lattice -= 2
            else:
                if obj_gate.y_lattice < 0:
                    obj_gate.y_lattice += 2

            # отображает все поверхности на игровое окно
            lattice_surface = pygame.Surface((40, 60), pygame.SRCALPHA)
            lattice_surface.blit(self.gates[2], (0, obj_gate.y_lattice))
            screen.blit(gate_surface, (obj_gate.x, obj_gate.y - 10))
            screen.blit(lattice_surface, (obj_gate.x + 11, obj_gate.y))
