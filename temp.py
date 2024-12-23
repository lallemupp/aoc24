import itertools
from itertools import repeat

from icecream import ic

import utils

if __name__ == '__main__':
    up = utils.permute(0, 1, 3)
    down = utils.permute(1, 0, 3)
    magic_lists = list(up + down)
    ic(list(magic_lists))