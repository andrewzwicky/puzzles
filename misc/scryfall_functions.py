import textwrap
import requests
from colored import bg, attr
import string
from collections import defaultdict
import difflib
import itertools


def compare_strings(name_1, name_2):
    print(f'"{name_1}" vs. "{name_2}"')
    n1_set = set(name_1.lower().replace(' ', ''))
    n2_set = set(name_2.lower().replace(' ', ''))

    in_both = n1_set & n2_set
    in_both_spaced = ''.join(l if l in in_both else ' ' for l in string.ascii_lowercase)

    print(f"     both: {in_both_spaced}")

    in_neither = set(string.ascii_lowercase)
    in_neither -= n1_set
    in_neither -= n2_set

    in_neither_spaced = ''.join(l if l in in_neither else ' ' for l in string.ascii_lowercase)

    print(f"  neither: {in_neither_spaced}")

    substring = longest_substring(name_1.lower(), name_2.lower())
    if len(substring) > 1:
        print(f"substring: '{substring}'")
    print()


# https://stackoverflow.com/a/18717762/2597564
def longest_substring(string1, string2):
    string1 = string1.lower()
    string2 = string2.lower()
    a,b,size = difflib.SequenceMatcher(a=string1, b=string2).find_longest_match(0, len(string1), 0, len(string2))

    return string1[a:a+size]


class Card:
    def __init__(self, card, targets=()):
        self.json = defaultdict(str, card)
        self.bg_color = ''
        self.name = self.json['name']
        if self.name in targets:
            self.bg_color = bg('deep_sky_blue_3a')
        self.artist = self.json['artist']
        self.set = self.json['set']
        self.power = self.json['power']
        self.toughness = self.json['toughness']
        self.pt = ''
        if self.power or self.toughness:
            self.pt = f'{self.power}/{self.toughness}'
        self.type = self.json['type_line']
        self.rarity = self.json['rarity']
        self.oracle = self.json['oracle_text'].replace('\n', '')
        self.flavor = self.json['flavor_text'].replace('\n', '')
        self.cost = self.json['mana_cost'].replace('{', '').replace('}', '')
        self.identity = ''.join(self.json['color_identity'])
        self.cmc = int(card['cmc'])
        self.FORMAT = f'{self.bg_color}' \
                      f'{self.name:<35.34}' \
                      f'{self.identity:<6}' \
                      f'{self.artist:<20.19}' \
                      f'{self.set:<4.3}' \
                      f'{self.rarity[0]:<2.1}' \
                      f'{self.cmc:<3}' \
                      f'{self.cost:<10}' \
                      f'{self.type:<40.39}' \
                      f'{self.pt}' \
                      f'{attr("reset")}'

    def print(self, verbose):
        print(self.FORMAT)
        if verbose:
            self.print_text()

    def print_text(self):
        wrapped_oracle = textwrap.wrap(self.oracle, width=50)
        wrapped_flavor = textwrap.wrap(self.flavor, width=50)

        for o_text, f_text in itertools.zip_longest(wrapped_oracle, wrapped_flavor, fillvalue=''):
            print(f"    {o_text:<50.50}    {f_text:<50.50}")
        print()


class Query:
    API = "https://api.scryfall.com/cards/search"

    def __init__(self, query='', targets=None, verbose=False, details=False):
        self.query = query
        self.response = None
        self.json = None
        self.total_cards = 0
        self.warnings = []
        self.cards = []
        self.targets = [] if targets is None else targets
        self.details = details
        self.verbose = verbose or details
        if self.details:
            if len(targets) == 2:
                self.query = f'(!"{targets[0]}") or (!"{targets[1]}")'
                self.targets = []
            else:
                raise ValueError("Enter a query that returns 2 cards only.")

    def execute(self):
        print("Query Length: {}".format(len(self.query)))
        self.run()
        self.parse_json()
        self.print_warnings()
        self.print_total_cards()
        self.parse_cards()
        self.print_cards()
        if self.details:
            self.print_details()

    def run(self):
        self.response = requests.get(self.API, params={'q': self.query})

    def parse_json(self):
        self.json = self.response.json()

    def print_warnings(self):
        try:
            self.warnings = self.json['warnings']
            for warn in self.warnings:
                print(' WARN: {}'.format(warn))
        except KeyError:
            pass

    def print_total_cards(self):
        self.total_cards = self.json['total_cards']
        print(' Total Cards: {}'.format(self.total_cards))

    def parse_cards(self):
        for card_json in self.json['data']:
            card = Card(card_json, self.targets)
            self.cards.append(card)

    def print_cards(self):
        for card in self.cards:
            card.print(verbose=self.verbose)

    def print_details(self):
        if len(self.cards) == 2:
            print()
            print("NAME")
            compare_strings(self.cards[0].name, self.cards[1].name)
            print("ARTIST")
            compare_strings(self.cards[0].artist, self.cards[1].artist)
            print("TYPE")
            compare_strings(self.cards[0].type, self.cards[1].type)
            print("ORACLE")
            compare_strings(self.cards[0].oracle, self.cards[1].oracle)
            print("FLAVOR")
            compare_strings(self.cards[0].flavor, self.cards[1].flavor)

        else:
            raise ValueError("Enter a query that returns 2 cards only.")

if __name__ == '__main__':
    Query('tor a:g -f year>2010', targets=['Crow Storm']).execute()
