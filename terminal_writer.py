#!/usr/bin/env python2

from sys import stdout as default_output

class Writer:
    # The output_file parameter allows the selection of another device or file
    # to use as output. The make_square parameter make all horizontal
    # manipulations twice as large to compensate for the fact that the terminal
    # character size is proportially tall
    def __init__(self, output_file = default_output, make_square = False):
        self.last_state = set()
        self.output_file = output_file
        self.make_square = make_square
        self.init_display()

    def __del__(self):
        self.reset_display()

    def write_new_state(self, new_state):
        # The dark cells are the cells which have become dark since the last
        # render. This set is created from the light cells in the last render
        # with the cells which are currently light taken out
        dark_cells = self.last_state - new_state

        # The light cells are the cells which have become light since the last
        # render. This is just the reverse of the previous statement
        light_cells = new_state - self.last_state

        for (x, y) in dark_cells:
            self.mask_dot(x, y)

        for (x, y) in light_cells:
            self.write_dot(x, y)

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
    
    def set_background_white(self):
        self.output_file.write("\x1B[47m")
    
    # Map the background colour to be the "reset colour" as the background will
    # be blank
    def set_background_black(self):
        self.reset_colours()
    
    # These two function combine the previous functions to either draw a dot or
    # to punch out a blank spot
    def write_dot(self, x, y):
        self.reset_colours()
        self.set_cursor_position(x, y)
        self.set_background_white()
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

