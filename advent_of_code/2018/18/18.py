from pathlib import Path
import itertools
from collections import Counter, namedtuple, defaultdict
from pprint import pprint
import re
from datetime import datetime
import numpy as np
import functools
from copy import copy, deepcopy
from enum import Enum, IntEnum
from IPython.display import clear_output

data = Path('input.txt').read_text().splitlines()
#data = Path('test.txt').read_text().splitlines()

class Space(IntEnum):
    Open = 1
    Tree = 2
    Yard = 3

mapping = {'#': Space.Yard,
           '.':Space.Open,
           '|':Space.Tree}


rev_mapping = {Space.Yard:'#',
           Space.Open:'.',
           Space.Tree:'|'}
woods = np.zeros((len(data[0]), len(data)), dtype=int)

for y,row in enumerate(data):
    for x,s in enumerate(row):
        woods[y,x] = mapping[s]


for _ in range(10):

    new_woods = np.copy(woods)

    for y,x in np.ndindex(woods.shape):
        if woods[y,x] == Space.Open:
            surroundings = woods[max(y-1, 0):min(y+2, len(data)),max(x-1, 0):min(x+2, len(data))]
            counts = dict(zip(*np.unique(surroundings, return_counts=True)))
            if Space.Tree in counts.keys() and counts[Space.Tree] >= 3:
                new_woods[y,x] = Space.Tree
        elif woods[y,x] == Space.Tree:
            surroundings = woods[max(y-1, 0):min(y+2, len(data)),max(x-1, 0):min(x+2, len(data))]
            counts = dict(zip(*np.unique(surroundings, return_counts=True)))
            if Space.Yard in counts.keys() and counts[Space.Yard] >= 3:
                new_woods[y,x] = Space.Yard
        else:
            surroundings = woods[max(y-1, 0):min(y+2, len(data)),max(x-1, 0):min(x+2, len(data))]
            counts = dict(zip(*np.unique(surroundings, return_counts=True)))
            if Space.Yard in counts.keys() and counts[Space.Yard] >= 2 and Space.Tree in counts.keys(): # must count self
                new_woods[y,x] = Space.Yard
            else:
                new_woods[y, x] = Space.Open

    woods = new_woods
    counts = dict(zip(*np.unique(woods, return_counts=True)))
    print(_, counts.values())
    #for row in woods:
    #    print(''.join([rev_mapping[i] for i in row]))
    #print()

print(counts[Space.Tree] * counts[Space.Yard])

"""
700 dict_values([1546, 608, 346])
701 dict_values([1565, 589, 346])
702 dict_values([1587, 570, 343])
===
703 dict_values([1614, 567, 319])
704 dict_values([1625, 557, 318])
705 dict_values([1629, 551, 320])
706 dict_values([1643, 554, 303])
707 dict_values([1641, 553, 306])
708 dict_values([1641, 548, 311])
709 dict_values([1639, 542, 319])
710 dict_values([1647, 538, 315])
711 dict_values([1653, 540, 307])
712 dict_values([1644, 546, 310])
713 dict_values([1640, 554, 306])
714 dict_values([1636, 565, 299])
715 dict_values([1622, 576, 302])
716 dict_values([1607, 587, 306])
717 dict_values([1600, 599, 301])
718 dict_values([1584, 605, 311])
719 dict_values([1570, 608, 322])
720 dict_values([1571, 618, 311])
721 dict_values([1555, 628, 317])
722 dict_values([1540, 635, 325])
723 dict_values([1530, 642, 328])
724 dict_values([1531, 646, 323])
725 dict_values([1526, 644, 330])
726 dict_values([1528, 637, 335])
727 dict_values([1527, 628, 345])
728 dict_values([1546, 608, 346])
729 dict_values([1565, 589, 346])
730 dict_values([1587, 570, 343])
===
731 dict_values([1614, 567, 319])
732 dict_values([1625, 557, 318])
733 dict_values([1629, 551, 320])
734 dict_values([1643, 554, 303])
735 dict_values([1641, 553, 306])
736 dict_values([1641, 548, 311])
737 dict_values([1639, 542, 319])
738 dict_values([1647, 538, 315])
739 dict_values([1653, 540, 307])
740 dict_values([1644, 546, 310])
741 dict_values([1640, 554, 306])
742 dict_values([1636, 565, 299])
743 dict_values([1622, 576, 302])
744 dict_values([1607, 587, 306])
745 dict_values([1600, 599, 301])
746 dict_values([1584, 605, 311])
747 dict_values([1570, 608, 322])
748 dict_values([1571, 618, 311])
749 dict_values([1555, 628, 317])
750 dict_values([1540, 635, 325])
751 dict_values([1530, 642, 328])
752 dict_values([1531, 646, 323])
753 dict_values([1526, 644, 330])
754 dict_values([1528, 637, 335])
755 dict_values([1527, 628, 345])
756 dict_values([1546, 608, 346])
757 dict_values([1565, 589, 346])
758 dict_values([1587, 570, 343])
===
759 dict_values([1614, 567, 319])
760 dict_values([1625, 557, 318])
761 dict_values([1629, 551, 320])
762 dict_values([1643, 554, 303])
763 dict_values([1641, 553, 306])
764 dict_values([1641, 548, 311])
765 dict_values([1639, 542, 319])
766 dict_values([1647, 538, 315])
767 dict_values([1653, 540, 307])
768 dict_values([1644, 546, 310])
769 dict_values([1640, 554, 306])
770 dict_values([1636, 565, 299])
771 dict_values([1622, 576, 302])
772 dict_values([1607, 587, 306])
773 dict_values([1600, 599, 301])
"""