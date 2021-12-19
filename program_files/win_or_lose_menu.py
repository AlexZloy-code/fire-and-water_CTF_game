from program_files.initializer_command import *
from program_files.constants import *


def win_or_lose_command(SET_TIME, GAME_IS_OVER, win, finished, CONNECTION, PAUSE):
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
    """

    for count_player, player in enumerate(players):
        for list in buttons:  # перебирает каждый список из buttons
            for button in list:
                for gate in gates:
                    draw.draw_cells(map.get_file(), player, count_player, button, gate, gates)  # зарисовка
                    # каждой игровой ячейки

    for decoration in decorations:  # рисует декор
        draw.draw_element(decoration)
    draw.draw_pause_button()  # отрисовка кнопки пазуы

    dark_screen = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)  # создание темной поверхности, будет наложена на
    # игровое окно, если выскакивает окно паузы, победы или поражения

    dark_screen.fill(0)  # делает эту поверхность прозрачной
    pygame.draw.rect(dark_screen, (0, 0, 0, 88), (0, 0, WIDTH, HEIGHT))  # отрисовка темного прямоугольника
    screen.blit(dark_screen, (0, 0))

    if SET_TIME == 0:
        SET_TIME = pygame.time.get_ticks()  # задаем начало отсчета работы с менюшкой "поражения"
    delta_time = pygame.time.get_ticks() - SET_TIME  # рабочий временной промежуток работы с менюшкой "поражения"
    if delta_time > 100:
        draw.draw_win_or_lose_menu(menu, delta_time, win, PAUSE)  # отрисовка менюшки"

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
            return SET_TIME, GAME_IS_OVER, finished, CONNECTION
        if event.type == pygame.MOUSEBUTTONDOWN:  # работа с кнопками менюшки
            size1, size2, size3 = menu.get_size_info()  # размер кнопки менюшки
            coordinates1, coordinates2, coordinates3 = menu.get_coordinates_info()  # координаты кнопок менюшки
            CONNECTION = True  # мышь зафиксирована, можно регулировать громкость
            if PAUSE:
                if coordinates1[0] < event.pos[0] < coordinates1[0] + size1[0] and \
                        coordinates1[1] < event.pos[1] < coordinates1[1] + size1[1]:  # попадание по кнопке "retry"

                    GAME_IS_OVER = False  # игра возобновляется
                    SET_TIME = 0  # время отсчета обнулилось
                    PAUSE = False
                    for player in players:
                        player.set_start_data()  # возвращает игроков в начальное положение
                    menu.set_start_data()  # возвращает менюшку в начальное положение
                if coordinates2[0] < event.pos[0] < coordinates2[0] + size2[0] and \
                        coordinates2[1] < event.pos[1] < coordinates2[1] + size2[1]:  # попадание по кнопке
                    # "back_to_menu"

                    GAME_IS_OVER = False  # игра возобновляется
                    SET_TIME = 0  # время отсчета обнулилось
                    PAUSE = False
                    menu.set_start_data()  # возвращает менюшку в начальное положение
                    print('gay2')
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
                    for player in players:
                        player.set_start_data()  # возвращает игроков в начальное положение
                    menu.set_start_data()  # возвращает менюшку в начальное положение
                if coordinates2[0] < event.pos[0] < coordinates2[0] + size2[0] and \
                        coordinates2[1] < event.pos[1] < coordinates2[1] + size2[1]:  # попадание по кнопке
                    # "back_to_menu"

                    GAME_IS_OVER = False  # игра возобновляется
                    SET_TIME = 0  # время отсчета обнулилось
                    for player in players:
                        player.set_start_data()  # возвращает игроков в начальное положение
                    menu.set_start_data()  # возвращает менюшку в начальное положение
                    print('gay2')
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

    return SET_TIME, GAME_IS_OVER, finished, CONNECTION, PAUSE  # SET_TIME - возвращает время отсчета работы с менюшкой,
    # GAME_IS_OVER - окончание/продолжение работы с менюшкой поражения, finished - окончание/продолжение игры,
    # CONNECTION - зажат ли курсор мыши или нет, PAUSE - приостановлена ли игра на паузу или нет
