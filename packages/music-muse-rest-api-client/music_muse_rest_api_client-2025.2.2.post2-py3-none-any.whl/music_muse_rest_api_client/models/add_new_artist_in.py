import datetime
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.artist_gender import ArtistGender
from ..types import UNSET, Unset

T = TypeVar("T", bound="AddNewArtistIn")


@_attrs_define
class AddNewArtistIn:
    """
    Attributes:
        name (str):
        gender (ArtistGender):
        description (Union[None, Unset, str]):
        birth_date (Union[None, Unset, datetime.date]):
        country (Union[Unset, str]):  Default: 'RUS'.
        genres_ids (Union[Unset, list[int]]):
        label_id (Union[None, Unset, int]):
        bio (Union[None, Unset, str]):
        is_verified (Union[Unset, bool]):  Default: False.
    """

    name: str
    gender: ArtistGender
    description: Union[None, Unset, str] = UNSET
    birth_date: Union[None, Unset, datetime.date] = UNSET
    country: Union[Unset, str] = "RUS"
    genres_ids: Union[Unset, list[int]] = UNSET
    label_id: Union[None, Unset, int] = UNSET
    bio: Union[None, Unset, str] = UNSET
    is_verified: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        gender = self.gender.value

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        birth_date: Union[None, Unset, str]
        if isinstance(self.birth_date, Unset):
            birth_date = UNSET
        elif isinstance(self.birth_date, datetime.date):
            birth_date = self.birth_date.isoformat()
        else:
            birth_date = self.birth_date

        country = self.country

        genres_ids: Union[Unset, list[int]] = UNSET
        if not isinstance(self.genres_ids, Unset):
            genres_ids = self.genres_ids

        label_id: Union[None, Unset, int]
        if isinstance(self.label_id, Unset):
            label_id = UNSET
        else:
            label_id = self.label_id

        bio: Union[None, Unset, str]
        if isinstance(self.bio, Unset):
            bio = UNSET
        else:
            bio = self.bio

        is_verified = self.is_verified

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "gender": gender,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if birth_date is not UNSET:
            field_dict["birth_date"] = birth_date
        if country is not UNSET:
            field_dict["country"] = country
        if genres_ids is not UNSET:
            field_dict["genres_ids"] = genres_ids
        if label_id is not UNSET:
            field_dict["label_id"] = label_id
        if bio is not UNSET:
            field_dict["bio"] = bio
        if is_verified is not UNSET:
            field_dict["is_verified"] = is_verified

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        gender = ArtistGender(d.pop("gender"))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_birth_date(data: object) -> Union[None, Unset, datetime.date]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                birth_date_type_0 = isoparse(data).date()

                return birth_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.date], data)

        birth_date = _parse_birth_date(d.pop("birth_date", UNSET))

        country = d.pop("country", UNSET)

        genres_ids = cast(list[int], d.pop("genres_ids", UNSET))

        def _parse_label_id(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        label_id = _parse_label_id(d.pop("label_id", UNSET))

        def _parse_bio(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        bio = _parse_bio(d.pop("bio", UNSET))

        is_verified = d.pop("is_verified", UNSET)

        add_new_artist_in = cls(
            name=name,
            gender=gender,
            description=description,
            birth_date=birth_date,
            country=country,
            genres_ids=genres_ids,
            label_id=label_id,
            bio=bio,
            is_verified=is_verified,
        )

        add_new_artist_in.additional_properties = d
        return add_new_artist_in

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
