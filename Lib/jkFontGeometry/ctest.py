from __future__ import absolute_import, division, print_function

from _fastgeometry import intersect, get_cubic_point, get_quadratic_point

print(intersect((0, 0), (1, 1), (2, 1), (3, 0)))

print(get_cubic_point(0, (0, 0), (1, 1), (2, 1), (3, 0)))
print(get_cubic_point(0.3, (0, 0), (1, 1), (2, 1), (3, 0)))
print(get_cubic_point(0.5, (0, 0), (1, 1), (2, 1), (3, 0)))
print(get_cubic_point(1, (0, 0), (1, 1), (2, 1), (3, 0)))
print(get_quadratic_point(0.3, (0, 0), (2, 1), (3, 0)))
