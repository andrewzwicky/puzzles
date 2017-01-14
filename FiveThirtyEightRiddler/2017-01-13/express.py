"""
It’s your 30th birthday (congrats, by the way), and your friends bought you
a cake with 30 candles on it. You make a wish and try to blow them out. Every
time you blow, you blow out a random number of candles between one and the
number that remain, including one and that other number. How many times do
you blow before all the candles are extinguished, on average?
"""


def calc_average(n):
    output = list(None for _ in range(n))
    output[0] = 1
    for i in range(1, n):
        output[i] = (1 + sum(1+j for j in output[0:i])) / (i+1)
    return output[-1]


print(calc_average(30))
