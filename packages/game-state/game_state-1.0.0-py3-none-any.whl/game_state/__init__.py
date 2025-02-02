"""
Game-State Manager
~~~~~~~~~~~~~~~~~~

A utility package for pygame to manage multiple screens.

:copyright: (c) 2024-present Jiggly-Balls
:license: MIT, see LICENSE for more details.

"""

__version__ = "1.0.0"
__title__ = "game-state"
__author__ = "Jiggly-Balls"
__license__ = "MIT"
__copyright__ = "Copyright 2024-present Jiggly Balls"

from game_state.manager import StateManager
from game_state.state import State
from typing import NamedTuple, Literal

__all__ = ("State", "StateManager")


class VersionInfo(NamedTuple):
    major: int
    minor: int
    release_level: Literal["alpha", "beta", "final"]


def _expand() -> VersionInfo:
    v = __version__.split(".")
    level_types = {"a": "alpha", "b": "beta"}
    level = level_types.get(v[-1], "final")
    return VersionInfo(major=v[0], minor=v[1], release_level=level)


version_info: VersionInfo = _expand()
