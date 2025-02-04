from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateContactBody")


@_attrs_define
class CreateContactBody:
    """
    Attributes:
        threema_id (str):  Example: B4UXXX11.
        first_name (Union[Unset, str]):  Example: Echo.
        last_name (Union[Unset, str]):  Example: Ohce.
        enabled (Union[Unset, bool]):  Example: True.
    """

    threema_id: str
    first_name: Union[Unset, str] = UNSET
    last_name: Union[Unset, str] = UNSET
    enabled: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        threema_id = self.threema_id

        first_name = self.first_name

        last_name = self.last_name

        enabled = self.enabled

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "threemaId": threema_id,
            }
        )
        if first_name is not UNSET:
            field_dict["firstName"] = first_name
        if last_name is not UNSET:
            field_dict["lastName"] = last_name
        if enabled is not UNSET:
            field_dict["enabled"] = enabled

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        threema_id = d.pop("threemaId")

        first_name = d.pop("firstName", UNSET)

        last_name = d.pop("lastName", UNSET)

        enabled = d.pop("enabled", UNSET)

        create_contact_body = cls(
            threema_id=threema_id,
            first_name=first_name,
            last_name=last_name,
            enabled=enabled,
        )

        create_contact_body.additional_properties = d
        return create_contact_body

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
