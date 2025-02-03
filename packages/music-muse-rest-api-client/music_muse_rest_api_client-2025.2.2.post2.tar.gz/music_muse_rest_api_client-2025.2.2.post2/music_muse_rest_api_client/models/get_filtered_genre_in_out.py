import datetime
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetFilteredGenreInOut")


@_attrs_define
class GetFilteredGenreInOut:
    """
    Attributes:
        pk (int):
        name (str):
        slug (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        description (Union[None, Unset, str]):
        parent_genre_id (Union[None, Unset, int]):
        image_cover (Union[None, Unset, str]):
    """

    pk: int
    name: str
    slug: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    description: Union[None, Unset, str] = UNSET
    parent_genre_id: Union[None, Unset, int] = UNSET
    image_cover: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        pk = self.pk

        name = self.name

        slug = self.slug

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        parent_genre_id: Union[None, Unset, int]
        if isinstance(self.parent_genre_id, Unset):
            parent_genre_id = UNSET
        else:
            parent_genre_id = self.parent_genre_id

        image_cover: Union[None, Unset, str]
        if isinstance(self.image_cover, Unset):
            image_cover = UNSET
        else:
            image_cover = self.image_cover

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "pk": pk,
                "name": name,
                "slug": slug,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if parent_genre_id is not UNSET:
            field_dict["parent_genre_id"] = parent_genre_id
        if image_cover is not UNSET:
            field_dict["image_cover"] = image_cover

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        pk = d.pop("pk")

        name = d.pop("name")

        slug = d.pop("slug")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_parent_genre_id(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        parent_genre_id = _parse_parent_genre_id(d.pop("parent_genre_id", UNSET))

        def _parse_image_cover(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        image_cover = _parse_image_cover(d.pop("image_cover", UNSET))

        get_filtered_genre_in_out = cls(
            pk=pk,
            name=name,
            slug=slug,
            created_at=created_at,
            updated_at=updated_at,
            description=description,
            parent_genre_id=parent_genre_id,
            image_cover=image_cover,
        )

        get_filtered_genre_in_out.additional_properties = d
        return get_filtered_genre_in_out

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
