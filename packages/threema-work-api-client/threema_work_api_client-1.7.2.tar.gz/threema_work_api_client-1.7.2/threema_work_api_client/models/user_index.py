from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.link import Link
    from ..models.paging import Paging
    from ..models.user import User


T = TypeVar("T", bound="UserIndex")


@_attrs_define
class UserIndex:
    """
    Attributes:
        field_links (Union[Unset, list['Link']]):  Example: [{'ref': 'subscription', 'link':
            'https://work.threema.ch/api/v1'}].
        users (Union[Unset, list['User']]): User List Example: [{'_links': [{'link':
            'https://work.threema.ch/api/v1/users/USER001', 'ref': 'detail'}, {'link':
            'https://work.threema.ch/api/v1/credentials/LAow0Rksa', 'ref': 'credential'}], 'id': 'USER001', 'lastCheck':
            '2021-12-01T00:00:00+0100', 'createdAt': '2017-01-01T00:00:00+0100', 'nickname': 'Alice', 'firstName': 'Al',
            'lastName': 'Ice', 'csi': 'AI000001', 'category': 'marketing,employees', 'jobTitle': 'Marketing Manager',
            'department': 'Marketing', 'version': 'android - 3.1k'}, {'_links': [{'link':
            'https://work.threema.ch/api/v1/users/USER002', 'ref': 'detail'}, {'link':
            'https://work.threema.ch/api/v1/credentials/Kpsow3lSdf', 'ref': 'credential'}], 'id': 'USER002', 'lastCheck':
            '2021-12-01T00:00:00+0100', 'createdAt': '2017-01-01T00:00:00+0100', 'nickname': 'Bob', 'firstName': 'B',
            'lastName': 'Ob', 'csi': 'AI000002', 'category': 'it,employees', 'jobTitle': 'Software Engineer', 'department':
            'IT', 'version': 'ios - 2.9k'}].
        paging (Union[Unset, Paging]):
    """

    field_links: Union[Unset, list["Link"]] = UNSET
    users: Union[Unset, list["User"]] = UNSET
    paging: Union[Unset, "Paging"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_links: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.field_links, Unset):
            field_links = []
            for field_links_item_data in self.field_links:
                field_links_item = field_links_item_data.to_dict()
                field_links.append(field_links_item)

        users: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.users, Unset):
            users = []
            for users_item_data in self.users:
                users_item = users_item_data.to_dict()
                users.append(users_item)

        paging: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.paging, Unset):
            paging = self.paging.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if field_links is not UNSET:
            field_dict["_links"] = field_links
        if users is not UNSET:
            field_dict["users"] = users
        if paging is not UNSET:
            field_dict["paging"] = paging

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.link import Link
        from ..models.paging import Paging
        from ..models.user import User

        d = src_dict.copy()
        field_links = []
        _field_links = d.pop("_links", UNSET)
        for field_links_item_data in _field_links or []:
            field_links_item = Link.from_dict(field_links_item_data)

            field_links.append(field_links_item)

        users = []
        _users = d.pop("users", UNSET)
        for users_item_data in _users or []:
            users_item = User.from_dict(users_item_data)

            users.append(users_item)

        _paging = d.pop("paging", UNSET)
        paging: Union[Unset, Paging]
        if isinstance(_paging, Unset):
            paging = UNSET
        else:
            paging = Paging.from_dict(_paging)

        user_index = cls(
            field_links=field_links,
            users=users,
            paging=paging,
        )

        user_index.additional_properties = d
        return user_index

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
