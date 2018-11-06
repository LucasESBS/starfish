"""
This module parses and retains the extras metadata attached to TileSet extras.
"""

from typing import Collection, Mapping, MutableMapping

from slicedimage import TileSet

from starfish.types import Indices


class TileMetadataKey:
    """
    This class is used to index into the TileMetadata class.
    """
    def __init__(self, *, round: int, ch: int, z: int) -> None:
        self._round = round
        self._ch = ch
        self._z = z

    @property
    def round(self) -> int:
        return self._round

    @property
    def ch(self) -> int:
        return self._ch

    @property
    def z(self) -> int:
        return self._z

    def __eq__(self, other) -> bool:
        if not isinstance(other, TileMetadataKey):
            return False

        return self._round == other.round and self._ch == other.ch and self._z == other.z

    def __hash__(self) -> int:
        return self._round ^ self._ch ^ self._z

    def __repr__(self) -> str:
        return f"round: {self._round} ch: {self._ch} z: {self._z}"


class TileSetMetadata:
    """
    This class parses and retains the extras metadata from a TileSet and the extras metadata from
    the individual tiles making up that TileSet.
    """
    def __init__(self, tileset: TileSet) -> None:
        tile_extras: MutableMapping[TileMetadataKey, dict] = dict()
        for tile in tileset.tiles():
            round_ = tile.indices[Indices.ROUND]
            ch = tile.indices[Indices.CH]
            z = tile.indices.get(Indices.Z, 0)

            tile_extras[TileMetadataKey(round=round_, ch=ch, z=z)] = tile.extras

        self.tile_extras: Mapping[TileMetadataKey, dict] = tile_extras
        self._extras = tileset.extras

    def __getitem__(self, tilekey: TileMetadataKey) -> dict:
        """Returns the extras metadata for a given tile, addressed by its TileMetadataKey"""
        return self.tile_extras[tilekey]

    def keys(self) -> Collection[TileMetadataKey]:
        """Returns a Collection of the TileMetadataKeys for all the tiles."""
        return self.tile_extras.keys()

    @property
    def extras(self) -> dict:
        """Returns the extras metadata for the TileSet."""
        return self._extras
