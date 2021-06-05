#!/usr/bin/env python
# Copyright (2021) by Jay M. Coskey

from datetime import datetime
import matplotlib.cm
import matplotlib.pyplot as plt
import numpy as np
import os

from dlx import DLX
from exact_cover_problem import ExactCoverProblem
from layout_info import Linfo


# Using Golomb's pentomino names, not Conways
class Block2DProblem(ExactCoverProblem):
    def __init__(self):
        pass

    def _get_prob_matrix(self):
        def _init_prob_row(row, block_index, layout, pos, pos2col):
            i, j = pos
            row[block_index] = True
            for row_index, layout_row in enumerate(layout):
                for col_index, val in enumerate(layout_row):
                    if val:
                        row[pos2col[i+row_index, j+col_index]] = True

        assert(self.board is not None)
        assert(self.blocks is not None)

        block_count = len(self.blocks)
        board_cell_count = np.nonzero(self.board)[0].size
        columns_count = block_count + board_cell_count

        # Assign ordinal values to the positions of the board.
        # Reserve the first N columns for the block_count blocks,
        #     then assign subsequent ordinals to playable board spaces,
        #     proceeding left-to-right, then top-to-bottom.
        pos2col = (block_count - 1
                   + np.cumsum(self.board).reshape(self.board.shape))

        rows = []
        for bi, block in enumerate(self.blocks):
            for layout in block.layouts:
                for pos in self.valid_positions(layout):
                    row = np.zeros(columns_count, dtype=np.bool)
                    _init_prob_row(row, bi, layout, pos, pos2col)
                    rows.append(row)

        prob_matrix = np.array(rows, dtype=np.bool)
        return prob_matrix

    def linfos(self):
        """Row ids, which tie the numerical results to the original problem
        The return value at problem setup must match those post-solution.
        """
        result = []
        for bi, block in enumerate(self.blocks):
            for li, layout in enumerate(block.layouts):
                for pos in self.valid_positions(layout):
                    result.append(Linfo(name=block.name,
                                        block_index=bi,
                                        layout_index=li,
                                        pos=pos))
        return result

    def plot_solution(self,
                      solution,
                      plot_filename=None,
                      do_save_plot=True,
                      do_display=True):
        def blocknum2color(block_index):
            return matplotlib.cm.rainbow(block_index / float(len(self.blocks)))

        if plot_filename is None:
            plot_filename = self.get_filename(self.name, 'plot')
        color_mat = np.zeros((self.board.shape[0], self.board.shape[1], 4))
        linfos = self.linfos()

        for lid in solution:
            linfo = linfos[lid]
            block_index = linfo.block_index
            layout_index = linfo.layout_index
            pos0, pos1 = linfo.pos
            layout = self.blocks[block_index].layouts[layout_index]
            color = blocknum2color(block_index)
            for lay0, linfo in enumerate(layout):
                for lay1, val in enumerate(linfo):
                    if val:
                        color_mat[pos0 + lay0, pos1 + lay1] = color

        plt.figure(num=self.name)
        plt.imshow(color_mat, interpolation='nearest')
        plt.axis('off')
        fig = plt.gcf()
        if do_display:
            plt.show()
        if do_save_plot:
            fig.savefig(fname=plot_filename, format='jpg')

    def set_solutions(self, solns):
        self.solutions = solns

    def solve(self,
              layouts_filename=None,
              linfos_filename=None,
              prob_filename=None,
              solns_filename=None,
              stats_filename=None,

              do_write_layouts=True,
              do_write_linfos=True,
              do_write_prob=True,
              do_write_solns=True,
              do_write_stats=True):
        name = self.name
        blocks = self.blocks
        linfos = self.linfos()
        prob_matrix = self.prob_matrix

        print('-' * 40)
        print(f'Solving problem: {name}')

        # TODO: Refactor to remove duplication and make concise?
        if layouts_filename is None:
            layouts_filename = self.get_filename(name, 'layouts')
        if linfos_filename is None:
            linfos_filename = self.get_filename(name, 'linfos')
        if prob_filename is None:
            prob_filename = self.get_filename(name, 'prob')
        if solns_filename is None:
            solns_filename = self.get_filename(name, 'solns')
        if stats_filename is None:
            stats_filename = self.get_filename(name, 'stats')

        # Assume all output files live in the same directory
        if '/' in os.path.relpath(prob_filename):
            os.makedirs(os.path.dirname(prob_filename), exist_ok=True)

        if do_write_layouts:
            with open(layouts_filename, 'w') as f:
                for bi, block in enumerate(blocks):
                    block.print(f'#{bi}', file=f)
        if do_write_linfos:
            with open(linfos_filename, 'w') as f:
                for li, linfo in enumerate(linfos):
                    f.write(f'{li}: {linfo}\n')
        if do_write_prob:
            self.io_write_prob_matrix(prob_matrix, prob_filename)

        dlx = DLX(name, prob_matrix)
        solns = dlx.find_solutions()

        if do_write_solns:
            self.io_write_solutions(solns, solns_filename)
        if do_write_stats:
            stats_filename = self.get_filename(name, 'stats')
            with open(stats_filename, 'a+') as f:
                datestamp = datetime.now().replace(microsecond=0).isoformat()
                updates_attr = f'updates={dlx.update_count}'
                solns_attr = f'solns={len(solns)}'
                elapsed_attr = f'elapsed={dlx.elapsed}'
                attrs = f'{updates_attr}, {solns_attr}, {elapsed_attr}'
                f.write(f'{datestamp}: {name}: {attrs}\n')

        return solns

    def valid_positions(self, layout):
        def is_valid_position(layout, pos):
            pos0, pos1 = pos
            lay0, lay1 = layout.shape

            region = self.board[pos0:pos0+lay0, pos1:pos1+lay1]
            return (region.shape == layout.shape
                    and np.array_equal(layout, layout & region))

        result = [(i, j)
                  for i in range(self.board.shape[0])
                  for j in range(self.board.shape[1])
                  if is_valid_position(layout, (i, j))
                  ]
        return result
