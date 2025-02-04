from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.link import Link


T = TypeVar("T", bound="Credential")


@_attrs_define
class Credential:
    """
    Attributes:
        field_links (Union[Unset, list['Link']]):  Example: [{'ref': 'detail', 'link':
            'https://work.threema.ch/api/v1/credentials/LAow0Rksa'}, {'ref': 'subscription', 'link':
            'https://work.threema.ch/api/v1'}].
        id (Union[Unset, str]): Unique id of a credential record Example: e7MCEXNCGmRDRX3BF71tJAoAiLVpvsu.
        username (Union[Unset, str]):  Example: alice.
        password (Union[Unset, str]):  Example: 3mawrk.
        usage (Union[Unset, int]):  Example: 1.
        hashed (Union[Unset, bool]): If you save the password as hash, there’s no way for you to retrieve it. Default:
            False. Example: True.
        locked (Union[Unset, bool]): Once the credentials are in use with a specific ID, they cannot be used in
            conjunction with any other ID (unless the original ID is either revoked or detached from this subscription).
            Example: True.
    """

    field_links: Union[Unset, list["Link"]] = UNSET
    id: Union[Unset, str] = UNSET
    username: Union[Unset, str] = UNSET
    password: Union[Unset, str] = UNSET
    usage: Union[Unset, int] = UNSET
    hashed: Union[Unset, bool] = False
    locked: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_links: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.field_links, Unset):
            field_links = []
            for field_links_item_data in self.field_links:
                field_links_item = field_links_item_data.to_dict()
                field_links.append(field_links_item)

        id = self.id

        username = self.username

        password = self.password

        usage = self.usage

        hashed = self.hashed

        locked = self.locked

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if field_links is not UNSET:
            field_dict["_links"] = field_links
        if id is not UNSET:
            field_dict["id"] = id
        if username is not UNSET:
            field_dict["username"] = username
        if password is not UNSET:
            field_dict["password"] = password
        if usage is not UNSET:
            field_dict["usage"] = usage
        if hashed is not UNSET:
            field_dict["hashed"] = hashed
        if locked is not UNSET:
            field_dict["locked"] = locked

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

        username = d.pop("username", UNSET)

        password = d.pop("password", UNSET)

        usage = d.pop("usage", UNSET)

        hashed = d.pop("hashed", UNSET)

        locked = d.pop("locked", UNSET)

        credential = cls(
            field_links=field_links,
            id=id,
            username=username,
            password=password,
            usage=usage,
            hashed=hashed,
            locked=locked,
        )

        credential.additional_properties = d
        return credential

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
