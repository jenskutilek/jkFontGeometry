import unittest

from fontgeometry.cubics import Cubic, SuperCubic


class CubicTests(unittest.TestCase):
    def test_instantiation(self):
        c = Cubic((0, 0), (1, 1), (3, 1), (4, 0))
        assert isinstance(c, Cubic)
        assert c.pt1 == (0, 0)
        assert c.pt2 == (1, 1)
        assert c.pt3 == (3, 1)
        assert c.pt4 == (4, 0)

    def test_extrema(self):
        c = Cubic((0, 0), (1, 1), (3, 1), (4, 0))
        assert c.extrema == [0.5]

    def test_extremum_points(self):
        c = Cubic((0, 0), (1, 1), (3, 1), (4, 0))
        assert c.extremum_points == [(2.0, 0.75)]

    def test_extremum_points_2(self):
        c = Cubic((4, 0), (5, 1), (7, 0), (8, 0))
        assert c.extremum_points == [(8, 0), (5.2592592592592595, 0.4444444444444444)]

    def test_inflections(self):
        c = Cubic((0, 0), (1, 1), (3, 0), (4, 0))
        assert c.inflections == [0.6972243622680054]

    def test_inflection_points(self):
        c = Cubic((0, 0), (1, 1), (3, 0), (4, 0))
        assert c.inflection_points == [(2.8721665810318613, 0.19175012845220896)]

    def test_inflections_none(self):
        c = Cubic((0, 0), (1, 1), (3, 1), (4, 0))
        assert c.inflections == []

    def test_inflection_points_none(self):
        c = Cubic((0, 0), (1, 1), (3, 1), (4, 0))
        assert c.inflection_points == []

    def test_length(self):
        c = Cubic((0, 0), (1, 1), (3, 1), (4, 0))
        assert c.length == 4.376310298502258

    def test_params(self):
        c = Cubic((0, 0), (1, 1), (3, 1), (4, 0))
        assert c.params == ((-2.0, 0.0), (3.0, -3.0), (3.0, 3.0), (0, 0))

    def test_raster_steps(self):
        c = Cubic((0, 0), (1, 1), (3, 1), (4, 0))
        assert c.raster_steps == 18

    def test_cubic_points_1(self):
        c = Cubic((0, 0), (1, 1), (3, 1), (4, 0), raster_length=1)
        assert c.cubic_points == [
            (0, 0),
            (0.90625, 0.5625),
            (2.0, 0.75),
            (3.09375, 0.5625),
            (4, 0),
        ]
        assert c.num_cubic_points == 4

    def test_cubic_points_2(self):
        c = Cubic((0, 0), (1, 1), (3, 1), (4, 0), raster_length=2)
        assert c.cubic_points == [(0, 0), (2.0, 0.75), (4, 0)]
        assert c.num_cubic_points == 2


class SuperCubicTests(unittest.TestCase):
    def test_instantiation(self):
        sc = SuperCubic()
        assert isinstance(sc, SuperCubic)

    def test_add_cubic_flat(self):
        sc = SuperCubic()
        sc.add_cubic_from_point_tuple([(0, 0), (3, 0)])
        c = sc.cubics[0]
        assert c.pt1 == (0, 0)
        assert c.pt2 == (1, 0)
        assert c.pt3 == (2, 0)
        assert c.pt4 == (3, 0)

    def test_extremum_points(self):
        sc = SuperCubic()
        sc.add_cubic_from_points((0, 0), (1, 1), (3, 1), (4, 0))
        sc.add_cubic_from_points((4, 0), (5, 1), (7, 0), (8, 0))
        assert sc.extremum_points == [
            (2.0, 0.75),
            (8, 0),
            (5.2592592592592595, 0.4444444444444444),
        ]

    def test_inflection_points(self):
        sc = SuperCubic()
        sc.add_cubic_from_points((0, 0), (1, 1), (3, 1), (4, 0))
        sc.add_cubic_from_points((4, 0), (5, 1), (7, 0), (8, 0))
        assert sc.inflection_points == [
            (6.872166581031861, 0.19175012845220896),
        ]

    def test_f_for_point(self):
        sc = SuperCubic()
        sc.add_cubic_from_points((0, 0), (1, 1), (3, 1), (4, 0))
        sc.add_cubic_from_points((4, 0), (5, 1), (7, 0), (8, 0))
        assert sc.t_for_point((4.5, 1)) == (0, 1.0)

    def test_split_at_pt(self):
        sc = SuperCubic()
        sc.add_cubic_from_points((0, 0), (1, 1), (3, 1), (4, 0))
        sc.add_cubic_from_points((4, 0), (5, 1), (7, 0), (8, 0))
        assert sc.split_at_pt((4.5, 1)) == (((0, 0), (1, 1), (3, 1), (4, 0)))
        assert sc.split_at_pt((4, 0)) == (((4, 0), (4, 0), (4, 0), (4, 0)))

    def test_split_at_pt_fast(self):
        sc = SuperCubic()
        sc.add_cubic_from_points((0, 0), (1, 1), (3, 1), (4, 0))
        sc.add_cubic_from_points((4, 0), (5, 1), (7, 0), (8, 0))
        assert sc.split_at_pt_fast((4.5, 1)) == (((0, 0), (1, 1), (3, 1), (4, 0)))
        assert sc.split_at_pt_fast((4, 0)) == (((4, 0), (4, 0), (4, 0), (4, 0)))
