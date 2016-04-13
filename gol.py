#!/usr/bin/env python2

# This is a implementation of Conway's Game of Life which is to show the
# capabilities of the terminal_writer

from time import sleep
import terminal_writer
from terminal_writer import Writer
from serial import Serial

WORLD_WIDTH = 80
WORLD_HEIGHT = 40

class World:
    def __init__(self, inital_cells):
        serial_port = Serial("/dev/ttyAMA0", 38400)
        self.alive_cells = inital_cells
        self.writer = Writer(output_file = serial_port)

    def update(self):
        new_cells = {}
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
                    new_cells[(x, y)] = terminal_writer.COLOUR_BLUE
                elif neighbor_count == 2 and (x, y) in self.alive_cells:
                    new_cells[(x, y)] = terminal_writer.COLOUR_CYAN
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
            (24, 0): terminal_writer.COLOUR_RED,
            (22, 1): terminal_writer.COLOUR_RED,
            (24, 1): terminal_writer.COLOUR_RED,
            (12, 2): terminal_writer.COLOUR_RED,
            (13, 2): terminal_writer.COLOUR_RED,
            (20, 2): terminal_writer.COLOUR_RED,
            (21, 2): terminal_writer.COLOUR_RED,
            (34, 2): terminal_writer.COLOUR_RED,
            (35, 2): terminal_writer.COLOUR_RED,
            (11, 3): terminal_writer.COLOUR_RED,
            (15, 3): terminal_writer.COLOUR_RED,
            (20, 3): terminal_writer.COLOUR_RED,
            (21, 3): terminal_writer.COLOUR_RED,
            (34, 3): terminal_writer.COLOUR_RED,
            (35, 3): terminal_writer.COLOUR_RED,
            (0, 4): terminal_writer.COLOUR_RED,
            (1, 4): terminal_writer.COLOUR_RED,
            (10, 4): terminal_writer.COLOUR_RED,
            (16, 4): terminal_writer.COLOUR_RED,
            (20, 4): terminal_writer.COLOUR_RED,
            (21, 4): terminal_writer.COLOUR_RED,
            (0, 5): terminal_writer.COLOUR_RED,
            (1, 5): terminal_writer.COLOUR_RED,
            (10, 5): terminal_writer.COLOUR_RED,
            (14, 5): terminal_writer.COLOUR_RED,
            (16, 5): terminal_writer.COLOUR_RED,
            (17, 5): terminal_writer.COLOUR_RED,
            (22, 5): terminal_writer.COLOUR_RED,
            (24, 5): terminal_writer.COLOUR_RED,
            (10, 6): terminal_writer.COLOUR_RED,
            (16, 6): terminal_writer.COLOUR_RED,
            (24, 6): terminal_writer.COLOUR_RED,
            (11, 7): terminal_writer.COLOUR_RED,
            (15, 7): terminal_writer.COLOUR_RED,
            (12, 8): terminal_writer.COLOUR_RED,
            (13, 8): terminal_writer.COLOUR_RED,
        })
        world.start_loop()
    except KeyboardInterrupt:
        pass
