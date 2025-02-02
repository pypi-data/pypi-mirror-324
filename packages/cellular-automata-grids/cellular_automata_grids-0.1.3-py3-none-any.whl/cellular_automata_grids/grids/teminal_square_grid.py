import curses
from curses import ascii
import time
from . import BaseGrid


class TerminalSquareGrid(BaseGrid):
    BLOCKS = [" ", "░", "▒", "▓", "█", "■"]
    SOLID_BLOCK = BLOCKS[4]
    DARK_BLOCK = BLOCKS[1]
    COLOR_PAIRS = (
        (1, curses.COLOR_WHITE, curses.COLOR_WHITE),
        (2, curses.COLOR_BLACK, curses.COLOR_BLACK),
        (3, curses.COLOR_RED, curses.COLOR_BLACK),
        (4, curses.COLOR_CYAN, curses.COLOR_BLACK),
        (5, curses.COLOR_MAGENTA, curses.COLOR_BLACK),
        (6, curses.COLOR_YELLOW, curses.COLOR_BLACK),
        (7, curses.COLOR_GREEN, curses.COLOR_WHITE),
        (8, curses.COLOR_BLUE, curses.COLOR_WHITE),
        (9, curses.COLOR_RED, curses.COLOR_WHITE),
        (10, curses.COLOR_CYAN, curses.COLOR_WHITE),
        (11, curses.COLOR_MAGENTA, curses.COLOR_WHITE),
        (12, curses.COLOR_YELLOW, curses.COLOR_WHITE),
    )

    def set_up_window(self) -> None:
        pass

    def update_display(self):
        pass

    def draw_grid(self):
        # Display matrix
        for row in range(len(self.automaton.grid)):
            for col in range(len(self.automaton.grid[0])):
                color = curses.color_pair(1 + self.automaton.grid[row][col] % len(self.COLOR_PAIRS))  # | curses.A_BOLD
                self.stdscr.addstr(row, col, self.SOLID_BLOCK, color)

        self.stdscr.refresh()

    def mainloop(self) -> None:
        curses.wrapper(self.run)

    def run(self, stdscr) -> None:
        """Main display loop."""

        self.stdscr = stdscr

        # Set up color pairs
        curses.start_color()
        for pair_number, fg, bg in self.COLOR_PAIRS:
            curses.init_pair(pair_number, fg, bg)

        # Hide cursor and disable input echo
        curses.curs_set(0)
        curses.noecho()

        while True:
            try:
                stdscr.nodelay(1)
                key = stdscr.getch()

                if key == ascii.ESC:
                    break
                elif key == ord("s"):
                    self.reset_automaton()
                elif key == ascii.SP:
                    self.animate = not self.animate
                elif key == curses.KEY_RIGHT:
                    if not self.animate:
                        self.make_a_step(no_max=True)

                next(self)
                time.sleep(1 / self.fps)
            except curses.error:
                continue
