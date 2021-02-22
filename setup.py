from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
from Cython.Distutils import build_ext

extensions = [
    Extension("gui", ["gui.py"])
]

setup(
    name="other_gui",
    cmdclass={'build_ext': build_ext},
    ext_modules=cythonize(extensions),
)