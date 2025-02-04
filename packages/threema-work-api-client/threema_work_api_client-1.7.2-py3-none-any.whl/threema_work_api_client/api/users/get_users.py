from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.user_index import UserIndex
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    filter_credential: Union[Unset, str] = UNSET,
    filter_username: Union[Unset, str] = UNSET,
    filter_query: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    page: Union[Unset, int] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["filterCredential"] = filter_credential

    params["filterUsername"] = filter_username

    params["filterQuery"] = filter_query

    params["pageSize"] = page_size

    params["page"] = page

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/users",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorResponse, UserIndex]]:
    if response.status_code == 200:
        response_200 = UserIndex.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400
    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[ErrorResponse, UserIndex]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    filter_credential: Union[Unset, str] = UNSET,
    filter_username: Union[Unset, str] = UNSET,
    filter_query: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    page: Union[Unset, int] = UNSET,
) -> Response[Union[ErrorResponse, UserIndex]]:
    """Users: List

     List all users of the package

    Args:
        filter_credential (Union[Unset, str]):
        filter_username (Union[Unset, str]):
        filter_query (Union[Unset, str]):
        page_size (Union[Unset, int]): Set the limit the filter result.
        page (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, UserIndex]]
    """

    kwargs = _get_kwargs(
        filter_credential=filter_credential,
        filter_username=filter_username,
        filter_query=filter_query,
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
    filter_credential: Union[Unset, str] = UNSET,
    filter_username: Union[Unset, str] = UNSET,
    filter_query: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    page: Union[Unset, int] = UNSET,
) -> Optional[Union[ErrorResponse, UserIndex]]:
    """Users: List

     List all users of the package

    Args:
        filter_credential (Union[Unset, str]):
        filter_username (Union[Unset, str]):
        filter_query (Union[Unset, str]):
        page_size (Union[Unset, int]): Set the limit the filter result.
        page (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, UserIndex]
    """

    return sync_detailed(
        client=client,
        filter_credential=filter_credential,
        filter_username=filter_username,
        filter_query=filter_query,
        page_size=page_size,
        page=page,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    filter_credential: Union[Unset, str] = UNSET,
    filter_username: Union[Unset, str] = UNSET,
    filter_query: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    page: Union[Unset, int] = UNSET,
) -> Response[Union[ErrorResponse, UserIndex]]:
    """Users: List

     List all users of the package

    Args:
        filter_credential (Union[Unset, str]):
        filter_username (Union[Unset, str]):
        filter_query (Union[Unset, str]):
        page_size (Union[Unset, int]): Set the limit the filter result.
        page (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, UserIndex]]
    """

    kwargs = _get_kwargs(
        filter_credential=filter_credential,
        filter_username=filter_username,
        filter_query=filter_query,
        page_size=page_size,
        page=page,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    filter_credential: Union[Unset, str] = UNSET,
    filter_username: Union[Unset, str] = UNSET,
    filter_query: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    page: Union[Unset, int] = UNSET,
) -> Optional[Union[ErrorResponse, UserIndex]]:
    """Users: List

     List all users of the package

    Args:
        filter_credential (Union[Unset, str]):
        filter_username (Union[Unset, str]):
        filter_query (Union[Unset, str]):
        page_size (Union[Unset, int]): Set the limit the filter result.
        page (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, UserIndex]
    """

    return (
        await asyncio_detailed(
            client=client,
            filter_credential=filter_credential,
            filter_username=filter_username,
            filter_query=filter_query,
            page_size=page_size,
            page=page,
        )
    ).parsed
