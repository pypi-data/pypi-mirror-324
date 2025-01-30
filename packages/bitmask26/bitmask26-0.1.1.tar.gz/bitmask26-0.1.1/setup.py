from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup


setup(
    name="bitmask26",
    version="0.1.1",
    author="Adwaith H Sivam",
    author_email="adwaithhs@gmail.com",
    description="A C++ optimized bitmask implementation with Python bindings",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/adwaithhs/bitmask26",
    ext_modules=[
        Pybind11Extension(
            "bitmask26",
            ["bitmask26.cpp"],
        ),
    ],
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    python_requires=">=3.8",
)
