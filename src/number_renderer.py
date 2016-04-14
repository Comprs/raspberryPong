#!/usr/bin/env python2

import terminal_writer

# ###
# # #
# # #
# # #
# ###

zero = [
    (0, 0),
    (0, 1),
    (0, 2),
    (0, 3),
    (0, 4),
    (1, 0),
    (1, 4),
    (2, 0),
    (2, 1),
    (2, 2),
    (2, 3),
    (2, 4),
]

#    #
#    #
#    #
#    #
#    #

one = [
    (2, 0),
    (2, 1),
    (2, 2),
    (2, 3),
    (2, 4),
]

# ###
#   #
# ###
# #  
# ###

two = [
    (0, 0),
    (0, 2),
    (0, 3),
    (0, 4),
    (1, 0),
    (1, 2),
    (1, 4),
    (2, 0),
    (2, 1),
    (2, 2),
    (2, 4),
]

# ###
#   #
# ###
#   #
# ###

three = [
    (0, 0),
    (0, 2),
    (0, 4),
    (1, 0),
    (1, 2),
    (1, 4),
    (2, 0),
    (2, 1),
    (2, 2),
    (2, 3),
    (2, 4),
]

# # #
# # #
# ###
#   #
#   #

four = [
    (0, 0),
    (0, 1),
    (0, 2),
    (1, 2),
    (2, 0),
    (2, 1),
    (2, 2),
    (2, 3),
    (2, 4),
]

# ###
# #  
# ###
#   #
# ###

five = [
    (0, 0),
    (0, 1),
    (0, 2),
    (0, 4),
    (1, 0),
    (1, 2),
    (1, 4),
    (2, 0),
    (2, 2),
    (2, 3),
    (2, 4),
]

# ###
# # 
# ###
# # #
# ###

six = [
    (0, 0),
    (0, 1),
    (0, 2),
    (0, 3),
    (0, 4),
    (1, 0),
    (1, 2),
    (1, 4),
    (2, 0),
    (2, 2),
    (2, 3),
    (2, 4),
]

# ###
#   #
#   #
#   #
#   #

seven = [
    (0, 0),
    (1, 0),
    (2, 0),
    (2, 1),
    (2, 2),
    (2, 3),
    (2, 4),
]

# ###
# # #
# ###
# # #
# ###

eight = [
    (0, 0),
    (0, 1),
    (0, 2),
    (0, 3),
    (0, 4),
    (1, 0),
    (1, 2),
    (1, 4),
    (2, 0),
    (2, 1),
    (2, 2),
    (2, 3),
    (2, 4),
]

# ###
# # #
# ###
#   #
# ###

nine = [
    (0, 0),
    (0, 1),
    (0, 2),
    (0, 4),
    (1, 0),
    (1, 2),
    (1, 4),
    (2, 0),
    (2, 1),
    (2, 2),
    (2, 3),
    (2, 4),
]

digits = [
    zero,
    one,
    two,
    three,
    four,
    five,
    six,
    seven,
    eight,
    nine,
]

def convert_digit(digit, offset = (0, 0), colour = terminal_writer.COLOUR_WHITE):
    return {(x + offset[0], y + offset[1]): colour for (x, y) in digits[digit]}

def convert_number(number, offset = (0, 0), colour = terminal_writer.COLOUR_WHITE):
    number_str = str(number)
    values = {}
    for (index, digit) in enumerate(map(int, number_str)):
        values.update(convert_digit(digit, (offset[0] + 4 * index, offset[1]), colour))
    return values
