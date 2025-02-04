from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.contact_category_index import ContactCategoryIndex
from ...models.error_response import ErrorResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    threema_id: str,
    *,
    page_size: Union[Unset, int] = UNSET,
    page: Union[Unset, int] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["pageSize"] = page_size

    params["page"] = page

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/contacts/{threema_id}/categories",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ContactCategoryIndex, ErrorResponse]]:
    if response.status_code == 200:
        response_200 = ContactCategoryIndex.from_dict(response.json())

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
) -> Response[Union[ContactCategoryIndex, ErrorResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    threema_id: str,
    *,
    client: AuthenticatedClient,
    page_size: Union[Unset, int] = UNSET,
    page: Union[Unset, int] = UNSET,
) -> Response[Union[ContactCategoryIndex, ErrorResponse]]:
    """Contact Categories: List

     List the categories of the given contact (Directory Feature required)

    Args:
        threema_id (str):  Example: B4UXXX11.
        page_size (Union[Unset, int]): Set the limit the filter result.
        page (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ContactCategoryIndex, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        threema_id=threema_id,
        page_size=page_size,
        page=page,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    threema_id: str,
    *,
    client: AuthenticatedClient,
    page_size: Union[Unset, int] = UNSET,
    page: Union[Unset, int] = UNSET,
) -> Optional[Union[ContactCategoryIndex, ErrorResponse]]:
    """Contact Categories: List

     List the categories of the given contact (Directory Feature required)

    Args:
        threema_id (str):  Example: B4UXXX11.
        page_size (Union[Unset, int]): Set the limit the filter result.
        page (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ContactCategoryIndex, ErrorResponse]
    """

    return sync_detailed(
        threema_id=threema_id,
        client=client,
        page_size=page_size,
        page=page,
    ).parsed


async def asyncio_detailed(
    threema_id: str,
    *,
    client: AuthenticatedClient,
    page_size: Union[Unset, int] = UNSET,
    page: Union[Unset, int] = UNSET,
) -> Response[Union[ContactCategoryIndex, ErrorResponse]]:
    """Contact Categories: List

     List the categories of the given contact (Directory Feature required)

    Args:
        threema_id (str):  Example: B4UXXX11.
        page_size (Union[Unset, int]): Set the limit the filter result.
        page (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ContactCategoryIndex, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        threema_id=threema_id,
        page_size=page_size,
        page=page,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    threema_id: str,
    *,
    client: AuthenticatedClient,
    page_size: Union[Unset, int] = UNSET,
    page: Union[Unset, int] = UNSET,
) -> Optional[Union[ContactCategoryIndex, ErrorResponse]]:
    """Contact Categories: List

     List the categories of the given contact (Directory Feature required)

    Args:
        threema_id (str):  Example: B4UXXX11.
        page_size (Union[Unset, int]): Set the limit the filter result.
        page (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ContactCategoryIndex, ErrorResponse]
    """

    return (
        await asyncio_detailed(
            threema_id=threema_id,
            client=client,
            page_size=page_size,
            page=page,
        )
    ).parsed
