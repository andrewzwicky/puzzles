"""
Problem E
Need for Speed
Time limit: 1 second

Sheila is a student and she drives a typical student car: it is old, slow, rusty, and falling apart. Recently, the 
needle on the speedometer fell off. She glued it back on, but she might have placed it at the wrong angle. Thus, when 
the speedometer reads s, her true speed is s + c, where c is an unknown constant (possibly negative).

Sheila made a careful record of a recent journey and wants to use this to compute c. The journey consisted of n 
segments. In the ith segment she traveled a distance of di and the speedometer read si for the entire segment. This 
whole journey took time t. Help Sheila by computing c.

Note that while Sheila’s speedometer might have negative readings, her true speed was greater than zero for each 
segment of the journey.
Input

The first line of input contains two integers n (1 ≤ n ≤ 1000), the number of sections in Sheila’s journey, and t 
(1 ≤ t ≤ 10^6), the total time. This is followed by n lines, each describing one segment of Sheila’s journey. The 
ith of these lines contains two integers di (1 ≤ di ≤ 1000) and si (|si | ≤ 1000), the distance and speedometer reading 
for the ith segment of the journey. Time is specified in hours, distance in miles, and speed in miles per hour.
Output

Display the constant c in miles per hour. Your answer should have an absolute or relative error of less than 10−6
"""

import sys


def parse_input(inp_string):
    inp_string = inp_string.split('\n')
    _, time = inp_string[0].split(" ")
    time = float(time)
    dists, speeds = zip(*[map(float, l.split(" ")) for l in inp_string[1:]])

    return time, dists, speeds


def calculate_time_from_guess(dists, speeds, c):
    return sum(d / (s + c) for d, s in zip(dists, speeds))


def compute_speedometer_offset(time, dists, speeds):
    init_back_jump = False
    jump = 100
    minc = -min(speeds) + 0.0001
    c = minc
    t = calculate_time_from_guess(dists, speeds, c)

    while abs(t - time) >= 10 ** -8:
        if t < time:
            # c too large
            if not init_back_jump:
                init_back_jump = True

            jump = jump / 2
            c -= jump

        else:
            # c too small
            if init_back_jump:
                jump = jump / 2

            c += jump

        t = calculate_time_from_guess(dists, speeds, c)

    return c


def e_speed(inp_string):
    return compute_speedometer_offset(*parse_input(inp_string))