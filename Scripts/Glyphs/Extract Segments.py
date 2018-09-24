# MenuTitle: Extract Segments
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from jkFontGeometry.cubics import SuperCubic
from jkFontGeometry.extract import CubicSegments


DEBUG_EXTRACT = True


try:
	from objectsGS import GSCURVE, GSLINE, GSOFFCURVE
	CURVE = GSCURVE
	LINE = GSLINE
	OFFCURVE = GSOFFCURVE
except ImportError:
	if DEBUG_EXTRACT: print("ExtractSegments imports: Falling back to string segment types. Probably we are just not in Glyphs.")
	CURVE    = "curve"
	LINE     = "line"
	OFFCURVE = "offcurve"




class CubicSegmentsGlyphs(CubicSegments):

	def extract_segments(self):
		# Extract the segments from the layer without using a pen.
		# See ExtractSegmentsPen for a pen-oriented object.

		self.segments = []

		# Glyphs API

		# FIXME: Segments are not grouped into SuperCubics across the start point

		for p in self.layer.paths:
			segment = []
			seen_oncurve = False
			partial = []
			for n in p.nodes:
				if n.type in (CURVE, LINE):
					if seen_oncurve:
						segment.append((n.x, n.y))
					else:
						seen_oncurve = True
						partial.append((n.x, n.y))
					if len(segment) > 2:
						self.segments.append(segment)
					segment = [(n.x, n.y)]
				elif n.type == OFFCURVE:
					if seen_oncurve:
						segment.append((n.x, n.y))
					else:
						partial.append((n.x, n.y))
			if DEBUG_EXTRACT:
				print("  Remaining segment:", segment)
				print("  Partial segment:  ", partial)
			remainder = segment + partial
			if len(remainder) > 2:
				self.segments.append(remainder)




if __name__ == '__main__':
	# Extract segments from current layer in Glyphs
	s = CubicSegmentsGlyphs(Layer)
	s.extract_segments()
	print(s)
	print(s.segments)
	print("Converting to SuperCubic ...")
	s.to_supercubics()
	print(s.super_cubics)
	for i, sc in enumerate(s.super_cubics):
		print("SuperCubic #%i" % i)
		print("   ", sc.cubics)
		# Inflections are only returned if they are not one of the on-curve points.
		print("    Inflections:", sc.inflection_points)
		print("    Extrema:    ", sc.extremum_points) 
