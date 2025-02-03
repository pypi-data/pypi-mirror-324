from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.apps_music_api_routes_labels_update_label_multi_part_body_params import (
    AppsMusicApiRoutesLabelsUpdateLabelMultiPartBodyParams,
)
from ...models.update_label_out import UpdateLabelOut
from ...types import Response


def _get_kwargs(
    label_pk: int,
    *,
    body: AppsMusicApiRoutesLabelsUpdateLabelMultiPartBodyParams,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/api/v1/music/labels/{label_pk}/",
    }

    _body = body.to_multipart()

    _kwargs["files"] = _body

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[UpdateLabelOut]:
    if response.status_code == 200:
        response_200 = UpdateLabelOut.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[UpdateLabelOut]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    label_pk: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: AppsMusicApiRoutesLabelsUpdateLabelMultiPartBodyParams,
) -> Response[UpdateLabelOut]:
    """Обновить лейбл

    Args:
        label_pk (int):
        body (AppsMusicApiRoutesLabelsUpdateLabelMultiPartBodyParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UpdateLabelOut]
    """

    kwargs = _get_kwargs(
        label_pk=label_pk,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    label_pk: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: AppsMusicApiRoutesLabelsUpdateLabelMultiPartBodyParams,
) -> Optional[UpdateLabelOut]:
    """Обновить лейбл

    Args:
        label_pk (int):
        body (AppsMusicApiRoutesLabelsUpdateLabelMultiPartBodyParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UpdateLabelOut
    """

    return sync_detailed(
        label_pk=label_pk,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    label_pk: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: AppsMusicApiRoutesLabelsUpdateLabelMultiPartBodyParams,
) -> Response[UpdateLabelOut]:
    """Обновить лейбл

    Args:
        label_pk (int):
        body (AppsMusicApiRoutesLabelsUpdateLabelMultiPartBodyParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UpdateLabelOut]
    """

    kwargs = _get_kwargs(
        label_pk=label_pk,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    label_pk: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: AppsMusicApiRoutesLabelsUpdateLabelMultiPartBodyParams,
) -> Optional[UpdateLabelOut]:
    """Обновить лейбл

    Args:
        label_pk (int):
        body (AppsMusicApiRoutesLabelsUpdateLabelMultiPartBodyParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UpdateLabelOut
    """

    return (
        await asyncio_detailed(
            label_pk=label_pk,
            client=client,
            body=body,
        )
    ).parsed
