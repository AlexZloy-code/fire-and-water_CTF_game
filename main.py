from class_Gate import *
from class_Fence import *
from class_Decoration import *
from class_Button import *
from class_Draw import *
from class_Player import *
from class_Map import *


finished = False
clock = pygame.time.Clock()

players = []  # массив из игроков
buttons = [[], [], []]  # массив из кнопок
fences = [[], [], []]  # массив из ограды
gates = []  # массив из ворот
decorations = []  # массив из декоратинвых элементов
map = Map('lvl1.txt')  # передает классу Map информацию об уровне
draw = Draw()  # класс отрисовки

# инициализирует большинство классов
map.player_initializer(CELLS['9'], Player, players)
map.button_fence_initializer(BUTTON_INITIALIZER, Button, buttons, Fence, fences)
map.gate_initializer(Gate, gates)
map.element_initializer(Decoration, decorations)

while not finished:

    clock.tick(FPS)
    draw.draw_background()  # рисует фон

    # рисует на screen и в файле баррикады
    for list_count, list in enumerate(buttons):  # перебирает каждый список из buttons. в каждом списке свой символ
        for button in list:  # перебирает все кнопки с одинаковым символом-индетификатором
            for fence in fences[list_count]:  # перебирает каждую баррикаду из списка. в списке все привязаны к одной
                # кнопке

                map.draw_fence(fence, button)

    # проверяет дозволенные направление движения
    for count_player, player in enumerate(players):
        for list in buttons:  # перебирает каждый список из buttons
            for button in list:
                map.collision(player, count_player, button)

    # обработчик событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.KEYDOWN:
            for motion_number, motion in enumerate(gamer1_keys + gamer2_keys):  # по нажатию кнопки w или ARROW_UP
                # персонаж прыгает. motion - кнопка из списка (gamer1_keys + gamer2_keys), motion_number - его номер

                if event.key == motion and motion_number == 1:
                    players[motion_number // 3].to_make_it_move(motion_number % 3)
                if event.key == motion and motion_number == 4:
                    players[motion_number // 3].to_make_it_move(motion_number % 3)

    # непрерывное управление персонажами по оси Ох
    for motion_number, motion in enumerate(gamer1_keys + gamer2_keys):
        if pygame.key.get_pressed()[motion] and (motion_number % 3 != 1):
            players[motion_number // 3].to_make_it_move(motion_number % 3)

    # беспрерывная анимация, зарисовка персонажей, проверка, попал ли персонаж в смертельную жидкость, нажатие кнопки
    for count_player, player in enumerate(players):

        # проверка на нажатие кнопки
        for list_count in buttons:  # перебирает каждый список из buttons
            for button in list_count:
                map.collision(player, count_player, button)

        # перемещает персонаж
        player.move()

        # зарисовывает каждую ячейку
        for list in buttons:  # перебирает каждый список из buttons
            for button in list:
                for gate in gates:
                    draw.draw_cells(map.load_map('lvl1.txt'), player, count_player, button, gate, gates)  # зарисовка
                    # каждой игровой ячейки

    for count_player, player in enumerate(players):
        # проверяет, столкнулся ли персонаж с жидкостью
        inform = player.inf()
        if not inform[3]:
            gamer_dead[count_player] = True
        else:
            draw.draw_character(count_player, inform)

    for decoration in decorations:  # рисует декорацию
        draw.draw_element(decoration)

    pygame.display.update()
    screen.fill((255, 255, 255))

pygame.quit()
