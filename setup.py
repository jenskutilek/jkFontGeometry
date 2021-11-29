from setuptools import setup
from setuptools_rust import Binding, RustExtension

setup(
    name="jkFontGeometry",
    version="0.2",
    description="Font geometry tools.",
    author="Jens Kutilek",
    url="http://www.kutilek.de/",
    packages=[
        "jkFontGeometry",
    ],
    package_dir={
        "": "Lib"
    },
    install_requires=[
        "setuptools",
        "setuptools_rust",
    ],
    rust_extensions=[
        RustExtension(
            "jkFontGeometry.fastgeometry",
            binding=Binding.PyO3
        )
    ],
    zip_safe=False,
)
