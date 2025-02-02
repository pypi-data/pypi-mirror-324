import datetime
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetFilteredAudioOut")


@_attrs_define
class GetFilteredAudioOut:
    """
    Attributes:
        created (datetime.datetime):
        updated (datetime.datetime):
        name (str):
        audio (str):
        id (Union[None, Unset, int]):
        slug (Union[None, Unset, str]):  Default: ''.
        description (Union[None, Unset, str]):
        transcription (Union[None, Unset, str]):
        duration (Union[None, Unset, str]):
    """

    created: datetime.datetime
    updated: datetime.datetime
    name: str
    audio: str
    id: Union[None, Unset, int] = UNSET
    slug: Union[None, Unset, str] = ""
    description: Union[None, Unset, str] = UNSET
    transcription: Union[None, Unset, str] = UNSET
    duration: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created = self.created.isoformat()

        updated = self.updated.isoformat()

        name = self.name

        audio = self.audio

        id: Union[None, Unset, int]
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        slug: Union[None, Unset, str]
        if isinstance(self.slug, Unset):
            slug = UNSET
        else:
            slug = self.slug

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        transcription: Union[None, Unset, str]
        if isinstance(self.transcription, Unset):
            transcription = UNSET
        else:
            transcription = self.transcription

        duration: Union[None, Unset, str]
        if isinstance(self.duration, Unset):
            duration = UNSET
        else:
            duration = self.duration

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created": created,
                "updated": updated,
                "name": name,
                "audio": audio,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if slug is not UNSET:
            field_dict["slug"] = slug
        if description is not UNSET:
            field_dict["description"] = description
        if transcription is not UNSET:
            field_dict["transcription"] = transcription
        if duration is not UNSET:
            field_dict["duration"] = duration

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        created = isoparse(d.pop("created"))

        updated = isoparse(d.pop("updated"))

        name = d.pop("name")

        audio = d.pop("audio")

        def _parse_id(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        id = _parse_id(d.pop("id", UNSET))

        def _parse_slug(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        slug = _parse_slug(d.pop("slug", UNSET))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_transcription(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        transcription = _parse_transcription(d.pop("transcription", UNSET))

        def _parse_duration(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        duration = _parse_duration(d.pop("duration", UNSET))

        get_filtered_audio_out = cls(
            created=created,
            updated=updated,
            name=name,
            audio=audio,
            id=id,
            slug=slug,
            description=description,
            transcription=transcription,
            duration=duration,
        )

        get_filtered_audio_out.additional_properties = d
        return get_filtered_audio_out

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
