import curses
from curses import ascii as curses_ascii
import time

from cellular_automata_grids.grids import BaseGrid


class TerminalSquareGrid(BaseGrid):
    BLOCKS = [" ", "░", "▒", "▓", "█"]
    color_patterns = {}

    def set_up_window(self) -> None:
        if self.fps < 0:
            self.fps = 20

        self.color_pairs = {}
        self.color_blocks = {}

        # Optimized for HPP LGCA, TODO: make it more general.
        for idx, val in enumerate(self.colors):
            if val == 0:
                continue

            block = self.BLOCKS[idx.bit_count() if idx < 0b1000_0000 else idx.bit_count() - 1]
            self.color_blocks[idx + 1] = block
            self.color_pairs[idx + 1] = (
                idx + 1,
                curses.COLOR_WHITE,
                curses.COLOR_BLACK if idx < 127 else curses.COLOR_RED,
            )

    def update_display(self):
        pass

    def draw_grid(self):
        # Display matrix
        for row in range(len(self.automaton.grid)):
            for col in range(len(self.automaton.grid[0])):
                pair_number = self.automaton.grid[row][col] + 1
                self.stdscr.addstr(row, col, self.color_blocks[pair_number], curses.color_pair(pair_number))

        self.stdscr.refresh()

    def mainloop(self) -> None:
        curses.wrapper(self.run)

    def run(self, stdscr) -> None:
        """Main display loop."""

        self.stdscr = stdscr

        # Set up color pairs
        curses.start_color()
        self.color_patterns = {}
        for pair_number, fg, bg in self.color_pairs.values():
            curses.init_pair(pair_number, fg, bg)

        # Hide cursor and disable input echo
        curses.curs_set(0)
        curses.noecho()

        while True:
            try:
                stdscr.nodelay(1)
                key = stdscr.getch()

                if key == curses_ascii.ESC:
                    break
                elif key == ord("s"):
                    self.reset_automaton()
                elif key == curses_ascii.SP:
                    self.animate = not self.animate
                elif key == curses.KEY_RIGHT:
                    if not self.animate:
                        self.make_a_step(no_max=True)

                next(self)
                time.sleep(1 / self.fps)
            except curses.error:
                continue
