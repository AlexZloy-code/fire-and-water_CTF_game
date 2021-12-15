class Gate:

    def __init__(self, x, y, letter):
        """
        информация о каждом выходе
        self.letter - символ-индетификатор врат (v, V)
        self.x, self.y - координаты левого верхнего угла surface
        self.x_lattice, self.y_lattice - координаты левого правого уга  surface решетки
        """

        self.x = x
        self.y = y
        self.x_lattice = 0
        self.y_lattice = 0
        self.letter = letter
