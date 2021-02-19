import random
import tkinter as tk
import tkinter.font as font

LINE = 10
COLUMN = 15


class Box:
    def __init__(self):
        self.__hasMine = False
        self.surroundingMines = 0
        self.__hasFlag = False
        self.__hasBeenDiscovered = False

    def put_mine(self):
        self.__hasMine = True

    def is_mined(self):
        return self.__hasMine

    def discover(self):
        self.__hasBeenDiscovered = True

    def has_been_discovered(self):
        return self.__hasBeenDiscovered

    def plant_a_flag_like_the_red_one_on_top_of_the_reichstag(self):
        self.__hasFlag = True

    def remove_this_nazi_flag_and_retake_stalingrad(self):
        self.__hasFlag = False

    def has_flag(self):
        return self.__hasFlag

    def __str__(self):
        """
        :return: if the box has been discovered :
                        if the box has a mine : 'X'
                        if the box has no mine : a string corresponding to the number of surrounding mines
                else :
                        if the box has a flag : '@'
                        else : 'U'
        """
        if self.__hasBeenDiscovered:
            if self.__hasMine:
                return 'X'
            else:
                return str(self.surroundingMines)
        elif self.__hasFlag:
            return '@'
        else:
            return "U"

    def debug_str(self):
        if not self.__hasBeenDiscovered:
            if self.__hasMine:
                return 'X'
            else:
                return str(self.surroundingMines)
        elif self.__hasFlag:
            return '@'
        else:
            return 'U'


class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.game_grid = Grid()
        self.master = master
        self.master.title("Mon app")
        self.master.geometry("800x600")
        self.button_list = [[] for x in range(LINE)]
        self.is_game_ended = False
        self.display_grid()
        self.pack()

    def display_grid(self):
        box_width = 35
        my_frame = tk.Frame(self, width=COLUMN * box_width, height=LINE * box_width)
        my_frame.pack()
        for i in range(LINE):
            for j in range(COLUMN):
                button_content = self.game_grid.get_box_state(i, j)
                # button_content = self.game_grid.grid[i][j].debug_str()
                if button_content == 'X':
                    new_button = MyButton(my_frame, self.game_grid.grid[i][j], image='bomb_img', coord=(i, j), parent=self)
                elif button_content == 'U':
                    new_button = MyButton(my_frame, self.game_grid.grid[i][j], bg='grey', coord=(i, j), parent=self)
                elif button_content == '@':
                    new_button = MyButton(my_frame, self.game_grid.grid[i][j], image='flag_img', coord=(i, j), parent=self)
                else:
                    if self.game_grid.grid[i][j].surroundingMines:
                        new_button = MyButton(my_frame, self.game_grid.grid[i][j], text=button_content, coord=(i, j), parent=self)
                    else:
                        # if the box has no surrounding bomb, the grid and the position of the box must be sent
                        # to the new object for internal methods
                        new_button = MyButton(my_frame, self.game_grid.grid[i][j], text=button_content,
                                              associated_grid=self.game_grid.grid, coord=(i, j), parent=self)
                new_button.button.place(x=j * box_width, y=i * box_width, width=box_width, height=box_width)
                self.button_list[i].append(new_button)

    def defeat(self):
        if not self.is_game_ended:
            self.is_game_ended = True
        for i in range(LINE):
            for j in range(COLUMN):
                self.button_list[i][j].left()
                self.button_list[i][j].button['state'] = tk.DISABLED


class MyButton:
    def __init__(self, my_frame, associated_box, text=None, image=None, bg=None,
                 associated_grid=None, coord=None, parent=None):
        self.images = {'bomb_img': tk.PhotoImage(file="img/mine.png"),
                       'flag_img': tk.PhotoImage(file="img/flag.png")}
        self.button = tk.Button(my_frame, bg=bg, text=text)
        self.coord = coord
        self.parent = parent
        if image:
            if image == 'bomb_img':
                self.button['image'] = self.images['bomb_img']
            else:
                self.button['image'] = self.images['flag_img']
        self.box = associated_box
        self.button.bind('<Button-3>', self.right)
        self.button.bind('<Button-1>', self.left)

    def left(self, event=None):
        if not self.box.has_been_discovered():
            if not self.box.has_flag():
                self.button['bg'] = 'white'
                self.box.discover()
                if self.box.is_mined():
                    self.button['image'] = self.images['bomb_img']
                    if not self.parent.is_game_ended:
                        self.parent.defeat()
                elif self.box.surroundingMines:
                    my_font = font.Font(weight='bold')
                    self.button['text'] = self.box.surroundingMines
                    self.button['font'] = my_font
                    if self.box.surroundingMines == 1:
                        self.button['fg'] = 'blue'
                    elif self.box.surroundingMines == 2:
                        self.button['fg'] = 'green'
                    elif self.box.surroundingMines == 3:
                        self.button['fg'] = 'red'
                    elif self.box.surroundingMines == 4:
                        self.button['fg'] = 'indigo'
                elif not self.box.surroundingMines:
                    self.show_surrounding_boxes()

    def right(self, event=None):
        if not self.box.has_been_discovered():
            if not self.box.has_flag():
                self.box.plant_a_flag_like_the_red_one_on_top_of_the_reichstag()
                self.button['image'] = self.images['flag_img']
            else:
                self.box.remove_this_nazi_flag_and_retake_stalingrad()
                self.button.config(image="")

    def show_surrounding_boxes(self):
        for i in range(-1,2):
            for j in range(-1, 2):
                if 0 <= self.coord[0]+i < LINE and 0 <= self.coord[1]+j < COLUMN:
                    if not self.parent.button_list[self.coord[0]+i][self.coord[1]+j].box.has_been_discovered():
                        self.parent.button_list[self.coord[0]+i][self.coord[1]+j].left()


class Grid:
    def __init__(self):
        self.grid = [[Box() for x in range(COLUMN)] for y in range(LINE)]
        # Create a list of coordinates couple to determine the places in which the bombs will be put
        _coordinates_list = [(i, j) for i in range(LINE) for j in range(COLUMN)]
        _coordinates_list = random.choices(_coordinates_list, k=(LINE * COLUMN) // 5)
        for i in _coordinates_list:
            self.grid[i[0]][i[1]].put_mine()
        # Set the number of mines surrounding each box
        for i in range(LINE):
            for j in range(COLUMN):
                for _line in range(-1, 2):
                    for _column in range(-1, 2):
                        if 0 <= i + _line < LINE and 0 <= j + _column < COLUMN:
                            if self.grid[i + _line][j + _column].is_mined():
                                self.grid[i][j].surroundingMines += 1

    def discover_box(self, line, column):
        _box = self.grid[line][column]
        _box.discover()
        if _box.is_mined():
            print("perdu")
            # TODO : Ajouter les fonctionnalités pour mettre fin à la partie quand on découvre une bombe
        elif _box.surroundingMines == 0:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if 0 <= line + i < LINE and 0 <= column + j < COLUMN:
                        if not self.grid[line + i][column + j].has_been_discovered() \
                                and not self.grid[line + i][column + j].has_flag():
                            self.discover_box(line + i, column + j)

    def dig(self, line, column):
        if line < 0 or line >= LINE or column < 0 or column >= COLUMN:
            print("Hors de la grille")
            return False
        elif self.grid[line][column].has_flag():
            print("Vous ne pouvez pas creuser ici")
            return False
        elif self.grid[line][column].has_been_discovered():
            print("Déjà creusé")
            return False
        else:
            self.discover_box(line, column)
            return True

    def get_box_state(self, line, column):
        return self.grid[line][column].__str__()

    def __str__(self):
        displayable_grid = ""
        for i in self.grid:
            for j in i:
                displayable_grid += str(j) + ' '
            displayable_grid += '\n'
        return displayable_grid

    def debug_str(self):
        displayable_grid = ""
        for i in self.grid:
            for j in i:
                displayable_grid += j.debug_str() + ' '
            displayable_grid += '\n'
        return displayable_grid


def game():
    root = tk.Tk()
    window = App(root)
    window.mainloop()
    # game_grid = Grid()
    # is_game_finished, is_valid_choice = False, False
    # place_to_dig = [0, 0]
    # while not is_game_finished:
    #     print(game_grid)
    #     while not is_valid_choice:
    #         place_to_dig[0] = int(input("Sur quelle ligne voulez-vous creuser ?   ")) - 1
    #         place_to_dig[1] = int(input("Sur quelle colonne voulez-vous creuser ? ")) - 1
    #         is_valid_choice = game_grid.dig(place_to_dig[0], place_to_dig[1])


if __name__ == '__main__':
    game()
"""
ma_grille = Grid()
print(ma_grille)
print(ma_grille.debug_str())
ma_grille.discover_box(1, 1)
print(ma_grille)
"""
