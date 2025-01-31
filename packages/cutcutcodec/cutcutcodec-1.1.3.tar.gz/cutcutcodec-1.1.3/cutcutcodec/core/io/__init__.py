#!/usr/bin/env python3

"""Manage the input/output layer."""

import logging
import pathlib
import typing

from cutcutcodec.core.exceptions import DecodeError
from cutcutcodec.core.classes.node import Node
from .read_ffmpeg_color import ContainerInputFFMPEGColor
from .read_image import ContainerInputImage
from .read_svg import ContainerInputSVG
from .write_ffmpeg import ContainerOutputFFMPEG


IMAGE_EXTENSION = {
    ".bmp", ".dib",  # always supported
    ".jpeg", ".jpg", ".jpe",
    ".jp2",
    ".png",
    ".webp",
    ".avif",
    ".pbm", ".pgm", ".ppm", ".pxm", ".pnm",  # always supported
    ".pfm",
    ".sr",  ".ras",
    ".tif", ".tiff",
    ".exr",
    ".hdr", ".pic"  # always supported
}
VIDEO_EXTENSION = {
    ".avi", ".mkv", ".mp4", ".vob", ".webm"
}


__all__ = ["read", "IMAGE_EXTENSION", "VIDEO_EXTENSION"]


def read(filename: typing.Union[str, bytes, pathlib.Path], **kwargs) -> Node:
    """Open the media file with the appropriate reader.

    Parameters
    ----------
    filename : pathlike
        The path to the file to be decoded.
    **kwargs : dict
        Transmitted to ``cutcutcodec.core.io.read_ffmpeg.ContainerInputFFMPEGColor``
        or ``cutcutcodec.core.io.read_image.ContainerInputImage``
        or ``cutcutcodec.core.io.read_svg.ContainerInputSVG``.

    Returns
    -------
    container : cutcutcodec.core.classes.container.ContainerInput
        The appropriated instanciated container, according to the nature of the file.

    Raises
    ------
    cutcutcodec.core.exceptions.DecodeError
        If the file can not be decoded by any reader.
    """
    extension = pathlib.Path(filename).suffix.lower()

    # simple case where extension is knowned
    if extension in VIDEO_EXTENSION:
        return ContainerInputFFMPEGColor(filename, **kwargs)
    if extension in IMAGE_EXTENSION:
        return ContainerInputImage(filename, **kwargs)
    if extension in {".svg"}:
        return ContainerInputSVG(filename, **kwargs)

    # case we have to try
    logging.warning("unknowned extension %s, try several readers", extension)
    try:
        return ContainerInputSVG(filename, **kwargs)
    except DecodeError:
        try:
            return ContainerInputImage(filename, **kwargs)
        except DecodeError:
            return ContainerInputFFMPEGColor(filename, **kwargs)


def write(*args, **kwargs):
    """Alias to ``cutcutcodec.core.io.write_ffmpeg.ContainerOutputFFMPEG``."""
    ContainerOutputFFMPEG(*args, **kwargs).write()
