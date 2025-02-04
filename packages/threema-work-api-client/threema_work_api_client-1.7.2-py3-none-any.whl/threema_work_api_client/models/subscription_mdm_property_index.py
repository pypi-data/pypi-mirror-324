from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.link import Link
    from ..models.subscription_mdm_property import SubscriptionMdmProperty


T = TypeVar("T", bound="SubscriptionMdmPropertyIndex")


@_attrs_define
class SubscriptionMdmPropertyIndex:
    """
    Attributes:
        field_links (Union[Unset, list['Link']]):  Example: [{'ref': 'subscription', 'link':
            'https://work.threema.ch/api/v1'}].
        parameters (Union[Unset, list['SubscriptionMdmProperty']]): List of settings Example: [{'_links': [{'link':
            'https://work.threema.ch/api/v1/mdm/th_disable_screenshots', 'ref': 'detail'}, {'link':
            'https://work.threema.ch/api/v1', 'ref': 'subscription'}], 'name': 'th_disable_screenshots', 'value': True},
            {'_links': [{'link': 'https://work.threema.ch/api/v1/mdm/th_nickname', 'ref': 'detail'}, {'link':
            'https://work.threema.ch/api/v1', 'ref': 'subscription'}], 'name': 'th_nickname', 'value': 'J.W.'}].
    """

    field_links: Union[Unset, list["Link"]] = UNSET
    parameters: Union[Unset, list["SubscriptionMdmProperty"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_links: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.field_links, Unset):
            field_links = []
            for field_links_item_data in self.field_links:
                field_links_item = field_links_item_data.to_dict()
                field_links.append(field_links_item)

        parameters: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.parameters, Unset):
            parameters = []
            for parameters_item_data in self.parameters:
                parameters_item = parameters_item_data.to_dict()
                parameters.append(parameters_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if field_links is not UNSET:
            field_dict["_links"] = field_links
        if parameters is not UNSET:
            field_dict["parameters"] = parameters

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.link import Link
        from ..models.subscription_mdm_property import SubscriptionMdmProperty

        d = src_dict.copy()
        field_links = []
        _field_links = d.pop("_links", UNSET)
        for field_links_item_data in _field_links or []:
            field_links_item = Link.from_dict(field_links_item_data)

            field_links.append(field_links_item)

        parameters = []
        _parameters = d.pop("parameters", UNSET)
        for parameters_item_data in _parameters or []:
            parameters_item = SubscriptionMdmProperty.from_dict(parameters_item_data)

            parameters.append(parameters_item)

        subscription_mdm_property_index = cls(
            field_links=field_links,
            parameters=parameters,
        )

        subscription_mdm_property_index.additional_properties = d
        return subscription_mdm_property_index

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
