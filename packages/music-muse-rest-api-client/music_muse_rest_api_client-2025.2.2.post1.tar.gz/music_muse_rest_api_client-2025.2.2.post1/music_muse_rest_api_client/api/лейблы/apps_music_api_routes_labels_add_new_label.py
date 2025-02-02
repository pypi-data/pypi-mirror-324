from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.add_new_label_out import AddNewLabelOut
from ...models.apps_music_api_routes_labels_add_new_label_multi_part_body_params import (
    AppsMusicApiRoutesLabelsAddNewLabelMultiPartBodyParams,
)
from ...types import Response


def _get_kwargs(
    *,
    body: AppsMusicApiRoutesLabelsAddNewLabelMultiPartBodyParams,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/music/labels/",
    }

    _body = body.to_multipart()

    _kwargs["files"] = _body

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[AddNewLabelOut]:
    if response.status_code == 200:
        response_200 = AddNewLabelOut.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[AddNewLabelOut]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: AppsMusicApiRoutesLabelsAddNewLabelMultiPartBodyParams,
) -> Response[AddNewLabelOut]:
    """Добавить новый лейбл

    Args:
        body (AppsMusicApiRoutesLabelsAddNewLabelMultiPartBodyParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AddNewLabelOut]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: AppsMusicApiRoutesLabelsAddNewLabelMultiPartBodyParams,
) -> Optional[AddNewLabelOut]:
    """Добавить новый лейбл

    Args:
        body (AppsMusicApiRoutesLabelsAddNewLabelMultiPartBodyParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AddNewLabelOut
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: AppsMusicApiRoutesLabelsAddNewLabelMultiPartBodyParams,
) -> Response[AddNewLabelOut]:
    """Добавить новый лейбл

    Args:
        body (AppsMusicApiRoutesLabelsAddNewLabelMultiPartBodyParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AddNewLabelOut]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: AppsMusicApiRoutesLabelsAddNewLabelMultiPartBodyParams,
) -> Optional[AddNewLabelOut]:
    """Добавить новый лейбл

    Args:
        body (AppsMusicApiRoutesLabelsAddNewLabelMultiPartBodyParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AddNewLabelOut
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
