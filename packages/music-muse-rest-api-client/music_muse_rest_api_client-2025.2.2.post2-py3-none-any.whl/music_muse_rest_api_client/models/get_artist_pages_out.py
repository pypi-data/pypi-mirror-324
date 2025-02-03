from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.get_artist_pages_item_out import GetArtistPagesItemOut


T = TypeVar("T", bound="GetArtistPagesOut")


@_attrs_define
class GetArtistPagesOut:
    """
    Attributes:
        items (list['GetArtistPagesItemOut']):
        total (int):
        per_page (int):
    """

    items: list["GetArtistPagesItemOut"]
    total: int
    per_page: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        total = self.total

        per_page = self.per_page

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "items": items,
                "total": total,
                "per_page": per_page,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.get_artist_pages_item_out import GetArtistPagesItemOut

        d = src_dict.copy()
        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = GetArtistPagesItemOut.from_dict(items_item_data)

            items.append(items_item)

        total = d.pop("total")

        per_page = d.pop("per_page")

        get_artist_pages_out = cls(
            items=items,
            total=total,
            per_page=per_page,
        )

        get_artist_pages_out.additional_properties = d
        return get_artist_pages_out

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
