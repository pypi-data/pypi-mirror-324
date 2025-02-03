import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.update_release_in_release_type import UpdateReleaseInReleaseType
    from ..models.update_release_in_status import UpdateReleaseInStatus


T = TypeVar("T", bound="UpdateReleaseIn")


@_attrs_define
class UpdateReleaseIn:
    """
    Attributes:
        name (Union[None, Unset, str]):
        description (Union[None, Unset, str]):
        label_ids (Union[Unset, list[int]]):
        artist_ids (Union[Unset, list[int]]):
        genre_ids (Union[Unset, list[int]]):
        release_type (Union[Unset, UpdateReleaseInReleaseType]):
        release_date (Union[None, Unset, datetime.date]):
        publication_time (Union[None, Unset, datetime.datetime]):
        status (Union[Unset, UpdateReleaseInStatus]):
    """

    name: Union[None, Unset, str] = UNSET
    description: Union[None, Unset, str] = UNSET
    label_ids: Union[Unset, list[int]] = UNSET
    artist_ids: Union[Unset, list[int]] = UNSET
    genre_ids: Union[Unset, list[int]] = UNSET
    release_type: Union[Unset, "UpdateReleaseInReleaseType"] = UNSET
    release_date: Union[None, Unset, datetime.date] = UNSET
    publication_time: Union[None, Unset, datetime.datetime] = UNSET
    status: Union[Unset, "UpdateReleaseInStatus"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        label_ids: Union[Unset, list[int]] = UNSET
        if not isinstance(self.label_ids, Unset):
            label_ids = self.label_ids

        artist_ids: Union[Unset, list[int]] = UNSET
        if not isinstance(self.artist_ids, Unset):
            artist_ids = self.artist_ids

        genre_ids: Union[Unset, list[int]] = UNSET
        if not isinstance(self.genre_ids, Unset):
            genre_ids = self.genre_ids

        release_type: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.release_type, Unset):
            release_type = self.release_type.to_dict()

        release_date: Union[None, Unset, str]
        if isinstance(self.release_date, Unset):
            release_date = UNSET
        elif isinstance(self.release_date, datetime.date):
            release_date = self.release_date.isoformat()
        else:
            release_date = self.release_date

        publication_time: Union[None, Unset, str]
        if isinstance(self.publication_time, Unset):
            publication_time = UNSET
        elif isinstance(self.publication_time, datetime.datetime):
            publication_time = self.publication_time.isoformat()
        else:
            publication_time = self.publication_time

        status: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if label_ids is not UNSET:
            field_dict["label_ids"] = label_ids
        if artist_ids is not UNSET:
            field_dict["artist_ids"] = artist_ids
        if genre_ids is not UNSET:
            field_dict["genre_ids"] = genre_ids
        if release_type is not UNSET:
            field_dict["release_type"] = release_type
        if release_date is not UNSET:
            field_dict["release_date"] = release_date
        if publication_time is not UNSET:
            field_dict["publication_time"] = publication_time
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.update_release_in_release_type import UpdateReleaseInReleaseType
        from ..models.update_release_in_status import UpdateReleaseInStatus

        d = src_dict.copy()

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        label_ids = cast(list[int], d.pop("label_ids", UNSET))

        artist_ids = cast(list[int], d.pop("artist_ids", UNSET))

        genre_ids = cast(list[int], d.pop("genre_ids", UNSET))

        _release_type = d.pop("release_type", UNSET)
        release_type: Union[Unset, UpdateReleaseInReleaseType]
        if isinstance(_release_type, Unset):
            release_type = UNSET
        else:
            release_type = UpdateReleaseInReleaseType.from_dict(_release_type)

        def _parse_release_date(data: object) -> Union[None, Unset, datetime.date]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                release_date_type_0 = isoparse(data).date()

                return release_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.date], data)

        release_date = _parse_release_date(d.pop("release_date", UNSET))

        def _parse_publication_time(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                publication_time_type_0 = isoparse(data)

                return publication_time_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        publication_time = _parse_publication_time(d.pop("publication_time", UNSET))

        _status = d.pop("status", UNSET)
        status: Union[Unset, UpdateReleaseInStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = UpdateReleaseInStatus.from_dict(_status)

        update_release_in = cls(
            name=name,
            description=description,
            label_ids=label_ids,
            artist_ids=artist_ids,
            genre_ids=genre_ids,
            release_type=release_type,
            release_date=release_date,
            publication_time=publication_time,
            status=status,
        )

        update_release_in.additional_properties = d
        return update_release_in

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
