from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.credential_mdm_property_index import CredentialMdmPropertyIndex
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/credentials/{id}/mdm",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[CredentialMdmPropertyIndex, ErrorResponse]]:
    if response.status_code == 200:
        response_200 = CredentialMdmPropertyIndex.from_dict(response.json())

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
) -> Response[Union[CredentialMdmPropertyIndex, ErrorResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[CredentialMdmPropertyIndex, ErrorResponse]]:
    """Individual App Configuration: List

     Show all individual settings of a credential

    Args:
        id (str): Unique id of a credential record Example: e7MCEXNCGmRDRX3BF71tJAoAiLVpvsu.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CredentialMdmPropertyIndex, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[CredentialMdmPropertyIndex, ErrorResponse]]:
    """Individual App Configuration: List

     Show all individual settings of a credential

    Args:
        id (str): Unique id of a credential record Example: e7MCEXNCGmRDRX3BF71tJAoAiLVpvsu.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CredentialMdmPropertyIndex, ErrorResponse]
    """

    return sync_detailed(
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[CredentialMdmPropertyIndex, ErrorResponse]]:
    """Individual App Configuration: List

     Show all individual settings of a credential

    Args:
        id (str): Unique id of a credential record Example: e7MCEXNCGmRDRX3BF71tJAoAiLVpvsu.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CredentialMdmPropertyIndex, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[CredentialMdmPropertyIndex, ErrorResponse]]:
    """Individual App Configuration: List

     Show all individual settings of a credential

    Args:
        id (str): Unique id of a credential record Example: e7MCEXNCGmRDRX3BF71tJAoAiLVpvsu.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CredentialMdmPropertyIndex, ErrorResponse]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed
