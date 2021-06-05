#!/usr/bin/env python
# Copyright (2021) by Jay M. Coskey

from collections import namedtuple


"""Layout info. Everything you need to know about the placement of a block
   A puzzle with N blocks has one of these Linfo objects for each block.
   Each Linfo stores the choice made of block, orientation, and placement.
   A solution then consists of N integers, where each solution integer
       is the ordinal number of a Linfo object in a canonical list.
"""
Linfo = namedtuple('Linfo', ['name', 'block_index', 'layout_index', 'pos'])
