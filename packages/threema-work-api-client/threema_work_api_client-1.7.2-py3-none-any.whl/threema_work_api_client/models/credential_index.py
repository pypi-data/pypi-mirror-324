from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.credential import Credential
    from ..models.link import Link
    from ..models.paging import Paging


T = TypeVar("T", bound="CredentialIndex")


@_attrs_define
class CredentialIndex:
    """
    Attributes:
        field_links (Union[Unset, list['Link']]):  Example: [{'ref': 'subscription', 'link':
            'https://work.threema.ch/api/v1'}].
        credentials (Union[Unset, list['Credential']]): Credential List Example: [{'_links': [{'ref': 'detail', 'link':
            'https://work.threema.ch/api/v1/credentials/LAow0Rksa'}], 'id': 'LAow0Rksa', 'username': 'alice', 'password':
            '3mawrk', 'usage': 0, 'hashed': False, 'locked': True}, {'_links': [{'ref': 'detail', 'link':
            'https://work.threema.ch/api/v1/credentials/pwq4Kslw'}], 'id': 'pwq4Kslw', 'username': 'bob', 'password': None,
            'usage': 0, 'hashed': True, 'locked': False}].
        paging (Union[Unset, Paging]):
    """

    field_links: Union[Unset, list["Link"]] = UNSET
    credentials: Union[Unset, list["Credential"]] = UNSET
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
        from ..models.credential import Credential
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
            credentials_item = Credential.from_dict(credentials_item_data)

            credentials.append(credentials_item)

        _paging = d.pop("paging", UNSET)
        paging: Union[Unset, Paging]
        if isinstance(_paging, Unset):
            paging = UNSET
        else:
            paging = Paging.from_dict(_paging)

        credential_index = cls(
            field_links=field_links,
            credentials=credentials,
            paging=paging,
        )

        credential_index.additional_properties = d
        return credential_index

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
