---
layout:     post
title:      "Tickets"
date:       2017-05-19 10:00:00
author:     Andrew
header-img: img/posts/speeding_commuters/traffic_bg.jpg
header-credit: https://unsplash.com/@glebson
tags:       programming riddler probability
---

This week's [riddler](http://fivethirtyeight.com/features/the-battle-for-riddler-nation-round-2/) was a solid one, not too difficult, but still a challenge!

> From Jerry Meyers, a careening commute problem:  
> &nbsp;  
> Our co-workers carpool to work each day. A driver is selected randomly for the drive to work and again randomly for the drive home. Each of the drivers has a lead foot, and each has a chance of being ticketed for speeding. Driver A has a 10 percent chance of getting a ticket each time he drives, Driver B a 15 percent chance, Driver C a 20 percent chance, and Driver D a 25 percent chance. The state will immediately revoke the license of a driver after his or her third ticket, and a driver will stop driving in the carpool once his license is revoked. Since there is only one police officer on the carpool rout, a maximum of one ticket will be issued per morning and a max of one per evening.    
> &nbsp;  
> Assuming that all four drivers start with no tickets, how many days can we expect the carpool to last until all the drivers have lost their licenses?

# Observations
First, let's make some observations about the problem.  At the beginning of each trip, each driver will have some amount of tickets.  I'm going to refer to these amounts as a **state**.  For example, if Drivers A & B each had 1 ticket, I'll write that state as `[1, 1, 0, 0]`. The intial state is `[0, 0, 0, 0]`.

#### 1. There are a limited number of states
Each driver starts with 0 tickets and stops receiving them after their 3rd.  Because there is a cap on the amount of tickets, and a fixed number of drivers, there is a finite number of ways that tickets can be distributed amongst our drivers.

The actual number of states is the number of ways that 0, 1, 2, or 3 can be arranged, including repeats, across the 4 drivers.  With 4 possible ticket amounts over 4 drivers, this will result in $$4^4$$ or 256 unique states.

#### 2. The probability for a ticket to be issued depends only on the state at that time.
If Driver A and Driver B each have 1 ticket, the probability that Driver C will receive a ticket is the same no matter the order that A and B received their tickets.  The only factors that influence each driver's probability of receiving a ticket are:
* the number of drivers remaining (more drivers means it's less likely that any particular driver will be selected)
* their individual ticket probability


#### 3. The state where all drivers have received the maximum number of tickets can be reached from any other state
The end state is the one where all drivers have received their maximum number of tickets, `[3, 3, 3, 3]`.

If I selected a distribution of tickets at random, e.g. `[0, 1, 2, 0]`, it's possible to reach the end state by issuing tickets.  No matter which state we pick, we can always make our way to the end state.  This is probably the most abstract of all of these observations, but it's important to the solution, so stick around!

#### In summary:
1. the number of states (ticket distributions) is finite.
2. the probability for a ticket to be issued depends only on the state at that time.
3. there is an end state that can be reached from any other state.

# Markov Chains

These observations lead me to think that describing this scenario as a [Markov chains](https://en.wikipedia.org/wiki/Markov_chain) might be a good method to solve this problem.  A *Markov process* is a process with some randomness that doesn't depend on previous state, i.e. it is "memoryless".  A *Markov chain* is a way to represent one of these processes, given it has a finite number of states.

As an example, let's pretend tomorrow's weather depends only on today's weather, and there are only two types of weather, **rainy** or **sunny**.  The weather follows these rules:
* If it's sunny today, tommorow's weather is: 
  * 90% likely sunny.
  * 10% likely rainy.
* If it's rainy today, tommorow's weather is: 
  * 50% likely sunny.
  * 50% likely rainy.

This can be visualized like this:
![weather_markov]({{ site.baseurl }}/img/posts/speeding_commuters/Markov_Chain_weather_model_matrix_as_a_graph.png)

and it can also be written as a [transition matrix](https://en.wikipedia.org/wiki/Stochastic_matrix).  In this matrix, each number represents the probability that, if the chain is currently in the state of the row, it will transition to the state in the column.  The weather model as a transition matrix is:

$$
T =
\begin{matrix}
 &
 \begin{matrix}
 S & R \\
 \end{matrix}
 \\
 \begin{matrix}
 S \\ R
 \end{matrix}
 &
  \begin{bmatrix}
 0.9 & \textbf{0.1} \\
 0.5 & 0.5 \\
 \end{bmatrix}
\end{matrix}
$$

The bolded entry in the matrix is highlighting that the probability to transition from **sunny** to **rainy** is 0.1.

## This relates how?
You might be wondering where this jump to Markov chains came from.  Hopefully I can tie the two things back together now so we can see how a Markov chain applies to our riddle.

How we can use Markov chains to our advantage is to set our riddle up as follows.  Take each possible state of ticket distribution, and make that a state in our Markov chain.  Because of observations **1** and **2** above, our process meets the criteria to be a proper Markov chain.  What this means is that if we calculated the probabilities to move between these states, we could make a transition matrix that represents the entire riddle, starting from 0 tickets to the time when all drivers are suspended.

What we need next is to explain why observation **3** is critical 

## Absorbing State

Our last observation was important because it allows us to use an even more specific Markov chain called an [Absorbing Markov chain](https://en.wikipedia.org/wiki/Absorbing_Markov_chain).  A chain is abosorbing if:
* it has an "absorbing" state, which is one that cannot be left once it's entered.  Our absorbing state is the end state, where each driver has the maximum number of tickets.
* that absorbing state can be reached from any other state in a finite number of steps.

The advantage of having an absorbing state, is that the transition matrix can be put into the following form (simplified because we only have 1 absorbing state): 

$$T =
\left(
\begin{array}{cc}
 Q & R\\
 [0 \dots 0] & 1
\end{array}
\right)$$    

* $$R$$ is an array of probabilities of entering the absorbing state from any of the other states
* $$Q$$ is the transition matrix between the non-absorbing states.
* $$[0 \dots 0]$$ just shows that the bottom row is all 0 except the last column

Observation **3** is critical because absorbing Markov chains have special properties that **allow for direct calculation of the expected number of steps to reach an absorbing state, starting from any other state**.  Because our absorbing state is that all drivers are suspended, and we can start with all drivers having 0 tickets, this is exactly what we're trying to calculate!

The fundamental matrix $$N$$ represents the expected number of times the chain is in the column state, given that the chain started in the row state.

$$N = (I - Q)^{-1}$$

$$I$$ is an [identity matrix](https://en.wikipedia.org/wiki/Identity_matrix) of the same size as $$Q$$

## Feeling lucky?

The next important part of our solution is calculating the probability that a driver receives a ticket.

We know that for each trip, there are $$x$$ available drivers, where $$x$$ is the number of drivers that do not have 3 tickets.  This means each driver has a $$\frac{1}{x}$$ chance of being selected to drive that trip.  Additionally, we know that each driver has a probability $$p$$ that they will receive a ticket *if they drive*.  This means that for each trip, *before the driver is selected*, the probability that an individual driver will be ticketed is $$\frac{1}{x} \times p$$. For example, assume the state is `[1, 1, 2, 0]`.  All 4 drivers are available, so $$x$$=4.  Driver C's $$p$$ is 0.20.  This makes Driver C's probability of receiving a ticket $$\frac{0.20}{4} = 0.05$$.

If the state was `[3, 1, 2, 0]` instead, Driver C would be more likely to receive a ticket because it's more likely they will be selected at random to drive!  Their ticket probability is now $$\frac{0.20}{3} = 0.067$$.

Because tickets cannot be taken away, and only 1 can be issued per trip, transitions are only possible between two states where exactly 1 ticket has been issued to exactly 1 driver, or no tickets have been issued.  The probability that no ticket will been issued can be found by adding all the probabilities that each individual driver will receive a ticket and subtracting that from 1.

# Give an example already!

Ok, that's enough theory for now.  To make things easier to view, let's modify the problem slightly.  Instead of our original problem parameters, assume there are only Drivers A and B (same probabilities), and that licenses are suspended after **2** tickets instead of 3.  This will reduce the number of possible states.

The possible states of ticket distribution amongst our two drivers are:
$$
\begin{array}{ccccccccc}
[0, 0] & [0, 1] & [0, 2] & [1, 0] & [1, 1] & [1, 2] & [2, 0] & [2, 1] & [2,2] \\
\end{array}
$$ 


All of the probabilities for transitioning are now calculated, and are show on the full Markov chain:
![ex_chain]({{ site.baseurl }}/img/posts/speeding_commuters/example_chain.png)

The resulting translation matrix for our scenario is:

![prob_mat]({{ site.baseurl }}/img/posts/speeding_commuters/prob_matrix.png)

We can double check that our translation matrix is plausible by confirming the following assumptions:
* there are no possible transitions that reduce the number of tickets
* there are no possible transitions that issue 2 tickers in 1 trip
* the end state can only be transitioned to from `[1, 2]` and `[2, 1]`
* rows sum to 1

Further breaking the translation matrix down into the fundamental matrix, we get the following submatrices
![prob_mat_canon]({{ site.baseurl }}/img/posts/speeding_commuters/prob_matrix_canonical.png)

![q_mat]({{ site.baseurl }}/img/posts/speeding_commuters/q_matrix.png)

![n_mat]({{ site.baseurl }}/img/posts/speeding_commuters/n_matrix.png)

![e_mat]({{ site.baseurl }}/img/posts/speeding_commuters/e_matrix.png)

This tells us that we should expect 33.33 trips, or ~16.5 days for both of our drivers to be suspended.  If both of our drivers started with 1 ticket, it would take exactly half as long, or a little over 8 days.

Now all that's left to do it perform this same analysis on the original problem parameters of 3 tickets and all the drivers.  Running through the numbers shows that we should expect all drivers to be suspended at **38.5 days**.

below is the python code I used to perform the number-crunching.


```python
import numpy as np
import itertools
from sympy import init_printing
from sympy.physics.vector import vlatex
init_printing(latex_printer=vlatex)
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


```python
def expected_days_all_suspended(max_tickets, ticket_probs):
    num_drivers = len(ticket_probs)
    
    ticket_states = list(itertools.product(range(0, max_tickets+1), repeat=num_drivers))
    num_ticket_states = len(ticket_states)
    
    probability_matrix = np.zeros((num_ticket_states,num_ticket_states))

    for row, start_state in enumerate(ticket_states):
        for col, end_state in enumerate(ticket_states):
            probability_matrix[row][col] = transition_probability(start_state,
                                                                  end_state,
                                                                  ticket_probs,
                                                                  max_tickets)

    for row,col in zip(*np.diag_indices_from(probability_matrix)):
        probability_matrix[row][col] = 1 - np.sum(probability_matrix[row])
        
    q = np.mat(probability_matrix[:-1,:-1])
    i = np.identity(num_ticket_states - 1)
    n = np.linalg.inv(i - q)
    
    expected_trips_to_states = np.array(n * np.ones((num_ticket_states-1,1)))
    return expected_trips_to_states[0][0] / 2 # 2 trips per day
```


```python
expected_days_all_suspended(2, [0.10, 0.15])
```




$$16.6666666667$$




```python
expected_days_all_suspended(3, [0.10, 0.15, 0.20, 0.25])
```




$$38.5$$



http://www4.stat.ncsu.edu/~jaosborn/research/RISK.pdf    
http://www.datagenetics.com/blog/november12011/    
http://www.math.uiuc.edu/~bishop/monopoly.pdf
