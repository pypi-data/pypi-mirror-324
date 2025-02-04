from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.category_source import CategorySource
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.link import Link


T = TypeVar("T", bound="Category")


@_attrs_define
class Category:
    """
    Attributes:
        field_links (Union[Unset, list['Link']]):  Example: [{'ref': 'detail', 'link':
            'https://work.threema.ch/api/v1/categories/yyyyyyyy'}, {'ref': 'contacts', 'link':
            'https://work.threema.ch/api/v1/contacts?cat=yyyyyyyy'}, {'ref': 'index', 'link':
            'https://work.threema.ch/api/v1/categories'}].
        id (Union[Unset, str]): Category id Example: yyyyyyyyyy.
        name (Union[Unset, str]): Name of the category Example: Category 1.
        source (Union[Unset, CategorySource]):  Example: custom.
        enabled (Union[Unset, bool]):  Example: true.
    """

    field_links: Union[Unset, list["Link"]] = UNSET
    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    source: Union[Unset, CategorySource] = UNSET
    enabled: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_links: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.field_links, Unset):
            field_links = []
            for field_links_item_data in self.field_links:
                field_links_item = field_links_item_data.to_dict()
                field_links.append(field_links_item)

        id = self.id

        name = self.name

        source: Union[Unset, str] = UNSET
        if not isinstance(self.source, Unset):
            source = self.source.value

        enabled = self.enabled

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if field_links is not UNSET:
            field_dict["_links"] = field_links
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if source is not UNSET:
            field_dict["source"] = source
        if enabled is not UNSET:
            field_dict["enabled"] = enabled

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.link import Link

        d = src_dict.copy()
        field_links = []
        _field_links = d.pop("_links", UNSET)
        for field_links_item_data in _field_links or []:
            field_links_item = Link.from_dict(field_links_item_data)

            field_links.append(field_links_item)

        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        _source = d.pop("source", UNSET)
        source: Union[Unset, CategorySource]
        if isinstance(_source, Unset):
            source = UNSET
        else:
            source = CategorySource(_source)

        enabled = d.pop("enabled", UNSET)

        category = cls(
            field_links=field_links,
            id=id,
            name=name,
            source=source,
            enabled=enabled,
        )

        category.additional_properties = d
        return category

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
