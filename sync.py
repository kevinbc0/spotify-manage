import common
import datetime


def sync(sc):
    saved_tracks = set(sc.get_all_saved_tracks())
    all_playlists = sc.get_all_owned_playlists()
    playlist_all_uri = all_playlists['all']
    playlist_all_tracks = set(sc.get_all_songs_in_playlist(playlist_all_uri))

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


def main():
    dt = datetime.datetime.now()
    print(f'[{str(dt)}] Starting sync')
    sc = common.get_spotify_client()
    sync(sc)
    print(f'Finished sync')


if __name__ == '__main__':
    main()
