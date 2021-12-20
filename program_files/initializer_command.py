from program_files.class_draw import *
from program_files.class_map import *
from program_files.class_menu import *
from program_files.class_player import *
from program_files.class_gate import *
from program_files.class_decoration import *
from program_files.class_fence import *
from program_files.class_button import *
from program_files.class_music import *


# инициализирует большинство классов
map = Map(FILES_NAME)  # передает классу Map информацию об уровне
draw = Draw()  # класс отрисовки
menu = Menu()  # класс меню
music = Music()  # класс музыки
map.player_initializer(CELLS['9'], Player)  # инициализирует всех персонажей
map.button_fence_initializer(BUTTON_INITIALIZER, Button, Fence)  # инициализирует кнопки и баррикады
map.gate_initializer(Gate)  # инизицлизирует враща
map.decoration_initializer(Decoration)  # инициализирует декорацию
