from io import BytesIO
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, File, FileJsonType, Unset

T = TypeVar("T", bound="AppsMusicApiRoutesLabelsUpdateLabelMultiPartBodyParams")


@_attrs_define
class AppsMusicApiRoutesLabelsUpdateLabelMultiPartBodyParams:
    """
    Attributes:
        name (Union[None, Unset, str]):
        description (Union[None, Unset, str]):
        logo (Union[Unset, File]):
    """

    name: Union[None, Unset, str] = UNSET
    description: Union[None, Unset, str] = UNSET
    logo: Union[Unset, File] = UNSET
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

        logo: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.logo, Unset):
            logo = self.logo.to_tuple()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if logo is not UNSET:
            field_dict["logo"] = logo

        return field_dict

    def to_multipart(self) -> dict[str, Any]:
        name: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.name, Unset):
            name = UNSET
        elif isinstance(self.name, str):
            name = (None, str(self.name).encode(), "text/plain")
        else:
            name = (None, str(self.name).encode(), "text/plain")

        description: Union[Unset, tuple[None, bytes, str]]

        if isinstance(self.description, Unset):
            description = UNSET
        elif isinstance(self.description, str):
            description = (None, str(self.description).encode(), "text/plain")
        else:
            description = (None, str(self.description).encode(), "text/plain")

        logo: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.logo, Unset):
            logo = self.logo.to_tuple()

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if logo is not UNSET:
            field_dict["logo"] = logo

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
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

        _logo = d.pop("logo", UNSET)
        logo: Union[Unset, File]
        if isinstance(_logo, Unset):
            logo = UNSET
        else:
            logo = File(payload=BytesIO(_logo))

        apps_music_api_routes_labels_update_label_multi_part_body_params = cls(
            name=name,
            description=description,
            logo=logo,
        )

        apps_music_api_routes_labels_update_label_multi_part_body_params.additional_properties = d
        return apps_music_api_routes_labels_update_label_multi_part_body_params

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
