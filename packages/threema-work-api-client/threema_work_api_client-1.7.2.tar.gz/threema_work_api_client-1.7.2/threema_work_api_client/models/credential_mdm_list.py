from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.credential_mdm_parameters import CredentialMdmParameters
    from ..models.link import Link
    from ..models.paging import Paging


T = TypeVar("T", bound="CredentialMdmList")


@_attrs_define
class CredentialMdmList:
    """
    Attributes:
        field_links (Union[Unset, list['Link']]):  Example: [{'ref': 'subscription', 'link':
            'https://work.threema.ch/api/v1'}].
        credentials (Union[Unset, list['CredentialMdmParameters']]): Array of credentials with individual app
            configuration settings Example: [[{'_links': [{'rel': 'detail', 'link':
            'https://work.threema.ch/api/v1/credentials/LAow0Rksa/mdm'}, {'rel': 'credential', 'link':
            'https://work.threema.ch/api/v1/credentials/LAow0Rksa'}], 'id': 'LAow0Rksa', 'parameters': [{'_links': [{'rel':
            'detail', 'link': 'https://work.threema.ch/api/v1/credentials/s3dEi7gcaphALd1/mdm/th_disable_screenshots'}],
            'name': 'th_disable_screenshots', 'value': True}, {'_links': [{'rel': 'detail', 'link':
            'https://work.threema.ch/api/v1/credentials/s3dEi7gcaphALd2/mdm/th_nickname'}], 'name': 'th_nickname', 'value':
            'Alice'}]}, {'_links': [{'rel': 'detail', 'link': 'https://work.threema.ch/api/v1/credentials/LAow0Rksa2/mdm'},
            {'rel': 'credential', 'link': 'https://work.threema.ch/api/v1/credentials/LAow0Rksa2'}], 'id': 'LAow0Rksa2',
            'parameters': [{'_links': [{'rel': 'detail', 'link':
            'https://work.threema.ch/api/v1/credentials/s3dEi7gcaphF0DK1/mdm/th_disable_screenshots'}], 'name':
            'th_disable_screenshots', 'value': True}, {'_links': [{'rel': 'detail', 'link':
            'https://work.threema.ch/api/v1/credentials/s3dEi7gcaphF0DK2/mdm/th_nickname'}], 'name': 'th_nickname', 'value':
            'Alice'}]}]].
        paging (Union[Unset, Paging]):
    """

    field_links: Union[Unset, list["Link"]] = UNSET
    credentials: Union[Unset, list["CredentialMdmParameters"]] = UNSET
    paging: Union[Unset, "Paging"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_links: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.field_links, Unset):
            field_links = []
            for field_links_item_data in self.field_links:
                field_links_item = field_links_item_data.to_dict()
                field_links.append(field_links_item)

        credentials: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.credentials, Unset):
            credentials = []
            for credentials_item_data in self.credentials:
                credentials_item = credentials_item_data.to_dict()
                credentials.append(credentials_item)

        paging: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.paging, Unset):
            paging = self.paging.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if field_links is not UNSET:
            field_dict["_links"] = field_links
        if credentials is not UNSET:
            field_dict["credentials"] = credentials
        if paging is not UNSET:
            field_dict["paging"] = paging

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.credential_mdm_parameters import CredentialMdmParameters
        from ..models.link import Link
        from ..models.paging import Paging

        d = src_dict.copy()
        field_links = []
        _field_links = d.pop("_links", UNSET)
        for field_links_item_data in _field_links or []:
            field_links_item = Link.from_dict(field_links_item_data)

            field_links.append(field_links_item)

        credentials = []
        _credentials = d.pop("credentials", UNSET)
        for credentials_item_data in _credentials or []:
            credentials_item = CredentialMdmParameters.from_dict(credentials_item_data)

            credentials.append(credentials_item)

        _paging = d.pop("paging", UNSET)
        paging: Union[Unset, Paging]
        if isinstance(_paging, Unset):
            paging = UNSET
        else:
            paging = Paging.from_dict(_paging)

        credential_mdm_list = cls(
            field_links=field_links,
            credentials=credentials,
            paging=paging,
        )

        credential_mdm_list.additional_properties = d
        return credential_mdm_list

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
