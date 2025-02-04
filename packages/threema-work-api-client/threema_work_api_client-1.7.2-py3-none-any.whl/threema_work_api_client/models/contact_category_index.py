from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.category import Category
    from ..models.link import Link
    from ..models.paging import Paging


T = TypeVar("T", bound="ContactCategoryIndex")


@_attrs_define
class ContactCategoryIndex:
    """
    Attributes:
        field_links (Union[Unset, list['Link']]):  Example: [{'ref': 'contact', 'link':
            'https://work.threema.ch/api/v1/contacts/ECHOECHO'}].
        categories (Union[Unset, list['Category']]): Categories Example: [{'_links': [{'ref': 'detail', 'link':
            'https://work.threema.ch/api/v1/category/yyyyyyyyyy'}], 'id': 'yyyyyyyyyy', 'name': 'Category 1 by MDM',
            'source': 'mdm'}, {'_links': [{'ref': 'detail', 'link': 'https://work.threema.ch/api/v1/category/xxxxxxxxx'}],
            'id': 'xxxxxxxxx', 'name': 'Category 2', 'source': 'custom'}].
        paging (Union[Unset, Paging]):
    """

    field_links: Union[Unset, list["Link"]] = UNSET
    categories: Union[Unset, list["Category"]] = UNSET
    paging: Union[Unset, "Paging"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_links: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.field_links, Unset):
            field_links = []
            for field_links_item_data in self.field_links:
                field_links_item = field_links_item_data.to_dict()
                field_links.append(field_links_item)

        categories: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.categories, Unset):
            categories = []
            for categories_item_data in self.categories:
                categories_item = categories_item_data.to_dict()
                categories.append(categories_item)

        paging: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.paging, Unset):
            paging = self.paging.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if field_links is not UNSET:
            field_dict["_links"] = field_links
        if categories is not UNSET:
            field_dict["categories"] = categories
        if paging is not UNSET:
            field_dict["paging"] = paging

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.category import Category
        from ..models.link import Link
        from ..models.paging import Paging

        d = src_dict.copy()
        field_links = []
        _field_links = d.pop("_links", UNSET)
        for field_links_item_data in _field_links or []:
            field_links_item = Link.from_dict(field_links_item_data)

            field_links.append(field_links_item)

        categories = []
        _categories = d.pop("categories", UNSET)
        for categories_item_data in _categories or []:
            categories_item = Category.from_dict(categories_item_data)

            categories.append(categories_item)

        _paging = d.pop("paging", UNSET)
        paging: Union[Unset, Paging]
        if isinstance(_paging, Unset):
            paging = UNSET
        else:
            paging = Paging.from_dict(_paging)

        contact_category_index = cls(
            field_links=field_links,
            categories=categories,
            paging=paging,
        )

        contact_category_index.additional_properties = d
        return contact_category_index

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
