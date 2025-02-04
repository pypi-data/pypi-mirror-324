from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.credential_mdm_parameters import CredentialMdmParameters


T = TypeVar("T", bound="UpdateBulkIndividualAppConfigurationsBody")


@_attrs_define
class UpdateBulkIndividualAppConfigurationsBody:
    """
    Attributes:
        credentials (Union[Unset, list['CredentialMdmParameters']]): Array of credentials with individual app
            configuration settings Example: [{'id': 'LAow0Rksa', 'parameters': [{'name': 'th_disable_screenshots', 'value':
            True}, {'name': 'th_nickname', 'value': 'Alice'}]}, {'id': 'LAow0Rksa2', 'parameters': [{'name':
            'th_disable_screenshots', 'value': True}, {'name': 'th_nickname', 'value': 'Alice'}]}].
    """

    credentials: Union[Unset, list["CredentialMdmParameters"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        credentials: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.credentials, Unset):
            credentials = []
            for credentials_item_data in self.credentials:
                credentials_item = credentials_item_data.to_dict()
                credentials.append(credentials_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if credentials is not UNSET:
            field_dict["credentials"] = credentials

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.credential_mdm_parameters import CredentialMdmParameters

        d = src_dict.copy()
        credentials = []
        _credentials = d.pop("credentials", UNSET)
        for credentials_item_data in _credentials or []:
            credentials_item = CredentialMdmParameters.from_dict(credentials_item_data)

            credentials.append(credentials_item)

        update_bulk_individual_app_configurations_body = cls(
            credentials=credentials,
        )

        update_bulk_individual_app_configurations_body.additional_properties = d
        return update_bulk_individual_app_configurations_body

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
