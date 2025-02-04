from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.contact import Contact
    from ..models.link import Link
    from ..models.paging import Paging


T = TypeVar("T", bound="ContactIndex")


@_attrs_define
class ContactIndex:
    """
    Attributes:
        field_links (Union[Unset, list['Link']]):  Example: [{'ref': 'subscription', 'link':
            'https://work.threema.ch/api/v1'}].
        contacts (Union[Unset, list['Contact']]): Contact List Example: [{'_links': [{'ref': 'detail', 'link':
            'https://work.threema.ch/api/v1/contacts/*THREEMA'}, {'ref': 'detail', 'link':
            'https://work.threema.ch/api/v1/contacts/*THREEMA/categories'}], 'id': '*THREEMA', 'type': 'custom',
            'firstName': 'Threema', 'lastName': 'Channel', 'enabled': False}, {'_links': [{'ref': 'detail', 'link':
            'https://work.threema.ch/api/v1/contacts/ECHOECHO'}, {'ref': 'detail', 'link':
            'https://work.threema.ch/api/v1/contacts/ECHOECHO/categories'}], 'id': 'ECHOECHO', 'type': 'auto', 'firstName':
            'Echo', 'lastName': 'Ohce', 'enabled': True}].
        paging (Union[Unset, Paging]):
    """

    field_links: Union[Unset, list["Link"]] = UNSET
    contacts: Union[Unset, list["Contact"]] = UNSET
    paging: Union[Unset, "Paging"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_links: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.field_links, Unset):
            field_links = []
            for field_links_item_data in self.field_links:
                field_links_item = field_links_item_data.to_dict()
                field_links.append(field_links_item)

        contacts: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.contacts, Unset):
            contacts = []
            for contacts_item_data in self.contacts:
                contacts_item = contacts_item_data.to_dict()
                contacts.append(contacts_item)

        paging: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.paging, Unset):
            paging = self.paging.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if field_links is not UNSET:
            field_dict["_links"] = field_links
        if contacts is not UNSET:
            field_dict["contacts"] = contacts
        if paging is not UNSET:
            field_dict["paging"] = paging

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.contact import Contact
        from ..models.link import Link
        from ..models.paging import Paging

        d = src_dict.copy()
        field_links = []
        _field_links = d.pop("_links", UNSET)
        for field_links_item_data in _field_links or []:
            field_links_item = Link.from_dict(field_links_item_data)

            field_links.append(field_links_item)

        contacts = []
        _contacts = d.pop("contacts", UNSET)
        for contacts_item_data in _contacts or []:
            contacts_item = Contact.from_dict(contacts_item_data)

            contacts.append(contacts_item)

        _paging = d.pop("paging", UNSET)
        paging: Union[Unset, Paging]
        if isinstance(_paging, Unset):
            paging = UNSET
        else:
            paging = Paging.from_dict(_paging)

        contact_index = cls(
            field_links=field_links,
            contacts=contacts,
            paging=paging,
        )

        contact_index.additional_properties = d
        return contact_index

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
