from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.credential_index import CredentialIndex
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    filter_username: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    page: Union[Unset, int] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["filterUsername"] = filter_username

    params["pageSize"] = page_size

    params["page"] = page

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/credentials",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[CredentialIndex, ErrorResponse]]:
    if response.status_code == 200:
        response_200 = CredentialIndex.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[CredentialIndex, ErrorResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    filter_username: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    page: Union[Unset, int] = UNSET,
) -> Response[Union[CredentialIndex, ErrorResponse]]:
    """Credentials: List

     List all credentials of the package

    Args:
        filter_username (Union[Unset, str]):
        page_size (Union[Unset, int]): Set the limit the filter result.
        page (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CredentialIndex, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        filter_username=filter_username,
        page_size=page_size,
        page=page,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    filter_username: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    page: Union[Unset, int] = UNSET,
) -> Optional[Union[CredentialIndex, ErrorResponse]]:
    """Credentials: List

     List all credentials of the package

    Args:
        filter_username (Union[Unset, str]):
        page_size (Union[Unset, int]): Set the limit the filter result.
        page (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CredentialIndex, ErrorResponse]
    """

    return sync_detailed(
        client=client,
        filter_username=filter_username,
        page_size=page_size,
        page=page,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    filter_username: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    page: Union[Unset, int] = UNSET,
) -> Response[Union[CredentialIndex, ErrorResponse]]:
    """Credentials: List

     List all credentials of the package

    Args:
        filter_username (Union[Unset, str]):
        page_size (Union[Unset, int]): Set the limit the filter result.
        page (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CredentialIndex, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        filter_username=filter_username,
        page_size=page_size,
        page=page,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    filter_username: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    page: Union[Unset, int] = UNSET,
) -> Optional[Union[CredentialIndex, ErrorResponse]]:
    """Credentials: List

     List all credentials of the package

    Args:
        filter_username (Union[Unset, str]):
        page_size (Union[Unset, int]): Set the limit the filter result.
        page (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CredentialIndex, ErrorResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            filter_username=filter_username,
            page_size=page_size,
            page=page,
        )
    ).parsed
