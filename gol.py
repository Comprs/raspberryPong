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
            (0, 24): terminal_writer.COLOUR_RED,
            (1, 22): terminal_writer.COLOUR_RED,
            (1, 24): terminal_writer.COLOUR_RED,
            (2, 12): terminal_writer.COLOUR_RED,
            (2, 13): terminal_writer.COLOUR_RED,
            (2, 20): terminal_writer.COLOUR_RED,
            (2, 21): terminal_writer.COLOUR_RED,
            (2, 34): terminal_writer.COLOUR_RED,
            (2, 35): terminal_writer.COLOUR_RED,
            (3, 11): terminal_writer.COLOUR_RED,
            (3, 15): terminal_writer.COLOUR_RED,
            (3, 20): terminal_writer.COLOUR_RED,
            (3, 21): terminal_writer.COLOUR_RED,
            (3, 34): terminal_writer.COLOUR_RED,
            (3, 35): terminal_writer.COLOUR_RED,
            (4, 0): terminal_writer.COLOUR_RED,
            (4, 1): terminal_writer.COLOUR_RED,
            (4, 10): terminal_writer.COLOUR_RED,
            (4, 16): terminal_writer.COLOUR_RED,
            (4, 20): terminal_writer.COLOUR_RED,
            (4, 21): terminal_writer.COLOUR_RED,
            (5, 0): terminal_writer.COLOUR_RED,
            (5, 1): terminal_writer.COLOUR_RED,
            (5, 10): terminal_writer.COLOUR_RED,
            (5, 14): terminal_writer.COLOUR_RED,
            (5, 16): terminal_writer.COLOUR_RED,
            (5, 17): terminal_writer.COLOUR_RED,
            (5, 22): terminal_writer.COLOUR_RED,
            (5, 24): terminal_writer.COLOUR_RED,
            (6, 10): terminal_writer.COLOUR_RED,
            (6, 16): terminal_writer.COLOUR_RED,
            (6, 24): terminal_writer.COLOUR_RED,
            (7, 11): terminal_writer.COLOUR_RED,
            (7, 15): terminal_writer.COLOUR_RED,
            (8, 12): terminal_writer.COLOUR_RED,
            (8, 13): terminal_writer.COLOUR_RED,
        })
        world.start_loop()
    except KeyboardInterrupt:
        pass
