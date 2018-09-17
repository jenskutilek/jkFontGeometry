# Adapted from robofab.pens.filterPen
from __future__ import absolute_import, division, print_function

from fontTools.misc.bezierTools import calcCubicParameters, calcQuadraticParameters, solveQuadratic
from jkFontGeometry.geometry import distance_between_points, half_point




def estimateCubicCurveLength(pt0, pt1, pt2, pt3, precision=10):
    """
    Estimate the length of this curve by iterating
    through it and averaging the length of the flat bits.
    """
    
    length = 0
    step = 1.0 / precision
    points = getPointListForCubic([f * step for f in range(precision + 1)], pt0, pt1, pt2, pt3)
    for i in range(len(points) - 1):
        pta = points[i]
        ptb = points[i + 1]
        length += distance_between_points(pta, ptb)
    return length


def getPointOnCubic(t, pt0, pt1, pt2, pt3):
    """
    Return the point for t on the cubic curve defined by pt0, pt1, pt2, pt3.
    """
    if t == 0:
        return pt0
    if t == 1:
        return pt3
    if t == 0.5:
        a = half_point(pt0, pt1)
        b = half_point(pt1, pt2)
        c = half_point(pt2, pt3)
        d = half_point(a, b)
        e = half_point(b, c)
        return half_point(d, e)
    else:
        cx = (pt1[0] - pt0[0]) * 3
        cy = (pt1[1] - pt0[1]) * 3
        bx = (pt2[0] - pt1[0]) * 3 - cx
        by = (pt2[1] - pt1[1]) * 3 - cy
        ax = pt3[0] - pt0[0] - cx - bx
        ay = pt3[1] - pt0[1] - cy - by
        t3 = t ** 3
        t2 = t * t
        x = ax * t3 + bx * t2 + cx * t + pt0[0]
        y = ay * t3 + by * t2 + cy * t + pt0[1]
        return x, y


def getPointListForCubic(ts, pt0, pt1, pt2, pt3):
    """
    Return a list of points for increments of t on the cubic curve defined by pt0, pt1, pt2, pt3.
    """
    (x0, y0), (x1, y1) = pt1, pt2
    cx = (x1 - x0) * 3
    cy = (y1 - y0) * 3
    bx = (pt2[0] - x1) * 3 - cx
    by = (pt2[1] - y1) * 3 - cy
    ax = pt3[0] - x0 - cx - bx
    ay = pt3[1] - y0 - cy - by
    path = []
    for t in ts:
        t3 = t ** 3
        t2 = t * t
        x = ax * t3 + bx * t2 + cx * t + x0
        y = ay * t3 + by * t2 + cy * t + y0
        path.append((x, y))
    return path


def getExtremaForCubic(pt1, pt2, pt3, pt4, h=True, v=False):
    (ax, ay), (bx, by), c, d = calcCubicParameters(pt1, pt2, pt3, pt4)
    ax *= 3.0
    ay *= 3.0
    bx *= 2.0
    by *= 2.0
    points = []
    vectors = []
    if h:
        roots = [t for t in solveQuadratic(ay, by, c[1]) if 0 < t < 1]
    if v:
        roots += [t for t in solveQuadratic(ax, bx, c[0]) if 0 < t < 1]
    return roots


def getInflectionsForCubic(pt1, pt2, pt3, pt4):
    # After https://github.com/mekkablue/InsertInflections
    roots = []

    x1, y1 = pt1
    x2, y2 = pt2
    x3, y3 = pt3
    x4, y4 = pt4

    ax = x2 - x1
    ay = y2 - y1
    bx = x3 - x2 - ax
    by = y3 - y2 - ay
    cx = x4 - x3 - ax - bx - bx
    cy = y4 - y3 - ay - by - by
    
    c0 = ( ax * by ) - ( ay * bx )
    c1 = ( ax * cy ) - ( ay * cx )
    c2 = ( bx * cy ) - ( by * cx )

    if abs(c2) > 0.00001:
        discr = ( c1 ** 2 ) - ( 4 * c0 * c2)
        c2 *= 2
        if abs(discr) < 0.000001:
            root = -c1 / c2
            if (root > 0.001) and (root < 0.99):
                roots.append(root)
        elif discr > 0:
            discr = discr ** 0.5
            root = ( -c1 - discr ) / c2
            if (root > 0.001) and (root < 0.99):
                roots.append(root)
    
            root = ( -c1 + discr ) / c2
            if (root > 0.001) and (root < 0.99):
                roots.append(root)
    elif c1 != 0.0:
        root = - c0 / c1
        if (root > 0.001) and (root < 0.99):
            roots.append(root)

    return roots


def getExtremaForQuadratic(pt1, pt2, pt3, h=True, v=False):
    (ax, ay), (bx, by), c = calcQuadraticParameters(pt1, pt2, pt3)
    ax *= 2.0
    ay *= 2.0
    points = []
    vectors = []
    if h:
        roots = [t for t in solveLinear(ay, by) if 0 < t < 1]
    if v:
        roots += [t for t in solveLinear(ax, bx) if 0 < t < 1]
    return roots


def solveLinear(a, b):
    if abs(a) < epsilon:
        if abs(b) < epsilon:
            roots = []
        else:
            roots = [0]
    else:
        DD = b * b
        if DD >= 0.0:
            rDD = sqrt(DD)
            roots = [(-b+rDD)/2.0/a, (-b-rDD)/2.0/a]
        else:
            roots = []
    return roots
