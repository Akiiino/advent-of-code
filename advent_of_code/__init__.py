from advent_of_code import utils
from advent_of_code.utils.jupyter import AOCMagic


def load_ipython_extension(ipython):
    ipython.register_magics(AOCMagic)
