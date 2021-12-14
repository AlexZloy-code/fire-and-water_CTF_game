from consntants import *


class Button:

    def __init__(self, x, y, letter):
        """
        информация о каждой кнопке
        self.pushed - показатель, говорящий нажата ли кнопка или нет
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
