from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.link import Link


T = TypeVar("T", bound="User")


@_attrs_define
class User:
    """
    Attributes:
        field_links (Union[Unset, list['Link']]):  Example: [{'ref': 'detail', 'link':
            'https://work.threema.ch/api/v1/users/ECHOECHO'}, {'ref': 'subscription', 'link':
            'https://work.threema.ch/api/v1'}, {'ref': 'credential', 'link':
            'https://work.threema.ch/api/v1/credentials/LAow0Rksa'}].
        id (Union[Unset, str]):  Example: B4UXXX11.
        nickname (Union[Unset, str]): Nickname, chosen by the user in the Threema App Example: Alice.
        first_name (Union[Unset, str]): First name of the user, configured by the MDM system or app configuration.
            Example: Al.
        last_name (Union[Unset, str]): Last name of the user, configured by the MDM system or app configuration.
            Example: Ice.
        csi (Union[Unset, str]): Any value (e.g. internal username), configured by the MDM system or app configuration.
            Example: AI000001.
        category (Union[Unset, str]): User category (e.g. group, team, location), configured by the MDM system or app
            configuration. Example: marketing,employees.
        job_title (Union[Unset, str]): Job title of the user, configured by the MDM system or app configuration.
            Example: Manager.
        department (Union[Unset, str]): Department of the user, configured by the MDM system or app configuration.
            Example: Marketing.
        version (Union[Unset, str]): Used Version
             *
             * Example: `android - 3.1k`
             *
             * | OS		| Separator | App Version |
             * |---------|-----------|-------------|
             * | `android` | ` - `   | `3.1k` |
             *  Example: android - 3.1k.
        last_check (Union[Unset, str]):  *ISO8601 formated date
             *Example: `2017-01-01T00:00:00+0100` Example: 2017-01-01T00:00:00+0100.
        created_at (Union[Unset, str]):  *ISO8601 formated date
             *Example: `2017-01-01T00:00:00+0100` Example: 2017-01-01T00:00:00+0100.
    """

    field_links: Union[Unset, list["Link"]] = UNSET
    id: Union[Unset, str] = UNSET
    nickname: Union[Unset, str] = UNSET
    first_name: Union[Unset, str] = UNSET
    last_name: Union[Unset, str] = UNSET
    csi: Union[Unset, str] = UNSET
    category: Union[Unset, str] = UNSET
    job_title: Union[Unset, str] = UNSET
    department: Union[Unset, str] = UNSET
    version: Union[Unset, str] = UNSET
    last_check: Union[Unset, str] = UNSET
    created_at: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_links: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.field_links, Unset):
            field_links = []
            for field_links_item_data in self.field_links:
                field_links_item = field_links_item_data.to_dict()
                field_links.append(field_links_item)

        id = self.id

        nickname = self.nickname

        first_name = self.first_name

        last_name = self.last_name

        csi = self.csi

        category = self.category

        job_title = self.job_title

        department = self.department

        version = self.version

        last_check = self.last_check

        created_at = self.created_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if field_links is not UNSET:
            field_dict["_links"] = field_links
        if id is not UNSET:
            field_dict["id"] = id
        if nickname is not UNSET:
            field_dict["nickname"] = nickname
        if first_name is not UNSET:
            field_dict["firstName"] = first_name
        if last_name is not UNSET:
            field_dict["lastName"] = last_name
        if csi is not UNSET:
            field_dict["csi"] = csi
        if category is not UNSET:
            field_dict["category"] = category
        if job_title is not UNSET:
            field_dict["jobTitle"] = job_title
        if department is not UNSET:
            field_dict["department"] = department
        if version is not UNSET:
            field_dict["version"] = version
        if last_check is not UNSET:
            field_dict["lastCheck"] = last_check
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at

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

        nickname = d.pop("nickname", UNSET)

        first_name = d.pop("firstName", UNSET)

        last_name = d.pop("lastName", UNSET)

        csi = d.pop("csi", UNSET)

        category = d.pop("category", UNSET)

        job_title = d.pop("jobTitle", UNSET)

        department = d.pop("department", UNSET)

        version = d.pop("version", UNSET)

        last_check = d.pop("lastCheck", UNSET)

        created_at = d.pop("createdAt", UNSET)

        user = cls(
            field_links=field_links,
            id=id,
            nickname=nickname,
            first_name=first_name,
            last_name=last_name,
            csi=csi,
            category=category,
            job_title=job_title,
            department=department,
            version=version,
            last_check=last_check,
            created_at=created_at,
        )

        user.additional_properties = d
        return user

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
