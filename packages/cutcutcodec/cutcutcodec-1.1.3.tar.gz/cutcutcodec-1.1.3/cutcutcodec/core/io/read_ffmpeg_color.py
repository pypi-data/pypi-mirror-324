#!/usr/bin/env python3

"""Delegate the reading to the module read_ffmpeg, and add a filter to manage the colorspace."""

import av
import sympy

from cutcutcodec.core.filter.identity import FilterIdentity
from cutcutcodec.core.filter.video.colorspace import convert
from cutcutcodec.core.filter.video.colorspace_cst import FFMPEG_PRIMARIES, FFMPEG_TRC
from cutcutcodec.core.filter.video.equation import FilterVideoEquation
from .pix_map import PIX_MAP
from .read_ffmpeg import ContainerInputFFMPEG, _StreamFFMPEGBase


class ContainerInputFFMPEGColor:
    """Same as ContainerInputFFMPEG with colorspace convertion.

    Examples
    --------
    >>> import torch
    >>> from cutcutcodec.core.analysis.stream.shape import optimal_shape_video
    >>> from cutcutcodec.core.io.read_ffmpeg_color import ContainerInputFFMPEGColor
    >>> container = ContainerInputFFMPEGColor("cutcutcodec/examples/intro.webm")
    >>> for stream in container.out_streams:
    ...     if stream.type == "video":
    ...         stream.snapshot(0, optimal_shape_video(stream)).shape
    ...     elif stream.type == "audio":
    ...         torch.round(stream.snapshot(0, rate=2, samples=3), decimals=5)
    ...
    (720, 1280, 3)
    (360, 640, 3)
    FrameAudio(0, 2, 'stereo', [[     nan,  0.1804 , -0.34765],
                                [     nan, -0.07236,  0.07893]])
    FrameAudio(0, 2, 'mono', [[     nan,  0.06998, -0.24758]])
    """

    def __new__(cls, *args, **kwargs):
        """Create a basic ContainerInputFFMPEG then convert the colorspace."""
        container = ContainerInputFFMPEG(*args, **kwargs)
        return cls.conv_colors(container.out_streams)

    @staticmethod
    def conv_colors(in_streams: tuple[_StreamFFMPEGBase]) -> FilterIdentity:
        """Apply the color convertion on the video streams."""
        assert all(isinstance(s, _StreamFFMPEGBase) for s in in_streams)
        streams = []
        for stream in in_streams:
            if stream.type == "video":
                stream_av = stream.av_container.streams[stream.index]
                # stream_av.codec_context.colorspace
                pix = PIX_MAP[stream_av.codec_context.format.name]
                # print(f"from {stream_av.codec_context.format.name} to {pix}")
                if "gray" in pix:
                    streams.append(stream)
                    continue
                if "yuv" in pix:
                    transfer_in = FFMPEG_TRC[stream_av.codec_context.color_trc]
                    # print(f"transfer_in = {transfer_in}")
                    yuv = sympy.symbols("y u v", real=True)
                    mapping = {yuv[0]: "b0", yuv[1]: "g0", yuv[2]: "r0"}
                else:
                    transfer_in = None
                    rgb = sympy.symbols("r g b", real=True)
                    mapping = {rgb[0]: "r0", rgb[1]: "g0", rgb[2]: "b0"}
                primaries_in = FFMPEG_PRIMARIES[stream_av.codec_context.color_primaries]
                # print(f"primaries_in = {primaries_in}")
                conv = sympy.Tuple(
                    *convert(
                        transfer_in=transfer_in,
                        primaries_in=primaries_in,
                        primaries_out="smpte240m",
                    )[::-1]  # rgb to bgr
                ).subs(mapping)
                if len(av.video.format.VideoFormat(pix).components) == 4:
                    conv = (*conv, "a0")
                streams.append(FilterVideoEquation([stream], *conv).out_streams[0])
            else:
                streams.append(stream)
        return FilterIdentity(streams)
