from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.subscription_type import SubscriptionType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.link import Link


T = TypeVar("T", bound="Subscription")


@_attrs_define
class Subscription:
    """
    Attributes:
        field_links (Union[Unset, list['Link']]):  Example: [{'ref': 'detail', 'link':
            'https://work.threema.ch/api/v1'}, {'ref': 'credentials', 'link': 'https://work.threema.ch/api/v1/credentials'},
            {'ref': 'users', 'link': 'https://work.threema.ch/api/v1/users'}, {'ref': 'contacts', 'link':
            'https://work.threema.ch/api/v1/contacts'}].
        id (Union[Unset, str]): Unique subscription identifier Example: XYZ0123456.
        name (Union[Unset, str]): Short description name of the subscription Example: My Threema Work subscription.
        valid_until (Union[Unset, str]):  *ISO8601 formated date
             *Example: `2017-01-01T00:00:00+0100` Example: 2017-01-01T00:00:00+0100.
        type_ (Union[Unset, SubscriptionType]): Chosen subscription type Example: professional.
        license_amount (Union[Unset, int]): Number of purchased licenses Example: 400.
    """

    field_links: Union[Unset, list["Link"]] = UNSET
    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    valid_until: Union[Unset, str] = UNSET
    type_: Union[Unset, SubscriptionType] = UNSET
    license_amount: Union[Unset, int] = UNSET
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

        valid_until = self.valid_until

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        license_amount = self.license_amount

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if field_links is not UNSET:
            field_dict["_links"] = field_links
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if valid_until is not UNSET:
            field_dict["validUntil"] = valid_until
        if type_ is not UNSET:
            field_dict["type"] = type_
        if license_amount is not UNSET:
            field_dict["licenseAmount"] = license_amount

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

        valid_until = d.pop("validUntil", UNSET)

        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, SubscriptionType]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = SubscriptionType(_type_)

        license_amount = d.pop("licenseAmount", UNSET)

        subscription = cls(
            field_links=field_links,
            id=id,
            name=name,
            valid_until=valid_until,
            type_=type_,
            license_amount=license_amount,
        )

        subscription.additional_properties = d
        return subscription

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
