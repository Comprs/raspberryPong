#!/usr/bin/env python2

# This is a implementation of Conway's Game of Life which is to show the
# capabilities of the terminal_writer

from time import sleep
from terminal_writer import Writer

WORLD_WIDTH = 80
WORLD_HEIGHT = 40

class World:
    def __init__(self, inital_cells):
        self.alive_cells = inital_cells
        self.writer = Writer()

    def update(self):
        new_cells = set()
        for x in range(WORLD_WIDTH):
            for y in range(WORLD_HEIGHT):
                neighbor_count = (int((x - 1, y - 1) in self.alive_cells) +
                                  int((x    , y - 1) in self.alive_cells) +
                                  int((x + 1, y - 1) in self.alive_cells) +
                                  int((x - 1, y    ) in self.alive_cells) +
                                  int((x + 1, y    ) in self.alive_cells) +
                                  int((x - 1, y + 1) in self.alive_cells) +
                                  int((x    , y + 1) in self.alive_cells) +
                                  int((x + 1, y + 1) in self.alive_cells))
                if neighbor_count == 3:
                    new_cells.add((x, y))
                elif neighbor_count == 2 and (x, y) in self.alive_cells:
                    new_cells.add((x, y))
        self.alive_cells = new_cells

    def render(self):
        self.writer.write_new_state(world.alive_cells)

    def start_loop(self):
        while True:
            self.render()
            sleep(0.04)
            self.update()

if __name__ == "__main__":
    try:
        world = World({
            (0, 24),
            (1, 22),
            (1, 24),
            (2, 12),
            (2, 13),
            (2, 20),
            (2, 21),
            (2, 34),
            (2, 35),
            (3, 11),
            (3, 15),
            (3, 20),
            (3, 21),
            (3, 34),
            (3, 35),
            (4, 0),
            (4, 1),
            (4, 10),
            (4, 16),
            (4, 20),
            (4, 21),
            (5, 0),
            (5, 1),
            (5, 10),
            (5, 14),
            (5, 16),
            (5, 17),
            (5, 22),
            (5, 24),
            (6, 10),
            (6, 16),
            (6, 24),
            (7, 11),
            (7, 15),
            (8, 12),
            (8, 13),
        })
        world.start_loop()
    except KeyboardInterrupt:
        pass
