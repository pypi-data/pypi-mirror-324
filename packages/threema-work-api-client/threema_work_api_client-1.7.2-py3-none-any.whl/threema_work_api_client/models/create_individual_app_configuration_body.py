from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CreateIndividualAppConfigurationBody")


@_attrs_define
class CreateIndividualAppConfigurationBody:
    """
    Attributes:
        property_ (str): Setting name (starting with `th_`) Example: th_firstname.
        value (Union[bool, int, str]): Value of the property
    """

    property_: str
    value: Union[bool, int, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        property_ = self.property_

        value: Union[bool, int, str]
        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "property": property_,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        property_ = d.pop("property")

        def _parse_value(data: object) -> Union[bool, int, str]:
            return cast(Union[bool, int, str], data)

        value = _parse_value(d.pop("value"))

        create_individual_app_configuration_body = cls(
            property_=property_,
            value=value,
        )

        create_individual_app_configuration_body.additional_properties = d
        return create_individual_app_configuration_body

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
