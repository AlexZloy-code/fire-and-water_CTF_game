class Decoration:

    def __init__(self, x_file, y_file, decoration_number):
        """
        информация о каждом декоратовном элементе
        self.x_file, self.y_file - координата левого правого угла surface
        self.decoration_number - номер декорации. у каждой декорации есть свой упорядоченный номер из глобального
        массива decorations
        """

        self.x = x_file
        self.y = y_file
        self.decoration_number = decoration_number
