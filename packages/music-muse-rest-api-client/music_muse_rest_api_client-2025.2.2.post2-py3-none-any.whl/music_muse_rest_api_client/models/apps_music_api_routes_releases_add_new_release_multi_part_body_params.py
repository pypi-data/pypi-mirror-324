import datetime
import json
from io import BytesIO
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, File, FileJsonType, Unset

if TYPE_CHECKING:
    from ..models.apps_music_api_routes_releases_add_new_release_multi_part_body_params_release_type import (
        AppsMusicApiRoutesReleasesAddNewReleaseMultiPartBodyParamsReleaseType,
    )
    from ..models.apps_music_api_routes_releases_add_new_release_multi_part_body_params_status import (
        AppsMusicApiRoutesReleasesAddNewReleaseMultiPartBodyParamsStatus,
    )


T = TypeVar("T", bound="AppsMusicApiRoutesReleasesAddNewReleaseMultiPartBodyParams")


@_attrs_define
class AppsMusicApiRoutesReleasesAddNewReleaseMultiPartBodyParams:
    """
    Attributes:
        name (str):
        description (Union[None, Unset, str]):
        label_ids (Union[Unset, list[int]]):
        artist_ids (Union[Unset, list[int]]):
        genre_ids (Union[Unset, list[int]]):
        release_type (Union[Unset, AppsMusicApiRoutesReleasesAddNewReleaseMultiPartBodyParamsReleaseType]):
        release_date (Union[None, Unset, datetime.date]):
        publication_time (Union[None, Unset, datetime.datetime]):
        status (Union[Unset, AppsMusicApiRoutesReleasesAddNewReleaseMultiPartBodyParamsStatus]):
        cover_image (Union[Unset, File]):
    """

    name: str
    description: Union[None, Unset, str] = UNSET
    label_ids: Union[Unset, list[int]] = UNSET
    artist_ids: Union[Unset, list[int]] = UNSET
    genre_ids: Union[Unset, list[int]] = UNSET
    release_type: Union[Unset, "AppsMusicApiRoutesReleasesAddNewReleaseMultiPartBodyParamsReleaseType"] = UNSET
    release_date: Union[None, Unset, datetime.date] = UNSET
    publication_time: Union[None, Unset, datetime.datetime] = UNSET
    status: Union[Unset, "AppsMusicApiRoutesReleasesAddNewReleaseMultiPartBodyParamsStatus"] = UNSET
    cover_image: Union[Unset, File] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
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

        cover_image: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.cover_image, Unset):
            cover_image = self.cover_image.to_tuple()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
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
        if cover_image is not UNSET:
            field_dict["cover_image"] = cover_image

        return field_dict

    def to_multipart(self) -> dict[str, Any]:
        name = (None, str(self.name).encode(), "text/plain")

        description: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.description, Unset):
            description = UNSET
        elif isinstance(self.description, str):
            description = (None, str(self.description).encode(), "text/plain")
        else:
            description = (None, str(self.description).encode(), "text/plain")

        label_ids: Union[Unset, tuple[None, bytes, str]] = UNSET
        if not isinstance(self.label_ids, Unset):
            _temp_label_ids = self.label_ids
            label_ids = (None, json.dumps(_temp_label_ids).encode(), "application/json")

        artist_ids: Union[Unset, tuple[None, bytes, str]] = UNSET
        if not isinstance(self.artist_ids, Unset):
            _temp_artist_ids = self.artist_ids
            artist_ids = (None, json.dumps(_temp_artist_ids).encode(), "application/json")

        genre_ids: Union[Unset, tuple[None, bytes, str]] = UNSET
        if not isinstance(self.genre_ids, Unset):
            _temp_genre_ids = self.genre_ids
            genre_ids = (None, json.dumps(_temp_genre_ids).encode(), "application/json")

        release_type: Union[Unset, tuple[None, bytes, str]] = UNSET
        if not isinstance(self.release_type, Unset):
            release_type = (None, json.dumps(self.release_type.to_dict()).encode(), "application/json")

        release_date: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.release_date, Unset):
            release_date = UNSET
        elif isinstance(self.release_date, datetime.date):
            release_date = self.release_date.isoformat().encode()
        else:
            release_date = (None, str(self.release_date).encode(), "text/plain")

        publication_time: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.publication_time, Unset):
            publication_time = UNSET
        elif isinstance(self.publication_time, datetime.datetime):
            publication_time = self.publication_time.isoformat().encode()
        else:
            publication_time = (None, str(self.publication_time).encode(), "text/plain")

        status: Union[Unset, tuple[None, bytes, str]] = UNSET
        if not isinstance(self.status, Unset):
            status = (None, json.dumps(self.status.to_dict()).encode(), "application/json")

        cover_image: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.cover_image, Unset):
            cover_image = self.cover_image.to_tuple()

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update(
            {
                "name": name,
            }
        )
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
        if cover_image is not UNSET:
            field_dict["cover_image"] = cover_image

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.apps_music_api_routes_releases_add_new_release_multi_part_body_params_release_type import (
            AppsMusicApiRoutesReleasesAddNewReleaseMultiPartBodyParamsReleaseType,
        )
        from ..models.apps_music_api_routes_releases_add_new_release_multi_part_body_params_status import (
            AppsMusicApiRoutesReleasesAddNewReleaseMultiPartBodyParamsStatus,
        )

        d = src_dict.copy()
        name = d.pop("name")

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
        release_type: Union[Unset, AppsMusicApiRoutesReleasesAddNewReleaseMultiPartBodyParamsReleaseType]
        if isinstance(_release_type, Unset):
            release_type = UNSET
        else:
            release_type = AppsMusicApiRoutesReleasesAddNewReleaseMultiPartBodyParamsReleaseType.from_dict(
                _release_type
            )

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
        status: Union[Unset, AppsMusicApiRoutesReleasesAddNewReleaseMultiPartBodyParamsStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = AppsMusicApiRoutesReleasesAddNewReleaseMultiPartBodyParamsStatus.from_dict(_status)

        _cover_image = d.pop("cover_image", UNSET)
        cover_image: Union[Unset, File]
        if isinstance(_cover_image, Unset):
            cover_image = UNSET
        else:
            cover_image = File(payload=BytesIO(_cover_image))

        apps_music_api_routes_releases_add_new_release_multi_part_body_params = cls(
            name=name,
            description=description,
            label_ids=label_ids,
            artist_ids=artist_ids,
            genre_ids=genre_ids,
            release_type=release_type,
            release_date=release_date,
            publication_time=publication_time,
            status=status,
            cover_image=cover_image,
        )

        apps_music_api_routes_releases_add_new_release_multi_part_body_params.additional_properties = d
        return apps_music_api_routes_releases_add_new_release_multi_part_body_params

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
