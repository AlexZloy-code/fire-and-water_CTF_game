from program_files.win_or_lose_menu import *
from program_files.playing_command import *
from program_files.choose_level import *


finished = False
clock = pygame.time.Clock()
music.play_music()

while not finished:

    clock.tick(FPS)

    if LEVEL_CHOICE:
        finished, level = choose_level()
        if len(level) > 2:
            LEVEL_CHOICE = False
        draw.draw_level_background(LEVELS_FILE)
    if not LEVEL_CHOICE:

        draw.draw_background()  # рисует фон

        for player in players:
            if not player.inf()[3]:
                GAME_IS_OVER = True

        if not GAME_IS_OVER and not PAUSE:
            finished, PAUSE = playing_command(finished, PAUSE)
            y = 0
            for gate in gates:
                y += gate.get_info()
            if y == -120:
                GAME_IS_OVER = True
        elif PAUSE:
            SET_TIME, GAME_IS_OVER, finished, CONNECTION, PAUSE = win_or_lose_command(
                SET_TIME,
                GAME_IS_OVER,
                False,
                finished,
                CONNECTION,
                PAUSE
            )
        elif GAME_IS_OVER:
            if y == -120:
                SET_TIME, GAME_IS_OVER, finished, CONNECTION, PAUSE = win_or_lose_command(
                    SET_TIME,
                    GAME_IS_OVER,
                    True,
                    finished,
                    CONNECTION,
                    PAUSE
                )  # True - победный интерфейс

            else:
                SET_TIME, GAME_IS_OVER, finished, CONNECTION, PAUSE = win_or_lose_command(
                    SET_TIME,
                    GAME_IS_OVER,
                    False,
                    finished,
                    CONNECTION,
                    PAUSE
                )  # False - мертвый интерфейс

pygame.quit()
