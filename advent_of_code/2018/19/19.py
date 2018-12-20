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

data = Path('input.txt').read_text().splitlines()
data = Path('test.txt').read_text().splitlines()

print()