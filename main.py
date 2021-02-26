from gui import *
from random import sample

LINE = 10
COLUMN = 20
BOMB_PROPORTION = 5


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


class Grid:
    def __init__(self):
        _nbr_of_boxes, _nbr_of_bombs = LINE * COLUMN, (LINE * COLUMN) // BOMB_PROPORTION
        self.grid = [[Box() for x in range(COLUMN)] for y in range(LINE)]
        self.__undiscovered_secured_boxes = _nbr_of_boxes - _nbr_of_bombs
        self.flags = 0
        # Create a list of coordinates couple to determine the places in which the bombs will be put
        _coordinates_list = [(i, j) for i in range(LINE) for j in range(COLUMN)]
        _coordinates_list = sample(_coordinates_list, k=_nbr_of_bombs)
        for i in _coordinates_list:
            self.grid[i[0]][i[1]].put_mine()
        # Set the number of mines surrounding each box
        for i in range(LINE):
            for j in range(COLUMN):
                if not self.grid[i][j].is_mined():
                    for _line in range(-1, 2):
                        for _column in range(-1, 2):
                            if 0 <= i + _line < LINE and 0 <= j + _column < COLUMN:
                                if self.grid[i + _line][j + _column].is_mined():
                                    self.grid[i][j].surroundingMines += 1

    def get_box_state(self, row, column):
        """
        @param row: the row position of the box to test
        @type row: int
        @param column: the column position of the box to test
        @type column: int
        @return: a string corresponding to the state of the box:
                if the box has been discovered :
                        if the box has a mine : 'X'
                        if the box has no mine : a string corresponding to the number of surrounding mines
                else :
                        if the box has a flag : '@'
                        else : 'U'
        @rtype:str
        """
        return self.grid[row][column].__str__()

    def get_nbr_of_surrounding_flags(self, row, column):
        """
        @param row: the row position of the box to test
        @type row: int
        @param column: the column position of the box to test
        @type column: int
        @return: the number of flags surrounding the tested box
        @rtype: int
        A method that returns the number of bombs surrounding a specific box in the grid
        """
        nbr_of_flags = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= i + row < LINE and 0 <= j + column < COLUMN:
                    if self.grid[i + row][j + column].has_flag():
                        nbr_of_flags += 1
        return nbr_of_flags

    def decrease_number_of_undiscovered_boxes(self):
        self.__undiscovered_secured_boxes -= 1

    def get_nbr_of_remaining_boxes(self):
        return self.__undiscovered_secured_boxes

    def is_grid_secured(self):
        return not self.__undiscovered_secured_boxes


def game():
    """
    main function of the program
    """
    root = tk.Tk()
    window = App(root)
    window.mainloop()


if __name__ == '__main__':
    game()
