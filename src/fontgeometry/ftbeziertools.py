from math import acos, cos, pi, sqrt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fontgeometry.typing import PointTuple

# A subset of the fontTools package, so it doesn't need to be installed
# separately. The fontTools code in this file is distributed under the
# following licence.

"""
Copyright 1999-2004
by Just van Rossum, Letterror, The Netherlands.

                        All Rights Reserved

Permission to use, copy, modify, and distribute this software and
its documentation for any purpose and without fee is hereby granted,
provided that the above copyright notice appear in all copies and
that both that copyright notice and this permission notice appear
in supporting documentation, and that the names of Just van Rossum
or Letterror not be used in advertising or publicity pertaining to
distribution of the software without specific, written prior
permission.

JUST VAN ROSSUM AND LETTERROR DISCLAIM ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS, IN NO EVENT SHALL JUST VAN ROSSUM OR
LETTERROR BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL
DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR
PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.


just@letterror.com
"""

epsilon = 1e-12


def solveQuadratic(a: float, b: float, c: float, sqrt=sqrt) -> list[float]:
    """Solve a quadratic equation where a, b and c are real.
        a*x*x + b*x + c = 0
    This function returns a list of roots. Note that the returned list
    is neither guaranteed to be sorted nor to contain unique values!
    """
    if abs(a) < epsilon:
        if abs(b) < epsilon:
            # We have a non-equation; therefore, we have no valid solution
            roots = []
        else:
            # We have a linear equation with 1 root.
            roots = [-c / b]
    else:
        # We have a true quadratic equation.  Apply the quadratic formula to find two roots.
        DD = b * b - 4.0 * a * c
        if DD >= 0.0:
            rDD = sqrt(DD)
            roots = [(-b + rDD) / 2.0 / a, (-b - rDD) / 2.0 / a]
        else:
            # complex roots, ignore
            roots = []
    return roots


def solveCubic(a: float, b: float, c: float, d: float) -> list[float]:
    """Solve a cubic equation where a, b, c and d are real.
        a*x*x*x + b*x*x + c*x + d = 0
    This function returns a list of roots. Note that the returned list
    is neither guaranteed to be sorted nor to contain unique values!
    """
    #
    # adapted from:
    #   CUBIC.C - Solve a cubic polynomial
    #   public domain by Ross Cottrell
    # found at: http://www.strangecreations.com/library/snippets/Cubic.C
    #
    if abs(a) < epsilon:
        # don't just test for zero; for very small values of 'a' solveCubic()
        # returns unreliable results, so we fall back to quad.
        return solveQuadratic(b, c, d)
    a = float(a)
    a1 = b / a
    a2 = c / a
    a3 = d / a

    Q = (a1 * a1 - 3.0 * a2) / 9.0
    R = (2.0 * a1 * a1 * a1 - 9.0 * a1 * a2 + 27.0 * a3) / 54.0
    R2_Q3 = R * R - Q * Q * Q

    if R2_Q3 < 0:
        theta = acos(R / sqrt(Q * Q * Q))
        rQ2 = -2.0 * sqrt(Q)
        x0 = rQ2 * cos(theta / 3.0) - a1 / 3.0
        x1 = rQ2 * cos((theta + 2.0 * pi) / 3.0) - a1 / 3.0
        x2 = rQ2 * cos((theta + 4.0 * pi) / 3.0) - a1 / 3.0
        return [x0, x1, x2]
    else:
        if Q == 0 and R == 0:
            x: float | int = 0
        else:
            x = pow(sqrt(R2_Q3) + abs(R), 1 / 3.0)
            x = x + Q / x
        if R >= 0.0:
            x = -x
        x = x - a1 / 3.0
        return [x]


#
# Conversion routines for points to parameters and vice versa
#


def calcQuadraticParameters(
    pt1: "PointTuple", pt2: "PointTuple", pt3: "PointTuple"
) -> "tuple[PointTuple, PointTuple, PointTuple]":
    x2, y2 = pt2
    x3, y3 = pt3
    cx, cy = pt1
    bx = (x2 - cx) * 2.0
    by = (y2 - cy) * 2.0
    ax = x3 - cx - bx
    ay = y3 - cy - by
    return (ax, ay), (bx, by), (cx, cy)


def calcCubicParameters(
    pt1: "PointTuple", pt2: "PointTuple", pt3: "PointTuple", pt4: "PointTuple"
) -> "tuple[PointTuple, PointTuple, PointTuple, PointTuple]":
    x2, y2 = pt2
    x3, y3 = pt3
    x4, y4 = pt4
    dx, dy = pt1
    cx = (x2 - dx) * 3.0
    cy = (y2 - dy) * 3.0
    bx = (x3 - x2) * 3.0 - cx
    by = (y3 - y2) * 3.0 - cy
    ax = x4 - dx - cx - bx
    ay = y4 - dy - cy - by
    return (ax, ay), (bx, by), (cx, cy), (dx, dy)
