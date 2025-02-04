from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.logo_variant import LogoVariant
from ...types import Response


def _get_kwargs(
    logo_variant: LogoVariant,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/logos/{logo_variant}",
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ErrorResponse]:
    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401
    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    logo_variant: LogoVariant,
    *,
    client: AuthenticatedClient,
) -> Response[ErrorResponse]:
    """Logo Variant: Show

     Access to your in-app logos

    Args:
        logo_variant (LogoVariant):  Example: dark.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse]
    """

    kwargs = _get_kwargs(
        logo_variant=logo_variant,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    logo_variant: LogoVariant,
    *,
    client: AuthenticatedClient,
) -> Optional[ErrorResponse]:
    """Logo Variant: Show

     Access to your in-app logos

    Args:
        logo_variant (LogoVariant):  Example: dark.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse
    """

    return sync_detailed(
        logo_variant=logo_variant,
        client=client,
    ).parsed


async def asyncio_detailed(
    logo_variant: LogoVariant,
    *,
    client: AuthenticatedClient,
) -> Response[ErrorResponse]:
    """Logo Variant: Show

     Access to your in-app logos

    Args:
        logo_variant (LogoVariant):  Example: dark.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse]
    """

    kwargs = _get_kwargs(
        logo_variant=logo_variant,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    logo_variant: LogoVariant,
    *,
    client: AuthenticatedClient,
) -> Optional[ErrorResponse]:
    """Logo Variant: Show

     Access to your in-app logos

    Args:
        logo_variant (LogoVariant):  Example: dark.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse
    """

    return (
        await asyncio_detailed(
            logo_variant=logo_variant,
            client=client,
        )
    ).parsed
