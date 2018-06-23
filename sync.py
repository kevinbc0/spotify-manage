import client
import datetime


def sync_saved(sc, all_playlists):
    """Sync with changes made to saved tracks."""
    print('=== Syncing Saved Tracks ===')
    saved_tracks = set(sc.get_all_saved_tracks())
    playlist_all_uri = all_playlists['all']
    playlist_all_tracks, _ = sc.get_all_songs_in_playlist(playlist_all_uri)
    playlist_all_tracks = set(playlist_all_tracks)

    # Sync newly added tracks.
    new_tracks = list(saved_tracks - playlist_all_tracks)
    print(f'{len(new_tracks)} new tracks\nNew tracks: {new_tracks}')
    if len(new_tracks) > 0:
        sc.add_tracks_to_playlist(playlist_all_uri, new_tracks)
        sc.add_tracks_to_playlist(all_playlists['current'], new_tracks)

    # Sync removed tracks.
    removed_tracks = list(playlist_all_tracks - saved_tracks)
    print(f'{len(removed_tracks)} removed tracks\nRemoved tracks: {removed_tracks}')
    if len(removed_tracks) > 0:
        playlist_uris = [uris for _, uris in all_playlists.items()]
        sc.remove_tracks_from_all_playlists(playlist_uris, removed_tracks)
        sc.add_tracks_to_playlist(all_playlists['retention'], removed_tracks)


def sync_current(sc, all_playlists):
    """Sync the 'current' playlist."""
    print('=== Syncing Playlist Current ===')
    playlist_current_uri = all_playlists['current']
    tracks, dates = sc.get_all_songs_in_playlist(playlist_current_uri)
    today = datetime.date.today()
    expired_songs = [
        track for track, date in zip(tracks, dates)
        if (today - datetime.datetime.strptime(date, '%Y-%m-%d')) > datetime.timedelta(weeks=4)
    ]
    print(f'{len(expired_songs)} expired songs\nExpired songs: {expired_songs}')
    sc.remove_tracks_from_playlist(playlist_current_uri, expired_songs)


def main():
    dt = datetime.datetime.now()
    print(f'[{str(dt)}] Starting sync')
    sc = client.get_spotify_client()
    all_playlists = sc.get_all_owned_playlists()
    sync_saved(sc, all_playlists)
    print(f'Finished sync')


if __name__ == '__main__':
    main()
