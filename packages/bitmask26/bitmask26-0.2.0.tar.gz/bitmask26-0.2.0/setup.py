from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup


setup(
    name="bitmask26",
    version="0.2.0",
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
    py_modules=["py_bitmask26"],
    package_data={"": ["bitmask26.pyi"]},
    include_package_data=True,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    python_requires=">=3.8",
)
