from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.link import Link


T = TypeVar("T", bound="Paging")


@_attrs_define
class Paging:
    """
    Attributes:
        count (Union[Unset, int]):  Example: 20.
        total (Union[Unset, int]):  Example: 400.
        page (Union[Unset, int]):  Example: 9.
        field_links (Union[Unset, list['Link']]):
    """

    count: Union[Unset, int] = UNSET
    total: Union[Unset, int] = UNSET
    page: Union[Unset, int] = UNSET
    field_links: Union[Unset, list["Link"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        count = self.count

        total = self.total

        page = self.page

        field_links: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.field_links, Unset):
            field_links = []
            for field_links_item_data in self.field_links:
                field_links_item = field_links_item_data.to_dict()
                field_links.append(field_links_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if count is not UNSET:
            field_dict["count"] = count
        if total is not UNSET:
            field_dict["total"] = total
        if page is not UNSET:
            field_dict["page"] = page
        if field_links is not UNSET:
            field_dict["_links"] = field_links

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.link import Link

        d = src_dict.copy()
        count = d.pop("count", UNSET)

        total = d.pop("total", UNSET)

        page = d.pop("page", UNSET)

        field_links = []
        _field_links = d.pop("_links", UNSET)
        for field_links_item_data in _field_links or []:
            field_links_item = Link.from_dict(field_links_item_data)

            field_links.append(field_links_item)

        paging = cls(
            count=count,
            total=total,
            page=page,
            field_links=field_links,
        )

        paging.additional_properties = d
        return paging

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
