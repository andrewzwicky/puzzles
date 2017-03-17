# https://www.reddit.com/r/dailyprogrammer/comments/5zxebw/20170317_challenge_306_hard_generate_strings_to/?st=j0e6yo9u&sh=163a4157
# Most everyone who programs using general purpose languages is familiar with regular expressions, which enable you to match inputs using patterns. Today, we'll do the inverse: given a regular expression, can you generate a pattern that will match?
# For this challenge we'll use a subset of regular expression syntax:
# character literals, like the letter A
# * meaning zero or more of the previous thing (a character or an entity)
# + meaning one or more of the previous thing
# . meaning any single literal
# [a-z] meaning a range of characters from a to z inclusive
# To tackle this you'll probably want to consider using a finite state machine and traversing it using a random walk.

import pytest
import re


def reverse_regex(input_regex):
    # parse through the regex, character by character:
    output_string = ''

    ONE_OR_MORE = '+'
    ZERO_OR_MORE = '*'
    OPEN_BRACKET = '['
    CLOSE_BRACKET = ']'

    SPECIAL_CHARACTERS = (ONE_OR_MORE, ZERO_OR_MORE, OPEN_BRACKET, CLOSE_BRACKET)


    input_regex_generator = iter(input_regex)
    prev_character = ''

    try:
        while True:
            char = next(input_regex_generator)
            if char not in SPECIAL_CHARACTERS:
                output_string += prev_character
                prev_character = char

            else:
                if char == ONE_OR_MORE:
                    output_string += prev_character
                    prev_character = ''

                elif char == ZERO_OR_MORE:
                    prev_character = ''

                elif char == OPEN_BRACKET:
                    output_string += prev_character

                    while char != CLOSE_BRACKET:
                        if char not in SPECIAL_CHARACTERS:
                            prev_character = char
                        char = next(input_regex_generator)                    

    except StopIteration:
        if prev_character not in SPECIAL_CHARACTERS:
            output_string += prev_character

    return output_string


@pytest.mark.parametrize("test_input,expected", [
    ('a+b', 'ab'),
    ('a+b+', 'ab'),
    ('abcd', 'abcd'),
    ('abc*d', 'abd'),
    ('[az]b', 'zb'),
    ('[c-z]b', 'zb'),
    ('[c-z]+b', 'zb'),
    ('[c-zA-Z]*b+', 'b'),
    ("[A-Za-z0-9$.+!*'(){},~:;=@#%_\-]*",""),
    ("ab[c-l]+jkm9*10+","abljkm10"),
    ("iqb[beoqob-q]872+0qbq*","iqbq8720qb"),
])
def test_eval(test_input, expected):
    assert reverse_regex(test_input) == expected
    assert re.match(test_input, expected) is not None
