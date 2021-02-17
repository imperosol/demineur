import random
import tkinter as tk

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

    def has_flag(self):
        return self.__hasFlag

    def __str__(self):
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
            return "U"


class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Mon app")
        self.master.minsize(800, 600)
        self.master.maxsize(800, 600)
        self.display_grid()
        self.pack()

    def display_grid(self):
        self.grid = tk.Canvas(self.master, width=800, height=600, background='grey')
        rect = []
        box_width = 30
        for i in range(50, LINE*box_width + 50, box_width):
            for j in range(50, COLUMN*box_width + 50, box_width):
                rect.append(self.grid.create_rectangle(i, j, i+box_width, j+box_width))
        self.grid.pack()


class Grid:
    def __init__(self):
        self.grid = [[Box() for x in range(COLUMN)] for y in range(LINE)]
        _coordinates_list = [(i, j) for i in range(LINE) for j in range(COLUMN)]
        _coordinates_list = random.choices(_coordinates_list, weights=None,
                                           cum_weights=None, k=(LINE * COLUMN) // 10)
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

    def __str__(self):
        displayable_grid = ""
        for i in self.grid:
            for j in i:
                displayable_grid += str(j) + ' '
            displayable_grid +=  '\n'
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
    game_grid = Grid()
    is_game_finished, is_valid_choice = False, False
    place_to_dig = [0, 0]
    while not is_game_finished:
        print(game_grid)
        while not is_valid_choice:
            place_to_dig[0] = int(input("Sur quelle ligne voulez-vous creuser ?   ")) - 1
            place_to_dig[1] = int(input("Sur quelle colonne voulez-vous creuser ? ")) - 1
            is_valid_choice = game_grid.dig(place_to_dig[0], place_to_dig[1])


if __name__ == '__main__':
    game()
"""
ma_grille = Grid()
print(ma_grille)
print(ma_grille.debug_str())
ma_grille.discover_box(1, 1)
print(ma_grille)
"""
