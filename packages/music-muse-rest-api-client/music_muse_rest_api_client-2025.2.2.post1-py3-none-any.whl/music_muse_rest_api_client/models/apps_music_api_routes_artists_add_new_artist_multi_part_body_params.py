import datetime
import json
from io import BytesIO
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.apps_music_api_routes_artists_add_new_artist_multi_part_body_params_artist_gender import (
    AppsMusicApiRoutesArtistsAddNewArtistMultiPartBodyParamsArtistGender,
)
from ..types import UNSET, File, FileJsonType, Unset

T = TypeVar("T", bound="AppsMusicApiRoutesArtistsAddNewArtistMultiPartBodyParams")


@_attrs_define
class AppsMusicApiRoutesArtistsAddNewArtistMultiPartBodyParams:
    """
    Attributes:
        name (str):
        gender (AppsMusicApiRoutesArtistsAddNewArtistMultiPartBodyParamsArtistGender):
        description (Union[None, Unset, str]):
        birth_date (Union[None, Unset, datetime.date]):
        country (Union[Unset, str]):  Default: 'RUS'.
        genres_ids (Union[Unset, list[int]]):
        label_id (Union[None, Unset, int]):
        bio (Union[None, Unset, str]):
        is_verified (Union[Unset, bool]):  Default: False.
        avatar (Union[Unset, File]):
    """

    name: str
    gender: AppsMusicApiRoutesArtistsAddNewArtistMultiPartBodyParamsArtistGender
    description: Union[None, Unset, str] = UNSET
    birth_date: Union[None, Unset, datetime.date] = UNSET
    country: Union[Unset, str] = "RUS"
    genres_ids: Union[Unset, list[int]] = UNSET
    label_id: Union[None, Unset, int] = UNSET
    bio: Union[None, Unset, str] = UNSET
    is_verified: Union[Unset, bool] = False
    avatar: Union[Unset, File] = UNSET
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

        avatar: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.avatar, Unset):
            avatar = self.avatar.to_tuple()

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
        if avatar is not UNSET:
            field_dict["avatar"] = avatar

        return field_dict

    def to_multipart(self) -> dict[str, Any]:
        name = (None, str(self.name).encode(), "text/plain")

        gender = (None, str(self.gender.value).encode(), "text/plain")

        description: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.description, Unset):
            description = UNSET
        elif isinstance(self.description, str):
            description = (None, str(self.description).encode(), "text/plain")
        else:
            description = (None, str(self.description).encode(), "text/plain")

        birth_date: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.birth_date, Unset):
            birth_date = UNSET
        elif isinstance(self.birth_date, datetime.date):
            birth_date = self.birth_date.isoformat().encode()
        else:
            birth_date = (None, str(self.birth_date).encode(), "text/plain")

        country = self.country if isinstance(self.country, Unset) else (None, str(self.country).encode(), "text/plain")

        genres_ids: Union[Unset, tuple[None, bytes, str]] = UNSET
        if not isinstance(self.genres_ids, Unset):
            _temp_genres_ids = self.genres_ids
            genres_ids = (None, json.dumps(_temp_genres_ids).encode(), "application/json")

        label_id: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.label_id, Unset):
            label_id = UNSET
        elif isinstance(self.label_id, int):
            label_id = (None, str(self.label_id).encode(), "text/plain")
        else:
            label_id = (None, str(self.label_id).encode(), "text/plain")

        bio: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.bio, Unset):
            bio = UNSET
        elif isinstance(self.bio, str):
            bio = (None, str(self.bio).encode(), "text/plain")
        else:
            bio = (None, str(self.bio).encode(), "text/plain")

        is_verified = (
            self.is_verified
            if isinstance(self.is_verified, Unset)
            else (None, str(self.is_verified).encode(), "text/plain")
        )

        avatar: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.avatar, Unset):
            avatar = self.avatar.to_tuple()

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

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
        if avatar is not UNSET:
            field_dict["avatar"] = avatar

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        gender = AppsMusicApiRoutesArtistsAddNewArtistMultiPartBodyParamsArtistGender(d.pop("gender"))

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

        _avatar = d.pop("avatar", UNSET)
        avatar: Union[Unset, File]
        if isinstance(_avatar, Unset):
            avatar = UNSET
        else:
            avatar = File(payload=BytesIO(_avatar))

        apps_music_api_routes_artists_add_new_artist_multi_part_body_params = cls(
            name=name,
            gender=gender,
            description=description,
            birth_date=birth_date,
            country=country,
            genres_ids=genres_ids,
            label_id=label_id,
            bio=bio,
            is_verified=is_verified,
            avatar=avatar,
        )

        apps_music_api_routes_artists_add_new_artist_multi_part_body_params.additional_properties = d
        return apps_music_api_routes_artists_add_new_artist_multi_part_body_params

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
