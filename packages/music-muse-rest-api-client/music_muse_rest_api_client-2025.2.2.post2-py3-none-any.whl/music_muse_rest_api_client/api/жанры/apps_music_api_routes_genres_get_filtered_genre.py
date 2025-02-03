from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_filtered_genre_in_out import GetFilteredGenreInOut
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    pk: Union[None, Unset, int] = UNSET,
    name: Union[None, Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_pk: Union[None, Unset, int]
    if isinstance(pk, Unset):
        json_pk = UNSET
    else:
        json_pk = pk
    params["pk"] = json_pk

    json_name: Union[None, Unset, str]
    if isinstance(name, Unset):
        json_name = UNSET
    else:
        json_name = name
    params["name"] = json_name

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/music/genres/filter/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[GetFilteredGenreInOut]:
    if response.status_code == 200:
        response_200 = GetFilteredGenreInOut.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[GetFilteredGenreInOut]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    pk: Union[None, Unset, int] = UNSET,
    name: Union[None, Unset, str] = UNSET,
) -> Response[GetFilteredGenreInOut]:
    """Получить жанр по фильтру

    Args:
        pk (Union[None, Unset, int]):
        name (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetFilteredGenreInOut]
    """

    kwargs = _get_kwargs(
        pk=pk,
        name=name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    pk: Union[None, Unset, int] = UNSET,
    name: Union[None, Unset, str] = UNSET,
) -> Optional[GetFilteredGenreInOut]:
    """Получить жанр по фильтру

    Args:
        pk (Union[None, Unset, int]):
        name (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetFilteredGenreInOut
    """

    return sync_detailed(
        client=client,
        pk=pk,
        name=name,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    pk: Union[None, Unset, int] = UNSET,
    name: Union[None, Unset, str] = UNSET,
) -> Response[GetFilteredGenreInOut]:
    """Получить жанр по фильтру

    Args:
        pk (Union[None, Unset, int]):
        name (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetFilteredGenreInOut]
    """

    kwargs = _get_kwargs(
        pk=pk,
        name=name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    pk: Union[None, Unset, int] = UNSET,
    name: Union[None, Unset, str] = UNSET,
) -> Optional[GetFilteredGenreInOut]:
    """Получить жанр по фильтру

    Args:
        pk (Union[None, Unset, int]):
        name (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetFilteredGenreInOut
    """

    return (
        await asyncio_detailed(
            client=client,
            pk=pk,
            name=name,
        )
    ).parsed
