from math import atan2, hypot, pi, sin
from typing import Optional, Tuple, Union
from jkFontGeometry import Point

"""
Slow geometry -- when the rust extension is not available.
"""


# Helper functions for geometry, tuple-based API with pt = (x, y)


def angle_between_points(
    p0: Point, p1: Point, do_round: bool = False
) -> Union[float, int]:
    phi = atan2(p1[1] - p0[1], p1[0] - p0[0])
    if do_round:
        return int(round(phi))
    else:
        return phi


def distance_between_points(
    p0: Point, p1: Point, do_round: bool = False
) -> Union[float, int]:
    d = hypot(p1[1] - p0[1], p1[0] - p0[0])
    if do_round:
        return int(round(d))
    else:
        return d


def half_point(p0: Point, p1: Point, do_round: bool = False) -> Point:
    # Get the coordinate tuple that lies halfway between two other points.
    hp = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
    if do_round:
        return round_point(hp)
    return hp


def round_point(pt: Point) -> Point:
    return (int(round(pt[0])), int(round(pt[1])))


def round_point_conditional(pt: Point, do_round: bool = True) -> Point:
    if do_round:
        return (int(round(pt[0])), int(round(pt[1])))
    else:
        return pt


# Triangle Geometry

# p0 is the first point of the Bezier segment and p3 the last point.
# p1 is the handle of p0 and p2 the handle of p3.

# A triangle is formed:
# b = hypotenuse, the line from p0 to p3
# a = p0 to I with I being the intersection point of the lines p0–p1 and p3–p2
# c = p3 to I "

# alpha = the angle between p0p1 and p0p3
# beta  = the angle between p3p0 and p3p2
# gamma = the angle between p3I and p0I


def triangle_angles(
    p0: Point, p1: Point, p2: Point, p3: Point
) -> Tuple[float, float, float]:

    # Calculate the angles

    alpha1 = atan2(p3[1] - p0[1], p3[0] - p0[0])
    alpha2 = atan2(p1[1] - p0[1], p1[0] - p0[0])
    alpha = alpha1 - alpha2

    gamma1 = atan2(p3[0] - p0[0], p3[1] - p0[1])
    gamma2 = atan2(p3[0] - p2[0], p3[1] - p2[1])
    gamma = gamma1 - gamma2

    beta = pi - alpha - gamma

    return alpha, beta, gamma


def triangle_area(
    a: Point, b: Point, c: Point, do_round: bool = False
) -> float:
    area = (b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])
    if do_round:
        return int(round(area))
    else:
        return area


def triangle_sides(
    p0: Point, p1: Point, p2: Point, p3: Point
) -> Tuple[float, float, float]:
    alpha, beta, gamma = triangle_angles(p0, p1, p2, p3)

    # Calculate the sides of the triangle

    b = abs(distance_between_points(p0, p3))
    try:
        a = b * sin(alpha) / sin(beta)
        c = b * sin(gamma) / sin(beta)
    except ZeroDivisionError:
        from math import radians

        print("Division by zero in triangle calculation:")
        print("    alpha:", radians(alpha))
        print("    beta: ", radians(beta))
        print("    gamma:", radians(gamma))
        raise ZeroDivisionError

    return a, b, c


def is_on_left(a: Point, b: Point, c: Point) -> bool:
    # Is point c on the left of ab?
    return triangle_area(a, b, c) > 0


def is_on_right(a: Point, b: Point, c: Point) -> bool:
    # Is point c on the right of ab?
    return triangle_area(a, b, c) < 0


def is_collinear(a: Point, b: Point, c: Point) -> bool:
    # Is point c on ab?
    return triangle_area(a, b, c) == 0


# Intersections


def dot_product_2d(p1: Point, p2: Point, p3: Point) -> float:
    # Return the dot product of the vectors p1_p2 and p1_p3
    p1x, p1y = p1
    p2x, p2y = p2
    p3x, p3y = p3

    # calculate unit vectors
    m1 = distance_between_points(p1, p2)
    m2 = distance_between_points(p1, p3)

    v1 = ((p2x - p1x) / m1, (p2y - p1y) / m1)
    v2 = ((p3x - p1x) / m2, (p3y - p1y) / m2)

    dp = v1[0] * v2[0] + v1[1] * v2[1]
    # print v1, v2, dp
    return dp


def same_direction(
    p0: Point, p1: Point, p2: Point, p3: Point, i: Point
) -> bool:
    # Check if the lines from p0_p1 and p0_i,
    # as well as p3_p2 and p3_i point in the same direction +- 90 degrees.
    if dot_product_2d(p0, p1, i) < 0:
        return False
    if dot_product_2d(p3, p2, i) < 0:
        return False
    return True


def line_coefficients(p1: Point, p2: Point) -> Tuple[float, float, float]:
    # https://stackoverflow.com/questions/20677795/how-do-i-compute-the-interse
    # ction-point-of-two-lines-in-python
    p1x, p1y = p1
    p2x, p2y = p2
    A = p1y - p2y
    B = p2x - p1x
    C = p1x * p2y - p2x * p1y
    return A, B, -C


def intersect_coeffs(
    L1: Tuple[float, float, float], L2: Tuple[float, float, float]
) -> Optional[Point]:
    D = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return x, y
    else:
        return None


def intersect(p0: Point, p1: Point, p2: Point, p3: Point) -> Optional[Point]:
    # Find the intersection of two lines given by two points on each line.
    L1 = line_coefficients(p0, p1)
    L2 = line_coefficients(p3, p2)
    return intersect_coeffs(L1, L2)
