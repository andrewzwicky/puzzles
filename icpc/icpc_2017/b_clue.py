"""
Problem B
Get a Clue!
Time limit: 4 seconds

Developed in the 1940s in the United Kingdom, the game of Cluedo is one of the most popular board games in the world.
The object of the game is to determine who murdered Mr. Body, which weapon was used to murder him, and where the murder
took place. The game uses a set of cards representing six persons (labeled A, B, . . . , F), six weapons (labeled G, H,
. . . , L) and nine rooms (labeled M, N, . . . , U). At the start of the game, one person card, one weapon card, and 
one room card are selected at random and removed from the deck so no one can see them – they represent the murderer, 
the murder weapon, and the murder location. The remaining 18 cards are shuffled and dealt to the players, starting 
with player 1, then to her right player 2, and so on. Some players may end up with one more card than others. For the 
purposes of this problem there are four players, so the person to the right of player 4 is player 1.

The rest of the game is spent searching for clues. Players take turns, starting with player 1 and moving to the right. 
A turn consists of making a suggestion (consisting of a murder suspect, a weapon, and a room) and asking other players 
if they have any evidence that refutes the suggestion. For example, you might say to another player “I believe the 
murderer was person A, using weapon L, in room T.” If the other player is holding exactly one of these cards, that 
player must show you (and only you) that card. If they have more than one such card, they can show you any one of them. 
When making a suggestion, you must first ask the person to your right for any evidence. If they have none, you continue 
with the person on their right, and so on, until someone has evidence, or no one has any of the cards in your 
suggestion.

Many times you can gain information even if you are not the person making the suggestion. Suppose, in the above 
example, you are the third player and have cards A and T. If someone else shows evidence to the suggester, you know 
that it must be weapon card L. Keeping track of suggestions and who gave evidence at each turn is an important strategy 
when playing the game. To win the game, you must make an accusation, where you state your final guess of the murderer, 
weapon, and room. After stating your accusation, you check the three cards that were set aside at the start of the game 
– if they match your accusation, you win! Needless to say, you want to be absolutely sure of your accusation before you
make it.

Here is your problem. You are player 1. Given a set of cards dealt to you and a history of suggestions and evidence, 
you need to decide how close you are to being able to make an accusation.

Input
The input starts with an integer n (1 ≤ n ≤ 50), the number of suggestions made during the game. Following this is a 
line containing the five cards you are dealt, all uppercase letters in the range ‘A’. . . ‘U’. The remaining n lines 
contain one suggestion per line. Each of these lines starts with three characters representing the suggestion (in the 
order person, weapon, room), followed by the responses of up to three players, beginning with the player to the right 
of the player making the suggestion. If a player presents no evidence, a ‘-’ (dash) is listed; otherwise an “evidence 
character” is listed. If the specific evidence card is seen by you (either because you provided it or you were the 
person receiving the evidence) then the evidence character identifies that card; otherwise the evidence character is 
‘*’. Note that only the last response can be an evidence character. All characters are separated by single spaces. 
Only valid suggestion/response sequences appear in the input.

Output
Display a three character string identifying the murderer, the murder weapon, and the room. If the murderer can be 
identified, use the appropriate letter for that person; otherwise use ‘?’. Do the same for the murder weapon and the 
room.
"""

from copy import deepcopy
from itertools import cycle

SUSPECTS = set('ABCDEF')
WEAPONS = set('GHIJKL')
ROOMS = set('MNOPQRSTU')
ALL_CARDS = SUSPECTS | WEAPONS | ROOMS


def parse_input(inp_string):
    cards, *guesses = [''.join(l.split(' ')) for l in inp_string.split('\n')[1:]]
    guesses = [(set(g.strip(' ')[:3]), g.strip(' ')[3:]) for g in guesses]
    return set(cards), guesses


def process_guesses(cards, guesses, num_others=3):
    suspect = set()
    weapon = set()
    room = set()

    player_cards = [cards] + [set() for _ in range(num_others)]
    player_not_cards = [ALL_CARDS - cards] + [set(cards) for _ in range(num_others)]

    while True:
        prev_player_cards = deepcopy(player_cards)
        for player_turn, (guess, reveals) in zip(cycle(range(4)), guesses):
            for player, reveal in enumerate(reveals):
                player_index = (player_turn + player + 1) % 4

                if reveal == '-':
                    player_not_cards[player_index].update(guess)

                elif reveal in ALL_CARDS:
                    player_cards[player_index].update(reveal)
                    [cards.update(reveal) for i, cards in enumerate(player_not_cards)
                     if i != player_index]

                elif reveal == '*':
                    # if two cards are known to not be remaining, we know the last card
                    possibles = guess - player_not_cards[player_index]
                    if len(possibles) == 1:
                        reveal = possibles
                        player_cards[player_index].update(reveal)
                        [cards.update(reveal) for i, cards in enumerate(player_not_cards)
                         if i != player_index]

        # either players have all cards except 1
        # or all cards except 1 have been proved to not be held
        none_have = set.intersection(*player_not_cards)

        if none_have:
            suspect = SUSPECTS & none_have
            weapon = WEAPONS & none_have
            room = ROOMS & none_have

        if not suspect:
            possibles = SUSPECTS - set.union(*player_cards)
            if len(possibles) == 1:
                suspect = possibles

        if not weapon:
            possibles = WEAPONS - set.union(*player_cards)
            if len(possibles) == 1:
                suspect = possibles

        if not room:
            possibles = ROOMS - set.union(*player_cards)
            if len(possibles) == 1:
                suspect = possibles

        if (suspect and weapon and room) or \
                all([p == o for p, o in zip(prev_player_cards, player_cards)]):
            # we have solution or
            # no new info was learned
            break

    outp = "{}{}{}".format(suspect.pop() if suspect else '?',
                           weapon.pop() if weapon else '?',
                           room.pop() if room else '?')
    return outp


def b_clue(inp_string):
    return process_guesses(*parse_input(inp_string))
