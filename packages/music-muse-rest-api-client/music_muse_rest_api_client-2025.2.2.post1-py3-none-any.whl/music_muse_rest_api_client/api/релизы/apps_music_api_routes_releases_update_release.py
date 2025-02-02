from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.apps_music_api_routes_releases_update_release_multi_part_body_params import (
    AppsMusicApiRoutesReleasesUpdateReleaseMultiPartBodyParams,
)
from ...models.update_release_out import UpdateReleaseOut
from ...types import Response


def _get_kwargs(
    release_id: int,
    *,
    body: AppsMusicApiRoutesReleasesUpdateReleaseMultiPartBodyParams,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/api/v1/music/releases/{release_id}/",
    }

    _body = body.to_multipart()

    _kwargs["files"] = _body

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[UpdateReleaseOut]:
    if response.status_code == 200:
        response_200 = UpdateReleaseOut.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[UpdateReleaseOut]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    release_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: AppsMusicApiRoutesReleasesUpdateReleaseMultiPartBodyParams,
) -> Response[UpdateReleaseOut]:
    """Обновление релиза

     Обновить релиз

    Args:
        release_id (int):
        body (AppsMusicApiRoutesReleasesUpdateReleaseMultiPartBodyParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UpdateReleaseOut]
    """

    kwargs = _get_kwargs(
        release_id=release_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    release_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: AppsMusicApiRoutesReleasesUpdateReleaseMultiPartBodyParams,
) -> Optional[UpdateReleaseOut]:
    """Обновление релиза

     Обновить релиз

    Args:
        release_id (int):
        body (AppsMusicApiRoutesReleasesUpdateReleaseMultiPartBodyParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UpdateReleaseOut
    """

    return sync_detailed(
        release_id=release_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    release_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: AppsMusicApiRoutesReleasesUpdateReleaseMultiPartBodyParams,
) -> Response[UpdateReleaseOut]:
    """Обновление релиза

     Обновить релиз

    Args:
        release_id (int):
        body (AppsMusicApiRoutesReleasesUpdateReleaseMultiPartBodyParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UpdateReleaseOut]
    """

    kwargs = _get_kwargs(
        release_id=release_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    release_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: AppsMusicApiRoutesReleasesUpdateReleaseMultiPartBodyParams,
) -> Optional[UpdateReleaseOut]:
    """Обновление релиза

     Обновить релиз

    Args:
        release_id (int):
        body (AppsMusicApiRoutesReleasesUpdateReleaseMultiPartBodyParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UpdateReleaseOut
    """

    return (
        await asyncio_detailed(
            release_id=release_id,
            client=client,
            body=body,
        )
    ).parsed
