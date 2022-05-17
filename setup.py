from setuptools import setup
# from setuptools_rust import Binding, RustExtension
from mypyc.build import mypycify

setup(
    # rust_extensions=[
    #     RustExtension(
    #         "jkFontGeometry.fastgeometry",
    #         binding=Binding.PyO3
    #     )
    # ],
    ext_modules=mypycify([
       "Lib/jkFontGeometry/__init__.py",
    ]),
)
