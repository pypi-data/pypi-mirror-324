import datetime
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetImagePagesOut")


@_attrs_define
class GetImagePagesOut:
    """
    Attributes:
        created (datetime.datetime):
        updated (datetime.datetime):
        name (str):
        id (Union[None, Unset, int]):
        slug (Union[None, Unset, str]):  Default: ''.
        description (Union[None, Unset, str]):
        image (Union[Unset, str]):
        image_width (Union[None, Unset, int]):
        image_height (Union[None, Unset, int]):
    """

    created: datetime.datetime
    updated: datetime.datetime
    name: str
    id: Union[None, Unset, int] = UNSET
    slug: Union[None, Unset, str] = ""
    description: Union[None, Unset, str] = UNSET
    image: Union[Unset, str] = UNSET
    image_width: Union[None, Unset, int] = UNSET
    image_height: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created = self.created.isoformat()

        updated = self.updated.isoformat()

        name = self.name

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

        image = self.image

        image_width: Union[None, Unset, int]
        if isinstance(self.image_width, Unset):
            image_width = UNSET
        else:
            image_width = self.image_width

        image_height: Union[None, Unset, int]
        if isinstance(self.image_height, Unset):
            image_height = UNSET
        else:
            image_height = self.image_height

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created": created,
                "updated": updated,
                "name": name,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if slug is not UNSET:
            field_dict["slug"] = slug
        if description is not UNSET:
            field_dict["description"] = description
        if image is not UNSET:
            field_dict["image"] = image
        if image_width is not UNSET:
            field_dict["image_width"] = image_width
        if image_height is not UNSET:
            field_dict["image_height"] = image_height

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        created = isoparse(d.pop("created"))

        updated = isoparse(d.pop("updated"))

        name = d.pop("name")

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

        image = d.pop("image", UNSET)

        def _parse_image_width(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        image_width = _parse_image_width(d.pop("image_width", UNSET))

        def _parse_image_height(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        image_height = _parse_image_height(d.pop("image_height", UNSET))

        get_image_pages_out = cls(
            created=created,
            updated=updated,
            name=name,
            id=id,
            slug=slug,
            description=description,
            image=image,
            image_width=image_width,
            image_height=image_height,
        )

        get_image_pages_out.additional_properties = d
        return get_image_pages_out

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
