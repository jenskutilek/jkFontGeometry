import pytest
import unittest


from jkFontGeometry.beziertools import (
    getPointListForCubic,
)


intersect_lines = (
    (
        [0, 1],
        ((0, 0), (0, 10), (-1, 5), (1, 5)),
        [(0, 0), (1, 5)]
    ),
    (
        [0, 0.5, 1],
        ((0, 0), (1, 0), (2, 0), (3, 0)),
        [(0, 0), (1.5, 0), (3, 0)]
    ),
)


class BeziertoolsTests(unittest.TestCase):
    def test_getPointListForCubic(self):
        for ts, curve, results in intersect_lines:
            p0, p1, p2, p3 = curve
            result = getPointListForCubic(ts, p0, p1, p2, p3)
            assert result == results
