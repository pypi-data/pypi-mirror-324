"""Model(s) for streamdetails."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from mashumaro import DataClassDictMixin

from .dsp import DSPDetails
from .enums import MediaType, StreamType, VolumeNormalizationMode
from .media_items import AudioFormat


@dataclass
class LivestreamMetadata(DataClassDictMixin):
    """Metadata of livestream."""

    title: str | None = None  # optional
    artist: str | None = None  # optional
    album: str | None = None  # optional
    image_url: str | None = None  # optional


@dataclass(kw_only=True)
class StreamDetails(DataClassDictMixin):
    """Model for streamdetails."""

    # NOTE: the actual provider/itemid of the streamdetails may differ
    # from the connected media_item due to track linking etc.
    # the streamdetails are only used to provide details about the content
    # that is going to be streamed.

    # mandatory fields
    provider: str
    item_id: str
    audio_format: AudioFormat
    media_type: MediaType = MediaType.TRACK
    stream_type: StreamType = StreamType.CUSTOM

    # optional fields

    # path: url or (local accessible) path to the stream (if not custom stream)
    path: str | None = None

    # duration of the item to stream, copied from media_item if omitted
    duration: int | None = None
    # total size in bytes of the item, calculated at eof when omitted
    size: int | None = None
    # data: provider specific data (not exposed externally)
    # this info is for example used to pass slong details to the get_audio_stream
    data: Any = None
    # allow_seek: bool to indicate that the content can/may be seeked
    # If set to False, seeking will be completely disabled.
    # NOTE: this is automatically disabled for duration-less streams (e/g. radio)
    allow_seek: bool = True
    # can_seek: bool to indicate that the custom audio stream can be seeked
    # if set to False, and allow seek is set to True, the core logic will attempt
    # to seek in the incoming (bytes)stream, which is not a guarantee it will work.
    # If allow_seek is also set to False, seeking will be completely disabled.
    can_seek: bool = True
    # extra_input_args: any additional input args to pass along to ffmpeg
    extra_input_args: list[str] = field(default_factory=list)
    # decryption_key: decryption key for encrypted streams
    decryption_key: str | None = None
    # stream_metadata: radio/live streams can optionally set/use this field
    # to set the metadata of any media during the stream
    stream_metadata: LivestreamMetadata | None = None

    # the fields below will be set/controlled by the streamcontroller
    seek_position: int = 0
    fade_in: bool = False
    loudness: float | None = None
    loudness_album: float | None = None
    prefer_album_loudness: bool = False
    volume_normalization_mode: VolumeNormalizationMode | None = None
    queue_id: str | None = None
    seconds_streamed: float | None = None
    target_loudness: float | None = None
    strip_silence_begin: bool = False
    strip_silence_end: bool = False
    stream_error: bool | None = None
    # This contains the DSPDetails of all players in the group.
    # In case of single player playback, dict will contain only one entry.
    # The leader will have is_leader set to True.
    # (keep in mind that PlayerGroups have no (explicit) leader!)
    dsp: dict[str, DSPDetails] | None = None

    def __str__(self) -> str:
        """Return pretty printable string of object."""
        return self.uri

    def __post_serialize__(self, d: dict[Any, Any]) -> dict[Any, Any]:
        """Execute action(s) on serialization."""
        d.pop("queue_id", None)
        d.pop("seconds_streamed", None)
        d.pop("seek_position", None)
        d.pop("fade_in", None)
        # for backwards compatibility
        d["stream_title"] = self.stream_title
        return d

    @property
    def uri(self) -> str:
        """Return uri representation of item."""
        return f"{self.provider}://{self.media_type.value}/{self.item_id}"

    @property
    def stream_title(self) -> str | None:
        """Return simple (instead of full metadata) streamtitle for backwards compatibility."""
        if self.stream_metadata and self.stream_metadata.title:
            if self.stream_metadata.artist:
                return f"{self.stream_metadata.artist} - {self.stream_metadata.title}"
            return self.stream_metadata.title
        return None

    @stream_title.setter
    def stream_title(self, value: str | None) -> None:
        """Set simple streamtitle (instead of full metadata) for backwards compatibility."""
        if value is None:
            self.stream_metadata = None
            return
        if not self.stream_metadata:
            self.stream_metadata = LivestreamMetadata()
        if " - " in value:
            artist, title = value.split(" - ", 1)
            self.stream_metadata.artist = artist
            self.stream_metadata.title = title
        else:
            self.stream_metadata.title = value
