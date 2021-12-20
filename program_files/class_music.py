import pygame


class Music:

    def __init__(self):
        """
        музыка, ползунок громкости
        self.music_interface_surface - поверхность поверхности, на которой будет нарисован полузнок громкости и курсор
        self.music_interface_surface_x, self.music_interface_surface_y - координаты поверхности, на которой будет
        нарисован полузнок громкости и курсор
        self.bar_x, self.bar_y - координаты полоски громкости внутри поверхности self.music_interface_surface
        self.slider_x, self.slider_y - координаты ползунка громкости внутри поверхности self.music_interface_surface
        """

        self.music_interface_surface = pygame.Surface((240, 40), pygame.SRCALPHA)
        self.music_interface_surface_x = 700
        self.music_interface_surface_y = 40
        self.bar_x = 20
        self.bar_y = 10
        self.slider_x = 200
        self.slider_y = 0

    @staticmethod
    def play_music():
        """ запускает фоновую музыку """

        pygame.mixer.music.load('music//music.mp3')  # фоновая музыка
        pygame.mixer.music.play(-1)  # циклирует музыку

    def slider_motion(self, x):
        """ перемещает slider по полосе прокрутке """

        if 0 <= x - self.music_interface_surface_x - self.bar_x <= 200:
            self.slider_x = x - self.music_interface_surface_x - self.bar_x

    def get_slider_coordinates(self):
        """ возвращает координаты slider на игровой площади """

        return self.slider_x + self.music_interface_surface_x, self.slider_y + self.music_interface_surface_y

    def music_set_volume(self):
        """ регулирует громкость музыки """

        pygame.mixer.music.set_volume(self.slider_x / 200)
