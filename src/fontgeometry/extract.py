from jkFontGeometry.cubics import SuperCubic


class CubicSegments:
    def __init__(self, layer):
        self.layer = layer
        self.segments = []

    def extract_segments(self):
        # Extract the segments from the layer without using a pen.
        # See ExtractSegmentsPen for a pen-oriented object.

        raise NotImplementedError

    def to_supercubics(self):
        self.super_cubics = []
        sc = SuperCubic()
        for segment in self.segments:
            if not sc.cubics:
                # The super cubic is empty, we can just add the current segment
                sc.add_cubic_from_point_tuple(segment)
            else:
                if sc.cubics[-1].p3 == segment[0]:
                    # The current cubic is a continuation of the previous cubic
                    sc.add_cubic_from_point_tuple(segment)
                else:
                    self.super_cubics.append(sc)
                    sc = SuperCubic()
                    sc.add_cubic_from_point_tuple(segment)
        if sc.cubics:
            # Add the last super cubic
            self.super_cubics.append(sc)
