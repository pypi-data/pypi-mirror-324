# This file is part of the Lima2 project
#
# Copyright (c) 2020-2024 Beamline Control Unit, ESRF
# Distributed under the MIT license. See LICENSE for more info.

"""Test suite for utility functions (lima2/client/utils.py)"""

import numpy as np
from lima2.client.utils import docstring_from, find_first_gap


def test_docstring_from():
    def parent():
        """cafedeca"""
        pass

    @docstring_from(parent)
    def child():
        """deadbeef"""
        pass

    assert child.__doc__ == "cafedeca"


def test_find_first_gap():
    gap_idx = find_first_gap(array=np.array([1, 2, 3, 4, 6, 7, 9]))
    assert gap_idx == 4

    gap_idx = find_first_gap(array=np.array([0, 4, 5, 6, 7]))
    assert gap_idx == 1
