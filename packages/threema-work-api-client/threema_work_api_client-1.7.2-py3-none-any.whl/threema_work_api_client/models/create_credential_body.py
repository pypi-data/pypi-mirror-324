from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateCredentialBody")


@_attrs_define
class CreateCredentialBody:
    """
    Attributes:
        username (str): Unique username Example: bob.
        password (str): Password of the credential Example: 3mawrk.
        hash_ (Union[Unset, bool]): If you save the password as hash, there’s no way for you to retrieve it. Default:
            False.
        license_count (Union[Unset, int]): Amount of ID creations allowed for the credentital. Only set to more then 1
            if credential should be a multi-user license. Example: 1.
        lock (Union[Unset, bool]): Once the credentials are in use with a specific ID, they cannot be used in
            conjunction with any other ID (unless the original ID is either revoked or detached from this subscription).
            Example: True.
    """

    username: str
    password: str
    hash_: Union[Unset, bool] = False
    license_count: Union[Unset, int] = UNSET
    lock: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        username = self.username

        password = self.password

        hash_ = self.hash_

        license_count = self.license_count

        lock = self.lock

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "username": username,
                "password": password,
            }
        )
        if hash_ is not UNSET:
            field_dict["hash"] = hash_
        if license_count is not UNSET:
            field_dict["licenseCount"] = license_count
        if lock is not UNSET:
            field_dict["lock"] = lock

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        username = d.pop("username")

        password = d.pop("password")

        hash_ = d.pop("hash", UNSET)

        license_count = d.pop("licenseCount", UNSET)

        lock = d.pop("lock", UNSET)

        create_credential_body = cls(
            username=username,
            password=password,
            hash_=hash_,
            license_count=license_count,
            lock=lock,
        )

        create_credential_body.additional_properties = d
        return create_credential_body

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
