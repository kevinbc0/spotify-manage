import spotipy
import spotipy.util as util

import config

MASTER_SCOPE = """user-library-read
                  playlist-read-private
                  user-library-modify
                  playlist-modify-public
                  user-read-recently-played
                  user-read-private
                  user-read-email
                  playlist-modify-private
                  streaming
                  user-top-read
                  user-read-birthdate
                  playlist-read-collaborative
                  user-modify-playback-state
                  user-follow-modify
                  user-read-currently-playing
                  user-read-playback-state
                  user-follow-read"""


def get_spotify_client():
    token = util.prompt_for_user_token(
        config.USERNAME,
        MASTER_SCOPE,
        client_id=config.CLIENT_ID,
        client_secret=config.CLIENT_SECRET,
        redirect_uri=config.REDIRECT_URI
    )
    sp = spotipy.Spotify(auth=token)
    return SpotifyClient(sp)


class SpotifyClient(object):

    def __init__(self, sp):
        self.sp = sp

    def get_all_saved_tracks(self):
        offset = 0
        limit = 50
        ret = []
        while True:
            results = self.sp.current_user_saved_tracks(limit=limit, offset=offset)
            if len(results['items']) == 0:
                break
            ret.extend([item['track']['uri'] for item in results['items']])
            offset += limit
        return ret

    def get_all_owned_playlists(self):
        """Returns dict mapping playlist name to URI."""
        offset = 0
        limit = 50
        ret = {}
        while True:
            results = self.sp.user_playlists(config.USERNAME, limit=limit, offset=offset)
            if len(results['items']) == 0:
                break
            for item in results['items']:
                owner = item['owner']['id']
                if owner == config.USERNAME:
                    ret[item['name']] = item['uri']
            offset += limit
        return ret

    def get_all_songs_in_playlist(self, playlist):
        offset = 0
        limit = 100
        uris = []
        dates = []
        while True:
            results = self.sp.user_playlist_tracks(
                config.USERNAME, playlist_id=playlist, limit=limit, offset=offset)
            if len(results['items']) == 0:
                break
            uris.extend([item['track']['uri'] for item in results['items']])
            dates.extend([item['added_at'].split('T')[0] for item in results['items']])
            offset += limit
        return uris, dates

    def add_tracks_to_playlist(self, playlist, tracks):
        self.sp.user_playlist_add_tracks(config.USERNAME, playlist, tracks)

    def remove_tracks_from_playlist(self, playlist, tracks):
        self.sp.user_playlist_remove_all_occurrences_of_tracks(config.USERNAME, playlist, tracks)

    def remove_tracks_from_all_playlists(self, playlists, tracks):
        for playlist in playlists:
            self.remove_tracks_from_playlist(playlist, tracks)
