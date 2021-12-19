from program_files.constants import *


class Button:

    def __init__(self, x, y, letter):
        """
        информация о каждой кнопке
        self.pushed - нажата ли кнопка или нет. self.pushed[0] - player_one, self.pushed[1] - player_two
        self.letter - инициализатор кнопки
        self.x_file, self.y_file - файловые координаты кнопки
        """

        self.pushed = [False, False]
        self.letter = letter
        self.x_file = x // DELTA
        self.y_file = y // DELTA

    def inf(self):
        """ возвращает информацию: нажата ли кнопка или нет """

        return self.pushed
