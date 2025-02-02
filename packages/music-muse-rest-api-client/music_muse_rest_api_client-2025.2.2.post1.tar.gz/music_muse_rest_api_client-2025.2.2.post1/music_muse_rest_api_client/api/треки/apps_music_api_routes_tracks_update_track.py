from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.apps_music_api_routes_tracks_update_track_multi_part_body_params import (
    AppsMusicApiRoutesTracksUpdateTrackMultiPartBodyParams,
)
from ...models.update_track_out import UpdateTrackOut
from ...types import Response


def _get_kwargs(
    track_id: int,
    *,
    body: AppsMusicApiRoutesTracksUpdateTrackMultiPartBodyParams,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/api/v1/music/tracks/{track_id}/",
    }

    _body = body.to_multipart()

    _kwargs["files"] = _body

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[UpdateTrackOut]:
    if response.status_code == 200:
        response_200 = UpdateTrackOut.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[UpdateTrackOut]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    track_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: AppsMusicApiRoutesTracksUpdateTrackMultiPartBodyParams,
) -> Response[UpdateTrackOut]:
    """Обновить трек

    Args:
        track_id (int):
        body (AppsMusicApiRoutesTracksUpdateTrackMultiPartBodyParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UpdateTrackOut]
    """

    kwargs = _get_kwargs(
        track_id=track_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    track_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: AppsMusicApiRoutesTracksUpdateTrackMultiPartBodyParams,
) -> Optional[UpdateTrackOut]:
    """Обновить трек

    Args:
        track_id (int):
        body (AppsMusicApiRoutesTracksUpdateTrackMultiPartBodyParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UpdateTrackOut
    """

    return sync_detailed(
        track_id=track_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    track_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: AppsMusicApiRoutesTracksUpdateTrackMultiPartBodyParams,
) -> Response[UpdateTrackOut]:
    """Обновить трек

    Args:
        track_id (int):
        body (AppsMusicApiRoutesTracksUpdateTrackMultiPartBodyParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UpdateTrackOut]
    """

    kwargs = _get_kwargs(
        track_id=track_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    track_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: AppsMusicApiRoutesTracksUpdateTrackMultiPartBodyParams,
) -> Optional[UpdateTrackOut]:
    """Обновить трек

    Args:
        track_id (int):
        body (AppsMusicApiRoutesTracksUpdateTrackMultiPartBodyParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UpdateTrackOut
    """

    return (
        await asyncio_detailed(
            track_id=track_id,
            client=client,
            body=body,
        )
    ).parsed
