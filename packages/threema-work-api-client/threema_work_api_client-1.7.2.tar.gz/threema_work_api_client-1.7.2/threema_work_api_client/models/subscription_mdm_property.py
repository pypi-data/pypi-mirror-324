from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.link import Link


T = TypeVar("T", bound="SubscriptionMdmProperty")


@_attrs_define
class SubscriptionMdmProperty:
    """
    Attributes:
        field_links (Union[Unset, list['Link']]):  Example: [{'ref': 'detail', 'link':
            'https://work.threema.ch/api/v1/mdm/th_disable_screenshots'}, {'ref': 'subscription', 'link':
            'https://work.threema.ch/api/v1'}].
        id (Union[Unset, str]): Setting name (starting with `th_`) Example: th_firstname.
        value (Union[Unset, bool, int, str]): Value of the property
    """

    field_links: Union[Unset, list["Link"]] = UNSET
    id: Union[Unset, str] = UNSET
    value: Union[Unset, bool, int, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_links: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.field_links, Unset):
            field_links = []
            for field_links_item_data in self.field_links:
                field_links_item = field_links_item_data.to_dict()
                field_links.append(field_links_item)

        id = self.id

        value: Union[Unset, bool, int, str]
        if isinstance(self.value, Unset):
            value = UNSET
        else:
            value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if field_links is not UNSET:
            field_dict["_links"] = field_links
        if id is not UNSET:
            field_dict["id"] = id
        if value is not UNSET:
            field_dict["value"] = value

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

        def _parse_value(data: object) -> Union[Unset, bool, int, str]:
            if isinstance(data, Unset):
                return data
            return cast(Union[Unset, bool, int, str], data)

        value = _parse_value(d.pop("value", UNSET))

        subscription_mdm_property = cls(
            field_links=field_links,
            id=id,
            value=value,
        )

        subscription_mdm_property.additional_properties = d
        return subscription_mdm_property

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
