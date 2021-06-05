#!/usr/bin/env python
# Copyright (2021) by Jay M. Coskey

import os
import sys

import numpy as np

from block2d import Block2D, pentominos
from block2d_problem import Block2DProblem
from exact_cover_problem import io_read_prob_matrix


# Month values: 0 .. 11
# Day values: 1 .. 31
class CalendarBlockProblem(Block2DProblem):
    month_names = """Jan Feb Mar Apr May Jun
                  Jul Aug Sep Oct Nov Dec""".split()
    def __init__(self, month, day):
        def date_str(month, day):
            assert(0 <= month <= 11)
            return f'{CalendarBlockProblem.month_names[month]}{day:02}'

        self.month = month
        self.day = day
        if month == 0 and day == 0:
            self.blocks = self._get_blocks()
            self.board = self._get_board()
            self.prob_matrix = None
            # Can now call self.load_prob(prob_filename)
            return

        assert(0 <= month <= 11)
        days_per_month = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        assert(0 <= day <= days_per_month[month])

        self.name = date_str(month, day)
        self.blocks = self._get_blocks()
        self.board = self._get_board()
        self.prob_matrix = self._get_prob_matrix()

    def _get_blocks(self):
        calendar_pentominos = [b for b in pentominos if b.name in 'LNUVYZ']
        block_a = Block2D('A', np.array([[1]]))
        block_b = Block2D('B', np.array(
                     [[1, 1],
                      [1, 1]]))
        block_c = Block2D('C', np.array(
                     [[1, 1, 1],
                      [1, 1, 1]]))
        return calendar_pentominos + [block_a, block_b, block_c]

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

    days_per_month = [31, 29, 31, 30, 31, 30,  31, 31, 30, 31, 30, 31]
    for month in range(12):
        solve_month(month)


if __name__ == '__main__':
    do_batch = len(sys.argv) == 2 and sys.argv[1] == '--batch'
    if len(sys.argv) == 1 or do_batch:
        solve_calendar_problems(do_batch)
    else:
        print(f'Unrecognized args: {sys.argv[1:]}')

    # TODO: Read in solutions from log files,
    #       including all info needed for interpretation,
    #       even if code has changed since the log files were generated.
    #
    # if len(sys.argv) == 4 and sys.argv[1] == '--plot_solns':
    #     prob_filename = sys.argv[2]
    #     solns_filename = sys.argv[3]
    #     prob = CalendarBlockProblem(0, 0)
    #     prob.load_prob(prob_filename)
    #     prob.load_solns(solns_filename)
    #     for soln in prob.solns:
    #         prob.plot_solution(soln,
    #                            plot_filename=None,
    #                            do_save_plot=False,
    #                            do_display=True)
