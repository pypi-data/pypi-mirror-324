from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.contact_type import ContactType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.link import Link


T = TypeVar("T", bound="Contact")


@_attrs_define
class Contact:
    """
    Attributes:
        field_links (Union[Unset, list['Link']]):  Example: [{'ref': 'detail', 'link':
            'https://work.threema.ch/api/v1/contacts/ECHOECHO'}, {'ref': 'categories', 'link':
            'https://work.threema.ch/api/v1/contacts/ECHOECHO/categories'}, {'ref': 'subscription', 'link':
            'https://work.threema.ch/api/v1'}].
        threema_id (Union[Unset, str]):  Example: B4UXXX11.
        type_ (Union[Unset, ContactType]):  Example: auto.
        first_name (Union[Unset, str]):  Example: Echo.
        last_name (Union[Unset, str]):  Example: Ohce.
        enabled (Union[Unset, bool]):  Example: True.
    """

    field_links: Union[Unset, list["Link"]] = UNSET
    threema_id: Union[Unset, str] = UNSET
    type_: Union[Unset, ContactType] = UNSET
    first_name: Union[Unset, str] = UNSET
    last_name: Union[Unset, str] = UNSET
    enabled: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_links: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.field_links, Unset):
            field_links = []
            for field_links_item_data in self.field_links:
                field_links_item = field_links_item_data.to_dict()
                field_links.append(field_links_item)

        threema_id = self.threema_id

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        first_name = self.first_name

        last_name = self.last_name

        enabled = self.enabled

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if field_links is not UNSET:
            field_dict["_links"] = field_links
        if threema_id is not UNSET:
            field_dict["threemaId"] = threema_id
        if type_ is not UNSET:
            field_dict["type"] = type_
        if first_name is not UNSET:
            field_dict["firstName"] = first_name
        if last_name is not UNSET:
            field_dict["lastName"] = last_name
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

        threema_id = d.pop("threemaId", UNSET)

        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, ContactType]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = ContactType(_type_)

        first_name = d.pop("firstName", UNSET)

        last_name = d.pop("lastName", UNSET)

        enabled = d.pop("enabled", UNSET)

        contact = cls(
            field_links=field_links,
            threema_id=threema_id,
            type_=type_,
            first_name=first_name,
            last_name=last_name,
            enabled=enabled,
        )

        contact.additional_properties = d
        return contact

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
