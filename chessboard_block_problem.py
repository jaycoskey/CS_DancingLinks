#!/usr/bin/env python
# Copyright (2021) by Jay M. Coskey

import sys

import numpy as np

from block2d import pentominos
from block2d_problem import Block2DProblem
from layout_info import Linfo


class ChessboardBlockProblem(Block2DProblem):
    """Data Scott's combinatorial chessboard problem and its variations"""
    def __init__(self, name):
        self.name = name
        self.blocks = pentominos
        self.board = np.array(
            [[1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 0, 0, 1, 1, 1],
             [1, 1, 1, 0, 0, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1]],
            dtype=np.bool)
        self.prob_matrix = self._get_prob_matrix()


# Provisional IDs used here for Data Scott's chessboard problems:
#   0 = Entire problem: 4x4 hole in center of chessboard,
#       but no further constraints on pentomino placement
#   1 = Scott's first sub-problem:  X at 23
#   2 = Scott's second sub-problem: X at 24
#   3 = Scott's third sub-problem:  X at 33, P not flipped
def mk_chessboard_block_problem(cb_id):
    if cb_id == 0:
        prob = ChessboardBlockProblem('chessboard_block_problem_full')
        return prob
    elif cb_id == 1:  # X at 23
        prob = ChessboardBlockProblem('chessboard_block_problem_sub1')
        constraint = np.array([linfo.name == 'X' and linfo.pos != (0, 1)
                               for linfo in prob.linfos()],
                              dtype=np.bool)
        prob.prob_matrix[constraint, :] = 0
        return prob
    elif cb_id == 2:  # X at 24
        prob = ChessboardBlockProblem('chessboard_block_problem_sub2')
        constraint = np.array([linfo.name == 'X' and linfo.pos != (0, 2)
                               for linfo in prob.linfos()],
                              dtype=np.bool)
        prob.prob_matrix[constraint, :] = 0
        return prob
    elif cb_id == 3:  # X at 33, P not flipped
        prob = ChessboardBlockProblem('chessboard_block_problem_sub3')
        xconstraint = np.array([linfo.name == 'X' and linfo.pos != (1, 1)
                                for linfo in prob.linfos()],
                               dtype=np.bool)
        pconstraint = np.array([linfo.name == 'P'
                                and linfo.layout_index % 2 == 0
                                for linfo in prob.linfos()],
                               dtype=np.bool)
        prob.prob_matrix[xconstraint, :] = 0
        prob.prob_matrix[pconstraint, :] = 0
        return prob
    else:
        raise ValueError(f'mk_chessboard_block_problem: cb_id={cb_id}')


def solve_chessboard_block_problem(k, do_batch=False):
    assert(0 <= k <= 3)
    expected_soln_count = {0: 520, 1: 19, 2: 20, 3: 26}
    prob = mk_chessboard_block_problem(k)
    solns = prob.solve()
    assert(len(solns) == expected_soln_count[k])
    prob.plot_solution(solns[0], do_display=not do_batch)


def solve_chessboard_block_problems(do_batch=False):
    for k in [1, 2, 3, 0]:
        solve_chessboard_block_problem(k, do_batch)


if __name__ == '__main__':
    do_batch = len(sys.argv) == 2 and sys.argv[1] == '--batch'
    solve_chessboard_block_problems(do_batch)
