from program_files.initializer_command import *
from program_files.constants import *


def win_or_lose_command(SET_TIME, GAME_IS_OVER, win, finished, CONNECTION, PAUSE, NUMBER, LEVEL_CHOICE, level, k_r=False):
    """
    функция воспроизовдит часть игры, когда персонаж умер
    SET_TIME - время начала отсчета
    GAME_IS_OVER - # состояние, проиграли лы вы или нет, после нажатия на какую-нибудь кнопку значение False
    трансформируется в True
    win - True or False, True - если оба персонажа достигли своих врат и игра требует побудную менюшку, False - менюшку
    поражения
    finished - передается значение False. Если в функции меняется на True, значит пользователь вышел из игры
    CONNECTION - переменная, говорящая о том, удержана ли кнопка мыши или нет.
    PAUSE - поставлена ли игра на паузу или нет (тип boolean)
    NUMBER - упорядоченный номер уровня
    LEVEL_CHOICE - сигнал, говорящий уровень выбирается или уже выбран (True/False)
    """

    for count_player, player in enumerate(players[NUMBER]):
        # перебирает каждый список из buttons
        for list in button_massive[NUMBER]:
            for button in list:
                for gate in gates[NUMBER]:
                    draw.draw_cells(
                        map.get_file()[NUMBER], player, count_player, button, gate, gates, NUMBER)
                    # зарисовка каждой игровой ячейки

    for decoration in decorations[NUMBER]:  # рисует декор
        draw.draw_element(decoration)
    draw.draw_pause_button()  # отрисовка кнопки пазуы

    # создание темной поверхности, будет наложена на
    dark_screen = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    # игровое окно, если выскакивает окно паузы, победы или поражения

    dark_screen.fill(0)  # делает эту поверхность прозрачной
    # отрисовка темного прямоугольника
    pygame.draw.rect(dark_screen, (0, 0, 0, 88), (0, 0, WIDTH, HEIGHT))
    screen.blit(dark_screen, (0, 0))

    if SET_TIME == 0:
        # задаем начало отсчета работы с менюшкой "поражения"
        SET_TIME = pygame.time.get_ticks()
    # рабочий временной промежуток работы с менюшкой "поражения"
    delta_time = pygame.time.get_ticks() - SET_TIME
    if delta_time > 100:
        draw.draw_win_or_lose_menu(
            menu, delta_time, win, level, PAUSE)  # отрисовка менюшки"

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
            return SET_TIME, GAME_IS_OVER, finished, CONNECTION
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                k_r = True
                break

        if event.type == pygame.MOUSEBUTTONDOWN:  # работа с кнопками менюшки
            size1, size2, size3 = menu.get_size_info()  # размер кнопки менюшки
            # координаты кнопок менюшки
            coordinates1, coordinates2, coordinates3 = menu.get_coordinates_info()
            CONNECTION = True  # мышь зафиксирована, можно регулировать громкость
            if PAUSE:
                if coordinates1[0] < event.pos[0] < coordinates1[0] + size1[0] and \
                        coordinates1[1] < event.pos[1] < coordinates1[1] + size1[1]:  # попадание по кнопке "retry"

                    GAME_IS_OVER = False  # игра возобновляется
                    SET_TIME = 0  # время отсчета обнулилось
                    PAUSE = False
                    for player in players[NUMBER]:
                        player.set_start_data()  # возвращает игроков в начальное положение
                    menu.set_start_data()  # возвращает менюшку в начальное положение
                if coordinates2[0] < event.pos[0] < coordinates2[0] + size2[0] and \
                        coordinates2[1] < event.pos[1] < coordinates2[1] + size2[1]:  # попадание по кнопке
                    # "back_to_menu"

                    GAME_IS_OVER = False  # игра возобновляется
                    SET_TIME = 0  # время отсчета обнулилось
                    PAUSE = False
                    menu.set_start_data()  # возвращает менюшку в начальное положение
                    LEVEL_CHOICE = True
                if coordinates3[0] < event.pos[0] < coordinates3[0] + size3[0] and \
                        coordinates3[1] < event.pos[1] < coordinates3[1] + size3[1]:  # попадание по кнопке
                    # continue

                    GAME_IS_OVER = False  # игра возобновляется
                    SET_TIME = 0  # время отсчета обнулилось
                    PAUSE = False
                    menu.set_start_data()  # возвращает менюшку в начальное положение
            else:
                if coordinates1[0] < event.pos[0] < coordinates1[0] + size1[0] and \
                        coordinates1[1] < event.pos[1] < coordinates1[1] + size1[1]:  # попадание по кнопке "retry"

                    GAME_IS_OVER = False  # игра возобновляется
                    SET_TIME = 0  # время отсчета обнулилось
                    for player in players[NUMBER]:
                        player.set_start_data()  # возвращает игроков в начальное положение
                    menu.set_start_data()  # возвращает менюшку в начальное положение
                if coordinates2[0] < event.pos[0] < coordinates2[0] + size2[0] and \
                        coordinates2[1] < event.pos[1] < coordinates2[1] + size2[1]:  # попадание по кнопке
                    # "back_to_menu"

                    GAME_IS_OVER = False  # игра возобновляется
                    SET_TIME = 0  # время отсчета обнулилось

                    for player in players[NUMBER]:
                        player.set_start_data()  # возвращает игроков в начальное положение
                    menu.set_start_data()  # возвращает менюшку в начальное положение
                    LEVEL_CHOICE = True
        if event.type == pygame.MOUSEBUTTONUP:
            CONNECTION = False  # кнопка мыши отжата, громкость регулировать нельзя
        if event.type == pygame.MOUSEMOTION and CONNECTION:
            slider_coordinates = music.get_slider_coordinates()  # получает координаты слайдера
            if slider_coordinates[0] < event.pos[0] < slider_coordinates[0] + 40 and \
                    slider_coordinates[1] < event.pos[1] < slider_coordinates[1] + 40:  # если курсор мыши попал по слайдеру

                music.slider_motion(event.pos[0])  # перемещает слайдер

    draw.draw_music_interface(music)  # рисует полоску громкости
    music.music_set_volume()  # регулирует громкость музыки

    pygame.display.update()
    screen.fill((255, 255, 255))

    if k_r:
        GAME_IS_OVER = False  # игра возобновляется
        SET_TIME = 0  # время отсчета обнулилось
        PAUSE = False
        for player in players[NUMBER]:
            player.set_start_data()  # возвращает игроков в начальное положение
        menu.set_start_data()  # возвращает менюшку в начальное положение

    # SET_TIME - возвращает время отсчета
    return SET_TIME, GAME_IS_OVER, finished, CONNECTION, PAUSE, LEVEL_CHOICE
    # работы с менюшкой, GAME_IS_OVER - окончание/продолжение работы с менюшкой поражения,
    # finished - окончание/продолжение игры, CONNECTION - зажат ли курсор мыши или нет, PAUSE - приостановлена ли игра
    # на паузу или нет
