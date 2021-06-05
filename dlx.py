#!/usr/bin/env python
# Copyright (2021) by Jay M. Coskey
"""Implementation of Donald Knuth's Dancing Links algorithm.
   See https://www-cs-faculty.stanford.edu/~knuth/programs/dance.w
"""

import numpy as np
from nptyping import NDArray
import sys
import time

from exact_cover_problem import ExactCoverProblem, io_read_prob_matrix


class Node:
    def __init__(self, val=None):
        self.val = val
        self.L = self
        self.R = self
        self.U = self
        self.D = self
        self.C = self

    def __repr__(self):
        return repr(self.val)


class DLX(ExactCoverProblem):
    class NodeIterator:
        def __init__(self, matrix: NDArray, start: Node, stop: Node, nextf):
            self.matrix = matrix
            self.start = start
            self.stop = stop
            self.nextf = nextf
            self.node_iter = start

        def __iter__(self):
            return self

        def __next__(self):
            cur_iter = self.node_iter
            self.node_iter = self.nextf(self.node_iter)
            if cur_iter == self.stop:
                raise StopIteration()
            return cur_iter

    # --------------------
    # Initialization
    # --------------------
    def __init__(self, name, matrix: NDArray, do_prioritize_columns=True):
        self.name = name
        self.matrix = matrix
        self.do_prioritize_columns = do_prioritize_columns

        self.root = Node()
        self.solution = None  # Preserved across recursive calls to search()
        self.solutions = None

        col_count = matrix.shape[1]
        self._init_col_hdrs(col_count)
        for row_index, row in enumerate(matrix):
            self._init_row(row, row_index)

    def _get_node(self, col_id, row_index):
        node = Node(row_index)
        col_hdr = self.col_hdrs[col_id]
        col_hdr.size += 1

        node.D = col_hdr
        node.U = col_hdr.U

        col_hdr.U.D = node
        col_hdr.U = node

        node.C = col_hdr
        return node

    def _init_col_hdrs(self, col_count):
        self.col_hdrs = [Node(k) for k in range(col_count)]
        for col_hdr in self.col_hdrs:
            col_hdr.size = 0

        hdr_iter = self.root  # Start at root
        for k in range(col_count):
            hdr_iter.R = self.col_hdrs[k]
            self.col_hdrs[k].L = hdr_iter
            hdr_iter = self.col_hdrs[k]  # Move to next col header

        # Make column header DLL circular
        if self.col_hdrs:
            self.col_hdrs[-1].R = self.root
            self.root.L = self.col_hdrs[-1]

    def _init_row(self, row, row_index):
        nonzero_indices = np.nonzero(row)[0]
        if nonzero_indices.size == 0:
            return

        first_node = self._get_node(nonzero_indices[0], row_index)
        node_iter = first_node

        for col_id in np.nonzero(row)[0][1:]:
            node = self._get_node(col_id, row_index)
            node_iter.R = node
            node.L = node_iter
            node_iter = node

        node_iter.R = first_node
        first_node.L = node_iter

    # --------------------
    # Iteration
    # --------------------
    def downward_node_iterator(self, start, stop):
        def nextf(node):
            return node.D
        return self.NodeIterator(self, start, stop, nextf)

    def leftward_node_iterator(self, start, stop):
        def nextf(node):
            return node.L
        return self.NodeIterator(self, start, stop, nextf)

    def rightward_node_iterator(self, start, stop):
        def nextf(node):
            return node.R
        return self.NodeIterator(self, start, stop, nextf)

    def upward_node_iterator(self, start, stop):
        def nextf(node):
            return node.U
        return self.NodeIterator(self, start, stop, nextf)

    # --------------------
    # Constraint methods
    # Each column in prob_matrix represents a covering-related constraint.
    # --------------------
    def remove_column(self, col_hdr: Node):
        """Knuth called this method "cover"."""
        col_hdr.R.L = col_hdr.L
        col_hdr.L.R = col_hdr.R

        for node_i in self.downward_node_iterator(
                start=col_hdr.D,
                stop=col_hdr):
            for node_j in self.rightward_node_iterator(
                    start=node_i.R,
                    stop=node_i):
                node_j.D.U = node_j.U  # Remove from vertical DLL
                node_j.U.D = node_j.D
                node_j.C.size -= 1

    # Knuth called this method "uncover".
    def restore_column(self, col_hdr: Node):
        """Knuth called this method "uncover"."""
        for node_i in self.upward_node_iterator(start=col_hdr.U, stop=col_hdr):
            for node_j in self.leftward_node_iterator(
                    start=node_i.L,
                    stop=node_i):
                node_j.C.size += 1
                node_j.D.U = node_j
                node_j.U.D = node_j

        col_hdr.R.L = col_hdr
        col_hdr.L.R = col_hdr

    # --------------------
    # Other methods
    # --------------------
    def find_solutions(self, do_print_stats=True):
        self.solution = []
        self.solutions = []
        self.update_count = 0  # Note: Incremented within search()

        start_time = time.perf_counter()
        self.search()
        stop_time = time.perf_counter()
        self.elapsed = stop_time - start_time

        if do_print_stats:
            print()
            print(f'Solutions found: {len(self.solutions):,}')
            print(f'    Update count: {self.update_count:,}')
            emins = int(self.elapsed / 60)
            esecs = round(self.elapsed) - 60 * emins
            print(f'    Time elapsed: {self.elapsed:.4f} ~ {emins}:{esecs:02}')

        return self.solutions

    def get_next_column(self):
        first_col_header = self.root.R
        if not self.do_prioritize_columns:
            return first_col_header

        mincol_size = sys.maxsize
        mincol = None

        col_iter = first_col_header
        while col_iter != self.root:
            if col_iter.size < mincol_size:
                mincol_size = col_iter.size
                mincol = col_iter
            col_iter = col_iter.R
        return mincol

    def search(self, depth=0):
        """Repeatedly satisfy columns, steadily accumulating the solution.
        Walk down the search tree with remove_column; up with restore_column.
        """
        # The problem representation is empty when there are no column headers,
        #     which occurs iff root is a degenerate DLL.
        # When the problem representation is empty, we have solution.
        is_empty = self.root.R == self.root
        if is_empty:
            self.solutions.append(np.array(self.solution))
            print('.', end='', flush=True)
            return

        col_hdr = self.get_next_column()
        self.update_count += 1
        self.remove_column(col_hdr)

        for node_i in self.downward_node_iterator(
                start=col_hdr.D,
                stop=col_hdr):
            self.solution.append(node_i.val)
            for node_j in self.rightward_node_iterator(
                    start=node_i.R,
                    stop=node_i):
                self.remove_column(node_j.C)
            self.search(depth+1)
            for node_j in self.leftward_node_iterator(
                    start=node_i.L,
                    stop=node_i):
                self.restore_column(node_j.C)
            self.solution.pop()

        self.restore_column(col_hdr)


if __name__ == '__main__':
    def main(name, prob_filename, solns_filename):
        matrix = io_read_prob_matrix(prob_filename)
        dlx = DLX(name, prob_filename, matrix)
        dlx.find_solutions()
        dlx.io_write_solutions(solns_filename)

    assert(len(sys.argv) == 3)
    prob_filename = sys.argv[1]
    solns_filename = sys.argv[2]
    # Assume that prob_filename begins with 'prob_'.
    main(prob_filename[5:], prob_filename, solns_filename)
