from time import sleep
from main import *
import tkinter as tk
import tkinter.font as font


class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.game_grid = Grid()
        self.master = master
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
                button_content = self.game_grid.get_box_state(i, j)
                if button_content == 'X':
                    new_button = MyButton(my_frame, self.game_grid.grid[i][j], image='bomb_img', coord=(i, j),
                                          parent=self)
                elif button_content == 'U':
                    new_button = MyButton(my_frame, self.game_grid.grid[i][j], bg='grey', coord=(i, j), parent=self)
                elif button_content == '@':
                    new_button = MyButton(my_frame, self.game_grid.grid[i][j], image='flag_img', coord=(i, j),
                                          parent=self)
                else:
                    if self.game_grid.grid[i][j].surroundingMines:
                        new_button = MyButton(my_frame, self.game_grid.grid[i][j], text=button_content, coord=(i, j),
                                              parent=self)
                    else:
                        # if the box has no surrounding bomb, the grid and the position of the box must be sent
                        # to the new object for internal methods
                        new_button = MyButton(my_frame, self.game_grid.grid[i][j], text=button_content,
                                              coord=(i, j), parent=self)
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
    def __init__(self, my_frame, associated_box, text=None, image=None, bg=None, coord=None, parent=None):
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
                self.parent.game_grid.decrease_number_of_undiscovered_boxes()
                self.parent.info_frame.update_info(remaining_boxes=self.parent.game_grid.get_nbr_of_remaining_boxes())
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
                if self.parent.game_grid.is_grid_secured() and not self.parent.is_game_ended:
                    self.parent.victory()

        else:
            if self.box.surroundingMines == self.parent.game_grid.get_nbr_of_surrounding_flags(self.coord[0],
                                                                                               self.coord[1]):
                self.show_surrounding_boxes()

    def right(self, event=None):
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


class InfoFrame:
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

# end
