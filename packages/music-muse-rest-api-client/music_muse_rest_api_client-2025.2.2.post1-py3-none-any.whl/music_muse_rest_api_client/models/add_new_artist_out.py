import datetime
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.artist_gender import ArtistGender
from ..types import UNSET, Unset

T = TypeVar("T", bound="AddNewArtistOut")


@_attrs_define
class AddNewArtistOut:
    """
    Attributes:
        id (int):
        name (str):
        country (str):
        is_verified (bool):
        gender (ArtistGender):
        description (Union[None, Unset, str]):
        birth_date (Union[None, Unset, datetime.date]):
        genres (Union[None, Unset, list[str]]):
        label (Union[None, Unset, str]):
        bio (Union[None, Unset, str]):
        avatar (Union[None, Unset, str]):
    """

    id: int
    name: str
    country: str
    is_verified: bool
    gender: ArtistGender
    description: Union[None, Unset, str] = UNSET
    birth_date: Union[None, Unset, datetime.date] = UNSET
    genres: Union[None, Unset, list[str]] = UNSET
    label: Union[None, Unset, str] = UNSET
    bio: Union[None, Unset, str] = UNSET
    avatar: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        country = self.country

        is_verified = self.is_verified

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

        genres: Union[None, Unset, list[str]]
        if isinstance(self.genres, Unset):
            genres = UNSET
        elif isinstance(self.genres, list):
            genres = self.genres

        else:
            genres = self.genres

        label: Union[None, Unset, str]
        if isinstance(self.label, Unset):
            label = UNSET
        else:
            label = self.label

        bio: Union[None, Unset, str]
        if isinstance(self.bio, Unset):
            bio = UNSET
        else:
            bio = self.bio

        avatar: Union[None, Unset, str]
        if isinstance(self.avatar, Unset):
            avatar = UNSET
        else:
            avatar = self.avatar

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "country": country,
                "is_verified": is_verified,
                "gender": gender,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if birth_date is not UNSET:
            field_dict["birth_date"] = birth_date
        if genres is not UNSET:
            field_dict["genres"] = genres
        if label is not UNSET:
            field_dict["label"] = label
        if bio is not UNSET:
            field_dict["bio"] = bio
        if avatar is not UNSET:
            field_dict["avatar"] = avatar

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        country = d.pop("country")

        is_verified = d.pop("is_verified")

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

        def _parse_genres(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                genres_type_0 = cast(list[str], data)

                return genres_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        genres = _parse_genres(d.pop("genres", UNSET))

        def _parse_label(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        label = _parse_label(d.pop("label", UNSET))

        def _parse_bio(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        bio = _parse_bio(d.pop("bio", UNSET))

        def _parse_avatar(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        avatar = _parse_avatar(d.pop("avatar", UNSET))

        add_new_artist_out = cls(
            id=id,
            name=name,
            country=country,
            is_verified=is_verified,
            gender=gender,
            description=description,
            birth_date=birth_date,
            genres=genres,
            label=label,
            bio=bio,
            avatar=avatar,
        )

        add_new_artist_out.additional_properties = d
        return add_new_artist_out

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
