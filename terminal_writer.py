#!/usr/bin/env python2

from sys import stdout as default_output

COLOUR_BLACK = "\x1B[40m"
COLOUR_RED = "\x1B[41m"
COLOUR_GREEN = "\x1B[42m"
COLOUR_YELLOW = "\x1B[43m"
COLOUR_BLUE = "\x1B[44m"
COLOUR_MAGENTA = "\x1B[45m"
COLOUR_CYAN = "\x1B[46m"
COLOUR_WHITE = "\x1B[47m"

class Writer:
    # The output_file parameter allows the selection of another device or file
    # to use as output. The make_square parameter make all horizontal
    # manipulations twice as large to compensate for the fact that the terminal
    # character size is proportionally tall
    def __init__(self, output_file = default_output, make_square = False):
        self.last_state = {}
        self.output_file = output_file
        self.make_square = make_square
        self.init_display()

    def __del__(self):
        self.reset_display()

    def write_new_state(self, new_state):
        # The dark cells are the cells which have become dark since the last
        # render. This set is created from the light cells in the last render
        # with the cells which are currently light taken out
        dark_cells = set(self.last_state.keys()) - set(new_state.keys())

        # The changed cells are the cells which have either been lit up since
        # the previous render or have changed colour
        changed_cells = {i for (i, j) in new_state.items() if j != self.last_state.get(i)}

        for (x, y) in dark_cells:
            self.mask_dot(x, y)

        for (x, y) in changed_cells:
            self.write_dot(x, y, new_state[(x, y)])

        # Store the new state to compare with next time
        self.last_state = new_state
        self.flush_output()

    # These functions write out the escape sequences which control the position
    # and display written to the output
    def hide_cursor(self):
        self.output_file.write("\x1B[?25l")
    
    def show_cursor(self):
        self.output_file.write("\x1B[?25h")
    
    def clear_display(self):
        self.output_file.write("\x1B[2J")
    
    def set_cursor_position(self, x, y):
        x += 1
        if self.make_square:
            y = 2 * y + 1
        else:
            y += 1
        self.output_file.write("\x1B[{};{}f".format(x, y))
    
    def reset_colours(self):
        self.output_file.write("\x1B[0m")
    
    def set_background_colour(self, colour):
        self.output_file.write(colour)
    
    # Map the background colour to be the "reset colour" as the background will
    # be blank
    def set_background_black(self):
        self.reset_colours()
    
    # These two function combine the previous functions to either draw a dot or
    # to punch out a blank spot
    def write_dot(self, x, y, colour):
        self.reset_colours()
        self.set_cursor_position(x, y)
        self.set_background_colour(colour)
        if self.make_square:
            self.output_file.write("  ")
        else:
            self.output_file.write(" ")
    
    def mask_dot(self, x, y):
        self.reset_colours()
        self.set_cursor_position(x, y)
        self.set_background_black()
        if self.make_square:
            self.output_file.write("  ")
        else:
            self.output_file.write(" ")
    
    # Flush output so that the display gets updated. This is usually done on
    # each newline but since newlines are not used in the previous functions,
    # this needs to be done manually
    def flush_output(self):
        self.output_file.flush()
    
    # Initialise the display. This involves hiding the cursor so that there
    # isn't a random dot on the display and clearing the display
    def init_display(self):
        self.clear_display();
        self.hide_cursor()
        self.flush_output()
    
    # Reset the display back into a useful state.
    def reset_display(self):
        self.show_cursor()
        self.reset_colours()
        self.clear_display()
        self.set_cursor_position(0, 0)
        self.flush_output()

