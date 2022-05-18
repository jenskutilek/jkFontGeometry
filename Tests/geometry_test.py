import pytest
import unittest

from random import random


from jkFontGeometry.geometry import half_point
from jkFontGeometry.geometry import intersect

from jkFontGeometry.geometry import (
    # get_cubic_point as get_cubic_point_slow,
    # get_quadratic_point as get_quadratic_point_slow,
    half_point as half_point_slow,
    intersect as intersect_slow,
)

from jkFontGeometry.beziertools import getPointOnCubic as get_cubic_point_slow
from jkFontGeometry.beziertools import getPointOnCubic as get_cubic_point


def random_point():
    return (
        (random() - 0.5) * 16384,
        (random() - 0.5) * 16384,
    )


intersect_lines = (
    (
        ((0, 0), (0, 10), (-1, 5), (1, 5)),
        (0.0, 5.0)
    ),
    (
        ((0, 0), (0, 10), (-1, 4), (1, 6)),
        (0.0, 5.0)
    ),
    (
        ((0, 0), (0, 10), (-1, 3), (1, 5)),
        (0.0, 4.0)
    ),
    (
        # Outside of defined line segments
        ((0, 0), (0, 10), (-1, 11), (1, 11)),
        (0.0, 11.0)
    ),
    (
        # Parallel lines vertical
        ((0, 0), (0, 10), (-1, 10), (-1, 11)),
        None
    ),
    (
        # Parallel lines horizontal
        ((2, 2), (4, 2), (-1, 4), (1, 4)),
        None
    ),
    (
        # Point with line
        ((2, 2), (2, 2), (1, 1), (2, 1)),
        None
    ),
)


class FastgeometryTests(unittest.TestCase):
    def test_half_point(self):
        from time import time
        points = [
            (
                random_point(),
                random_point(),
            )
            for _ in range(10000)
        ]

        start = time()
        for p0, p1 in points:
            _result = half_point(p0, p1)
        stop = time()
        print("Rs:", stop - start)

        start = time()
        for p0, p1 in points:
            _result = half_point_slow(p0, p1)
        stop = time()
        print("Py:", stop - start)

    def test_intersect(self):
        for line, intersection in intersect_lines:
            p0, p1, p2, p3 = line
            result = intersect(p0, p1, p2, p3)
            assert result == intersection

    def test_intersect_many(self):
        from time import time
        points = [
            (
                random_point(),
                random_point(),
                random_point(),
                random_point(),
            )
            for _ in range(10000)
        ]

        start = time()
        for p0, p1, p2, p3 in points:
            _result = intersect(p0, p1, p2, p3)
        stop = time()
        print("Rs:", stop - start)

        start = time()
        for p0, p1, p2, p3 in points:
            _result = intersect_slow(p0, p1, p2, p3)
        stop = time()
        print("Py:", stop - start)

    def test_get_cubic_point(self):
        from time import time
        points = [
            (
                random(),
                random_point(),
                random_point(),
                random_point(),
                random_point(),
            )
            for _ in range(10000)
        ]

        start = time()
        for t, p0, p1, p2, p3 in points:
            result = get_cubic_point(t, p0, p1, p2, p3)
        stop = time()
        print("Rs:", stop - start)

        start = time()
        for t, p0, p1, p2, p3 in points:
            _result = get_cubic_point_slow(t, p0, p1, p2, p3)
        stop = time()
        print("Py:", stop - start)
        # assert 0 == 1
