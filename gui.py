from main import *
import tkinter as tk
import tkinter.font as font


class App(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.menu_bar = Menu(master)

        self.game_grid = Grid()
        self.master.title('Minesweeper')
        self.master.geometry("800x600")
        self.button_list = [[] for x in range(LINE)]
        self.is_game_ended = False
        self.display_grid()
        self.info_frame = InfoFrame(master=self)
        self.pack()

    def display_grid(self):
        box_width = 35
        my_frame = tk.Frame(self, width=COLUMN * box_width, height=LINE * box_width)
        my_frame.pack(pady=(50, 0))
        for i in range(LINE):
            for j in range(COLUMN):
                new_button = MyButton(my_frame, self.game_grid.grid[i][j], coord=(i, j), parent=self)
                new_button.button.place(x=j * box_width, y=i * box_width, width=box_width, height=box_width)
                self.button_list[i].append(new_button)

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
            if not self.box.has_flag():
                self.button['bg'] = 'white'
                self.box.discover()
                self.parent.game_grid.decrease_number_of_undiscovered_boxes()
                self.parent.info_frame.update_info(remaining_boxes=self.parent.game_grid.get_nbr_of_remaining_boxes())
                if self.box.is_mined():  # the player has revealed a bomb and therefore lost
                    self.button['image'] = self.images['bomb_img']
                    if not self.parent.is_game_ended:
                        self.parent.defeat()
                elif self.box.surroundingMines:  # the player revealed a box surrounded by at least one bomb
                    self.button['text'] = self.box.surroundingMines
                    self.set_number_font()  # Set the number font and colour according to its value
                else:  # the player revealed a box surrounded by no bomb
                    self.show_surrounding_boxes()
                if self.parent.game_grid.is_grid_secured() and not self.parent.is_game_ended:
                    self.parent.victory()
        elif self.box.surroundingMines <= self.parent.game_grid.get_nbr_of_surrounding_flags(self.coord[0],
                                                                                             self.coord[1]):
            # display all the non-secured surrounding boxes if the player has put as many flags as necessary
            self.show_surrounding_boxes()

    def right(self, event=None):  # events when the player right clicks on the button
        if not self.box.has_been_discovered():
            if not self.box.has_flag():
                self.box.plant_a_flag_like_the_red_one_on_top_of_the_reichstag()
                self.button['image'] = self.images['flag_img']
                self.parent.game_grid.flags += 1
            else:
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
            _number -= 1
            _colours = ('blue', 'green', 'red', 'purple', 'brown', '#006d00')
            self.button['fg'] = _colours[_number]


class InfoFrame:  # widget containing the written information on the current game
    def __init__(self, master=None):
        self.label = tk.LabelFrame(master, text='Game info')
        self.label.pack(fill="both")
        self.remaining_boxes = tk.Label(self.label,
                                        text=f'Remaining boxes : {LINE*COLUMN - (LINE * COLUMN) // BOMB_PROPORTION}')
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


class Menu:
    def __init__(self, master):
        bar = tk.Menu(master)
        submenu = tk.Menu(bar, tearoff=0)
        # submenu.add_command(label="Créer", command=master.reload_game)
        submenu.add_command(label="Editer", command=self.do_something)
        submenu.add_command(label="Quitter", command=self.do_something)
        bar.add_cascade(label="Fichier", menu=submenu)

        master.config(menu=bar)

    def do_something(self, event=None):
        print("hello")


# end
