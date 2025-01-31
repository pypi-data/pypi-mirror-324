#!/usr/bin/env python3

"""Transformation to change the colorimetric space.

The equations are the same as for ffmpeg's
`zscale <https://github.com/sekrit-twc/zimg/blob/master/src/zimg/colorspace/colorspace_param.cpp>`_
filter.

A full documentation an model can be found here: http://www.brucelindbloom.com/index.html.

A python implementation here: colour-science
"""

# in the linux kernel documentation, there is some primaries values:
# https://www.kernel.org/doc/html/v6.12/userspace-api/media/v4l/colorspaces-details.html
# For the transition between YUV and RGB, you can refer to https://en.wikipedia.org/wiki/YCbCr.
# To add a chromaticity correction http://www.brucelindbloom.com/index.html?Eqn_ChromAdapt.html
# somme filters are implemented here: https://github.com/FFmpeg/FFmpeg/tree/master/libavfilter

import numbers
import typing

import sympy

from .colorspace_cst import PRIMARIES, TRC, V, L

NBR = numbers.Real | sympy.core.basic.Basic


def convert(
    primaries_in: typing.Optional[str] = None,
    primaries_out: typing.Optional[str] = None,
    transfer_in: typing.Optional[str] = None,
    transfer_out: typing.Optional[str] = None,
) -> tuple[sympy.core.basic.Basic, sympy.core.basic.Basic, sympy.core.basic.Basic]:
    r"""Return the symbolic expression to convert colorspace.

    Here's the string to go from space :math:`e_1` to :math:`e_2`:

    .. math::

        \begin{pmatrix} y \\ u \\ v \end{pmatrix}_{e_1}
        \overset{T_{yuv \to rgb}^{e_1}}\longrightarrow
        \begin{pmatrix} r \\ g \\ b \end{pmatrix}_{e_1}
        \overset{T_{rgb \to xyz}^{e_1}}\longrightarrow
        \begin{pmatrix} x \\ y \\ z \end{pmatrix}_{\text{CIE}}
        \overset{T_{xyz \to rgb}^{e_2}}\longrightarrow
        \begin{pmatrix} r \\ g \\ b \end{pmatrix}_{e_2}
        \overset{T_{rgb \to yuv}^{e_2}}\longrightarrow
        \begin{pmatrix} y \\ u \\ v \end{pmatrix}_{e_2}

    With:

        * :math:`T_{yuv \to rgb}^{e_1}` is a non linear transformation using gamma correction
          and a linear transformation given by the inverse of
          :py:func:`cutcutcodec.core.filter.video.colorspace.rgb2yuv_matrix_from_kr_kb`
          matrix. It use ``transfer_in`` and ``primaries_in``.
        * :math:`T_{rgb \to xyz}^{e_1}` is a linear transformation given by the
          :py:func:`cutcutcodec.core.filter.video.colorspace.rgb2xyz_matrix_from_chroma`
          matrix. It use ``primaries_in``.
        * :math:`T_{xyz \to rgb}^{e_2}` is a linear transformation given by the inverse of
          :py:func:`cutcutcodec.core.filter.video.colorspace.rgb2xyz_matrix_from_chroma`
          matrix. It use ``primaries_out``.
        * :math:`T_{rgb \to yuv}^{e_2}` is a non linear transformation using gamma correction
          and a linear transformation given by
          :py:func:`cutcutcodec.core.filter.video.colorspace.rgb2yuv_matrix_from_kr_kb`
          matrix. It use ``transfer_out`` and ``primaries_out``.

    Symbols are floats (not integers) with values in the following ranges:

        * :math:`(y, u, v) \in [0, 1] \times \left[-\frac{1}{2}, \frac{1}{2}\right]^2`
        * :math:`(r, g, b) \in [0, 1]^3`
        * :math:`(x, y, z) \in \mathbb{R}^3`

    Parameters
    ----------
    primaries_in : str, optional
        Input data gamut color space name.
    primaries_out : str, optional
        Output data gamut color space name.
    transfer_in : str, optional
        The input transfer function (gamma). This value cannot be supplied without ``primaries_in``.

        * If provided, the input space is YUV,
          so the symbols Y, U and V symbols will be present in the final equation.
        * If it is not supplied but ``primaries_in`` is, the starting space is an RGB space,
          so the symbols R, G and B symbols will be present in the final equation.
        * If it is not supplied and ``primaries_in`` either, the starting space is CIE 1936 XYZ,
          so the symbols X, Y and Z symbols will be present in the final equation.
    transfer_out : str, optional
        The output transfer function (gamma).
        This value cannot be supplied without ``primaries_out``.

        * If provided, the output space is YUV.
        * If it is not supplied but ``primaries_out`` is, the output space is an RGB space.
        * If it is not supplied and ``primaries_in`` either, the final space is CIE 1936 XYZ.

    Returns
    -------
    componants : tuple[sympy.core.basic.Basic, sympy.core.basic.Basic, sympy.core.basic.Basic]
        The 3 sympy equations that link the input color space components,
        to each of the output components.

    Examples
    --------
    >>> import sympy
    >>> import torch
    >>> from cutcutcodec.core.compilation.sympy_to_torch.lambdify import Lambdify
    >>> from cutcutcodec.core.filter.video.colorspace import convert
    >>> # T from rgb to xyz in space e_1
    >>> sympy.Matrix(convert(primaries_in="bt709")).evalf(n=5)
    Matrix([
    [ 0.41239*b + 0.18048*g + 0.35758*r],
    [0.21264*b + 0.072192*g + 0.71517*r],
    [0.019331*b + 0.95053*g + 0.11919*r]])
    >>> # T from xyz to rgb in space e_2
    >>> sympy.Matrix(convert(primaries_out="bt2020")).evalf(n=5)
    Matrix([
    [-0.66668*x + 1.6165*y + 0.015769*z],
    [ 0.01764*x - 0.042771*y + 0.9421*z],
    [  1.7167*x - 0.35567*y - 0.25337*z]])
    >>> # T from rgb in space e_1 to rgb in space e_2
    >>> sympy.Matrix(convert(primaries_in="bt709", primaries_out="bt2020")).evalf(n=5)
    Matrix([
    [0.069097*b + 0.011362*g + 0.91954*r],
    [ 0.016391*b + 0.8956*g + 0.088013*r],
    [  0.6274*b + 0.043313*g + 0.32928*r]])
    >>>
    >>> trans_symb = convert(  # convertion from rec.709 to rec.2020
    ...     transfer_in="bt709",
    ...     primaries_in="bt709",
    ...     primaries_out="bt2020",
    ...     transfer_out="smpte2084",
    ... )
    >>> trans_func = Lambdify(trans_symb, shapes={sympy.symbols("y u v", real=True)})
    >>> yuv_709 = torch.rand(1_000_000), torch.rand(1_000_000)-0.5, torch.rand(1_000_000)-0.5
    >>> yuv_2020 = trans_func(y=yuv_709[0], u=yuv_709[1], v=yuv_709[2])
    >>>
    """
    assert transfer_in is None or primaries_in is not None, \
        "you must provide primaries_in if you provide transfer_in"
    assert transfer_out is None or primaries_out is not None, \
        "you must provide primaries_out if you provide transfer_out"

    # initialisation
    yuv = sympy.symbols("y u v", real=True)
    rgb = sympy.symbols("r g b", real=True)
    xyz = sympy.symbols("x y z", real=True)
    componants = sympy.Matrix(yuv)  # column vector

    # YUV -> RGB
    if transfer_in is not None:
        assert primaries_in in PRIMARIES, f"{primaries_in} not in {sorted(PRIMARIES)}"
        assert transfer_in in TRC, f"{transfer_in} not in {sorted(TRC)}"
        componants = rgb2yuv_matrix_from_kr_kb(
            *yuv_cst_from_chroma(*PRIMARIES[primaries_in])  # get kr and kb
        )**-1 @ componants
        trans = TRC[transfer_in][1]
        componants[0, 0] = trans.subs(V, componants[0, 0], simultaneous=True)
        componants[1, 0] = trans.subs(V, componants[1, 0], simultaneous=True)
        componants[2, 0] = trans.subs(V, componants[2, 0], simultaneous=True)
    else:
        componants = componants.subs(zip(yuv, rgb), simultaneous=True)

    # RGB -> XYZ
    if primaries_in is not None:
        assert primaries_in in PRIMARIES, f"{primaries_in} not in {sorted(PRIMARIES)}"
        componants = rgb2xyz_matrix_from_chroma(*PRIMARIES[primaries_in]) @ componants
    else:
        componants = componants.subs(zip(rgb, xyz), simultaneous=True)

    # XYZ -> RGB
    if primaries_out is not None:
        assert primaries_out in PRIMARIES, f"{primaries_out} not in {sorted(PRIMARIES)}"
        componants = rgb2xyz_matrix_from_chroma(*PRIMARIES[primaries_out])**-1 @ componants

    # RGB -> YUV
    if transfer_out:
        assert primaries_out in PRIMARIES, f"{primaries_out} not in {sorted(PRIMARIES)}"
        assert transfer_out in TRC, f"{transfer_out} not in {sorted(TRC)}"
        trans = TRC[transfer_out][0]
        componants[0, 0] = trans.subs(L, componants[0, 0], simultaneous=True)
        componants[1, 0] = trans.subs(L, componants[1, 0], simultaneous=True)
        componants[2, 0] = trans.subs(L, componants[2, 0], simultaneous=True)
        componants = rgb2yuv_matrix_from_kr_kb(
            *yuv_cst_from_chroma(*PRIMARIES[primaries_out])  # get kr and kb
        ) @ componants

    return (componants[0, 0], componants[1, 0], componants[2, 0])


def rgb2xyz_matrix_from_chroma(
    xy_r: tuple[NBR, NBR], xy_g: tuple[NBR, NBR], xy_b: tuple[NBR, NBR], xy_w: tuple[NBR, NBR]
) -> sympy.Matrix:
    r"""Compute the RGB to XYZ matrix from chromaticity coordinates and white point.

    Relationship between tristimulus values in CIE XYZ 1936 colour space and in RGB signal space.

    It is an implementation of the International Telecomunication Union Report ITU-R BT.2380-2.

    Returns the :math:`\mathbf{M}` matrix with :math:`(r, g, b) \in [0, 1]^3` such as:

    .. math::
        :label: rgb2xyz

        \begin{pmatrix} x \\ y \\ z \\ \end{pmatrix}
        = \mathbf{M} \begin{pmatrix} r \\ g \\ b \\ \end{pmatrix}

    Where

    .. math::

        \begin{cases}
            (x'_r, y'_r, z'_r) = \left(\frac{x_r}{y_r}, 1, \frac{1-x_r-y_r}{y_r}\right) \\
            (x'_g, y'_g, z'_g) = \left(\frac{x_g}{y_g}, 1, \frac{1-x_g-y_g}{y_g}\right) \\
            (x'_r, y'_r, z'_r) = \left(\frac{x_r}{y_r}, 1, \frac{1-x_r-y_r}{y_r}\right) \\
            (x'_w, y'_w, z'_w) = \left(\frac{x_w}{y_w}, 1, \frac{1-x_w-y_w}{y_w}\right) \\
            \begin{pmatrix}  s_r \\ s_g \\ s_b \end{pmatrix} = \begin{pmatrix}
                x'_r & x'_g & x'_b \\
                y'_r & y'_g & y'_b \\
                z'_r & z'_g & z'_b \\
            \end{pmatrix}^{-1} \begin{pmatrix} x'_w \\ y'_w \\ z'_w \end{pmatrix} \\
            \mathbf{M} = \begin{pmatrix}
                s_r x'_r & s_g x'_g & s_b x'_b \\
                s_r y'_r & s_g y'_g & s_b y'_b \\
                s_r z'_r & s_g z'_g & s_b z'_b \\
            \end{pmatrix} \\
        \end{cases}

    Parameters
    ----------
    xy_r : tuple
        The red point :math:`(x_r, y_r)` in the xyz space.
    xy_g : tuple
        The green point :math:`(x_g, y_g)` in the xyz space.
    xy_b : tuple
        The blue point :math:`(x_b, y_b)` in the xyz space.
    xy_w : tuple
        The white point :math:`(x_w, y_w)` in the xyz space.

    Returns
    -------
    rgb2xyz : sympy.Matrix
        The 3x3 :math:`\mathbf{M}` matrix, sometimes called ``primaries``,
        which converts points from RGB space to XYZ space :eq:`rgb2xyz`.

    Examples
    --------
    >>> import sympy
    >>> from cutcutcodec.core.filter.video.colorspace import rgb2xyz_matrix_from_chroma
    >>> wrgb = sympy.Matrix([[1, 1, 0, 0],  # red
    ...                      [1, 0, 1, 0],  # green
    ...                      [1, 0, 0, 1]]) # blue
    ...
    >>> # rec.709
    >>> xy_r, xy_g, xy_b, white = (0.640, 0.330), (0.300, 0.600), (0.150, 0.060), (0.3127, 0.3290)
    >>> m_709 = rgb2xyz_matrix_from_chroma(xy_r, xy_g, xy_b, white)
    >>> # rec.2020
    >>> xy_r, xy_g, xy_b, white = (0.708, 0.292), (0.170, 0.797), (0.131, 0.046), (0.3127, 0.3290)
    >>> m_2020 = rgb2xyz_matrix_from_chroma(xy_r, xy_g, xy_b, white)
    >>>
    >>> # convert from rec.709 to rec.2020
    >>> (m_2020**-1 @ m_709 @ wrgb).evalf(n=5)
    Matrix([
    [1.0,   0.6274,  0.32928, 0.043313],
    [1.0, 0.069097,  0.91954, 0.011362],
    [1.0, 0.016391, 0.088013,   0.8956]])
    >>>
    """
    assert isinstance(xy_r, tuple), xy_r.__class__.__name__
    assert isinstance(xy_g, tuple), xy_g.__class__.__name__
    assert isinstance(xy_b, tuple), xy_b.__class__.__name__
    assert isinstance(xy_w, tuple), xy_w.__class__.__name__
    assert len(xy_r) == 2, xy_r
    assert len(xy_g) == 2, xy_g
    assert len(xy_b) == 2, xy_b
    assert len(xy_w) == 2, xy_w

    def xy_to_xyz(x, y):
        return [x / y, 1, (1 - x - y) / y]

    # columns rbg, rows xyz
    rgb2xyz = sympy.Matrix([xy_to_xyz(*xy_r), xy_to_xyz(*xy_g), xy_to_xyz(*xy_b)]).T
    s_rgb = rgb2xyz**-1 @ sympy.Matrix([xy_to_xyz(*xy_w)]).T  # column vectors
    rgb2xyz = rgb2xyz @ sympy.diag(*s_rgb)  # hack for elementwise product

    return rgb2xyz


def rgb2yuv_matrix_from_kr_kb(k_r: NBR, k_b: NBR) -> sympy.Matrix:
    r"""Compute the RGB to YpPbPr matrix from the kr and kb constants.

    Relationship between gamma corrected R'G'B' colour space and Y'PbPr colour space.

    It is an implementation based on wikipedia.

    Returns the :math:`\mathbf{A}` matrix with :math:`(r', g', b') \in [0, 1]^3`
    and :math:`(y', p_b, p_r) \in [0, 1] \times \left[-\frac{1}{2}, \frac{1}{2}\right]^2` such as:

    .. math::
        :label: rgb2yuv

        \begin{pmatrix} y' \\ p_b \\ p_r \\ \end{pmatrix}
        = \mathbf{A} \begin{pmatrix} r' \\ g' \\ b' \\ \end{pmatrix}

    Where

    .. math::

        \begin{cases}
            k_r + k_g + k_b = 1 \\
            \mathbf{A} = \begin{pmatrix}
                k_r & k_g & k_b \\
                -\frac{k_r}{2-2k_b} & -\frac{k_g}{2-2k_b} & \frac{1}{2} \\
                \frac{1}{2} & -\frac{k_g}{2-2k_r} & -\frac{k_b}{2-2k_r} \\
            \end{pmatrix} \\
        \end{cases}


    Parameters
    ----------
    k_r, k_b
        The 2 scalars :math:`k_r` and :math:`k_b` :eq:`krkb`.
        They may come from :py:func:`cutcutcodec.core.filter.video.colorspace.yuv_cst_from_chroma`.

    Returns
    -------
    rgb2yuv : sympy.Matrix
        The 3x3 :math:`\mathbf{A}` color matrix.

    Examples
    --------
    >>> import sympy
    >>> from cutcutcodec.core.filter.video.colorspace import rgb2yuv_matrix_from_kr_kb
    >>> wrgb = sympy.Matrix([[1, 1, 0, 0],  # red
    ...                      [1, 0, 1, 0],  # green
    ...                      [1, 0, 0, 1]]) # blue
    ...
    >>> kr, kb = sympy.Rational(0.2126), sympy.Rational(0.0722)  # rec.709
    >>> a_709 = rgb2yuv_matrix_from_kr_kb(kr, kb)
    >>> (a_709 @ wrgb).evalf(n=5)
    Matrix([
    [1.0,   0.2126,   0.7152,    0.0722],
    [  0, -0.11457, -0.38543,       0.5],
    [  0,      0.5, -0.45415, -0.045847]])
    >>> kr = kb = sympy.sympify("1/3")  # for demo
    >>> rgb2yuv_matrix_from_kr_kb(kr, kb) @ wrgb
    Matrix([
    [1,  1/3,  1/3,  1/3],
    [0, -1/4, -1/4,  1/2],
    [0,  1/2, -1/4, -1/4]])
    >>>
    """
    assert isinstance(k_b, NBR), k_b.__class__.__name__
    assert isinstance(k_r, NBR), k_r.__class__.__name__

    k_g = 1 - k_r - k_b
    uscale = 1 / (2 - 2 * k_b)
    vscale = 1 / (2 - 2 * k_r)
    return sympy.Matrix([[k_r, k_g, k_b],
                         [-k_r * uscale, -k_g * uscale, sympy.core.numbers.Half()],
                         [sympy.core.numbers.Half(), -k_g * vscale, -k_b * vscale]])


def yuv_cst_from_chroma(
    xy_r: tuple[NBR, NBR], xy_g: tuple[NBR, NBR], xy_b: tuple[NBR, NBR], xy_w: tuple[NBR, NBR]
) -> tuple[NBR, NBR]:
    r"""Compute the kr and kb constants from chromaticity coordinates and white point.

    It is an implementation of the
    International Telecomunication Union Recomandation ITU-T H.273 (V4).

    .. math::
        :label: krkb

        k_r = \frac{\det\mathbf{R}}{\det\mathbf{D}} \\
        k_b = \frac{\det\mathbf{B}}{\det\mathbf{D}} \\

    Where

    .. math::

        \begin{cases}
            (x'_r, y'_r, z'_r) = \left(\frac{x_r}{y_r}, 1, \frac{1-x_r-y_r}{y_r}\right) \\
            (x'_g, y'_g, z'_g) = \left(\frac{x_g}{y_g}, 1, \frac{1-x_g-y_g}{y_g}\right) \\
            (x'_r, y'_r, z'_r) = \left(\frac{x_r}{y_r}, 1, \frac{1-x_r-y_r}{y_r}\right) \\
            (x'_w, y'_w, z'_w) = \left(\frac{x_w}{y_w}, 1, \frac{1-x_w-y_w}{y_w}\right) \\
            \mathbf{D} = \begin{pmatrix}
                x'_r & y'_r & z'_r \\
                x'_g & y'_g & z'_g \\
                x'_b & y'_b & z'_b \\
            \end{pmatrix} \\
            \mathbf{R} = \begin{pmatrix}
                x'_w & x'_g & x'_b \\
                y'_w & y'_g & y'_b \\
                z'_w & z'_g & z'_b \\
            \end{pmatrix} \\
            \mathbf{B} = \begin{pmatrix}
                x'_w & x'_r & x'_g \\
                y'_w & y'_r & y'_g \\
                z'_w & z'_r & z'_g \\
            \end{pmatrix} \\
        \end{cases}

    Parameters
    ----------
    xy_r : tuple
        The red point :math:`(x_r, y_r)` in the xyz space.
    xy_g : tuple
        The green point :math:`(x_g, y_g)` in the xyz space.
    xy_b : tuple
        The blue point :math:`(x_b, y_b)` in the xyz space.
    xy_w : tuple
        The white point :math:`(x_w, y_w)` in the xyz space.

    Returns
    -------
    k_r, k_b
        The 2 scalars :math:`k_r` and :math:`k_b` :eq:`krkb` used in rgb to yuv convertion.

    Examples
    --------
    >>> from cutcutcodec.core.filter.video.colorspace import yuv_cst_from_chroma
    >>> # rec.709
    >>> xy_r, xy_g, xy_b, white = (0.640, 0.330), (0.300, 0.600), (0.150, 0.060), (0.3127, 0.3290)
    >>> kr, kb = yuv_cst_from_chroma(xy_r, xy_g, xy_b, white)
    >>> round(kr, 5), round(kb, 5)
    (0.21264, 0.07219)
    >>> # rec.2020
    >>> xy_r, xy_g, xy_b, white = (0.708, 0.292), (0.170, 0.797), (0.131, 0.046), (0.3127, 0.3290)
    >>> kr, kb = yuv_cst_from_chroma(xy_r, xy_g, xy_b, white)
    >>> round(kr, 5), round(kb, 5)
    (0.26270, 0.05930)
    >>>
    """
    assert isinstance(xy_r, tuple), xy_r.__class__.__name__
    assert isinstance(xy_g, tuple), xy_g.__class__.__name__
    assert isinstance(xy_b, tuple), xy_b.__class__.__name__
    assert isinstance(xy_w, tuple), xy_w.__class__.__name__
    assert len(xy_r) == 2, xy_r
    assert len(xy_g) == 2, xy_g
    assert len(xy_b) == 2, xy_b
    assert len(xy_w) == 2, xy_w

    def xy_to_xyz(x, y):
        return [x / y, 1, (1 - x - y) / y]

    # version zscale
    xyz_r = xy_to_xyz(*xy_r)
    xyz_g = xy_to_xyz(*xy_g)
    xyz_b = xy_to_xyz(*xy_b)
    xyz_w = xy_to_xyz(*xy_w)
    denom = sympy.det(sympy.Matrix([xyz_r, xyz_g, xyz_b]))
    k_r = sympy.det(sympy.Matrix([xyz_w, xyz_g, xyz_b])) / denom  # det(A) = det(At)
    k_b = sympy.det(sympy.Matrix([xyz_w, xyz_r, xyz_g])) / denom

    # # version ITU
    # # this version is mathematically equivalent to the formula above
    # xyz_r = [*xy_r, 1 - (xy_r[0] + xy_r[1])]
    # xyz_g = [*xy_g, 1 - (xy_g[0] + xy_g[1])]
    # xyz_b = [*xy_b, 1 - (xy_b[0] + xy_b[1])]
    # xyz_w = [*xy_w, 1 - (xy_w[0] + xy_w[1])]
    # denom = xyz_w[1] * (
    #     xyz_r[0] * (xyz_g[1] * xyz_b[2] - xyz_b[1] * xyz_g[2])
    #     + xyz_g[0] * (xyz_b[1] * xyz_r[2] - xyz_r[1] * xyz_b[2])
    #     + xyz_b[0] * (xyz_r[1] * xyz_g[2] - xyz_g[1] * xyz_r[2])
    # )
    # k_r = xyz_r[1] * (
    #     xyz_w[0] * (xyz_g[1] * xyz_b[2] - xyz_b[1] * xyz_g[2])
    #     + xyz_w[1] * (xyz_b[0] * xyz_g[2] - xyz_g[0] * xyz_b[2])
    #     + xyz_w[2] * (xyz_g[0] * xyz_b[1] - xyz_b[0] * xyz_g[1])
    # ) / denom
    # k_b = xyz_b[1] * (
    #     xyz_w[0] * (xyz_r[1] * xyz_g[2] - xyz_g[1] * xyz_r[2])
    #     + xyz_w[1] * (xyz_g[0] * xyz_r[2] - xyz_r[0] * xyz_g[2])
    #     + xyz_w[2] * (xyz_r[0] * xyz_g[1] - xyz_g[0] * xyz_r[1])
    # ) / denom

    return k_r, k_b
