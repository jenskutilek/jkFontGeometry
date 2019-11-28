#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from jkFontGeometry.beziertools import estimateCubicCurveLength, \
    getInflectionsForCubic, getExtremaForCubic


DEBUG_SPLIT = False
use_scipy = False


if use_scipy:
    try:
        from scipy import spatial
        use_scipy = False
    except ImportError:
        use_scipy = False
        print("scipy is not available.")


# from time import time

from fontTools.misc.bezierTools import calcCubicParameters, solveCubic
from math import hypot


try:
    from jkFontGeometry._fastgeometry import get_cubic_point
except ImportError:
    print("Fast geometry extension not available, falling back to slower version.")
    from jkFontGeometry.beziertools import getPointOnCubic as get_cubic_point


class Cubic(object):

    def __init__(self, p0, p1, p2, p3, raster_length=0.25):
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

        # The estimated length of each distance if the cubic is converted to points
        self.raster_length = raster_length

        # The list of points on the cubic, with estimated raster_length distance
        self._cubic_points = None
        self._num_cubic_points = None

        # The calculated estimated curve length
        self._estimated_length = None

        # The number of steps to achieve the desired point distances
        self._raster_steps = None

        # The current split point (will be moved along the curve when splitting)
        self._t = 0.0

        # Cache for Cubic params (a, b, c, d)
        self._params = None

        # Cache for inflection points
        self._inflections = None
        self._inflection_points = None

        # Cache for extremum points
        self._extrema = None
        self._extremum_points = None

    def __repr__(self):
        return "<Cubic p0=%s, p3=%s>" % (self.p0, self.p3)

    @property
    def extrema(self):
        if self._extrema is None:
            self._extrema = self.calculate_extrema()
        return self._extrema

    @property
    def extremum_points(self):
        if self._extremum_points is None:
            self._extremum_points = self.calculate_extremum_points()
        return self._extremum_points

    @property
    def inflections(self):
        if self._inflections is None:
            self._inflections = self.calculate_inflections()
        return self._inflections

    @property
    def inflection_points(self):
        if self._inflection_points is None:
            self._inflection_points = self.calculate_inflection_points()
        return self._inflection_points

    @property
    def length(self):
        if self._estimated_length is None:
            self._estimated_length = estimateCubicCurveLength(self.p0, self.p1, self.p2, self.p3)
        return self._estimated_length

    @property
    def params(self):
        if self._params is None:
            self._params = calcCubicParameters(self.p0, self.p1, self.p2, self.p3)
        return self._params

    @property
    def raster_steps(self):
        if self._raster_steps is None:
            self._raster_steps = int(round(self.length / self.raster_length))
        return self._raster_steps

    @property
    def cubic_points(self):
        # Calculate or return the cached list of t to point mappings.
        if self._cubic_points is None:
            self._cubic_points = self.calculate_cubic_points()
            if use_scipy:
                self._num_cubic_points = len(self._cubic_points.data) - 1
            else:
                self._num_cubic_points = len(self._cubic_points) - 1
        return self._cubic_points

    @property
    def num_cubic_points(self):
        if self._num_cubic_points is None:
            self._cubic_points = self.calculate_cubic_points()
            if use_scipy:
                self._num_cubic_points = len(self._cubic_points.data) - 1
            else:
                self._num_cubic_points = len(self._cubic_points) - 1
        return self._num_cubic_points

    def calculate_cubic_points(self):
        # Return a dict of t values to point coordinates for the cubic curve
        # st = time()
        t_list = []
        if self.raster_steps < 2 or (self.p0 == self.p1) and (self.p2 == self.p3):
            t_list = [self.p0, self.p3]
        else:
            step = 1 / self.raster_steps
            t_list = [
                get_cubic_point(t * step, self.p0, self.p1, self.p2, self.p3)
                for t in range(0, self.raster_steps + 1)
            ]

        # et = time()
        # print("calculate_cubic_points: %0.3f ms" % ((et-st)*1000))
        if use_scipy:
            return spatial.KDTree(t_list)
        else:
            return t_list

    def calculate_extrema(self):
        return getExtremaForCubic(
            self.p0, self.p1, self.p2, self.p3,
            h=True,
            v=False,
            include_start_end=True
        )

    def calculate_extremum_points(self):
        return [get_cubic_point(t, self.p0, self.p1, self.p2, self.p3) for t in self.extrema]

    def calculate_inflections(self):
        # TODO: Inflections "between" segments
        return getInflectionsForCubic(self.p0, self.p1, self.p2, self.p3)

    def calculate_inflection_points(self):
        return [get_cubic_point(t, self.p0, self.p1, self.p2, self.p3) for t in self.inflections]

    def reset_split(self):
        self._t = 0.0

    def split_at_t(self, t):

        # From https://stackoverflow.com/questions/878862/drawing-part-of-a-bézier-curve-by-reusing-a-basic-bézier-curve-function

        # st = time()

        t0 = self._t
        t1 = t

        u0 = 1.0 - t0
        u1 = 1.0 - t1

        x1, y1 = self.p0
        bx1, by1 = self.p1
        bx2, by2 = self.p2
        x2, y2 = self.p3

        qxa =  x1 * u0 * u0 + bx1 * 2 * t0 * u0 + bx2 * t0 * t0
        qxb =  x1 * u1 * u1 + bx1 * 2 * t1 * u1 + bx2 * t1 * t1
        qxc = bx1 * u0 * u0 + bx2 * 2 * t0 * u0 +  x2 * t0 * t0
        qxd = bx1 * u1 * u1 + bx2 * 2 * t1 * u1 +  x2 * t1 * t1

        qya =  y1 * u0 * u0 + by1 * 2 * t0 * u0 + by2 * t0 * t0
        qyb =  y1 * u1 * u1 + by1 * 2 * t1 * u1 + by2 * t1 * t1
        qyc = by1 * u0 * u0 + by2 * 2 * t0 * u0 +  y2 * t0 * t0
        qyd = by1 * u1 * u1 + by2 * 2 * t1 * u1 +  y2 * t1 * t1

        xa = qxa * u0 + qxc * t0
        xb = qxa * u1 + qxc * t1
        xc = qxb * u0 + qxd * t0
        xd = qxb * u1 + qxd * t1

        ya = qya * u0 + qyc * t0
        yb = qya * u1 + qyc * t1
        yc = qyb * u0 + qyd * t0
        yd = qyb * u1 + qyd * t1

        self._t = t

        # et = time()
        # print("split_at_t: %0.3f ms" % ((et-st)*1000))

        return ((xa, ya), (xb, yb), (xc, yc), (xd, yd))


class SuperCubic(object):

    # Collection of multiple Cubic segments

    def __init__(self):
        self.cubics = []
        self._split_index = 0

        # The cached map of t to point
        self._t_points = {}

        # Keep track of current t for faster searching
        self._t_step = 0

        self._inflection_points = None
        self._extremum_points = None

    def __repr__(self):
        return "<SuperCubic len=%i>" % len(self.cubics)

    @property
    def inflection_points(self):
        # All inflection points from the sub-cubics
        if self._inflection_points is None:
            self._inflection_points = []
            for cubic in self.cubics:
                if cubic.inflection_points:
                    self._inflection_points.extend(cubic.inflection_points)
        return self._inflection_points

    @property
    def extremum_points(self):
        # All extremum points from the sub-cubics
        if self._extremum_points is None:
            self._extremum_points = []
            for cubic in self.cubics:
                if cubic.extremum_points:
                    self._extremum_points.extend(cubic.extremum_points)
        return self._extremum_points

    def add_cubic_from_points(self, p0, p1, p2, p3, raster_length=0.25):
        cubic = Cubic(p0, p1, p2, p3, raster_length)
        self.cubics.append(cubic)

    def add_cubic_from_point_tuple(self, point_tuple, raster_length=0.25):
        try:
            p0, p1, p2, p3 = point_tuple
        except ValueError:
            print("WARNING: Not a curve:", point_tuple)
            # Add a flat curve
            p0, p3 = point_tuple
            p1 = (p0[0] + 0.333333 * (p3[0] - p0[0]), p0[1] + 0.333333 * (p3[1] - p0[1]))
            p2 = (p0[0] + 0.666667 * (p3[0] - p0[0]), p0[1] + 0.666667 * (p3[1] - p0[1]))
        self.add_cubic_from_points(p0, p1, p2, p3, raster_length)

    def t_for_point(self, pt):
        # TODO: Cache previous pt so the search can start there?
        return self._t_points.get(pt, self.calculate_t_for_point(pt))

    def calculate_t_for_point(self, pt):
        # Calculate the t value for the closest distance of point pt to a series of cubic Beziers

        x, y = pt

        # Check special case: Is the point close to the first or last points of any of the cubics?

        for index in range(self._split_index, len(self.cubics)):
            cubic = self.cubics[index]
            p0x = round(cubic.p0[0])
            p0y = round(cubic.p0[1])
            p3x = round(cubic.p3[0])
            p3y = round(cubic.p3[1])
            # print("Quick check:", x, y, "in", p0x, p0y, p3x, p3y)

            if p0x - 1 <= x <= p0x + 1 and p0y - 1 <= y <= p0y + 1:
                self._split_index = index
                self._t_step = 0
                # tx, ty = get_cubic_point(0, cubic.p0, cubic.p1, cubic.p2, cubic.p3)
                # print("                Fast Found t = 0 -> (%0.3f, %0.3f)" % (tx, ty))
                return index, 0.0
            elif p3x - 1 <= x <= p3x + 1 and p3y - 1 <= y <= p3y + 1:
                self._split_index = index
                self._t_step = cubic.num_cubic_points
                # tx, ty = get_cubic_point(1, cubic.p0, cubic.p1, cubic.p2, cubic.p3)
                # print("                Fast Found t = 1 -> (%0.3f, %0.3f)" % (tx, ty))
                return index, 1.0

        # Take the long road

        # print("Need long calculation ...", self._split_index, len(self.cubics))
        prev_dist = None
        for index in range(self._split_index, len(self.cubics)):
            cubic = self.cubics[index]
            self._split_index = index
            if len(cubic.cubic_points) == 2:
                # Straight curve, use ratio of requested point to full line length
                p = cubic.cubic_points[0]
                px, py = p
                self._t_step = hypot(y - py, x - px) / cubic.length
                return index, self._t_step

            for step in range(self._t_step, cubic.num_cubic_points + 1):
                p = cubic.cubic_points[step]
                px, py = p
                dist = hypot(y - py, x - px)  # Point distance
                if prev_dist is not None:
                    if dist > prev_dist:
                        self._t_points[pt] = (index, step / cubic.num_cubic_points)
                        # print("                Searching for t in cubic %i from step %i to %i of %i ..." % (self._split_index, self._t_step, step, cubic.num_cubic_points))
                        # tx, ty = get_cubic_point(step / cubic.num_cubic_points, cubic.p0, cubic.p1, cubic.p2, cubic.p3)
                        # print("                Found t = %0.3f -> (%0.3f, %0.3f)" % (step / cubic.num_cubic_points, tx, ty))
                        self._t_step = step
                        return self._t_points[pt]
                prev_dist = dist
            self.reset_t()
            prev_dist = None
        # Nothing was found ...
        print("Could not find t for point %s in cubics %s" % (pt, self.cubics))
        return None

    if use_scipy:
        def calculate_t_for_point(self, pt):
            # Calculate the t value for the closest distance of point pt to a series of cubic Beziers

            cubic = self.cubics[self._split_index]
            distance, step = cubic.cubic_points.query(pt)
            self._t_points[pt] = (self._split_index, step / cubic.num_cubic_points)
            # print("cubic #%i, t = %0.3f" % self._t_points[pt])
            return self._t_points[pt]

    def reset_split(self):
        for c in self.cubics:
            c.reset_split()
        self._split_index = 0
        self.reset_t()

    def reset_t(self):
        self._t_step = 0

    def split_at_pt(self, pt):
        if DEBUG_SPLIT:
            print("SuperCubic.split_at_pt", pt, "->")
        index, t = self.t_for_point(pt)
        # FIXME: This only splits inside one cubic segment?
        if DEBUG_SPLIT:
            print("    Splitting cubic %i from %0.4f to %0.4f ..." % (
                index,
                self.cubics[index]._t,
                t
            ))
        # self._split_index = index
        return self.cubics[index].split_at_t(t)

    def split_at_pt_fast(self, pt):
        index = 0
        x, y = pt
        a, b, c, d = self.cubics[0].params
        solutions_h = solveCubic(a[1], b[1], c[1], d[1] - y)
        solutions_v = solveCubic(a[0], b[0], c[0], d[0] - x)
        solutions_h = [t for t in solutions_h if 0 <= t < 1]
        solutions_v = [t for t in solutions_v if 0 <= t < 1]
        if len(solutions_h) == 1:
            t = (solutions_v[0] + solutions_h[0]) * 0.5
            # t = solutions_h[0]
        else:
            print("Multiple solutions found:", solutions_h)
            index, t = self.t_for_point(pt)
        self._split_index = index
        return self.cubics[0].split_at_t(t)

    def split_remainder(self):
        return self.cubics[self._split_index].split_at_t(1.0)
