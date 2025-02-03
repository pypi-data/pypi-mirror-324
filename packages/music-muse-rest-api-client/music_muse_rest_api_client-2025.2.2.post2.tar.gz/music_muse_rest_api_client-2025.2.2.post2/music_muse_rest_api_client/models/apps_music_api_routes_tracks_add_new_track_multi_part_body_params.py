import json
from io import BytesIO
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, File, FileJsonType, Unset

if TYPE_CHECKING:
    from ..models.apps_music_api_routes_tracks_add_new_track_multi_part_body_params_status import (
        AppsMusicApiRoutesTracksAddNewTrackMultiPartBodyParamsStatus,
    )


T = TypeVar("T", bound="AppsMusicApiRoutesTracksAddNewTrackMultiPartBodyParams")


@_attrs_define
class AppsMusicApiRoutesTracksAddNewTrackMultiPartBodyParams:
    """
    Attributes:
        name (str):
        release_id (int):
        audio (File):
        description (Union[None, Unset, str]):
        label_id (Union[None, Unset, int]):
        artist_ids (Union[Unset, list[int]]):
        genre_ids (Union[Unset, list[int]]):
        status (Union[Unset, AppsMusicApiRoutesTracksAddNewTrackMultiPartBodyParamsStatus]):
        video (Union[Unset, File]):
        cover (Union[Unset, File]):
    """

    name: str
    release_id: int
    audio: File
    description: Union[None, Unset, str] = UNSET
    label_id: Union[None, Unset, int] = UNSET
    artist_ids: Union[Unset, list[int]] = UNSET
    genre_ids: Union[Unset, list[int]] = UNSET
    status: Union[Unset, "AppsMusicApiRoutesTracksAddNewTrackMultiPartBodyParamsStatus"] = UNSET
    video: Union[Unset, File] = UNSET
    cover: Union[Unset, File] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        release_id = self.release_id

        audio = self.audio.to_tuple()

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        label_id: Union[None, Unset, int]
        if isinstance(self.label_id, Unset):
            label_id = UNSET
        else:
            label_id = self.label_id

        artist_ids: Union[Unset, list[int]] = UNSET
        if not isinstance(self.artist_ids, Unset):
            artist_ids = self.artist_ids

        genre_ids: Union[Unset, list[int]] = UNSET
        if not isinstance(self.genre_ids, Unset):
            genre_ids = self.genre_ids

        status: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.to_dict()

        video: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.video, Unset):
            video = self.video.to_tuple()

        cover: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.cover, Unset):
            cover = self.cover.to_tuple()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "release_id": release_id,
                "audio": audio,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if label_id is not UNSET:
            field_dict["label_id"] = label_id
        if artist_ids is not UNSET:
            field_dict["artist_ids"] = artist_ids
        if genre_ids is not UNSET:
            field_dict["genre_ids"] = genre_ids
        if status is not UNSET:
            field_dict["status"] = status
        if video is not UNSET:
            field_dict["video"] = video
        if cover is not UNSET:
            field_dict["cover"] = cover

        return field_dict

    def to_multipart(self) -> dict[str, Any]:
        name = (None, str(self.name).encode(), "text/plain")

        release_id = (None, str(self.release_id).encode(), "text/plain")

        audio = self.audio.to_tuple()

        description: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.description, Unset):
            description = UNSET
        elif isinstance(self.description, str):
            description = (None, str(self.description).encode(), "text/plain")
        else:
            description = (None, str(self.description).encode(), "text/plain")

        label_id: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.label_id, Unset):
            label_id = UNSET
        elif isinstance(self.label_id, int):
            label_id = (None, str(self.label_id).encode(), "text/plain")
        else:
            label_id = (None, str(self.label_id).encode(), "text/plain")

        artist_ids: Union[Unset, tuple[None, bytes, str]] = UNSET
        if not isinstance(self.artist_ids, Unset):
            _temp_artist_ids = self.artist_ids
            artist_ids = (None, json.dumps(_temp_artist_ids).encode(), "application/json")

        genre_ids: Union[Unset, tuple[None, bytes, str]] = UNSET
        if not isinstance(self.genre_ids, Unset):
            _temp_genre_ids = self.genre_ids
            genre_ids = (None, json.dumps(_temp_genre_ids).encode(), "application/json")

        status: Union[Unset, tuple[None, bytes, str]] = UNSET
        if not isinstance(self.status, Unset):
            status = (None, json.dumps(self.status.to_dict()).encode(), "application/json")

        video: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.video, Unset):
            video = self.video.to_tuple()

        cover: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.cover, Unset):
            cover = self.cover.to_tuple()

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update(
            {
                "name": name,
                "release_id": release_id,
                "audio": audio,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if label_id is not UNSET:
            field_dict["label_id"] = label_id
        if artist_ids is not UNSET:
            field_dict["artist_ids"] = artist_ids
        if genre_ids is not UNSET:
            field_dict["genre_ids"] = genre_ids
        if status is not UNSET:
            field_dict["status"] = status
        if video is not UNSET:
            field_dict["video"] = video
        if cover is not UNSET:
            field_dict["cover"] = cover

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.apps_music_api_routes_tracks_add_new_track_multi_part_body_params_status import (
            AppsMusicApiRoutesTracksAddNewTrackMultiPartBodyParamsStatus,
        )

        d = src_dict.copy()
        name = d.pop("name")

        release_id = d.pop("release_id")

        audio = File(payload=BytesIO(d.pop("audio")))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_label_id(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        label_id = _parse_label_id(d.pop("label_id", UNSET))

        artist_ids = cast(list[int], d.pop("artist_ids", UNSET))

        genre_ids = cast(list[int], d.pop("genre_ids", UNSET))

        _status = d.pop("status", UNSET)
        status: Union[Unset, AppsMusicApiRoutesTracksAddNewTrackMultiPartBodyParamsStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = AppsMusicApiRoutesTracksAddNewTrackMultiPartBodyParamsStatus.from_dict(_status)

        _video = d.pop("video", UNSET)
        video: Union[Unset, File]
        if isinstance(_video, Unset):
            video = UNSET
        else:
            video = File(payload=BytesIO(_video))

        _cover = d.pop("cover", UNSET)
        cover: Union[Unset, File]
        if isinstance(_cover, Unset):
            cover = UNSET
        else:
            cover = File(payload=BytesIO(_cover))

        apps_music_api_routes_tracks_add_new_track_multi_part_body_params = cls(
            name=name,
            release_id=release_id,
            audio=audio,
            description=description,
            label_id=label_id,
            artist_ids=artist_ids,
            genre_ids=genre_ids,
            status=status,
            video=video,
            cover=cover,
        )

        apps_music_api_routes_tracks_add_new_track_multi_part_body_params.additional_properties = d
        return apps_music_api_routes_tracks_add_new_track_multi_part_body_params

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
