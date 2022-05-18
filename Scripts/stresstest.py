from random import random
from time import time
from jkFontGeometry.geometry import intersect
from jkFontGeometry.beziertools import getPointOnCubic


def random_point():
    return (
        (random() - 0.5) * 16384,
        (random() - 0.5) * 16384,
    )


points = [
    (
        random_point(),
        random_point(),
        random_point(),
        random_point(),
    )
    for _ in range(10000)
]

print("Doing 10000 intersections ...")

start = time()
for p0, p1, p2, p3 in points:
    _result = intersect(p0, p1, p2, p3)
stop = time()
print("Time:", stop - start)


print("Doing 10000 getPointOnCubic ...")

points = [
    (
        random(),
        random_point(),
        random_point(),
        random_point(),
        random_point(),
    )
    for _ in range(10000)
]

start = time()
for t, p0, p1, p2, p3 in points:
    result = getPointOnCubic(t, p0, p1, p2, p3)
stop = time()
print("Time:", stop - start)
