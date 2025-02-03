from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.add_new_track_in_status import AddNewTrackInStatus


T = TypeVar("T", bound="AddNewTrackIn")


@_attrs_define
class AddNewTrackIn:
    """
    Attributes:
        name (str):
        release_id (int):
        description (Union[None, Unset, str]):
        label_id (Union[None, Unset, int]):
        artist_ids (Union[Unset, list[int]]):
        genre_ids (Union[Unset, list[int]]):
        status (Union[Unset, AddNewTrackInStatus]):
    """

    name: str
    release_id: int
    description: Union[None, Unset, str] = UNSET
    label_id: Union[None, Unset, int] = UNSET
    artist_ids: Union[Unset, list[int]] = UNSET
    genre_ids: Union[Unset, list[int]] = UNSET
    status: Union[Unset, "AddNewTrackInStatus"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        release_id = self.release_id

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

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "release_id": release_id,
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

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.add_new_track_in_status import AddNewTrackInStatus

        d = src_dict.copy()
        name = d.pop("name")

        release_id = d.pop("release_id")

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
        status: Union[Unset, AddNewTrackInStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = AddNewTrackInStatus.from_dict(_status)

        add_new_track_in = cls(
            name=name,
            release_id=release_id,
            description=description,
            label_id=label_id,
            artist_ids=artist_ids,
            genre_ids=genre_ids,
            status=status,
        )

        add_new_track_in.additional_properties = d
        return add_new_track_in

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
