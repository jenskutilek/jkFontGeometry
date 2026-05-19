from math import hypot
from typing import TYPE_CHECKING, Sequence

from fontgeometry.beziertools import (
    estimateCubicCurveLength,
    getExtremaForCubic,
    getInflectionsForCubic,
    getPointOnCubic,
)
from fontgeometry.ftbeziertools import calcCubicParameters, solveCubic

if TYPE_CHECKING:
    from fontgeometry.typing import PointTuple

DEBUG_SPLIT = False


class Cubic:
    def __init__(
        self,
        pt1: "PointTuple",
        pt2: "PointTuple",
        pt3: "PointTuple",
        pt4: "PointTuple",
        raster_length: float = 0.25,
    ) -> None:
        self.pt1 = pt1
        self.pt2 = pt2
        self.pt3 = pt3
        self.pt4 = pt4

        # The estimated length of each distance if the cubic is converted to points
        self.raster_length = raster_length

        # The list of points on the cubic, with estimated raster_length distance
        self._cubic_points: "list[PointTuple] | None" = None
        self._num_cubic_points: int | None = None

        # The calculated estimated curve length
        self._estimated_length: float | None = None

        # The number of steps to achieve the desired point distances
        self._raster_steps: int | None = None

        # The current split point (will be moved along the curve when splitting)
        self._t = 0.0

        # Cache for Cubic params (a, b, c, d)
        self._params: "tuple[PointTuple, PointTuple, PointTuple, PointTuple] | None" = (
            None
        )

        # Cache for inflection points
        self._inflections: list[float] | None = None
        self._inflection_points: "list[PointTuple] | None" = None

        # Cache for extremum points
        self._extrema: list[float] | None = None
        self._extremum_points: "list[PointTuple] | None" = None

    def __repr__(self) -> str:
        return "<Cubic pt1=%s, pt4=%s>" % (self.pt1, self.pt4)

    @property
    def extrema(self) -> list[float]:
        if self._extrema is None:
            self._extrema = self.calculate_extrema()
        return self._extrema

    @property
    def extremum_points(self) -> "list[PointTuple]":
        if self._extremum_points is None:
            self._extremum_points = self.calculate_extremum_points()
        return self._extremum_points

    @property
    def inflections(self) -> list[float]:
        if self._inflections is None:
            self._inflections = self.calculate_inflections()
        return self._inflections

    @property
    def inflection_points(self) -> "list[PointTuple]":
        if self._inflection_points is None:
            self._inflection_points = self.calculate_inflection_points()
        return self._inflection_points

    @property
    def length(self) -> float:
        if self._estimated_length is None:
            self._estimated_length = estimateCubicCurveLength(
                self.pt1, self.pt2, self.pt3, self.pt4
            )
        return self._estimated_length

    @property
    def params(self) -> "tuple[PointTuple, PointTuple, PointTuple, PointTuple]":
        if self._params is None:
            self._params = calcCubicParameters(self.pt1, self.pt2, self.pt3, self.pt4)
        return self._params

    @property
    def raster_steps(self) -> int:
        if self._raster_steps is None:
            self._raster_steps = int(round(self.length / self.raster_length))
        return self._raster_steps

    @property
    def cubic_points(self) -> "list[PointTuple]":
        # Calculate or return the cached list of t to point mappings.
        if self._cubic_points is None:
            self._cubic_points = self.calculate_cubic_points()
            self._num_cubic_points = len(self._cubic_points) - 1
        return self._cubic_points

    @property
    def num_cubic_points(self) -> int:
        if self._num_cubic_points is None:
            self._cubic_points = self.calculate_cubic_points()
            self._num_cubic_points = len(self._cubic_points) - 1
        return self._num_cubic_points

    def calculate_cubic_points(self) -> "list[PointTuple]":
        # Return a list of point coordinates for the cubic curve according to the
        # current raster_steps value
        # st = time()
        t_list = []
        if self.raster_steps < 2 or (self.pt1 == self.pt2) and (self.pt3 == self.pt4):
            t_list = [self.pt1, self.pt4]
        else:
            step = 1 / self.raster_steps
            t_list = [
                self.get_cubic_point(t * step) for t in range(0, self.raster_steps + 1)
            ]

        # et = time()
        # print("calculate_cubic_points: %0.3f ms" % ((et-st)*1000))
        return t_list

    def calculate_extrema(self) -> list[float]:
        return getExtremaForCubic(
            self.pt1,
            self.pt2,
            self.pt3,
            self.pt4,
            h=True,
            v=False,
            include_start_end=True,
        )

    def calculate_extremum_points(self) -> "list[PointTuple]":
        return [self.get_cubic_point(t) for t in self.extrema]

    def calculate_inflections(self) -> list[float]:
        # TODO: Inflections "between" segments
        return getInflectionsForCubic(self.pt1, self.pt2, self.pt3, self.pt4)

    def calculate_inflection_points(self) -> "list[PointTuple]":
        return [self.get_cubic_point(t) for t in self.inflections]

    def get_cubic_point(self, t: float) -> "PointTuple":
        return getPointOnCubic(t, self.pt1, self.pt2, self.pt3, self.pt4)

    def reset_split(self) -> None:
        self._t = 0.0

    def split_at_t(
        self, t: float
    ) -> "tuple[PointTuple, PointTuple, PointTuple, PointTuple]":

        # From https://stackoverflow.com/questions/878862/drawing-part-of-a-bézier-curve
        # -by-reusing-a-basic-bézier-curve-function

        # st = time()

        t0 = self._t
        t1 = t

        u0 = 1.0 - t0
        u1 = 1.0 - t1

        x1, y1 = self.pt1
        bx1, by1 = self.pt2
        bx2, by2 = self.pt3
        x2, y2 = self.pt4

        qxa = x1 * u0 * u0 + bx1 * 2 * t0 * u0 + bx2 * t0 * t0
        qxb = x1 * u1 * u1 + bx1 * 2 * t1 * u1 + bx2 * t1 * t1
        qxc = bx1 * u0 * u0 + bx2 * 2 * t0 * u0 + x2 * t0 * t0
        qxd = bx1 * u1 * u1 + bx2 * 2 * t1 * u1 + x2 * t1 * t1

        qya = y1 * u0 * u0 + by1 * 2 * t0 * u0 + by2 * t0 * t0
        qyb = y1 * u1 * u1 + by1 * 2 * t1 * u1 + by2 * t1 * t1
        qyc = by1 * u0 * u0 + by2 * 2 * t0 * u0 + y2 * t0 * t0
        qyd = by1 * u1 * u1 + by2 * 2 * t1 * u1 + y2 * t1 * t1

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


class SuperCubic:
    # Collection of multiple Cubic segments

    def __init__(self) -> None:
        self.cubics: list[Cubic] = []
        self._split_index = 0

        # The cached map of t to point
        self._t_points: "dict[PointTuple, tuple[int, float]]" = {}

        # Keep track of current t for faster searching
        self._t_step = 0

        self._inflection_points: "list[PointTuple] | None" = None
        self._extremum_points: "list[PointTuple] | None" = None

    def __repr__(self) -> str:
        return "<SuperCubic len=%i>" % len(self.cubics)

    @property
    def inflection_points(self) -> "list[PointTuple]":
        """
        Return all inflection points from the sub-cubics. The points are not necessarily
        in order. Explicit inflection points (i.e. between cubics) are omitted.

        Returns:
            list[PointTuple]: The list of inflection points
        """
        if self._inflection_points is None:
            self._inflection_points = []
            for cubic in self.cubics:
                if cubic.inflection_points:
                    self._inflection_points.extend(cubic.inflection_points)
        return self._inflection_points

    @property
    def extremum_points(self) -> "list[PointTuple]":
        """
        Return all extremum points from the sub-cubics. The points are not necessarily
        in order.

        Returns:
            list[PointTuple]: The list of extremum points
        """
        if self._extremum_points is None:
            self._extremum_points = []
            for cubic in self.cubics:
                if cubic.extremum_points:
                    self._extremum_points.extend(cubic.extremum_points)
        return self._extremum_points

    def add_cubic_from_points(
        self,
        pt1: "PointTuple",
        pt2: "PointTuple",
        pt3: "PointTuple",
        pt4: "PointTuple",
        raster_length: float = 0.25,
    ) -> None:
        """
        Add a cubic by specifying four points.

        Args:
            pt1 (PointTuple): The first point
            pt2 (PointTuple): The second point
            pt3 (PointTuple): The third point
            pt4 (PointTuple): The fourth point
            raster_length (float, optional): The raster length. Defaults to 0.25.
        """
        cubic = Cubic(pt1, pt2, pt3, pt4, raster_length)
        self.cubics.append(cubic)

    def add_cubic_from_point_tuple(
        self, point_tuple: "Sequence[PointTuple]", raster_length: float = 0.25
    ) -> None:
        """
        Add a cubic by specifying a sequence of points. If the sequence has two points,
        it is assumed that it is a line, and is converted to a flat curve before adding
        it.

        Args:
            point_tuple (Sequence[PointTuple]): The points
            raster_length (float, optional): The raster length. Defaults to 0.25.

        Raises:
            ValueError: If the sequence has an unhandled number of points
        """
        num_points = len(point_tuple)
        if num_points == 4:
            pt1, pt2, pt3, pt4 = point_tuple
        elif num_points == 2:
            print("WARNING: Not a curve:", point_tuple)
            # Add a flat curve
            pt1, pt4 = point_tuple
            pt2 = (
                pt1[0] + 0.3333333333333333 * (pt4[0] - pt1[0]),
                pt1[1] + 0.3333333333333333 * (pt4[1] - pt1[1]),
            )
            pt3 = (
                pt1[0] + 0.6666666666666667 * (pt4[0] - pt1[0]),
                pt1[1] + 0.6666666666666667 * (pt4[1] - pt1[1]),
            )
        else:
            raise ValueError
        self.add_cubic_from_points(pt1, pt2, pt3, pt4, raster_length)

    def t_for_point(self, pt: "PointTuple") -> tuple[int, float] | None:
        """
        Return the index of the sub-cubics, and the t value inside it for the given
        point.

        Args:
            pt (PointTuple): The point for which to find t

        Returns:
            tuple[int, float] | None: The cubics index and t
        """
        # TODO: Cache previous pt so the search can start there?
        return self._t_points.get(pt, self.calculate_t_for_point(pt))

    def calculate_t_for_point(self, pt: "PointTuple") -> tuple[int, float] | None:
        # Calculate the t value for the closest distance of point pt to a series of
        # cubic Beziers

        x, y = pt

        # Check special case: Is the point close to the first or last points of any of
        # the cubics?

        for index in range(self._split_index, len(self.cubics)):
            cubic = self.cubics[index]
            pt1x = round(cubic.pt1[0])
            pt1y = round(cubic.pt1[1])
            pt4x = round(cubic.pt4[0])
            pt4y = round(cubic.pt4[1])

            if pt1x - 1 <= x <= pt1x + 1 and pt1y - 1 <= y <= pt1y + 1:
                self._split_index = index
                self._t_step = 0
                # tx, ty = getPointOnCubic(
                #     0, cubic.pt1, cubic.pt2, cubic.pt3, cubic.pt4
                # )
                # print(
                #     "                "
                #     "Fast Found t = 0 -> (%0.3f, %0.3f)" % (tx, ty)
                # )
                return (index, 0.0)
            elif pt4x - 1 <= x <= pt4x + 1 and pt4y - 1 <= y <= pt4y + 1:
                self._split_index = index
                self._t_step = cubic.num_cubic_points
                # tx, ty = getPointOnCubic(
                #     1, cubic.pt1, cubic.pt2, cubic.pt3, cubic.pt4
                # )
                # print(
                #     "                "
                #     "Fast Found t = 1 -> (%0.3f, %0.3f)" % (tx, ty)
                # )
                return (index, 1.0)

        # Take the long road

        prev_dist: float | None = None
        for index in range(self._split_index, len(self.cubics)):
            cubic = self.cubics[index]
            self._split_index = index
            for step in range(self._t_step, cubic.num_cubic_points + 1):
                p = cubic.cubic_points[step]
                px, py = p
                dist = hypot(y - py, x - px)  # Point distance
                if prev_dist is not None and dist > prev_dist:
                    if prev_dist is not None:
                        index_step = (
                            index,
                            step / cubic.num_cubic_points,
                        )
                        self._t_points[pt] = index_step
                        # print(
                        #     "                "
                        #     f"Searching for t in cubic {self._split_index} "
                        #     f"from step {self._t_step} to {step} of "
                        #     f"{cubic.num_cubic_points} ..."
                        # )
                        # tx, ty = getPointOnCubic(
                        #     step / cubic.num_cubic_points,
                        #     cubic.pt1,
                        #     cubic.pt2,
                        #     cubic.pt3,
                        #     cubic.pt4,
                        # )
                        # print(
                        #     "                "
                        #     "Found t = %0.3f -> (%0.3f, %0.3f)" % (
                        #         step / cubic.num_cubic_points, tx, ty
                        #     )
                        # )
                        self._t_step = step
                        return index_step
                prev_dist = dist
            self.reset_t()
            prev_dist = None
        return None

    def reset_split(self) -> None:
        for c in self.cubics:
            c.reset_split()
        self._split_index = 0
        self.reset_t()

    def reset_t(self) -> None:
        self._t_step = 0

    def split_at_pt(
        self, pt: "PointTuple"
    ) -> "tuple[PointTuple, PointTuple, PointTuple, PointTuple]":
        if DEBUG_SPLIT:
            print("SuperCubic.split_at_pt", pt, "->")
        index_t = self.t_for_point(pt)
        if index_t is None:
            raise ValueError

        index, t = index_t
        # FIXME: This only splits inside one cubic segment?
        if DEBUG_SPLIT:
            print(
                "    Splitting cubic %i from %0.4f to %0.4f ..."
                % (index, self.cubics[index]._t, t)
            )
        # self._split_index = index
        return self.cubics[index].split_at_t(t)

    def split_at_pt_fast(
        self, pt: "PointTuple"
    ) -> "tuple[PointTuple, PointTuple, PointTuple, PointTuple]":
        if DEBUG_SPLIT:
            print("SuperCubic.split_at_pt_fast", pt, "->")
        index = 0
        x, y = pt
        a, b, c, d = self.cubics[0].params
        solutions_h = solveCubic(a[1], b[1], c[1], d[1] - y)
        solutions_v = solveCubic(a[0], b[0], c[0], d[0] - x)
        solutions_h = [t for t in solutions_h if 0 <= t < 1]
        solutions_v = [t for t in solutions_v if 0 <= t < 1]
        if DEBUG_SPLIT:
            print(solutions_h, solutions_v)
        if len(solutions_h) == 1 and solutions_v:
            # Take the average of both values
            t = (solutions_v[0] + solutions_h[0]) * 0.5
        else:
            print(
                "    Different number of solutions for h and v:",
                solutions_h,
                solutions_v,
            )
            index_t = self.t_for_point(pt)
            if index_t is None:
                raise ValueError

            index, t = index_t
            print("        Choosing via thorough method:", t)
        self._split_index = index
        return self.cubics[index].split_at_t(t)

    def split_remainder(
        self,
    ) -> "tuple[PointTuple, PointTuple, PointTuple, PointTuple]":
        return self.cubics[self._split_index].split_at_t(1.0)
