from program_files.win_or_lose_menu import *
from program_files.playing_command import *
from program_files.choose_level import *


finished = False
clock = pygame.time.Clock()
music.play_music()  # запуск фоновой музыки

while not finished:

    clock.tick(FPS)

    if LEVEL_CHOICE:  # происходит выбор уровня
        finished, level = choose_level()
        if len(level) > 2:  # т.к. название уровня (его расположение) длинее двух символом, то можно наложить такое
            # специфическое условие того, что уровень был выбран

            LEVEL_CHOICE = False  # знак того, что уровень был выбран
        draw.draw_level_background(LEVELS_FILE)
        for lev_count, lev in enumerate(FILES_NAME):
            if lev == level:
                NUMBER = lev_count  # номер уровня из массива FILES_NAME
    if not LEVEL_CHOICE:  # если уровень уже выбран

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                # если курсор
                if WIDTH // 2 - 40 <= event.pos[0] <= WIDTH // 2 + 40 and 0 <= event.pos[1] <= 40:
                    # мыши попал по кнопке паузы, что расположена наверху игрового окна

                    PAUSE = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    SET_TIME, GAME_IS_OVER, finished, CONNECTION, PAUSE, LEVEL_CHOICE = win_or_lose_command(
                        SET_TIME,
                        GAME_IS_OVER,
                        False,
                        finished,
                        CONNECTION,
                        PAUSE,
                        NUMBER,
                        LEVEL_CHOICE,
                        level,
                        k_r=True
                    )
                    break

                for motion_number, motion in enumerate(gamer1_keys + gamer2_keys):
                    # персонаж прыгает. motion - кнопка из списка (gamer1_keys + gamer2_keys), motion_number - его номер

                    if event.key == motion and motion_number == 1:
                        players[NUMBER][motion_number //
                                        3].to_make_it_move(motion_number % 3)
                    if event.key == motion and motion_number == 4:
                        players[NUMBER][motion_number //
                                        3].to_make_it_move(motion_number % 3)
        draw.draw_background()  # рисует фон

        for player in players[NUMBER]:
            if not player.inf()[3]:  # если персонаж умер
                GAME_IS_OVER = True

        if not GAME_IS_OVER and not PAUSE:  # если персонажи живы и не пауза
            finished, PAUSE = playing_command(finished, PAUSE, NUMBER)
            y = 0
            for gate in gates[NUMBER]:
                y += gate.get_info()
            if y == -120:
                GAME_IS_OVER = True
        elif PAUSE:  # если пауза
            SET_TIME, GAME_IS_OVER, finished, CONNECTION, PAUSE, LEVEL_CHOICE = win_or_lose_command(
                SET_TIME,
                GAME_IS_OVER,
                False,
                finished,
                CONNECTION,
                PAUSE,
                NUMBER,
                LEVEL_CHOICE,
                level
            )
        elif GAME_IS_OVER:  # если оба персонажа достиглы выхода
            if y == -120:
                SET_TIME, GAME_IS_OVER, finished, CONNECTION, PAUSE, LEVEL_CHOICE = win_or_lose_command(
                    SET_TIME,
                    GAME_IS_OVER,
                    True,
                    finished,
                    CONNECTION,
                    PAUSE,
                    NUMBER,
                    LEVEL_CHOICE,
                    level
                )  # True - победный интерфейс

            else:  # если персонажи мертвы (персонаж мертв)
                SET_TIME, GAME_IS_OVER, finished, CONNECTION, PAUSE, LEVEL_CHOICE = win_or_lose_command(
                    SET_TIME,
                    GAME_IS_OVER,
                    False,
                    finished,
                    CONNECTION,
                    PAUSE,
                    NUMBER,
                    LEVEL_CHOICE,
                    level
                )  # False - мертвый интерфейс

pygame.quit()
