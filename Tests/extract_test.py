import unittest

import pytest

from fontgeometry.extract import CubicSegments


class CubicSegmentsTests(unittest.TestCase):
    def test_instantiate(self) -> None:
        cs = CubicSegments(layer=None)
        assert isinstance(cs, CubicSegments)

    def test_extract_segments(self) -> None:
        # Must be implemented in a subclass
        cs = CubicSegments(layer=None)
        with pytest.raises(NotImplementedError):
            cs.extract_segments()

    def test_to_supercubics(self) -> None:
        cs = CubicSegments(layer=None)
        cs.to_supercubics()
        assert cs.super_cubics == []
