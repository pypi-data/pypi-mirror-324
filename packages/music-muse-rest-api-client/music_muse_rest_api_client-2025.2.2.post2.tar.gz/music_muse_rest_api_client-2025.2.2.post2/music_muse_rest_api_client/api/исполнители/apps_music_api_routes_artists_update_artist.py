from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.apps_music_api_routes_artists_update_artist_multi_part_body_params import (
    AppsMusicApiRoutesArtistsUpdateArtistMultiPartBodyParams,
)
from ...models.update_artist_out import UpdateArtistOut
from ...types import Response


def _get_kwargs(
    artist_id: int,
    *,
    body: AppsMusicApiRoutesArtistsUpdateArtistMultiPartBodyParams,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/api/v1/music/artists/{artist_id}/",
    }

    _body = body.to_multipart()

    _kwargs["files"] = _body

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[UpdateArtistOut]:
    if response.status_code == 200:
        response_200 = UpdateArtistOut.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[UpdateArtistOut]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    artist_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: AppsMusicApiRoutesArtistsUpdateArtistMultiPartBodyParams,
) -> Response[UpdateArtistOut]:
    """Обновить исполнителя

    Args:
        artist_id (int):
        body (AppsMusicApiRoutesArtistsUpdateArtistMultiPartBodyParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UpdateArtistOut]
    """

    kwargs = _get_kwargs(
        artist_id=artist_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    artist_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: AppsMusicApiRoutesArtistsUpdateArtistMultiPartBodyParams,
) -> Optional[UpdateArtistOut]:
    """Обновить исполнителя

    Args:
        artist_id (int):
        body (AppsMusicApiRoutesArtistsUpdateArtistMultiPartBodyParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UpdateArtistOut
    """

    return sync_detailed(
        artist_id=artist_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    artist_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: AppsMusicApiRoutesArtistsUpdateArtistMultiPartBodyParams,
) -> Response[UpdateArtistOut]:
    """Обновить исполнителя

    Args:
        artist_id (int):
        body (AppsMusicApiRoutesArtistsUpdateArtistMultiPartBodyParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UpdateArtistOut]
    """

    kwargs = _get_kwargs(
        artist_id=artist_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    artist_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: AppsMusicApiRoutesArtistsUpdateArtistMultiPartBodyParams,
) -> Optional[UpdateArtistOut]:
    """Обновить исполнителя

    Args:
        artist_id (int):
        body (AppsMusicApiRoutesArtistsUpdateArtistMultiPartBodyParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UpdateArtistOut
    """

    return (
        await asyncio_detailed(
            artist_id=artist_id,
            client=client,
            body=body,
        )
    ).parsed
