from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.subscription_mdm_property import SubscriptionMdmProperty
from ...types import Response


def _get_kwargs(
    property_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/mdm/{property_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorResponse, SubscriptionMdmProperty]]:
    if response.status_code == 200:
        response_200 = SubscriptionMdmProperty.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400
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


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[ErrorResponse, SubscriptionMdmProperty]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    property_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[ErrorResponse, SubscriptionMdmProperty]]:
    """Global App Configuration: Show

     Load a global setting (selected by `property_id`) of a subscription. The `property_id` is the unique
    name of a setting.

    Args:
        property_id (str): Setting name (starting with `th_`) Example: th_firstname.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, SubscriptionMdmProperty]]
    """

    kwargs = _get_kwargs(
        property_id=property_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    property_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[ErrorResponse, SubscriptionMdmProperty]]:
    """Global App Configuration: Show

     Load a global setting (selected by `property_id`) of a subscription. The `property_id` is the unique
    name of a setting.

    Args:
        property_id (str): Setting name (starting with `th_`) Example: th_firstname.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, SubscriptionMdmProperty]
    """

    return sync_detailed(
        property_id=property_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    property_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[ErrorResponse, SubscriptionMdmProperty]]:
    """Global App Configuration: Show

     Load a global setting (selected by `property_id`) of a subscription. The `property_id` is the unique
    name of a setting.

    Args:
        property_id (str): Setting name (starting with `th_`) Example: th_firstname.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, SubscriptionMdmProperty]]
    """

    kwargs = _get_kwargs(
        property_id=property_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    property_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[ErrorResponse, SubscriptionMdmProperty]]:
    """Global App Configuration: Show

     Load a global setting (selected by `property_id`) of a subscription. The `property_id` is the unique
    name of a setting.

    Args:
        property_id (str): Setting name (starting with `th_`) Example: th_firstname.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, SubscriptionMdmProperty]
    """

    return (
        await asyncio_detailed(
            property_id=property_id,
            client=client,
        )
    ).parsed
