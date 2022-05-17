from math import sqrt
from typing import (
    Callable,
    List,
    SupportsFloat,
    SupportsIndex,
    Tuple,
    Union
)

Point = Tuple[float, float]


epsilon: float


def calcCubicParameters(
    pt1: Point,
    pt2: Point,
    pt3: Point,
    pt4: Point
) -> Tuple[Point, Point, Point, Point]: ...


def calcQuadraticParameters(
    pt1: Point,
    pt2: Point,
    pt3: Point
) -> Tuple[Point, Point, Point]: ...


def solveCubic(a: float, b: float, c: float, d: float) -> List[float]: ...


def solveQuadratic(
    a: float,
    b: float,
    c: float,
    sqrt: Callable[[Union[SupportsFloat, SupportsIndex]], float] = sqrt
) -> List[float]: ...
