#!/usr/bin/env python
# Copyright (2021) by Jay M. Coskey

import sys

import numpy as np


class Block2D:
    def __init__(self, name, reference_layout):
        self.name = name
        self.reference_layout = reference_layout.astype(np.bool)
        self.layouts = self._get_layouts()

    # TODO: Refactor to reduce recurrence of "file=file".
    #   Originally this only printing to stdout, but was adapted for logging.
    def print(self, tag, file=sys.stdout):
        def as_int(x):
            return x.astype(np.int)

        def print_ndarray(ndarray, indent='', file=file):
            ndarray = as_int(ndarray)
            for row in ndarray:
                print(indent, end='', file=file)
                for item in row:
                    print(item, end='', file=file)
                print(file=file)

        print(f'block ({tag}): {self.name}', file=file)
        print('\treference_layout:', file=file)
        print_ndarray(self.reference_layout, indent='\t\t', file=file)
        for li, layout in enumerate(self.layouts):
            print(f'\tlayout #{li}:', file=file)
            print_ndarray(layout, indent='\t\t', file=file)
            print('\t\t--------------------', file=file)

    def _get_layouts(self):
        result = [self.reference_layout]

        for rot90s in [0, 1, 2, 3]:
            for do_flip in [False, True]:
                layout = self.layout(rot90s, do_flip)
                do_insert = not any(np.array_equal(layout, r) for r in result)
                if do_insert:
                    result.append(layout)
        return result

    def layout(self, rot90s, do_flip):
        result = self.reference_layout
        for i in range(rot90s):
            result = np.rot90(result)
        if do_flip:
            result = np.fliplr(result)
        return result


pentominos = [
    Block2D('F', np.array(
        [[0, 1, 1],
         [1, 1, 0],
         [0, 1, 0]])),
    Block2D('I', np.array(
        [[1],
         [1],
         [1],
         [1],
         [1]])),
    Block2D('L', np.array(
        [[1, 1],
         [0, 1],
         [0, 1],
         [0, 1]])),
    Block2D('P', np.array(
        [[1, 1],
         [1, 1],
         [1, 0]])),
    Block2D('N', np.array(
        [[1, 0],
         [1, 1],
         [0, 1],
         [0, 1]])),
    Block2D('T', np.array(
        [[1, 1, 1],
         [0, 1, 0],
         [0, 1, 0]])),
    Block2D('U', np.array(
        [[1, 0, 1],
         [1, 1, 1]])),
    Block2D('V', np.array(
        [[1, 0, 0],
         [1, 0, 0],
         [1, 1, 1]])),
    Block2D('W', np.array(
        [[1, 0, 0],
         [1, 1, 0],
         [0, 1, 1]])),
    Block2D('X', np.array(
        [[0, 1, 0],
         [1, 1, 1],
         [0, 1, 0]])),
    Block2D('Y', np.array(
        [[0, 1],
         [1, 1],
         [0, 1],
         [0, 1]])),
    Block2D('Z', np.array(
        [[1, 1, 0],
         [0, 1, 0],
         [0, 1, 1]]))
    ]

if __name__ == '__main__':
    for k, p in enumerate(pentominos):
        p.print(k)
