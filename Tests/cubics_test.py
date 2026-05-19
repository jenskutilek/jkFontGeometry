import unittest

import pytest

from fontgeometry.cubics import Cubic, SuperCubic


class CubicTests(unittest.TestCase):
    def test_instantiation(self):
        c = Cubic((0, 0), (1, 1), (3, 1), (4, 0))
        assert isinstance(c, Cubic)
        assert c.pt1 == (0, 0)
        assert c.pt2 == (1, 1)
        assert c.pt3 == (3, 1)
        assert c.pt4 == (4, 0)


class SuperCubicTests(unittest.TestCase):
    def test_instantiation(self):
        sc = SuperCubic()
        assert isinstance(sc, SuperCubic)
