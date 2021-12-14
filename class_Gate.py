class Gate:

    def __init__(self, x, y, letter):
        """
        информация о каждой двери
        self.letter - символ-индетификатор баррикады: (w, e, s, d, x, c)
        self.x, self.y - координаты левого правого угла
        """

        self.x = x
        self.y = y
        self.x_lattice = 0
        self.y_lattice = 0
        self.letter = letter
