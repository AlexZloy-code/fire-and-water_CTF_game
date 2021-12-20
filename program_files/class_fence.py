class Fence:

    def __init__(self, x, y, letter):
        """
        информация о каждой баррикаде
        self.letter - символ-индетификатор баррикады: (w, e, s, d, x, c)
        self.x, self.y - координаты левого верхнего угла surface
        """

        self.letter = letter
        self.x = x
        self.y = y
