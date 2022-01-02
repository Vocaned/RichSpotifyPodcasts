import time
import pypresence
import spotipy
from spotipy.oauth2 import SpotifyPKCE

DISCORD_ID = '817471274833674260'
SPOTIFY_ID = '75f5cdaea37948259cdf1ad16585546a'
REDIRECT_URI = 'http://127.0.0.1:37211'

def main():
    spotify = spotipy.Spotify(auth_manager=SpotifyPKCE(client_id=SPOTIFY_ID, redirect_uri=REDIRECT_URI,
                                                       scope='user-read-playback-state'))

    discord = pypresence.Presence(DISCORD_ID)
    discord.connect()
    print('Running RPC.')

    while True:
        episode = spotify.currently_playing(additional_types='episode')

        if not episode['context'] or episode['currently_playing_type'] != 'episode':
            discord.clear()
            time.sleep(10)
            continue

        large_image = 'spotify'
        details = f'{episode["item"]["show"]["name"]} - {episode["item"]["name"]}'
        state = f'by {episode["item"]["show"]["publisher"]}'

        if not episode['is_playing']:
            small_image = 'paused'
            small_text = 'Paused'
            end = None
        else:
            small_image = None
            small_text = None
            end = int(time.time() - episode["progress_ms"]/1000 + episode["item"]["duration_ms"]/1000)

        discord.update(large_image=large_image, small_image=small_image, small_text=small_text, details=details, state=state, end=end,
                       buttons=[{'label': 'Listen', 'url': episode['item']['external_urls']['spotify']}])
        time.sleep(10)


if __name__ == '__main__':
    main()
