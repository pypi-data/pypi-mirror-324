from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AddNewGenreIn")


@_attrs_define
class AddNewGenreIn:
    """
    Attributes:
        pk (int):
        name (str):
        description (Union[None, Unset, str]):
        parent_genre_id (Union[None, Unset, int]):
        short_name (Union[None, Unset, str]):
        russian_name (Union[None, Unset, str]):
    """

    pk: int
    name: str
    description: Union[None, Unset, str] = UNSET
    parent_genre_id: Union[None, Unset, int] = UNSET
    short_name: Union[None, Unset, str] = UNSET
    russian_name: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        pk = self.pk

        name = self.name

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

        short_name: Union[None, Unset, str]
        if isinstance(self.short_name, Unset):
            short_name = UNSET
        else:
            short_name = self.short_name

        russian_name: Union[None, Unset, str]
        if isinstance(self.russian_name, Unset):
            russian_name = UNSET
        else:
            russian_name = self.russian_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "pk": pk,
                "name": name,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if parent_genre_id is not UNSET:
            field_dict["parent_genre_id"] = parent_genre_id
        if short_name is not UNSET:
            field_dict["short_name"] = short_name
        if russian_name is not UNSET:
            field_dict["russian_name"] = russian_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        pk = d.pop("pk")

        name = d.pop("name")

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

        def _parse_short_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        short_name = _parse_short_name(d.pop("short_name", UNSET))

        def _parse_russian_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        russian_name = _parse_russian_name(d.pop("russian_name", UNSET))

        add_new_genre_in = cls(
            pk=pk,
            name=name,
            description=description,
            parent_genre_id=parent_genre_id,
            short_name=short_name,
            russian_name=russian_name,
        )

        add_new_genre_in.additional_properties = d
        return add_new_genre_in

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
