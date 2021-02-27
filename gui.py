from main import *
import tkinter as tk
import tkinter.font as font


class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.game_grid = Grid()
        self.master.title('Minesweeper')
        self.master.geometry("800x600")
        self.button_list = [[] for x in range(LINE)]
        self.is_game_ended = False
        self.display_grid()
        self.info_frame = InfoFrame(master=self)
        self.menu_bar = Menu(master)
        self.pack()

    def display_grid(self):
        box_width = self.__define_box_width()
        my_frame = tk.Frame(self, width=COLUMN * box_width, height=LINE * box_width)
        my_frame.pack(pady=(20, 0))
        for i in range(LINE):
            for j in range(COLUMN):
                new_button = MyButton(my_frame, self.game_grid.grid[i][j], coord=(i, j), parent=self)
                new_button.button.place(x=j * box_width, y=i * box_width, width=box_width, height=box_width)
                self.button_list[i].append(new_button)

    @staticmethod
    def __define_box_width():
        if COLUMN > 21 or LINE > 14:  # if there is more lines or columns than the window can contain
            _width_by_row = 510 // LINE
            _width_by_column = 760 // COLUMN
            box_width = _width_by_row if (_width_by_row < _width_by_column) else _width_by_column
        else:
            box_width = 35
        return box_width

    def defeat(self):
        self.end_game()
        defeat_font = font.Font(weight='bold')
        tk.Label(self, text="Defeat", fg='red', font=defeat_font).pack()

    def victory(self):
        self.end_game()
        victory_font = font.Font(weight='bold')
        tk.Label(self, text="Victory", fg='green', font=victory_font).pack()

    def end_game(self):
        if not self.is_game_ended:
            self.is_game_ended = True
        for i in range(LINE):
            for j in range(COLUMN):
                if self.button_list[i][j].box.has_flag():
                    self.button_list[i][j].box.remove_this_nazi_flag_and_retake_stalingrad()
                    self.button_list[i][j].button.config(image="")
                self.button_list[i][j].left()
                self.button_list[i][j].button['state'] = tk.DISABLED
        self.info_frame.update_info(remaining_boxes=0, flags=0)
    #
    # def reload_game(self):
    #     self.game_grid = Grid()
    #     self.button_list = [[] for x in range(LINE)]
    #     self.is_game_ended = False
    #     self.display_grid()
    #     self.info_frame = InfoFrame(master=self)
    #     self.pack()


class MyButton:
    def __init__(self, my_frame, associated_box, text=None, coord=None, parent=None):
        self.images = {'bomb_img': tk.PhotoImage(file="img/mine.png"),
                       'flag_img': tk.PhotoImage(file="img/flag.png")}
        self.button = tk.Button(my_frame, bg='grey')
        self.coord = coord
        self.parent = parent
        self.box = associated_box
        self.button.bind('<Button-3>', self.right)
        self.button.bind('<Button-1>', self.left)

    def left(self, event=None):  # events when the player left clicks on the button
        if not self.box.has_been_discovered():
            # the player has not left clicked on this box before
            if not self.box.has_flag():
                # the player has not secured this box with a flag
                self.button['bg'] = 'white'  # change the box colour to white
                self.box.discover()  # set the box as discovered
                self.parent.game_grid.decrease_number_of_undiscovered_boxes()
                # update the bomb number displayed in the square below the game grid
                self.parent.info_frame.update_info(remaining_boxes=self.parent.game_grid.get_nbr_of_remaining_boxes())
                if self.box.is_mined():  # the player has revealed a bomb and therefore lost
                    self.button['image'] = self.images['bomb_img']  # display a bomb image
                    if not self.parent.is_game_ended:
                        self.parent.defeat()  # set the game as lost
                elif self.box.surroundingMines:  # the player revealed a box surrounded by at least one bomb
                    self.button['text'] = self.box.surroundingMines
                    self.set_number_font()  # Set the number font and colour according to its value
                else:  # the player revealed a box surrounded by no bomb
                    self.show_surrounding_boxes()  # reveal all the surrounding bombs
                    # if one or more box has no surrounding bombs, this box will be recursively discovered by
                    # a virtual left click
                if self.parent.game_grid.is_grid_secured() and not self.parent.is_game_ended:
                    self.parent.victory()  # set the game as won
        elif self.box.surroundingMines <= self.parent.game_grid.get_nbr_of_surrounding_flags(self.coord[0],
                                                                                             self.coord[1]):
            # display all the non-secured surrounding boxes if the player has put as many flags as necessary
            self.show_surrounding_boxes()

    def right(self, event=None):  # events when the player right clicks on the button
        if not self.box.has_been_discovered():
            if not self.box.has_flag():
                # The player puts a flag on the box : a flag image is displayed, the box is blocked and the flag number
                # is increased
                self.box.plant_a_flag_like_the_red_one_on_top_of_the_reichstag()
                self.button['image'] = self.images['flag_img']
                self.parent.game_grid.flags += 1
            else:
                # The player removes the flag : the flag image is removed, the box reactivated, and flag number -=1
                self.box.remove_this_nazi_flag_and_retake_stalingrad()
                self.button.config(image="")
                self.parent.game_grid.flags -= 1
            self.parent.info_frame.update_info(flags=self.parent.game_grid.flags)

    def show_surrounding_boxes(self):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= self.coord[0] + i < LINE and 0 <= self.coord[1] + j < COLUMN:
                    if not self.parent.button_list[self.coord[0] + i][self.coord[1] + j].box.has_been_discovered():
                        self.parent.button_list[self.coord[0] + i][self.coord[1] + j].left()

    def set_number_font(self):
        _number = self.box.surroundingMines
        self.button['font'] = font.Font(weight='bold')
        if _number:
            # a box cannot be surrounded by more than 8 bombs, so there is no risk of being out of range
            _colours = ('blue', 'green', 'red', 'purple', 'brown', '#006d00', 'black', 'grey')
            self.button['fg'] = _colours[_number - 1]


class InfoFrame:  # widget containing the written information on the current game
    def __init__(self, master=None):
        self.label = tk.LabelFrame(master, text='Game info')
        self.label.pack(fill="both")
        self.remaining_boxes = tk.Label(self.label,
                                        text=f'Remaining boxes : {LINE * COLUMN - (LINE * COLUMN) // BOMB_PROPORTION}')
        self.remaining_boxes.grid(row=0, column=0, sticky='w', padx=20)
        self.flags = tk.Label(self.label, text="Flags : 0")
        self.flags.grid(row=0, column=1, sticky='ew', padx=20)
        tk.Label(self.label,
                 text=f'Bombs : {(LINE * COLUMN) // BOMB_PROPORTION}').grid(row=1, column=0, columnspan=2, sticky='')
        self.label.columnconfigure(1, weight=1)
        self.label.rowconfigure(1, weight=1)

    def update_info(self, bombs=None, remaining_boxes=-1, flags=-1):
        if remaining_boxes >= 0:
            self.remaining_boxes['text'] = f'Remaining boxes : {remaining_boxes}'
        if flags >= 0:
            self.flags['text'] = f'Flags : {flags}'


# class Menu:
#     def __init__(self, master):
#         self.parent = master
#         bar = tk.Menu(master)
#         submenu = tk.Menu(bar, tearoff=0)
#         # submenu.add_command(label="Créer", command=self.reload_game)
#         submenu.add_command(label="Editer", command=self.do_something)
#         submenu.add_command(label="Quitter", command=self.do_something)
#         bar.add_cascade(label="Fichier", menu=submenu)
#         self.__new_settings = {"LINE": LINE, "COLUMN": COLUMN, "BOMB_PROPORTION": BOMB_PROPORTION}
#
#         master.config(menu=bar)
#
#     @staticmethod
#     def do_something(event=None):
#         print("hello")

    # def reload_game(self, event=None):
    #     for widget in self.parent.winfo_children():
    #         if widget.winfo_name() != '!menu':
    #             widget.destroy()
    #     super().__init__()
# end
