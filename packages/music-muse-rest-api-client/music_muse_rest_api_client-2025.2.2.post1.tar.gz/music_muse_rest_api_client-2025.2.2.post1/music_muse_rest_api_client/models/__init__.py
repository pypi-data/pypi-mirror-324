"""Contains all the data models used in inputs/outputs"""

from .add_new_artist_in import AddNewArtistIn
from .add_new_artist_out import AddNewArtistOut
from .add_new_audio_in import AddNewAudioIn
from .add_new_audio_out import AddNewAudioOut
from .add_new_genre_in import AddNewGenreIn
from .add_new_genre_out import AddNewGenreOut
from .add_new_image_in import AddNewImageIn
from .add_new_image_out import AddNewImageOut
from .add_new_label_in import AddNewLabelIn
from .add_new_label_out import AddNewLabelOut
from .add_new_release_in import AddNewReleaseIn
from .add_new_release_in_release_type import AddNewReleaseInReleaseType
from .add_new_release_in_status import AddNewReleaseInStatus
from .add_new_release_out import AddNewReleaseOut
from .add_new_track_in import AddNewTrackIn
from .add_new_track_in_status import AddNewTrackInStatus
from .add_new_track_out import AddNewTrackOut
from .add_new_video_in import AddNewVideoIn
from .add_new_video_out import AddNewVideoOut
from .apps_music_api_routes_artists_add_new_artist_multi_part_body_params import (
    AppsMusicApiRoutesArtistsAddNewArtistMultiPartBodyParams,
)
from .apps_music_api_routes_artists_add_new_artist_multi_part_body_params_artist_gender import (
    AppsMusicApiRoutesArtistsAddNewArtistMultiPartBodyParamsArtistGender,
)
from .apps_music_api_routes_artists_update_artist_multi_part_body_params import (
    AppsMusicApiRoutesArtistsUpdateArtistMultiPartBodyParams,
)
from .apps_music_api_routes_artists_update_artist_multi_part_body_params_artist_gender import (
    AppsMusicApiRoutesArtistsUpdateArtistMultiPartBodyParamsArtistGender,
)
from .apps_music_api_routes_content_add_new_audio_multi_part_body_params import (
    AppsMusicApiRoutesContentAddNewAudioMultiPartBodyParams,
)
from .apps_music_api_routes_content_add_new_image_multi_part_body_params import (
    AppsMusicApiRoutesContentAddNewImageMultiPartBodyParams,
)
from .apps_music_api_routes_content_add_new_video_multi_part_body_params import (
    AppsMusicApiRoutesContentAddNewVideoMultiPartBodyParams,
)
from .apps_music_api_routes_genres_add_new_genre_multi_part_body_params import (
    AppsMusicApiRoutesGenresAddNewGenreMultiPartBodyParams,
)
from .apps_music_api_routes_genres_update_genre_multi_part_body_params import (
    AppsMusicApiRoutesGenresUpdateGenreMultiPartBodyParams,
)
from .apps_music_api_routes_labels_add_new_label_multi_part_body_params import (
    AppsMusicApiRoutesLabelsAddNewLabelMultiPartBodyParams,
)
from .apps_music_api_routes_labels_update_label_multi_part_body_params import (
    AppsMusicApiRoutesLabelsUpdateLabelMultiPartBodyParams,
)
from .apps_music_api_routes_releases_add_new_release_multi_part_body_params import (
    AppsMusicApiRoutesReleasesAddNewReleaseMultiPartBodyParams,
)
from .apps_music_api_routes_releases_add_new_release_multi_part_body_params_release_type import (
    AppsMusicApiRoutesReleasesAddNewReleaseMultiPartBodyParamsReleaseType,
)
from .apps_music_api_routes_releases_add_new_release_multi_part_body_params_status import (
    AppsMusicApiRoutesReleasesAddNewReleaseMultiPartBodyParamsStatus,
)
from .apps_music_api_routes_releases_update_release_multi_part_body_params import (
    AppsMusicApiRoutesReleasesUpdateReleaseMultiPartBodyParams,
)
from .apps_music_api_routes_releases_update_release_multi_part_body_params_release_type import (
    AppsMusicApiRoutesReleasesUpdateReleaseMultiPartBodyParamsReleaseType,
)
from .apps_music_api_routes_releases_update_release_multi_part_body_params_status import (
    AppsMusicApiRoutesReleasesUpdateReleaseMultiPartBodyParamsStatus,
)
from .apps_music_api_routes_tracks_add_new_track_multi_part_body_params import (
    AppsMusicApiRoutesTracksAddNewTrackMultiPartBodyParams,
)
from .apps_music_api_routes_tracks_add_new_track_multi_part_body_params_status import (
    AppsMusicApiRoutesTracksAddNewTrackMultiPartBodyParamsStatus,
)
from .apps_music_api_routes_tracks_update_track_multi_part_body_params import (
    AppsMusicApiRoutesTracksUpdateTrackMultiPartBodyParams,
)
from .apps_music_api_routes_tracks_update_track_multi_part_body_params_status import (
    AppsMusicApiRoutesTracksUpdateTrackMultiPartBodyParamsStatus,
)
from .artist_gender import ArtistGender
from .get_artist_pages_item_out import GetArtistPagesItemOut
from .get_artist_pages_out import GetArtistPagesOut
from .get_audio_pages_out import GetAudioPagesOut
from .get_filtered_artist_in import GetFilteredArtistIn
from .get_filtered_artist_out import GetFilteredArtistOut
from .get_filtered_audio_out import GetFilteredAudioOut
from .get_filtered_content_in import GetFilteredContentIn
from .get_filtered_genre_in import GetFilteredGenreIn
from .get_filtered_genre_in_out import GetFilteredGenreInOut
from .get_filtered_labels_in import GetFilteredLabelsIn
from .get_filtered_labels_out import GetFilteredLabelsOut
from .get_filtered_release_in import GetFilteredReleaseIn
from .get_filtered_release_out import GetFilteredReleaseOut
from .get_filtered_track_in import GetFilteredTrackIn
from .get_filtered_track_out import GetFilteredTrackOut
from .get_filtered_video_out import GetFilteredVideoOut
from .get_genre_pages_out import GetGenrePagesOut
from .get_image_pages_out import GetImagePagesOut
from .get_labels_pages_out import GetLabelsPagesOut
from .get_release_pages_item_out import GetReleasePagesItemOut
from .get_releases_pages_out import GetReleasesPagesOut
from .get_track_pages_item_out import GetTrackPagesItemOut
from .get_track_pages_out import GetTrackPagesOut
from .get_video_pages_out import GetVideoPagesOut
from .input_ import Input
from .paged_get_audio_pages_out import PagedGetAudioPagesOut
from .paged_get_genre_pages_out import PagedGetGenrePagesOut
from .paged_get_image_pages_out import PagedGetImagePagesOut
from .paged_get_labels_pages_out import PagedGetLabelsPagesOut
from .paged_get_video_pages_out import PagedGetVideoPagesOut
from .release_types import ReleaseTypes
from .statuses import Statuses
from .update_artist_out import UpdateArtistOut
from .update_genre_in import UpdateGenreIn
from .update_genre_out import UpdateGenreOut
from .update_label_in import UpdateLabelIn
from .update_label_out import UpdateLabelOut
from .update_release_in import UpdateReleaseIn
from .update_release_in_release_type import UpdateReleaseInReleaseType
from .update_release_in_status import UpdateReleaseInStatus
from .update_release_out import UpdateReleaseOut
from .update_track_out import UpdateTrackOut

__all__ = (
    "AddNewArtistIn",
    "AddNewArtistOut",
    "AddNewAudioIn",
    "AddNewAudioOut",
    "AddNewGenreIn",
    "AddNewGenreOut",
    "AddNewImageIn",
    "AddNewImageOut",
    "AddNewLabelIn",
    "AddNewLabelOut",
    "AddNewReleaseIn",
    "AddNewReleaseInReleaseType",
    "AddNewReleaseInStatus",
    "AddNewReleaseOut",
    "AddNewTrackIn",
    "AddNewTrackInStatus",
    "AddNewTrackOut",
    "AddNewVideoIn",
    "AddNewVideoOut",
    "AppsMusicApiRoutesArtistsAddNewArtistMultiPartBodyParams",
    "AppsMusicApiRoutesArtistsAddNewArtistMultiPartBodyParamsArtistGender",
    "AppsMusicApiRoutesArtistsUpdateArtistMultiPartBodyParams",
    "AppsMusicApiRoutesArtistsUpdateArtistMultiPartBodyParamsArtistGender",
    "AppsMusicApiRoutesContentAddNewAudioMultiPartBodyParams",
    "AppsMusicApiRoutesContentAddNewImageMultiPartBodyParams",
    "AppsMusicApiRoutesContentAddNewVideoMultiPartBodyParams",
    "AppsMusicApiRoutesGenresAddNewGenreMultiPartBodyParams",
    "AppsMusicApiRoutesGenresUpdateGenreMultiPartBodyParams",
    "AppsMusicApiRoutesLabelsAddNewLabelMultiPartBodyParams",
    "AppsMusicApiRoutesLabelsUpdateLabelMultiPartBodyParams",
    "AppsMusicApiRoutesReleasesAddNewReleaseMultiPartBodyParams",
    "AppsMusicApiRoutesReleasesAddNewReleaseMultiPartBodyParamsReleaseType",
    "AppsMusicApiRoutesReleasesAddNewReleaseMultiPartBodyParamsStatus",
    "AppsMusicApiRoutesReleasesUpdateReleaseMultiPartBodyParams",
    "AppsMusicApiRoutesReleasesUpdateReleaseMultiPartBodyParamsReleaseType",
    "AppsMusicApiRoutesReleasesUpdateReleaseMultiPartBodyParamsStatus",
    "AppsMusicApiRoutesTracksAddNewTrackMultiPartBodyParams",
    "AppsMusicApiRoutesTracksAddNewTrackMultiPartBodyParamsStatus",
    "AppsMusicApiRoutesTracksUpdateTrackMultiPartBodyParams",
    "AppsMusicApiRoutesTracksUpdateTrackMultiPartBodyParamsStatus",
    "ArtistGender",
    "GetArtistPagesItemOut",
    "GetArtistPagesOut",
    "GetAudioPagesOut",
    "GetFilteredArtistIn",
    "GetFilteredArtistOut",
    "GetFilteredAudioOut",
    "GetFilteredContentIn",
    "GetFilteredGenreIn",
    "GetFilteredGenreInOut",
    "GetFilteredLabelsIn",
    "GetFilteredLabelsOut",
    "GetFilteredReleaseIn",
    "GetFilteredReleaseOut",
    "GetFilteredTrackIn",
    "GetFilteredTrackOut",
    "GetFilteredVideoOut",
    "GetGenrePagesOut",
    "GetImagePagesOut",
    "GetLabelsPagesOut",
    "GetReleasePagesItemOut",
    "GetReleasesPagesOut",
    "GetTrackPagesItemOut",
    "GetTrackPagesOut",
    "GetVideoPagesOut",
    "Input",
    "PagedGetAudioPagesOut",
    "PagedGetGenrePagesOut",
    "PagedGetImagePagesOut",
    "PagedGetLabelsPagesOut",
    "PagedGetVideoPagesOut",
    "ReleaseTypes",
    "Statuses",
    "UpdateArtistOut",
    "UpdateGenreIn",
    "UpdateGenreOut",
    "UpdateLabelIn",
    "UpdateLabelOut",
    "UpdateReleaseIn",
    "UpdateReleaseInReleaseType",
    "UpdateReleaseInStatus",
    "UpdateReleaseOut",
    "UpdateTrackOut",
)
