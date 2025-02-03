from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.apps_music_api_routes_genres_update_genre_multi_part_body_params import (
    AppsMusicApiRoutesGenresUpdateGenreMultiPartBodyParams,
)
from ...models.update_genre_out import UpdateGenreOut
from ...types import Response


def _get_kwargs(
    genre_id: int,
    *,
    body: AppsMusicApiRoutesGenresUpdateGenreMultiPartBodyParams,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/api/v1/music/genres/{genre_id}/",
    }

    _body = body.to_multipart()

    _kwargs["files"] = _body

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[UpdateGenreOut]:
    if response.status_code == 200:
        response_200 = UpdateGenreOut.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[UpdateGenreOut]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    genre_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: AppsMusicApiRoutesGenresUpdateGenreMultiPartBodyParams,
) -> Response[UpdateGenreOut]:
    """Обновить жанр

     Обновление музыкального жанра

    Args:
        genre_id (int):
        body (AppsMusicApiRoutesGenresUpdateGenreMultiPartBodyParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UpdateGenreOut]
    """

    kwargs = _get_kwargs(
        genre_id=genre_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    genre_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: AppsMusicApiRoutesGenresUpdateGenreMultiPartBodyParams,
) -> Optional[UpdateGenreOut]:
    """Обновить жанр

     Обновление музыкального жанра

    Args:
        genre_id (int):
        body (AppsMusicApiRoutesGenresUpdateGenreMultiPartBodyParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UpdateGenreOut
    """

    return sync_detailed(
        genre_id=genre_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    genre_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: AppsMusicApiRoutesGenresUpdateGenreMultiPartBodyParams,
) -> Response[UpdateGenreOut]:
    """Обновить жанр

     Обновление музыкального жанра

    Args:
        genre_id (int):
        body (AppsMusicApiRoutesGenresUpdateGenreMultiPartBodyParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UpdateGenreOut]
    """

    kwargs = _get_kwargs(
        genre_id=genre_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    genre_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: AppsMusicApiRoutesGenresUpdateGenreMultiPartBodyParams,
) -> Optional[UpdateGenreOut]:
    """Обновить жанр

     Обновление музыкального жанра

    Args:
        genre_id (int):
        body (AppsMusicApiRoutesGenresUpdateGenreMultiPartBodyParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UpdateGenreOut
    """

    return (
        await asyncio_detailed(
            genre_id=genre_id,
            client=client,
            body=body,
        )
    ).parsed
