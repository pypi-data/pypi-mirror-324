from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.credential_mdm_property import CredentialMdmProperty


T = TypeVar("T", bound="CredentialMdmParameters")


@_attrs_define
class CredentialMdmParameters:
    """
    Attributes:
        id (Union[Unset, str]):  Example: LAow0Rksa.
        parameters (Union[Unset, list['CredentialMdmProperty']]): app configuration settings Example: [{'name':
            'th_nickname', 'value': 'Bob'}, {'name': 'th_disable_screenshots', 'value': False}].
    """

    id: Union[Unset, str] = UNSET
    parameters: Union[Unset, list["CredentialMdmProperty"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        parameters: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.parameters, Unset):
            parameters = []
            for parameters_item_data in self.parameters:
                parameters_item = parameters_item_data.to_dict()
                parameters.append(parameters_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if parameters is not UNSET:
            field_dict["parameters"] = parameters

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.credential_mdm_property import CredentialMdmProperty

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        parameters = []
        _parameters = d.pop("parameters", UNSET)
        for parameters_item_data in _parameters or []:
            parameters_item = CredentialMdmProperty.from_dict(parameters_item_data)

            parameters.append(parameters_item)

        credential_mdm_parameters = cls(
            id=id,
            parameters=parameters,
        )

        credential_mdm_parameters.additional_properties = d
        return credential_mdm_parameters

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
