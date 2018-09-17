from distutils.core import setup, Extension

setup(
		name = "jkFontGeometry",
		version = "0.1",
		description = "Font geometry tools.",
		author = "Jens Kutilek",
		url = "http://www.kutilek.de/",
		packages = [
			"jkFontGeometry",
		],
		package_dir = {
			"": "Lib"
		},
		ext_modules = [
			Extension(
				"jkFontGeometry._fastgeometry", [
					"Lib/jkFontGeometry/_fastgeometry.cpp",
					"Lib/jkFontGeometry/fastgeometry.cpp"
				]
			)
		],
	)
