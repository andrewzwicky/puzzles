---
layout:     post
title:      "Tickets"
date:       2017-05-19 10:00:00
author:     Andrew
header-img: img/posts/speeding_commuters/traffic_bg.jpg
header-credit: https://unsplash.com/@glebson
tags:       programming riddler probability
---

> From Jerry Meyers, a careening commute problem:

> Four co-workers carpool to work each day. A driver is selected randomly for the drive to work and again randomly for the drive home. Each of the drivers has a lead foot, and each has a chance of being ticketed for speeding. Driver A has a 10 percent chance of getting a ticket each time he drives, Driver B a 15 percent chance, Driver C a 20 percent chance, and Driver D a 25 percent chance. The state will immediately revoke the license of a driver after his or her third ticket, and a driver will stop driving in the carpool once his license is revoked. Since there is only one police officer on the carpool rout, a maximum of one ticket will be issued per morning and a max of one per evening.

> Assuming that all four drivers start with no tickets, how many days can we expect the carpool to last until all the drivers have lost their licenses?

## Observations
First, let's make some observations about the problem.  At the beginning of each trip, each driver will have some amount of tickets.  I'm going to refer to these amounts as a **state**.  For example, if Drivers A & B each had 1 ticket, I'll write that state as `[1, 1, 0, 0]`.

#### 1. There are a limited number of possiblities for how tickets could be distributed amongst the drivers
Each driver starts with 0 tickets and stops receiving them after their 3rd.  Because there are a limited number of ticket counts, and a limited number of drivers, there is a finite number of ways that tickets can be distributed amongst our drivers.

This finite number of states is the number of ways that 0,1,2, or 3 can be arranged, including repeats, across the 4 drivers.  With 4 possible ticket amounts over 4 drivers, this will result in $$4^4$$ ,or 256, possible distributions of tickets amongst the drivers.

#### 2. The possibility of a driver receiving a ticket does not depend on the order that tickets were issued in
There is no impact of the past on the likelihood that an individual driver will receive a ticket.  If Driver A and Driver B each have 1 ticket, the likelihood that Driver C will receive a ticket is not influenced by the order that A and B received their ticket.  The only factors that influence each drivers likelihood of receiving a ticket are:
* the number of drivers remaining (more drivers means it's less likely that any individual driver will be selected randomly)
* their lead foot (i.e. their individual ticket probability)

#### 3. The state where all drivers have received the maximum number of tickets can be reached from any other state.
To rephrase this, if you picked any distribution of tickets, e.g. `[0, 1, 2, 0]` or `[3, 0, 0, 1]` or `[1, 3, 2, 3]`, you can reach the end state, `[3, 3, 3, 3]`. Intuitively, this makes sense because any drivers with fewer than `3` tickets will continue to accumulate tickets until they also have `3`.  This is probably the most abstract of all of these observations, but it's important to the solution, so stick around!

To summarize what we've learned so far:
* the number of possible ticket distributions is finite
* the probability for a ticket to be issued depends only on the state at that time. 
* there is an end state that can be reached from any other state

## Markov Chains

These observations hint that a good possible method is using [Markov chains](https://en.wikipedia.org/wiki/Markov_chain).  A *Markov process* is a process with randomness that doesn't depend on previous state (it is "memoryless").  A *Markov chain* is a way to represent a Markov process that has a finite number of states.

As an example, let's preted tomorrow's weather depends only on today's weather, and there are only two types of weather **rainy** and **sunny**.  The weather follows these rules:
* If it's sunny today, tommorow's weather is: 
  * 90% likely sunny.
  * 10% likely rainy.
* If it's rainy today, tommorow's weather is: 
  * 50% likely sunny.
  * 50% likely rainy.

This can be visualized like this:
![weather_markov]({{ site.baseurl }}/img/posts/speeding_commuters/Markov_Chain_weather_model_matrix_as_a_graph.png)

This can be represented mathematically as a [transition matrix](https://en.wikipedia.org/wiki/Stochastic_matrix).  In this matrix, the row represents the current state, and each column represents the next state.  The number at the each intersection is the probability of transitioning from that row's state to that columns's state.  Here is the above model as a matrix:

$$
T = 
\begin{matrix}
    &
    \begin{matrix}
    S & R
    \end{matrix}
    \\
    \begin{matrix}
    S \\ R
    \end{matrix}
    &
    \begin{bmatrix}
    0.9 & 0.1 \\
    0.5 & 0.5
    \end{bmatrix}
\end{matrix}
$$

This accounts for observations 1 & 2 above, but why do we care about observation 3?

### Absorbing State

OIur last observation was important because it means we can use an even more specific Markov chain called an [Absorbing Markov chain](https://en.wikipedia.org/wiki/Absorbing_Markov_chain).  A chain is abosorbing if:
* it has an "absorbing" state, which is one that cannot be left once it's entered.
* that absorbing state can be reached from any other state in a finite number of steps.

## Probability of getting a ticket

This leads to an important part of this solution, how do we get this matrix for our problem?

If we take a random initial state: `[1, 1, 2, 0]`, let's calculate the probability of Driver A receiving another ticket on the next trip (`[2, 1, 2, 0]`).  We know that at the start of the trip, a driver is randomly selected from those with fewer than three tickets.  In this case, all drivers are eligable, so Driver A has a 25% chance of being selected.  If Driver A is selected, there is a 10% chance that they receive a ticket.  .25 * .10 = .025.  The probability of transitioning from `[1, 1, 2, 0]` -> `[2, 1, 2, 0]` is 0.025.

So we can create a function that calculates these probabilities for any two states.  Transitions are only possible between two states where exactly 1 ticket has been issued to exactly 1 driver, or no tickets have been issued.  Any other transitions has 0 probability.

The probability that no ticket has been issued can be found by adding all the probabilities that tickets have been issued, and subtracting that from 1.


```python
import numpy as np
import itertools
from collections import Counter
from sympy import init_printing, Matrix
from sympy.physics.vector import vlatex
init_printing(latex_printer=vlatex, latex_mode='equation')
```


```python
def transition_probability(initial, final, ticket_probs, ticket_limit=3):
    initial = np.array(initial)
    final = np.array(final)
    num_drivers = len(ticket_probs)
    
    ticket_diff = np.subtract(final, initial)
    # probabilities are only calculated if exactly 1 driver's ticket count
    # has increased by exactly 1.  Other state transitions are impossible.
    # probabilities to remain in a state are calculated later.
    if  len(np.argwhere(ticket_diff == 1)) == 1 \
    and len(np.argwhere(ticket_diff == 0)) == num_drivers - 1:
        avail_drivers = len(np.argwhere(initial < ticket_limit))
        ticketed_driver_indx = np.argwhere(ticket_diff == 1)[0][0]
        return (1/avail_drivers) * ticket_probs[ticketed_driver_indx]
    else:
        return 0    
```

## Smaller example

Let's run through an example that might help tie everything together.  Instead of our original problem parameters, assume there are only Drivers A and B, and that licenses are suspended after 2 tickets instead of 3.  This will greatly reduce the number of possible states.


```python
max_tickets = 2
ticket_probs = np.array([0.10, 0.15])
num_drivers = len(ticket_probs)
```


```python
ticket_states = list(itertools.product(range(0, max_tickets+1), repeat=num_drivers))
num_ticket_states = len(ticket_states)
```

Here are all the possible ways that tickets could be distributed across our two drivers:

![states]({{ site.baseurl }}/img/posts/speeding_commuters/states.png)


```python
probability_matrix = np.zeros((num_ticket_states,num_ticket_states))

for row, start_state in enumerate(ticket_states):
    for col, end_state in enumerate(ticket_states):
        probability_matrix[row][col] = transition_probability(start_state,
                                                              end_state,
                                                              ticket_probs,
                                                              max_tickets)
        
for row,col in zip(*np.diag_indices_from(probability_matrix)):
    probability_matrix[row][col] = 1 - np.sum(probability_matrix[row])
```

![prob_mat]({{ site.baseurl }}/img/posts/speeding_commuters/prob_matrix.png)


```python
max_tickets = 3
ticket_probs = np.array([0.10, 0.15, 0.20, 0.25])
num_drivers = len(ticket_probs)
```


```python
ticket_states = list(itertools.product(range(0, max_tickets+1), repeat=num_drivers))
num_ticket_states = len(ticket_states)
```


```python
probability_matrix = np.zeros((num_ticket_states,num_ticket_states))

for row, start_state in enumerate(ticket_states):
    for col, end_state in enumerate(ticket_states):
        probability_matrix[row][col] = transition_probability(start_state,
                                                              end_state,
                                                              ticket_probs,
                                                              max_tickets)
        
for row,col in zip(*np.diag_indices_from(probability_matrix)):
    probability_matrix[row][col] = 1 - np.sum(probability_matrix[row])
```


```python
q = np.mat(probability_matrix[:-1,:-1])
i = np.identity(num_ticket_states - 1)
n = np.linalg.inv(i - q)
expected_trips_to_states = np.array(n * np.ones((num_ticket_states-1,1)))
expected_trips_to_all_suspended = expected_trips_to_states[0][0]
expected_days_to_all_suspended = expected_trips_to_all_suspended / 2
expected_days_to_all_suspended
```




$$38.5$$



http://www4.stat.ncsu.edu/~jaosborn/research/RISK.pdf    
http://www.datagenetics.com/blog/november12011/    
http://www.math.uiuc.edu/~bishop/monopoly.pdf


```python

```
