# -*- coding: utf-8 -*-
# Helper functions for geometry, point-based API with pt.x and pt.y
# These are just wrapper functions for the tuple-based functions in jkRFTools.geometry.
from __future__ import absolute_import, division, print_function

from jkFontGeometry import geometry


def angle_between_points(p0, p1, do_round=False):
    return geometry.angle_between_points((p0.x, p0.y), (p1.x, p1.y), do_round)


def distance_between_points(p0, p1, do_round=False):
    return geometry.distance_between_points(
        (p0.x, p0.y), (p1.x, p1.y), do_round
    )


def half_point(p0, p1, do_round=False):
    # Get the coordinate tuple that lies halfway between two other points.
    hp = p0.copy()
    hp.x, hp.y = geometry.half_point((p0.x, p0.y), (p1.x, p1.y), do_round)
    return hp


def round_point(pt):
    return (int(round(pt.x)), int(round(pt.y)))


def round_point_conditional(pt, do_round=True):
    if do_round:
        return (int(round(pt.x)), int(round(pt.y)))
    else:
        return pt


# Triangle Geometry

# p0 is the first point of the Bezier segment and p3 the last point.
# p1 is the handle of p0 and p2 the handle of p3.

# A triangle is formed:
# b = hypotenuse, the line from p0 to p3
# a = p0 to I with I being the intersection point of the lines p0 to p1 and p3 to p2
# c = p3 to I "

# alpha = the angle between p0p1 and p0p3
# beta  = the angle between p3p0 and p3p2
# gamma = the angle between p3I and p0I


def triangle_angles(p0, p1, p2, p3):
    # Calculate the angles
    return geometry.triangle_angles(
        (p0.x, p0.y), (p1.x, p1.y), (p2.x, p2.y), (p3.x, p3.y),
    )


def triangle_area(a, b, c, do_round=False):
    return geometry.triangle_area(
        (a.x, a.y), (b.x, b.y), (c.x, c.y), do_round,
    )


def triangle_sides(p0, p1, p2, p3):
    # Calculate the sides of the triangle
    return geometry.triangle_sides(
        (p0.x, p0.y), (p1.x, p1.y), (p2.x, p2.y), (p3.x, p3.y),
    )


def is_on_left(a, b, c):
    # Is point c on the left of ab?
    return geometry.is_on_left((a.x, a.y), (b.x, b.y), (c.x, c.y),)


def is_on_right(a, b, c):
    # Is point c on the right of ab?
    return geometry.is_on_right((a.x, a.y), (b.x, b.y), (c.x, c.y),)


def is_collinear(a, b, c):
    # Is point c on ab?
    return geometry.is_collinear((a.x, a.y), (b.x, b.y), (c.x, c.y),)
