#!/usr/bin/env python
# Copyright (2021) by Jay M. Coskey

import os
import sys

import numpy as np

from block2d import Block2D, pentominos
from block2d_problem import Block2DProblem
from exact_cover_problem import io_read_prob_matrix


month_names = """Jan Feb Mar Apr May Jun
                 Jul Aug Sep Oct Nov Dec""".split()
days_per_month = [31, 29, 31, 30, 31, 30,  31, 31, 30, 31, 30, 31]


DO_RESTRICT_DATES = True


# Month values: 0 .. 11
# Day values: 1 .. 31
class CalendarBlockProblem(Block2DProblem):
    def __init__(self, month, day):
        def date_str(month, day):
            return f'{month_names[month]}{day:02}'

        self.month = month
        self.day = day
        if month == 0 and day == 0:
            self.blocks = self._get_blocks()
            self.board = self._get_board()
            self.prob_matrix = None
            # Can now call self.load_prob(prob_filename)
            return

        assert(month in range(12))
        assert(day in range(31))

        self.name = date_str(month, day)
        self.blocks = self._get_blocks()
        self.board = self._get_board()
        self.prob_matrix = self._get_prob_matrix()

    def _get_blocks(self):
        calendar_pentominos = [b for b in pentominos if b.name in 'LNPUVYZ']
        block_o = Block2D('O', np.array(
                     [[1, 1, 1],
                      [1, 1, 1]]))
        return calendar_pentominos + [block_o]

    def _get_board(self):
        result = np.array(
            [[1, 1, 1, 1, 1, 1, 0],
             [1, 1, 1, 1, 1, 1, 0],
             [1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 0, 0, 0, 0]],
            dtype=np.bool)
        result[int(self.month / 6), self.month % 6] = 0
        d1 = self.day - 1
        result[2 + int(d1 / 7), d1 % 7] = 0
        return result

    def load_prob(self, prob_filename):
        basename = os.path.basename(prob_filename)
        assert(len(basename) == 10 and basename[0:5] == 'prob_')
        self.name = basename[5:]
        month_str = basename[5:5+3]
        self.month = CalendarBlockProblem.month_names.index(month_str)
        day_str = basename[-2:]
        self.day = int(day_str)
        self.prob_matrix = io_read_prob_matrix(prob_filename)

    def load_solns(self, solns_filename):
        self.solns = self.io_read_solutions(solns_filename)


def solve_calendar_problem(month, day, do_batch=False):
    prob = CalendarBlockProblem(month, day)
    solns = prob.solve()
    prob.plot_solution(solns[0], do_display=not do_batch)


def solve_calendar_problems(do_batch=False):
    def solve_month(month):
        for day in range(1, days_per_month[month] + 1):
            solve_calendar_problem(month, day, do_batch)

    for month in range(12):
        solve_month(month)


def usage():
    def eprint(foo):
        print(foo, file=sys.stderr)

    eprint(f'Unrecognized args: {sys.argv[1:]}')
    eprint('Usage: calendar_block_problem.py [Options]')
    eprint('Options:')
    eprint('\t* --batch: Run for all dates without displaying plot images')
    eprint('\t* --date MONTH DAY: Run for the specified date only')
    eprint('\t\tMONTH should be one of Jan, Feb, ... Dec')
    eprint('\t\tDAY should be an integer in the range 1 .. 31')
    eprint('Without no options, all dates are solved, and plots displayed')


if __name__ == '__main__':
    if len(sys.argv) == 1:
        solve_calendar_problems()
    elif len(sys.argv) == 2 and sys.argv[1] == '--batch':
        solve_calendar_problems(do_batch=True)
    elif len(sys.argv) == 4 and sys.argv[1] == '--date':
        month_str = sys.argv[2]
        day_str = sys.argv[3]
        months = [(m, name) for (m, name) in enumerate(month_names)
                  if name.lower() == month_str.lower()]
        day = int(day_str)

        has_error = False
        if not months:
            print(f'Error: Unrecognized month name: {month_str}')
        else:
            month = months[0][0]
            valid_day_range = (
                    range(1, days_per_month[month] + 1) if DO_RESTRICT_DATES
                    else range(1, 31 + 1)
                    )
            if day not in valid_day_range:
                if DO_RESTRICT_DATES:
                    msg = f'Dates for that month must range from 1 to {days_per_month[month]}'
                    printf(f'Error: {msg}')
                else:
                    printf(f'Error: Dates must range from 1 to 31')
            solve_calendar_problem(month, day)
    else:
        usage()
