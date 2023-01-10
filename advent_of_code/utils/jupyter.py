import time

from IPython.core.magic import Magics, cell_magic, magics_class

import advent_of_code.utils as utils


@magics_class
class AOCMagic(Magics):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shell.run_cell("import advent_of_code.utils")

    @cell_magic
    def aoc(self, line, cell):
        day, part = map(int, line.split()[:2])

        inputs = utils.get_input(day)  # noqa
        answer = None  # noqa

        self.shell.push(["inputs", "answer"])

        time_start = time.time()
        self.shell.run_cell(cell)
        exec_time = time.time() - time_start

        result = self.shell.ev("answer")

        print(f"Execution time: {exec_time:.2g} seconds")

        if result:
            if utils.check_answer(result, day, part):
                print("Correct!")
            else:
                print("Wrong!")

        #TODO: if succesful, save to file and run test.
        #      If it succeeds, replace cell contents.
