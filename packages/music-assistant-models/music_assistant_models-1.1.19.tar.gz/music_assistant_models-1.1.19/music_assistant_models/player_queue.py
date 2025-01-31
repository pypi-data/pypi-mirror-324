"""Model(s) for PlayerQueue."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Self

from mashumaro import DataClassDictMixin

from .enums import PlayerState, RepeatMode
from .media_items import MediaItemType
from .queue_item import QueueItem


@dataclass
class PlayLogEntry:
    """Representation of a PlayLogEntry within Music Assistant."""

    queue_item_id: str
    duration: int | None = None
    seconds_streamed: float | None = None


@dataclass
class PlayerQueue(DataClassDictMixin):
    """Representation of a PlayerQueue within Music Assistant."""

    queue_id: str
    active: bool
    display_name: str
    available: bool
    items: int

    shuffle_enabled: bool = False
    repeat_mode: RepeatMode = RepeatMode.OFF
    dont_stop_the_music_enabled: bool = False
    # current_index: index that is active (e.g. being played) by the player
    current_index: int | None = None
    # index_in_buffer: index that has been preloaded/buffered by the player
    index_in_buffer: int | None = None
    elapsed_time: float = 0
    elapsed_time_last_updated: float = field(default_factory=time.time)
    state: PlayerState = PlayerState.IDLE
    current_item: QueueItem | None = None
    next_item: QueueItem | None = None
    radio_source: list[MediaItemType] = field(default_factory=list)
    enqueued_media_items: list[MediaItemType] = field(default_factory=list)
    flow_mode: bool = False
    resume_pos: int = 0
    flow_mode_stream_log: list[PlayLogEntry] = field(default_factory=list)
    next_track_enqueued: str | None = None

    @property
    def corrected_elapsed_time(self) -> float:
        """Return the corrected/realtime elapsed time."""
        return self.elapsed_time + (time.time() - self.elapsed_time_last_updated)

    def __post_serialize__(self, d: dict[Any, Any]) -> dict[Any, Any]:
        """Execute action(s) on serialization."""
        d.pop("flow_mode_stream_log", None)
        d.pop("next_track_enqueued", None)
        return d

    def to_cache(self) -> dict[str, Any]:
        """Return the dict that is suitable for storing into the cache db."""
        d = self.to_dict()
        d.pop("current_item", None)
        d.pop("next_item", None)
        d.pop("index_in_buffer", None)
        d.pop("flow_mode", None)
        d.pop("next_track_enqueued", None)
        d.pop("flow_mode_stream_log", None)
        return d

    @classmethod
    def from_cache(cls, d: dict[Any, Any]) -> Self:
        """Restore a PlayerQueue from a cache dict."""
        d.pop("current_item", None)
        d.pop("next_item", None)
        d.pop("index_in_buffer", None)
        d.pop("flow_mode", None)
        d.pop("next_track_enqueued", None)
        d.pop("flow_mode_stream_log", None)
        return cls.from_dict(d)
