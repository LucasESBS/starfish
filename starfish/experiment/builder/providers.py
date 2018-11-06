"""
This module describes the contracts to provide data to the experiment builder.
"""

from starfish.imagestack.providers import FetchedTile


class TileFetcher:
    """
    This is the contract for providing the image data for constructing a
    :class:`slicedimage.Collection`.
    """
    def get_tile(self, fov: int, r: int, ch: int, z: int) -> FetchedTile:
        """
        Given fov, r, ch, and z, return an instance of a :class:`.FetchedImage` that can be
        queried for the image data.
        """
        raise NotImplementedError()
