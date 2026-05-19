from math import sqrt
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
