from program_files.constants import *


class Menu:

    def __init__(self):
        """
        self.x, self.y - координаты выскакивающего окна
        self.retry_x, self.retry_y - координаты поверхности кнопки retry
        self.retry_surface - поверхность кнопки menu
        self.back_to_menu_x, self.back_to_menu_y - координаты поверхности кнопки menu
        self.back_to_menu_surface - поверхность кнопки retry
        self.contin_x, self.contin_y - координаты кнопки continue
        self.contin_surface - поверхность кнопки continue
        """

        self.x = 300
        self.y = -400
        self.retry_x = self.x + 170
        self.retry_y = self.y + 70
        self.retry_surface = FONT.render('retry', True, (255, 255, 255))
        self.back_to_menu_x = self.retry_x - 100
        self.back_to_menu_y = self.retry_y + 100
        self.back_to_menu_surface = FONT.render('go back to menu', True, (255, 255, 255))
        self.contin_x = self.retry_x - 40
        self.contin_y = self.retry_y - 70
        self.contin_surface = FONT.render('continue', True, (255, 255, 255))

    @staticmethod
    def get_size_info():
        """ возвращает размер кнопок """

        return FONT.size('retry'), FONT.size('go back to menu'), FONT.size('continue')

    def get_coordinates_info(self):
        """ возвращает координаты кнопок """

        return (self.retry_x, self.retry_y), (self.back_to_menu_x, self.back_to_menu_y), (self.contin_x, self.contin_y)

    def set_start_data(self):
        """ задает менюшке 'поражения' начальные данные """

        self.x = 300
        self.y = -400
        self.retry_x = self.x + 170
        self.retry_y = self.y + 70
        self.back_to_menu_x = self.retry_x - 100
        self.back_to_menu_y = self.retry_y + 100
        self.contin_x = self.retry_x - 40
        self.contin_y = self.retry_y - 70
