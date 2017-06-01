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
from itertools import combinations

SUSPECTS = set('ABCDEF')
WEAPONS = set('GHIJKL')
ROOMS = set('MNOPQRSTU')
ALL_CARDS = SUSPECTS | WEAPONS | ROOMS

NUM_PLAYERS = 4


class Player:
    def __init__(self, max_cards):
        self.max_cards = max_cards
        self.cards = set()
        self.possible_groups = set()
        self.not_cards = set()

    def has_cards(self, cards):
        cards = set(cards)
        self.cards |= cards
        self.not_cards -= cards

    def doesnt_have_cards(self, cards):
        cards = set(cards)
        self.possible_groups = set(frozenset(p - cards) for p in self.possible_groups)
        self.possible_groups.discard(frozenset())
        self.not_cards |= cards

    def add_possible_group(self, p_group):
        self.possible_groups.add(frozenset(p_group))

    def all_possibles(self):
        result = set()
        [result.update(p_group) for p_group in self.possible_groups]
        return result

    def __eq__(self, other):
        return self.cards == other.cards and \
               self.not_cards == other.not_cards and \
               self.possible_groups == other.possible_groups


def parse_input(inp_string):
    cards, *guesses = [''.join(l.split(' ')) for l in inp_string.split('\n')[1:]]
    guesses = [(set(g.strip(' ')[:3]), g.strip(' ')[3:]) for g in guesses]
    return set(cards), guesses


def process_guesses(cards, guesses):
    
    final_suspect = set()
    final_weapon = set()
    final_room = set()

    players = [Player(max_cards) for max_cards in [5, 5, 4, 4]]

    players[0].has_cards(cards)
    players[0].doesnt_have_cards(ALL_CARDS - cards)
    [player.doesnt_have_cards(cards) for i, player in enumerate(players) if i != 0]

    while True:
        prev_players = deepcopy(players)

        for turn_index, (guess, reveals) in zip(cycle(range(NUM_PLAYERS)), guesses):
            for player, reveal in enumerate(reveals, start=1):
                reveal_index = (turn_index + player) % 4

                if reveal == '-':
                    # add card to not_cards, remove from possibles
                    players[reveal_index].doesnt_have_cards(guess)

                elif reveal in ALL_CARDS:
                    # add to card, add to others not_cards, remove from other's possibles
                    players[reveal_index].has_cards(reveal)
                    [player.doesnt_have_cards(reveal) for i, player in enumerate(players) if i != reveal_index]

                elif reveal == '*':
                    # if two cards are known to not be remaining, we know the last card
                    possibles = guess - players[reveal_index].not_cards
                    if len(possibles) == 1:
                        players[reveal_index].has_cards(possibles)
                        [player.doesnt_have_cards(possibles) for i, player in enumerate(players) if i != reveal_index]
                    else:
                        players[reveal_index].add_possible_group(possibles)

        accounted = set()

        # look for triplets
        triplets = set.intersection(*[player.possible_groups for player in players[1:]])
        for trip in triplets:
            accounted |= trip

        # look for pairs
        for i, j in combinations(range(1, NUM_PLAYERS), 2):
            overlap_possible_groups = players[i].possible_groups & players[j].possible_groups
            for p_group in overlap_possible_groups:
                if len(p_group) == 2:
                    accounted |= p_group
                    for k in range(NUM_PLAYERS):
                        if k != i and k != j:
                            players[k].doesnt_have_cards(p_group)

        for j in range(1, NUM_PLAYERS):
            for p_group in set(players[j].possible_groups): # call with set to avoid modifying while iterating
                if len(p_group) == 1:
                    players[j].has_cards(p_group)
                    players[j].possible_groups.discard(p_group)
                    [player.doesnt_have_cards(p_group) for i, player in enumerate(players) if i != j]

        none_have = set.intersection(*[player.not_cards for player in players])

        suspects = SUSPECTS & none_have
        weapons = WEAPONS & none_have
        rooms = ROOMS & none_have

        if suspects:
            final_suspect = suspects.pop()

        if weapons:
            final_weapon = weapons.pop()

        if rooms:
            final_room = rooms.pop()

        [accounted.update(player.cards) for player in players]

        if final_suspect:
            [player.doesnt_have_cards(final_suspect) for i, player in enumerate(players) if i != j]
        else:
            suspects = SUSPECTS - accounted
            if len(suspects) == 1:
                final_suspect = suspects.pop()
                [player.doesnt_have_cards(final_suspect) for i, player in enumerate(players) if i != j]
        
        if final_weapon:
            [player.doesnt_have_cards(final_weapon) for i, player in enumerate(players) if i != j]
        else:
            weapons = WEAPONS - accounted
            if len(weapons) == 1:
                final_weapon = weapons.pop()
                [player.doesnt_have_cards(final_weapon) for i, player in enumerate(players) if i != j]

        if final_room:
            [player.doesnt_have_cards(final_room) for i, player in enumerate(players) if i != j]
        else:
            rooms = ROOMS - accounted
            if len(rooms) == 1:
                final_room = rooms.pop()
                [player.doesnt_have_cards(final_room) for i, player in enumerate(players) if i != j]

        possibles_remaining = suspects | weapons | rooms

        for j in range(1, NUM_PLAYERS):
            if len(players[j].cards) < players[j].max_cards:
                possible_possibles = possibles_remaining - players[j].not_cards
                if len(possible_possibles) == 1:
                    players[j].has_cards(possible_possibles)
                    [player.doesnt_have_cards(final_room) for i, player in enumerate(players) if i != j]

        solution_found = final_suspect and final_weapon and final_room
        no_changes = all([p == o for p, o in zip(prev_players, players)])

        if solution_found or no_changes:
            break

    outp = "{}{}{}".format(final_suspect if final_suspect else '?',
                           final_weapon if final_weapon else '?',
                           final_room if final_room else '?')
    return outp


def b_clue(inp_string):
    return process_guesses(*parse_input(inp_string))
