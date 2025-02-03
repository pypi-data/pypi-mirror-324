# -*- coding: utf-8 -*-
#
# This file is part of the Lima2 project
#
# Copyright (c) 2020-2024 Beamline Control Unit, ESRF
# Distributed under the MIT license. See LICENSE for more info.

"""Utility functions"""

import numpy as np


def docstring_from(parent):
    """Inherit the docstring from `parent`, overwriting the current one"""

    def decorated(child):
        child.__doc__ = parent.__doc__
        return child

    return decorated


class classproperty:
    """A decorator to create a class property from a class method.

    Example:
    ```
    class Rose:
        @classproperty
        def color(cls):
            return "RED"

    assert Rose.color == "RED"
    ```
    """

    def __init__(self, method):
        self.getter = method

    def __get__(self, instance, cls):
        """Getter called when the property is accessed. Calls the class method."""
        return self.getter(cls)


def find_first_gap(array: np.ndarray) -> int:
    """Find the index of the first element after a gap in a sorted array."""
    gap_idx = np.where(np.diff(array) > 1)[0]

    return gap_idx[0] + 1 if gap_idx.size > 0 else array.size
