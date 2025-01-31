"""
This module provides access to Blender's image manipulation API.

imbuf.types.rst

:maxdepth: 1
:caption: Submodules

"""

import typing
import collections.abc
import typing_extensions
import imbuf.types

from . import types as types

def load(filepath: str) -> imbuf.types.ImBuf:
    """Load an image from a file.

    :param filepath: the filepath of the image.
    :type filepath: str
    :return: the newly loaded image.
    :rtype: imbuf.types.ImBuf
    """

def new(size) -> imbuf.types.ImBuf:
    """Load a new image.

    :param size: The size of the image in pixels.
    :return: the newly loaded image.
    :rtype: imbuf.types.ImBuf
    """

def write(image: imbuf.types.ImBuf, filepath: str):
    """Write an image.

    :param image: the image to write.
    :type image: imbuf.types.ImBuf
    :param filepath: the filepath of the image.
    :type filepath: str
    """
