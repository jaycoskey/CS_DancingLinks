#!/usr/bin/env python
# Copyright (2021) by Jay M. Coskey

import numpy as np


class ExactCoverProblem:
    def get_filename(self, prob_name, category):
        result = f'{prob_name}/{category}_{prob_name}'
        if category == 'plot':
            result += '.png'
        return result

    def io_read_solutions(self, solns_filename):
        with open(solns_filename) as f:
            return [np.fromstring(line, dtype=np.int, sep=' ') for line in f]

    def io_write_prob_matrix(self, prob_matrix, prob_filename):
        np.savetxt(prob_filename, prob_matrix.astype(np.int), fmt='%r')

    def io_write_solutions(self, solns, solns_filename):
        with open(solns_filename, 'w') as f:
            def soln_repr(soln):
                return ' '.join(map(str, soln)) + '\n'
            solns_txt = map(soln_repr, solns)
            f.writelines(solns_txt)


def io_read_prob_matrix(prob_filename):
    return np.loadtxt(prob_filename)
