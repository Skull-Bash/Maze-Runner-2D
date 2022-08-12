import tkinter as tk
from tkinter import messagebox, filedialog
from typing import Callable
from PIL import Image, ImageTk
from a2_solution import *
from a3_support import *
from constants import GAME_FILE, TASK
import time, os


# Write your classes here

class LevelView(AbstractGrid):
    """ Manages all the view elements for every level """

    def draw(self, tiles: list[list['Tile']], items: dict[tuple[int, int], 'Item'],
             player_pos: tuple[int, int]) -> None:
        """ Clears and redraws the entire level eg: Maze & Entities

        Parameters:
            tiles: A list of lists of Tiles denoting the whole Maze.
            items: A dictionary of Items with their position as keys.
            player_pos: A tuple denoting the co-ordinates of the player.
        """
        self.clear()
        self._draw_tiles(tiles)
        self._place_items(items)
        self._place_player(player_pos)

    def _place_player(self, player_pos: tuple[int, int]) -> None:
        """ Assigns the player to current position in the Maze.

        Parameters:
            player_pos: A tuple denoting the co-ordinates of the player.
        """
        self.create_oval(self.get_bbox(player_pos), fill=ENTITY_COLOURS[PLAYER])
        self.create_text(self.get_midpoint(player_pos), font=TEXT_FONT, text=PLAYER)

    def _place_items(self, items: dict[tuple[int, int], 'Item']) -> None:
        """ Assigns all the available items to their respective position in the Maze.

        Parameters:
            items: A dictionary of Items with their position as keys.
        """
        for item in items:
            self.create_oval(self.get_bbox(items[item].get_position()), fill=ENTITY_COLOURS[items[item].get_id()])
            if items[item].get_id() == COIN:
                self.create_text(self.get_midpoint(items[item].get_position()), font=TEXT_FONT, text=COIN)
            elif items[item].get_id() == POTION:
                self.create_text(self.get_midpoint(items[item].get_position()), font=TEXT_FONT, text=POTION)
            elif items[item].get_id() == HONEY:
                self.create_text(self.get_midpoint(items[item].get_position()), font=TEXT_FONT, text=HONEY)
            elif items[item].get_id() == APPLE:
                self.create_text(self.get_midpoint(items[item].get_position()), font=TEXT_FONT, text=APPLE)
            elif items[item].get_id() == WATER:
                self.create_text(self.get_midpoint(items[item].get_position()), font=TEXT_FONT, text=WATER)

    def _draw_tiles(self, tiles: list[list['Tile']]) -> None:
        """ Assigns all the tiles to their respective position in the Maze.

        Parameters:
            tiles: A list of lists of Tiles denoting the whole Maze.
        """
        y = -1
        for y_tile in tiles:
            x = 0
            y += 1
            for x_tile in y_tile:
                if x_tile.get_id() == LAVA:
                    self.create_rectangle(self.get_bbox((y, x)), fill=TILE_COLOURS[LAVA])
                elif x_tile.get_id() == WALL:
                    self.create_rectangle(self.get_bbox((y, x)), fill=TILE_COLOURS[WALL])
                elif x_tile.get_id() == DOOR:
                    self.create_rectangle(self.get_bbox((y, x)), fill=TILE_COLOURS[DOOR])
                elif x_tile.get_id() == EMPTY:
                    self.create_rectangle(self.get_bbox((y, x)), fill=TILE_COLOURS[EMPTY])
                x += 1


class ImageLevelView(LevelView):
    """ A child class of LevelView, which also manager view object of each level with Images """

    def __init__(self, master: Union[tk.Tk, tk.Frame], dimensions: tuple[int, int], size: tuple[int, int],
                 **kwargs) -> None:
        """ Sets up a new LevelView with images in the master frame with the given size.

        Parameters:
            master: The root tkinter frame
            dimensions: The number of rows & columns of the maze
            size: Max height & width of the maze
        """
        super().__init__(master, dimensions, size, **kwargs)
        self.update_images()

    def update_images(self) -> None:
        """ Reinitialize all the images & resizes according to the given dimension """
        self._lavaImage = ImageTk.PhotoImage(Image.open("images/" + TILE_IMAGES[LAVA]).resize(self.get_cell_size()))
        self._wallImage = ImageTk.PhotoImage(Image.open("images/" + TILE_IMAGES[WALL]).resize(self.get_cell_size()))
        self._doorImage = ImageTk.PhotoImage(Image.open("images/" + TILE_IMAGES[DOOR]).resize(self.get_cell_size()))
        self._emptyImage = ImageTk.PhotoImage(Image.open("images/" + TILE_IMAGES[EMPTY]).resize(self.get_cell_size()))
        self._coinImage = ImageTk.PhotoImage(Image.open("images/" + ENTITY_IMAGES[COIN]).resize(self.get_cell_size()))
        self._appleImage = ImageTk.PhotoImage(Image.open("images/" + ENTITY_IMAGES[APPLE]).resize(self.get_cell_size()))
        self._honeyImage = ImageTk.PhotoImage(Image.open("images/" + ENTITY_IMAGES[HONEY]).resize(self.get_cell_size()))
        self._waterImage = ImageTk.PhotoImage(Image.open("images/" + ENTITY_IMAGES[WATER]).resize(self.get_cell_size()))
        self._potionImage = ImageTk.PhotoImage(
            Image.open("images/" + ENTITY_IMAGES[POTION]).resize(self.get_cell_size()))
        self._playerImage = ImageTk.PhotoImage(
            Image.open("images/" + ENTITY_IMAGES[PLAYER]).resize(self.get_cell_size()))

    def _draw_tiles(self, tiles: list[list['Tile']]) -> None:
        """ Assigns all the tiles at their respective position with images in the Maze.

        Parameters:
            tiles: A list of lists of Tiles denoting the whole Maze.
        """
        y = -1
        for y_tile in tiles:
            x = 0
            y += 1
            for x_tile in y_tile:
                if x_tile.get_id() == LAVA:
                    self.create_image(self.get_midpoint((y, x))[0], self.get_midpoint((y, x))[1], anchor="center",
                                      image=self._lavaImage)
                elif x_tile.get_id() == WALL:
                    self.create_image(self.get_midpoint((y, x))[0], self.get_midpoint((y, x))[1], anchor="center",
                                      image=self._wallImage)
                elif x_tile.get_id() == DOOR:
                    self.create_image(self.get_midpoint((y, x))[0], self.get_midpoint((y, x))[1], anchor="center",
                                      image=self._doorImage)
                elif x_tile.get_id() == EMPTY:
                    self.create_image(self.get_midpoint((y, x))[0], self.get_midpoint((y, x))[1], anchor="center",
                                      image=self._emptyImage)
                x += 1

    def _place_items(self, items: dict[tuple[int, int], 'Item']) -> None:
        """ Assigns all the available items at their respective position with images in the Maze.

        Parameters:
            items: A dictionary of Items with their position as keys.
        """
        for item in items:
            if items[item].get_id() == COIN:
                self.create_image(self.get_midpoint(items[item].get_position()), anchor="center", image=self._coinImage)
            elif items[item].get_id() == POTION:
                self.create_image(self.get_midpoint(items[item].get_position()), anchor="center",
                                  image=self._potionImage)
            elif items[item].get_id() == HONEY:
                self.create_image(self.get_midpoint(items[item].get_position()), anchor="center",
                                  image=self._honeyImage)
            elif items[item].get_id() == APPLE:
                self.create_image(self.get_midpoint(items[item].get_position()), anchor="center",
                                  image=self._appleImage)
            elif items[item].get_id() == WATER:
                self.create_image(self.get_midpoint(items[item].get_position()), anchor="center",
                                  image=self._waterImage)

    def _place_player(self, player_pos: tuple[int, int]) -> None:
        """ Assigns the player at the given position with image.

         Parameters:
            player_pos: A tuple denoting the players current position
         """
        self.create_image(self.get_midpoint(player_pos), anchor="center", image=self._playerImage)


class StatsView(AbstractGrid):
    """ This view class is to show the current stats of the player. """

    def __init__(self, master: Union[tk.Tk, tk.Frame], width: int) -> None:
        """  Sets up a new StatsView in the master frame with the given width.

         Parameters:
            master: The root master frame.
            width: max width of the stats frame.
        """
        super().__init__(master, (2, 4), (width, STATS_HEIGHT), bg=THEME_COLOUR)
        self.create_text(self.get_midpoint((0, 0)), font=TEXT_FONT, text="HP")
        self.create_text(self.get_midpoint((0, 1)), font=TEXT_FONT, text="Hunger")
        self.create_text(self.get_midpoint((0, 2)), font=TEXT_FONT, text="Thirst")
        self.create_text(self.get_midpoint((0, 3)), font=TEXT_FONT, text="Coins")
        self._values = []

    def draw_stats(self, stats: tuple[int, int, int]) -> None:
        """ Draws the player's stats (hp, hunger, thirst).

        Parameters:
            stats: A tuple consisting of the player stats
        """
        self._values.append(self.create_text(self.get_midpoint((1, 0)), font=TEXT_FONT, text=str(stats[0])))
        self._values.append(self.create_text(self.get_midpoint((1, 1)), font=TEXT_FONT, text=str(stats[1])))
        self._values.append(self.create_text(self.get_midpoint((1, 2)), font=TEXT_FONT, text=str(stats[2])))

    def draw_coins(self, coin_count: int) -> None:
        """ Draws the number of coins.

        Parameters:
            coin_count: Denotes number of coins the player has.
        """
        self._values.append(self.create_text(self.get_midpoint((1, 3)), font=TEXT_FONT, text=str(coin_count)))

    def clear(self) -> None:
        """ Clears all the player stat values """
        for value in self._values:
            self.itemconfig(value, text="")


class InventoryView(tk.Frame):
    """ InventoryView is a view class which inherits from tk.Frame, and displays the items the player
        has in their inventory """

    _callback = None

    def __init__(self, master: Union[tk.Tk, tk.Frame], **kw) -> None:
        """ Creates a new Inventory view(Frame) within master.
        Parameters:
            master: the root master frame.
        """
        super().__init__(master, width=INVENTORY_WIDTH, **kw)
        tk.Label(self, text="Inventory", font=HEADING_FONT + ("bold",)).pack(fill=tk.X)
        self._labels = {}

    def clear(self) -> None:
        """ Removes all the items from inventory """
        # for label in self._labels.values():
        #     label.pack_forget()

    def set_click_callback(self, callback: Callable[[str], None]) -> None:
        """ Assigns the function to be called when a label is clicked.

        Parameters:
            callback: A callback function which takes item name (str) as parameter
        """
        self._callback = callback

    def _draw_item(self, name: str, num: int, colour: str) -> None:
        """ Draws and binds a tk.Label with mouse click in the InventoryView frame.

        Parameters:
            name: Name of the item
            num: Number of the item available in players inventory
            colour: Background colour of the label for the given item
        """
        if name in self._labels:
            self._labels[name].config(text=name + ": " + str(num))
        else:
            self._labels[name] = tk.Label(self, text=name + ": " + str(num), bg=colour, font=TEXT_FONT,
                                          relief=tk.RAISED,
                                          borderwidth=1)
        self._labels[name].pack(side=tk.TOP, fill=tk.X)
        if not self._callback:
            return
        self._labels[name].bind("<Button-1>", lambda event: self._callback(name))

    def draw_inventory(self, inventory: 'Inventory') -> None:
        """ Draws any non-coin item from the players inventory to InventoryView

        Parameters:
            inventory: The instance of the players inventory
        """
        for items in inventory.get_items():
            if items != "Coin" and len(inventory.get_items()[items]) > 0:
                self._draw_item(items, len(inventory.get_items()[items]),
                                ENTITY_COLOURS[inventory.get_items()[items][0].get_id()])


class ControlsFrame(tk.Frame):
    """ A class which inherits from tk.Frame, and displays 2/3 buttons(Depending on Task) and a timer """

    _callback = None
    _reset_callback = None
    _widgets = []

    def __init__(self, master: Union[tk.Tk, tk.Frame], **kw) -> None:
        """ Creates a new ControlsFrame in master.

        Parameters:
            master: the root frame
        """
        super().__init__(master, **kw)
        self._start = 0.0
        self._elapsed_time = 0.0
        self._running = 0
        self.time_str = tk.StringVar()
        global ITEM_PRICE
        self._price = ITEM_PRICE
        self._makeWidgets()

    def set_callback(self, callback: Callable[[str], None], reset_callback: Callable[[], None]) -> None:
        """ Assigns the function to be called when shop Button is clicked.

        Parameters:
            callback: A callback function which takes item id (str) as parameter
            reset_callback: A callback function which resets the game
        """
        self._callback = callback
        self._reset_callback = reset_callback

    def _makeWidgets(self) -> None:
        """ Initializes all the widgets in the ControlsFrame eg:ShopButton, RestartButton, NewGame Button, Timer """
        pad = 50
        if TASK > 2:
            pad = 40
            tk.Button(self, text="Shop", font=TEXT_FONT, relief=tk.GROOVE, bg='white',
                      command=self.open_shop).pack(pady=10, padx=pad, side=tk.LEFT, fill=tk.X, expand=True)

        self._widgets.append(
            tk.Button(self, text="Restart game", font=TEXT_FONT, command=self._restart, relief=tk.GROOVE,
                      bg='white'))
        self._widgets[-1].pack(pady=10, padx=pad, side=tk.LEFT, fill=tk.X, expand=True)
        self._widgets.append(tk.Button(self, text="New game", font=TEXT_FONT, command=self._new_game, relief=tk.GROOVE,
                                       bg='white'))
        self._widgets[-1].pack(pady=10, padx=pad, side=tk.LEFT, fill=tk.X, expand=True)

        timerFrame = tk.Frame(self)
        timerFrame.pack(pady=10, padx=pad, side=tk.LEFT, fill=tk.X, expand=True)
        self._widgets.append(tk.Label(timerFrame, text="Timer", font=TEXT_FONT))
        self._widgets[-1].pack()
        self.timer = tk.Label(timerFrame, textvariable=self.time_str, font=TEXT_FONT)
        self.timer.pack()
        self._setTime(self._elapsed_time)

    def open_shop(self) -> None:
        """ Creates a new tk.TopLevel frame and generates the shop interface """

        self._shop = tk.Toplevel(self.master)
        self._shop.title('Shop')
        self._appleImage = ImageTk.PhotoImage(Image.open("images/" + ENTITY_IMAGES[APPLE]).resize((200, 200)))
        self._waterImage = ImageTk.PhotoImage(Image.open("images/" + ENTITY_IMAGES[WATER]).resize((200, 200)))
        self._honeyImage = ImageTk.PhotoImage(Image.open("images/" + ENTITY_IMAGES[HONEY]).resize((200, 200)))
        self._potionImage = ImageTk.PhotoImage(Image.open("images/" + ENTITY_IMAGES[POTION]).resize((200, 200)))
        self._candyImage = ImageTk.PhotoImage(Image.open("images/" + ENTITY_IMAGES[CANDY]).resize((200, 200)))

        tk.Label(self._shop, text="Shop", font=BANNER_FONT + ("bold",), bg=THEME_COLOUR).pack(fill='x')
        frame = tk.Frame(self._shop)
        frame.pack()
        tk.Button(frame, command=lambda: self._callback(APPLE), image=self._appleImage,
                  text="$" + str(self._price[APPLE]),
                  font=TEXT_FONT, compound="top", relief=tk.GROOVE).grid(row=0, column=0)
        tk.Button(frame, command=lambda: self._callback(WATER), image=self._waterImage,
                  text="$" + str(self._price[WATER]), font=TEXT_FONT, compound="top",
                  relief=tk.GROOVE).grid(row=0, column=1)
        tk.Button(frame, command=lambda: self._callback(HONEY), image=self._honeyImage,
                  text="$" + str(self._price[HONEY]), font=TEXT_FONT, compound="top",
                  relief=tk.GROOVE).grid(row=0, column=2)

        frame = tk.Frame(self._shop)
        frame.pack()

        tk.Button(frame, command=lambda: self._callback(POTION), image=self._potionImage,
                  text="$" + str(self._price[POTION]), font=TEXT_FONT, compound="top",
                  relief=tk.GROOVE).grid(row=1, column=0, padx=50)
        tk.Button(frame, command=lambda: self._callback(CANDY), image=self._candyImage,
                  text="$" + str(self._price[CANDY]), font=TEXT_FONT, compound="top",
                  relief=tk.GROOVE).grid(row=1, column=1, padx=50)

        tk.Button(self._shop, command=self._shop.destroy, text="Done", bg='white', font=TEXT_FONT,
                  relief=tk.GROOVE).pack()

        self._shop.mainloop()

    def _update(self) -> None:
        """ Update the label with elapsed time. """
        self._elapsed_time = time.time() - self._start
        self._setTime(self._elapsed_time)
        self._timer = self.after(50, self._update)

    def _setTime(self, elap: float) -> None:
        """ Set the time string to Minutes:Seconds:Hundreths

        Parameters:
            elap: Denotes the elapsed time
        """
        minutes = int(elap / 60)
        seconds = int(elap - minutes * 60.0)
        self.time_str.set('%01dm %01ds' % (minutes, seconds))

    def start_timer(self) -> None:
        """ Start the stopwatch, ignore if running. """
        if not self._running:
            self._start = time.time() - self._elapsed_time
            self._update()
            self._running = 1

    def stop_timer(self) -> None:
        """ Stop the stopwatch, ignore if stopped. """
        if self._running:
            self.after_cancel(self._timer)
            self._elapsed_time = time.time() - self._start
            self._setTime(self._elapsed_time)
            self._running = 0

    def Reset(self) -> None:
        """ Reset the stopwatch. """
        self._start = time.time()
        self._elapsed_time = 0.0
        self._setTime(self._elapsed_time)

    def _restart(self) -> None:
        """ Restarts the whole game a runs the current game from start """
        self.Reset()
        self._reset_callback()

    def _new_game(self) -> None:
        """ Creates a new tk.TopLevel frame and asks the user for a valid game file """
        self._top = tk.Toplevel(self.master)
        tk.Label(self._top, text="Choose a Valid Game File!", font=TEXT_FONT).pack(pady=10)
        self._dir = tk.Label(self._top, font=TEXT_FONT)
        self._dir.pack(pady=10)
        tk.Button(self._top, text="Browse", font=TEXT_FONT, command=self._open_file).pack(pady=10)
        tk.Button(self._top, text="Play", font=TEXT_FONT, command=self._restart).pack(pady=10)
        self._top.mainloop()

    def _open_file(self) -> None:
        """ Opens up a file explorer window & takes in the game file, also validates that file """
        global LOCAL_GAME_FILE
        file = filedialog.askopenfile(mode='r', filetypes=[('Text Files', '*.txt')])
        if file and is_game_valid(file.name):
            self._dir.config(text=file.name)
            LOCAL_GAME_FILE = file.name
        else:
            tk.messagebox.showwarning("Alert", "Enter Valid File")


class Candy(Food):
    """ Candy restores the player's hunger to 0 & reduce health by 2. """

    _id = CANDY

    def apply(self, player: 'Player') -> None:
        """ restores the player's hunger to 0 & reduce health by 2 """
        player.change_hunger(-10)
        player.change_health(-2)


class GraphicalInterface(UserInterface):
    """ GraphicalInterface inherits from UserInterface and arranges all the views together """

    def __init__(self, master: tk.Tk) -> None:
        """ Creates a new GraphicalInterface in master frame. Assigns a title to the master frame.

        Parameters:
            master: the root frame.
        """
        self._master = master
        self._master.title("MazeRunner")
        tk.Label(self._master, text="MazeRunner", font=BANNER_FONT + ("bold",), bg=THEME_COLOUR).pack(side=tk.TOP,
                                                                                                      fill=tk.X)

    def create_interface(self, dimensions: tuple[int, int]) -> None:
        """ Creates the components (level view, inventory view, and stats view) in the master frame
            for this interface.

        Parameters:
            dimensions: A tuple denoting the number of rows & columns of the maze.
        """
        self.middleFrame = tk.Frame(self._master)
        self.middleFrame.pack(expand=True, fill=tk.X)

        # Arranging LevelView According to TASK
        if TASK == 1:
            self.level_view = LevelView(self.middleFrame, dimensions, (MAZE_WIDTH, MAZE_HEIGHT))
        elif TASK > 1:
            self.level_view = ImageLevelView(self.middleFrame, dimensions, (MAZE_WIDTH, MAZE_HEIGHT))
        self.level_view.pack(side=tk.LEFT)

        # Initializing InventoryView
        self.inventory_view = InventoryView(self.middleFrame)
        self.inventory_view.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # Initializing StatsView
        self.stats_view = StatsView(self._master, MAZE_WIDTH + INVENTORY_WIDTH)
        self.stats_view.pack()

        if TASK > 1:
            # Setting up Control Frame in TASK is > 1
            self.controlFrame = ControlsFrame(self._master)
            self.controlFrame.pack(side=tk.BOTTOM)

            # Setting up Menu Bar
            self.menu = MenuBar(self._master, self.controlFrame)

    def clear_all(self) -> None:
        """ Clears each component views """
        self.inventory_view.clear()
        self.level_view.clear()
        self.stats_view.clear()

    def set_maze_dimensions(self, dimensions: tuple[int, int]) -> None:
        """ Updates the dimensions of the maze in the level. """
        self.level_view.set_dimensions(dimensions)

    def bind_keypress(self, command: Callable[[tk.Event], None]) -> None:
        """ Binds the given command to the general keypress event.

        Parameters:
            command: A callback function that takes tk.Event as a parameter, and controls the players moves
            when ['w','a','s','d'] is clicked.
         """
        self._master.bind("<KeyPress>", lambda event: command(event))

    def set_inventory_callback(self, command: Callable[[str], None]) -> None:
        """  Sets the function to be called when an item is clicked in the inventory view

        Parameters:
            command: A callback function that takes item name (str) as a parameter, and uses that item
            when mouse clicks.
        """
        self.inventory_view.set_click_callback(command)

    def draw_inventory(self, inventory: 'Inventory') -> None:
        """ Draws any non-coin inventory items with their quantities and binds the callback for each

        Parameters:
            inventory: The inventory instance of the player
         """
        self._draw_inventory(inventory)

    def draw(self, maze: 'Maze', items: dict[tuple[int, int], Item], player_position: tuple[int, int],
             inventory: 'Inventory', player_stats: tuple[int, int, int]) -> None:
        """ Draws the current game state.

        Parameters:
            maze: The current Maze instance
            items: The items on the maze
            player_position: The position of the player
            inventory: The player's current inventory
            player_stats: The (HP, hunger, thirst) of the player
        """
        self.clear_all()

        self._draw_level(maze, items, player_position)

        self._draw_inventory(inventory)

        self._draw_player_stats(player_stats)

    def _draw_inventory(self, inventory: 'Inventory') -> None:
        """ Draws the inventory information. Also Updates Coins in player stats.

        Parameters:
            inventory: The player's current inventory
        """
        self.inventory_view.draw_inventory(inventory)
        if "Coin" in inventory.get_items():
            self.stats_view.draw_coins(len(inventory.get_items()["Coin"]))
        else:
            self.stats_view.draw_coins(0)

    def _draw_player_stats(self, player_stats: tuple[int, int, int]) -> None:
        """ Draws the players stats.

        Parameters:
            player_stats: The player's current (HP, hunger, thirst)
        """
        self.stats_view.draw_stats(player_stats)

    def _draw_level(self, maze: 'Maze', items: dict[tuple[int, int], Item], player_position: tuple[int, int]) -> None:
        """ Draws the maze and all its items.

        Parameters:
            maze: The current maze for the level
            items: Maps locations to the items currently at those locations
            player_position: The current position of the player
        """
        self.level_view.set_dimensions(maze.get_dimensions())
        self.level_view.draw(maze.get_tiles(), items, player_position)


class MenuBar:
    """ A class to setup menu bar in the master frame """

    _model = None
    _restart_callback = None
    _load_game_callback = None

    def __init__(self, master: tk.Tk, controlFrame: 'ControlsFrame') -> None:
        """  Initializes a menu bar in master frame.

        Parameters:
            master: the root frame.
            controlFrame: The instance of ControlsFrame of the game
        """
        self._master = master
        menu_bar = tk.Menu(self._master)
        self._control_frame = controlFrame
        file = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label='File', menu=file)
        file.add_command(label='Save game', command=self.save_current_game)
        file.add_command(label='Load game', command=self.load_game)
        file.add_command(label='Restart game', command=self.restart)
        file.add_separator()
        file.add_command(label='Quit', command=self._master.destroy)

        self._master.config(menu=menu_bar)

    def set_model_callbacks(self, model: 'Model', reset_callback: Callable[[], None],
                            load_callback: Callable[[], None]) -> None:
        """ Assigns the model instance and callbacks for the game

        Parameters:
             model: instance of Model class of current game
             reset_callback: A callback to reset game
             load_callback: A callback to load new game
        """
        self._model = model
        self._restart_callback = reset_callback
        self._load_game_callback = load_callback

    def load_game(self) -> None:
        """ Loads up the game files saved in the directory chosen by user. It will use two text files,
            naming maze.txt & stats.txt to load all the necessary information like player stats,
            player inventory, maze status in
        """
        global CUSTOM_GAME_FILE
        global CUSTOM_GAME_STATS
        global LOCAL_GAME_FILE

        selected_dir = filedialog.askdirectory()
        maze = selected_dir + "/maze.txt"
        if not os.path.isfile(maze):
            tk.messagebox.showwarning("Alert", "Select Valid Game Directory!")
            return
        LOCAL_GAME_FILE = maze

        stat = selected_dir + "/stats.txt"
        if not os.path.isfile(stat):
            tk.messagebox.showwarning("Alert", "Select Valid Game Directory!")
            return
        CUSTOM_GAME_FILE = True
        CUSTOM_GAME_STATS = stat

        self._load_game_callback()

    def restart(self) -> None:
        """ Restarts the current Game """
        self._control_frame.Reset()
        self._restart_callback()

    def save_current_game(self) -> None:
        """ Saves the current instance of the game in the directory chosen by the user, it will save all the
            necessary information like player stats, player inventory, maze status in two text files,
            naming maze.txt & stats.txt
        """
        selected_dir = filedialog.askdirectory()
        levels = self._model._levels
        curr_level = levels.index(self._model.get_level())
        lvl = 1
        maze = selected_dir + "/maze.txt"
        f = open(maze, "w")
        for i in range(curr_level, len(levels)):
            f.write("Maze " + str(lvl) + " - " + str(levels[i].get_dimensions()[0]) + " " + str(
                levels[i].get_dimensions()[1]) + "\n")
            if curr_level == i:
                f.write(get_maze_in_text(levels[i].get_maze(), levels[i].get_items(),
                                         self._model.get_player().get_position()))
            else:
                f.write(get_maze_in_text(levels[i].get_maze(), levels[i].get_items(), levels[i].get_player_start()))
            lvl += 1
        f.close()

        # storing inventory & stats
        stats = selected_dir + "/stats.txt"
        f = open(stats, "w")
        f.write("Stats : " + str(self._model.get_player_stats()[0]) + "-" + str(
            self._model.get_player_stats()[1]) + "-" + str(self._model.get_player_stats()[2]) + " \n")

        f.write("Inventory\n")
        for i in self._model.get_player_inventory().get_items().values():
            for j in i:
                f.write(j.get_name() + "-" + str(j.get_position()[0]) + "-" + str(j.get_position()[1]) + " \n")
        f.close()


class GraphicalMazeRunner(MazeRunner):
    """ It operates the game to enable use of GraphicalInterface instead of a TextInterface, """

    def __init__(self, game_file: str, root: tk.Tk) -> None:
        """ Creates a new Graphical-MazeRunner game, with the view inside the given root widget.

        Parameters:
            game_file: Game file to load the game.
            root: the root tk.Tk frame.
        """
        self.root = root
        self.interface = GraphicalInterface(root)
        self._model = Model(game_file)
        super(GraphicalMazeRunner, self).__init__(game_file, self.interface)

    def _update_player_stats(self) -> None:
        """ If the game is loaded from directory or where the game was saved, then the player status will be updated """
        f = open(CUSTOM_GAME_STATS, "r")
        inv = False
        for line in f:
            line.split()
            if inv:
                item = line.split('-')
                if item[0] == "Coin":
                    self._model.get_player_inventory().add_item(Coin((int(item[1]), int(item[2]))))
                elif item[0] == "Honey":
                    self._model.get_player_inventory().add_item(Honey((int(item[1]), int(item[2]))))
                elif item[0] == "Potion":
                    self._model.get_player_inventory().add_item(Potion((int(item[1]), int(item[2]))))
                elif item[0] == "Apple":
                    self._model.get_player_inventory().add_item(Apple((int(item[1]), int(item[2]))))
                elif item[0] == "Water":
                    self._model.get_player_inventory().add_item(Water((int(item[1]), int(item[2]))))
                elif item[0] == "Candy":
                    self._model.get_player_inventory().add_item(Candy((int(item[1]), int(item[2]))))
                else:
                    break

            if line.startswith('Stats'):
                stats = line[8:].split('-')
                stats = [int(stat) for stat in stats]
                self._model.get_player().change_health(-(100 - stats[0]))
                self._model.get_player().change_hunger(stats[1])
                self._model.get_player().change_thirst(stats[2])
            elif line.startswith('Inventory'):
                inv = True

    def _handle_keypress(self, e: tk.Event) -> None:
        """ Handles a keypress. If the key pressed was one of [`w', `a', `s', or `d'] a move is attempted.

        Parameters:
            e: A tk.Event that states which button was pressed by user.
        """
        if e.char == "w":
            self._move_up()
        elif e.char == "a":
            self._move_left()
        elif e.char == "s":
            self._move_down()
        elif e.char == "d":
            self._move_right()
        self._refresh()

    def _move_up(self) -> None:
        """ When w is pressed the player moves up. """
        self._model.move_player(MOVE_DELTAS[UP])

    def _move_down(self) -> None:
        """ When s is pressed the player moves down. """
        self._model.move_player(MOVE_DELTAS[DOWN])

    def _move_left(self) -> None:
        """ When a is pressed the player moves left. """
        self._model.move_player(MOVE_DELTAS[LEFT])

    def _move_right(self) -> None:
        """ When d is pressed the player moves right. """
        self._model.move_player(MOVE_DELTAS[RIGHT])

    def buy_item(self, item_id):
        """ The item will be added to user inventory. and the respective price will be deducted from player.

        Parameters:
            item_id: The ID of the item that will be purchased.
        """
        global ITEM_PRICE
        price = ITEM_PRICE[item_id]
        coins = self._model.get_player_inventory().get_items().get('Coin')
        if coins is None:
            coins = 0
        else:
            coins = len(coins)
        if coins >= price:
            while price:
                self._model.get_player_inventory().get_items()['Coin'].pop(0)
                price -= 1

            if item_id == APPLE:
                self._model.get_player_inventory().add_item(Apple((0, 0)))
            elif item_id == WATER:
                self._model.get_player_inventory().add_item(Water((0, 0)))
            elif item_id == HONEY:
                self._model.get_player_inventory().add_item(Honey((0, 0)))
            elif item_id == POTION:
                self._model.get_player_inventory().add_item(Potion((0, 0)))
            elif item_id == CANDY:
                self._model.get_player_inventory().add_item(Candy((0, 0)))
            self._refresh()
        else:
            tk.messagebox.showinfo("Warning!", "You do not have enough coins to buy this!")

    def _apply_item(self, item_name: str) -> None:
        """ Attempts to apply an item with the given item to the player

        Parameters:
            item_name: name of item that need be applies on the player
        """
        self._model.get_player_inventory().get_items()[item_name][0].apply(self._model.get_player())
        self._model.get_player_inventory().get_items()[item_name].pop(0)
        self._refresh()

    def _handle_callbacks(self) -> None:
        """ Assigns all the necessary callback to the respective classes. """
        self.interface.set_inventory_callback(self._apply_item)
        if TASK > 1:
            self.interface.menu.set_model_callbacks(self._model, self.restart, self.load_new_game)
        if TASK > 2:
            self.interface.controlFrame.set_callback(self.buy_item, self.load_new_game)

    def _handle_controls(self) -> None:
        """ Assigns all the necessary keypress event callbacks to the respective classes. """
        self.interface.bind_keypress(self._handle_keypress)

    def _refresh(self) -> None:
        """ Refreshes all the components of the game """
        if self._model.has_won():
            if TASK > 1:
                self.interface.controlFrame.stop_timer()
            tk.messagebox.showinfo("Congratulations", WIN_MESSAGE)
            exit(0)
        elif self._model.has_lost():
            if TASK > 1:
                self.interface.controlFrame.stop_timer()
            tk.messagebox.showinfo("Sorry!", LOSS_MESSAGE)
            exit(0)
        elif self._model.did_level_up():
            tk.messagebox.showinfo("Congratulations", "Level Up!")
            if TASK > 1:
                global INITIAL_PLAYER_INVENTORY
                for item in self._model.get_player_inventory().get_items():
                    INITIAL_PLAYER_INVENTORY[item] = self._model.get_player_inventory().get_items()[item].copy()
                self.interface.level_view.set_dimensions(self._model.get_current_maze().get_dimensions())
                self.interface.level_view.update_images()

        self.interface.draw(self._model.get_current_maze(), self._model.get_current_items(),
                            self._model.get_player().get_position(), self._model.get_player_inventory(),
                            self._model.get_player_stats())

    def play(self) -> None:
        """ Called to cause gameplay to occur. """
        self.interface.create_interface(self._model.get_current_maze().get_dimensions())
        self._handle_controls()
        self._handle_callbacks()
        self.interface.draw(self._model.get_current_maze(), self._model.get_current_items(),
                            self._model.get_player().get_position(), self._model.get_player_inventory(),
                            self._model.get_player_stats())

        if TASK > 1:
            self.interface.controlFrame.start_timer()

        if TASK >= 2:
            self.interface.controlFrame.set_callback(self.buy_item, self.load_new_game)

    def load_new_game(self) -> None:
        """ Loads up a new game """
        global INITIAL_PLAYER_INVENTORY
        INITIAL_PLAYER_INVENTORY.clear()
        self._model = Model(LOCAL_GAME_FILE)
        if TASK > 1:
            self.interface.level_view.set_dimensions(self._model.get_current_maze().get_dimensions())
            self.interface.level_view.update_images()
        if TASK > 1 and CUSTOM_GAME_FILE:
            self._update_player_stats()
        self._model.get_level().attempt_unlock_door()
        self._refresh()

    def restart(self) -> None:
        """ Restarts the game """
        global INITIAL_PLAYER_INVENTORY
        level_count = self._model._level_num
        self._model = Model(LOCAL_GAME_FILE)
        while level_count:
            self._model.level_up()
            self._model._did_level_up = False
            level_count -= 1
        for item in INITIAL_PLAYER_INVENTORY:
            self._model.get_player_inventory().get_items()[item] = INITIAL_PLAYER_INVENTORY[item].copy()
        self._refresh()


def is_game_valid(filename: str) -> bool:
    """ Validating if the selected game file is valid or not

    Parameters:
        filename: The selected file by the user

    Returns:
        A boolean representing if the file is valid or not
    """
    global CUSTOM_GAME_FILE
    levels = 0
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('Maze'):
                levels += 1
    if levels > 0:
        return True
    else:
        CUSTOM_GAME_FILE = False
        return False


def get_maze_in_text(maze: 'Maze', items: dict[tuple[int, int], 'Item'], player_pos: tuple[int, int]) -> str:
    """ A function to convert the instance of the maze to string

     Parameters:
         maze: The current maze instance
         items: The available items on the maze
         player_pos: Player's current position

     Returns:
         string representation of the current maze

     Note:
        In the a2_solution.py file's load_game function, when each line is read, the lines are stripped. And if for
        a specific row the tile starts or ends with EMPTY tile (ID = " "), those tiles are also stripped. As I was not
        allowed to manipulates the a2_solution.py file, here while saving the maze status, I replaced those EMPTY tiles
        with WALL tiles, which are in the start or end except the EMPTY tiles which were actually a door first.
    """
    m = ""
    for i in range(maze.get_dimensions()[0]):
        for j in range(maze.get_dimensions()[1]):
            if player_pos == (i, j):
                m += PLAYER
            elif (i, j) in items:
                m += items[(i, j)].get_id()
            else:
                if (j == 0 or j == maze.get_dimensions()[1] - 1) and isinstance(maze.get_tile((i, j)), Empty):
                    m += WALL
                elif isinstance(maze.get_tile((i, j)), Door):
                    m += DOOR
                else:
                    m += maze.get_tile((i, j)).get_id()

        m += "\n"
    return m + "\n"


def play_game(root: tk.Tk) -> None:
    """ The initial function which start the game """
    global LOCAL_GAME_FILE
    game = GraphicalMazeRunner(LOCAL_GAME_FILE, root)
    game.play()
    root.mainloop()


def main() -> None:
    """ The main function which creates the root tk.Tk frame """
    root = tk.Tk()
    play_game(root)


# Some important global variables
LOCAL_GAME_FILE = GAME_FILE
CUSTOM_GAME_FILE = False
CUSTOM_GAME_STATS = ""
INITIAL_PLAYER_INVENTORY = {}
ITEM_PRICE = {APPLE: 1, WATER: 1, HONEY: 2, POTION: 2, CANDY: 3}

if __name__ == '__main__':
    main()
