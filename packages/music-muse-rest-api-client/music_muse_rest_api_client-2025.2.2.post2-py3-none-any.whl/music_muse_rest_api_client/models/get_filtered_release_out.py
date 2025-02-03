import datetime
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.release_types import ReleaseTypes
from ..models.statuses import Statuses
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetFilteredReleaseOut")


@_attrs_define
class GetFilteredReleaseOut:
    """
    Attributes:
        pk (int):
        name (str):
        release_type (ReleaseTypes):
        status (Statuses):
        created (datetime.datetime):
        updated (datetime.datetime):
        description (Union[None, Unset, str]):
        cover_image (Union[None, Unset, str]):
        release_date (Union[None, Unset, datetime.date]):
        labels_names (Union[None, Unset, list[str]]):
        artists_names (Union[None, Unset, list[str]]):
        genres_names (Union[None, Unset, list[str]]):
    """

    pk: int
    name: str
    release_type: ReleaseTypes
    status: Statuses
    created: datetime.datetime
    updated: datetime.datetime
    description: Union[None, Unset, str] = UNSET
    cover_image: Union[None, Unset, str] = UNSET
    release_date: Union[None, Unset, datetime.date] = UNSET
    labels_names: Union[None, Unset, list[str]] = UNSET
    artists_names: Union[None, Unset, list[str]] = UNSET
    genres_names: Union[None, Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        pk = self.pk

        name = self.name

        release_type = self.release_type.value

        status = self.status.value

        created = self.created.isoformat()

        updated = self.updated.isoformat()

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        cover_image: Union[None, Unset, str]
        if isinstance(self.cover_image, Unset):
            cover_image = UNSET
        else:
            cover_image = self.cover_image

        release_date: Union[None, Unset, str]
        if isinstance(self.release_date, Unset):
            release_date = UNSET
        elif isinstance(self.release_date, datetime.date):
            release_date = self.release_date.isoformat()
        else:
            release_date = self.release_date

        labels_names: Union[None, Unset, list[str]]
        if isinstance(self.labels_names, Unset):
            labels_names = UNSET
        elif isinstance(self.labels_names, list):
            labels_names = self.labels_names

        else:
            labels_names = self.labels_names

        artists_names: Union[None, Unset, list[str]]
        if isinstance(self.artists_names, Unset):
            artists_names = UNSET
        elif isinstance(self.artists_names, list):
            artists_names = self.artists_names

        else:
            artists_names = self.artists_names

        genres_names: Union[None, Unset, list[str]]
        if isinstance(self.genres_names, Unset):
            genres_names = UNSET
        elif isinstance(self.genres_names, list):
            genres_names = self.genres_names

        else:
            genres_names = self.genres_names

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "pk": pk,
                "name": name,
                "release_type": release_type,
                "status": status,
                "created": created,
                "updated": updated,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if cover_image is not UNSET:
            field_dict["cover_image"] = cover_image
        if release_date is not UNSET:
            field_dict["release_date"] = release_date
        if labels_names is not UNSET:
            field_dict["labels_names"] = labels_names
        if artists_names is not UNSET:
            field_dict["artists_names"] = artists_names
        if genres_names is not UNSET:
            field_dict["genres_names"] = genres_names

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        pk = d.pop("pk")

        name = d.pop("name")

        release_type = ReleaseTypes(d.pop("release_type"))

        status = Statuses(d.pop("status"))

        created = isoparse(d.pop("created"))

        updated = isoparse(d.pop("updated"))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_cover_image(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        cover_image = _parse_cover_image(d.pop("cover_image", UNSET))

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

        def _parse_labels_names(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                labels_names_type_0 = cast(list[str], data)

                return labels_names_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        labels_names = _parse_labels_names(d.pop("labels_names", UNSET))

        def _parse_artists_names(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                artists_names_type_0 = cast(list[str], data)

                return artists_names_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        artists_names = _parse_artists_names(d.pop("artists_names", UNSET))

        def _parse_genres_names(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                genres_names_type_0 = cast(list[str], data)

                return genres_names_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        genres_names = _parse_genres_names(d.pop("genres_names", UNSET))

        get_filtered_release_out = cls(
            pk=pk,
            name=name,
            release_type=release_type,
            status=status,
            created=created,
            updated=updated,
            description=description,
            cover_image=cover_image,
            release_date=release_date,
            labels_names=labels_names,
            artists_names=artists_names,
            genres_names=genres_names,
        )

        get_filtered_release_out.additional_properties = d
        return get_filtered_release_out

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
