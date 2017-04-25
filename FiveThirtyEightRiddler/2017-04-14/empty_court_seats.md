
---
layout:     post
title:      "Supreme Gridlock"
date:       2017-04-23 12:00:00
author:     Andrew
header-img: img/posts/supreme_court_seats/bench.jpg
header-credit: https://unsplash.com/@willpat
tags:       programming riddler politics puzzles
---

Last week I won the FiveThityEight [Riddler](https://fivethirtyeight.com/features/how-many-bingo-cards-are-there-in-the-world/)!  (don't get too excited, the winner is randomly selected 😉)

![winner]({{ site.baseurl }}/img/posts/supreme_court_seats/classic_winner.png)

I don't share every riddler I work on, but this one is straightforward yet interesting, politically applicable, and was fun to work on.

Here is the riddle:
> Imagine that U.S. Supreme Court nominees are only confirmed if the same party holds the presidency and the Senate. What is the expected number of vacancies on the bench in the long run?    
You can assume the following:
* You start with an empty, nine-person bench.
* There are two parties, and each has a 50 percent chance of winning the presidency and a 50 percent chance of winning the Senate in each election.
* The outcomes of Senate elections and presidential elections are independent.
* The length of time for which a justice serves is uniformly distributed between zero and 40 years.

Additional clarifications I made:
* President elected every 4 years, Senate every 2 years.
* Judicial terms will be integers (whole years), and if a judge leaves on an election year, the subsequent government will nominate.

Note: I have omitted some of the plotting code in favor of just displaying the results.  Full code [here](https://github.com/andrewzwicky/puzzles/blob/master/FiveThirtyEightRiddler/2017-04-14/empty_court_seats.ipynb)
<!--break-->

```python
from enum import Enum
import itertools
import random
from collections import Counter
import numpy as np
from plotting import *
from multiprocessing import Pool

%matplotlib inline
```

First we'll need a way to differentiate which party the Senate & President are part of.  The `Party` [enumeration](https://en.wikipedia.org/wiki/Enumerated_type) provides an easy way to assign names to the different parties.  Assigning names helps keep the code easily readable.


```python
class Party(Enum):
    D = 1
    R = 2
    
color_trans = {Party.D:'blue', Party.R:'red'}
```

We'll also make a class to represent each judge.  When a new `Justice` is created, they'll be assigned a party, given a fake name, and a term of somewhere between 0 and 40 years.  The names are just for fun, they don't have any impact on the solution.


```python
class Justice:
    
    def __init__(self, party):
        self.party = party
        self.term = random.randint(0,40)
        
        
    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):
        return "{party}-{term}".format(party=self.party.name,term=self.term)
```


```python
print(Justice(Party.D))
print(Justice(Party.R))
```

    D-35
    R-17


Our lass class is `Bench`.  This class will represent all of the `Justices` currently on the Supreme Court.  When the `Bench` is first formed, no seats will be filled.  We care about modifying the `Bench` in a few ways:

1. Filling all available seats with judges of a certain party (`fill_seats`).
2. Adding years to determine if judges have vacated their seats on any given year (`add_years`).
3. Getting the composition of the court at a particular year, used for displaying the data later (`breakdown`).

Empty seats in the court are represented by `None`, and judges are removed when they have `0` years left in their term.


```python
class Bench:
    
    SIZE = 9
    
    def __init__(self):
        self.seats = [None] * self.SIZE
    
    def fill_seats(self, party):
        # loop through all seats
        for i in range(self.SIZE):
            if self.seats[i] is None:
                # if seat is empty, add new 
                # justice of the correct party
                self.seats[i] = Justice(party)
                
    def add_years(self, num_years):
        for i in range(self.SIZE):
            if self.seats[i] is not None:
                # for occupied seats, remove the given
                # number of years from their remaining
                # term.  If their term is less than 0
                # this means their seat should now
                # be empty again.
                self.seats[i].term -= num_years
                if self.seats[i].term <= 0:
                    self.seats[i] = None
    
    def breakdown(self):
        empty = 0
        dems = 0
        reps = 0
        
        for seat in self.seats:
            if seat is None:
                empty += 1
            else:
                if seat.party == Party.D:
                    dems += 1
                else:
                    reps += 1

        return (dems, empty, reps)
    
    def __repr__(self):
        return "\n".join(map(str,self.seats))
```


```python
b = Bench()
b.fill_seats(Party.R)
b.add_years(4)
print(b)
```

    None
    R-14
    R-29
    R-28
    R-33
    R-16
    R-4
    R-22
    R-3


This is where the actual simulation begins.  This simulation will loop through years (by 2).  

At each 2 year period, Senate elections will be held.
Each 4 year period, President elections will be held.

At the end of the elections, if the government is aligned, empty seats on the bench should be filled by that party.


```python
def simulate(years):
    president_party = None
    senate_party = None
    bench = Bench()
        
    for year in range(years+1):
        bench.add_years(1)
        
        if year % 2 == 0:
            senate_party = random.choice(list(Party))
        
        if year % 4 == 0:
            president_party = random.choice(list(Party))
        
        if president_party == senate_party:
            bench.fill_seats(president_party)
        
        yield year, bench.breakdown(), president_party, senate_party
```

To make meaningful data, the simulation needs to be run for a number of years.  `run_simulation` will execute the simulation for the supplied number of years, and return the following information:    
`years`: an array of all the years that have data.    
`bench_stacks`: the stacked bar graph data for the composition of the court at each year.    
`president_parties`: an array of the president party at each year.    
`senate_parties`: an array of the senate party at each year.    
`mean`: an array with the mean number of vacancies per year over the life of the court.


```python
def run_simulation(simulation_years):
    years, benches, president_parties, senate_parties = zip(*list(simulate(simulation_years)))
    bench_stacks = np.row_stack(zip(*benches))
    mean = np.cumsum(bench_stacks[1]) / ([1] + list(years[1:]))
    return years, bench_stacks, president_parties, senate_parties, mean
```


```python
sim_years = 200

years, bench_stacks, president_parties, senate_parties, mean = run_simulation(sim_years)

stacked_plot_bench_over_time_with_parties(years,
                                          bench_stacks,
                                          president_parties,
                                          senate_parties,
                                          color_trans)
```


![png](empty_court_seats_files/empty_court_seats_16_0.png)


This plot shows how the court functions over 200 years, including the respective party affiliations at any time.  In the periods of divided government, the vacancies get larger, and when the government is aligned, the court becomes full again (no surprise, that what it's supposed to do!).  However, the interesting thing is determining more precisely how many vacancies we can expect at any given time.


```python
sim_years = 1000

years, bench_stacks, president_parties, senate_parties, mean = run_simulation(sim_years)

stacked_plot_bench_over_time(years, bench_stacks, mean)
```


![png](empty_court_seats_files/empty_court_seats_18_0.png)


In this plot, let's extend the timeline to 1000 years to give the average a longer time to settle.  This simulation shows that we should expect a little less than 1 vacancy per year.

However, this is only 1 simulation that includes randomness.  To give a better estimate of where this probability actually falls, let's run multiple simulations and examine the distribution of expected vacancies.


```python
sim_years = 50000
sample_size = 2000

with Pool(processes=4) as p:
    results = p.map(run_simulation, itertools.repeat(sim_years,sample_size))
    
years, _, _, _, means = zip(*results)
```


```python
plot_sims(years[0], means)
```


![png](empty_court_seats_files/empty_court_seats_21_0.png)


Running the 50000 year simulation 2000 times shows us the expected distribution and it would be more accurate to say that we should expect ~0.7 vacancies per year, instead of the singular value we received above.

## Related Reading
[https://hectorpefo.github.io/2017-04-16-supreme-vacancies/](https://hectorpefo.github.io/2017-04-16-supreme-vacancies/)    
[http://www.laurentlessard.com/bookproofs/a-supreme-court-puzzle/](http://www.laurentlessard.com/bookproofs/a-supreme-court-puzzle/)
