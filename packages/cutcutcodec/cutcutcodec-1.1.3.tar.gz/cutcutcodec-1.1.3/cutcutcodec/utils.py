#!/usr/bin/env python3

"""Pythonic tools."""

import pathlib

import numpy as np


def get_compilation_rules() -> dict:
    """Return the extra compilation rules."""
    return {
        "define_macros": [("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")],  # for warning
        "extra_compile_args": [
            "-fopenmp",  # for threads
            "-fopenmp-simd",  # for single instruction multiple data
            "-lc",  # include standard c library
            "-lm",  # for math functions
            "-march=native",  # uses local processor instructions for optimization
            # "-mtune=native",  # can be conflictual with march
            "-O2",  # hight optimization, -O3 include -ffast-math
            "-ffast-math",  # not activated in -O2
            # "-Wall", "-Wextra",  # "-Wconversion",  # -Wtraditional,  # activate warnings
            # "-pedantic", # ensurse all is standard and compilable anywhere
            "-std=gnu11",  # use iso c norm (gnu23 not yet supported on readthedoc)
            "-flto",  # enable link time optimization
            "-pipe",  # use pipline rather than tempory files
        ],
        "include_dirs": [np.get_include()],  # requires for  #include numpy
    }


def get_project_root() -> pathlib.Path:
    """Return the absolute project root folder.

    Examples
    --------
    >>> from cutcutcodec.utils import get_project_root
    >>> root = get_project_root()
    >>> root.is_dir()
    True
    >>> root.name
    'cutcutcodec'
    >>> sorted(p.name for p in root.iterdir())
    ['__init__.py', '__main__.py', '__pycache__', 'core', 'examples', 'gui', 'testing', 'utils.py']
    >>>
    """
    return pathlib.Path(__file__).resolve().parent
