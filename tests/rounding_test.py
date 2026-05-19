import unittest

import pytest

from fontgeometry.rounding import round_hup


class CubicSegmentsTests(unittest.TestCase):
    def test_0(self) -> None:
        result = round_hup(0)
        assert result == 0
        assert isinstance(result, int)

    def test_0_float(self) -> None:
        result = round_hup(0.0)
        assert result == 0
        assert isinstance(result, int)

    def test_05_neg(self) -> None:
        result = round_hup(-0.5)
        assert result == -1
        assert isinstance(result, int)

    def test_10_neg(self) -> None:
        result = round_hup(-1.0)
        assert result == -1
        assert isinstance(result, int)

    def test_15_neg(self) -> None:
        result = round_hup(-1.5)
        assert result == -2
        assert isinstance(result, int)

    def test_25_neg(self) -> None:
        result = round_hup(-2.5)
        assert result == -3
        assert isinstance(result, int)

    def test_05(self) -> None:
        result = round_hup(0.5)
        assert result == 1
        assert isinstance(result, int)

    def test_10(self) -> None:
        result = round_hup(1.0)
        assert result == 1
        assert isinstance(result, int)

    def test_15(self) -> None:
        result = round_hup(1.5)
        assert result == 2
        assert isinstance(result, int)

    def test_25(self) -> None:
        result = round_hup(2.5)
        assert result == 3
        assert isinstance(result, int)
