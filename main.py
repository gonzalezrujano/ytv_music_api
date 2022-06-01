from __future__ import unicode_literals
import json
import pprint
import youtube_dl
from ytmusicapi import YTMusic


def get_headers_auth():
    """
    Extract auth headers to file json (Please consult: https://ytmusicapi.readthedocs.io/en/latest/setup.html#manual-file-creation)
    :return: {"x-goog-authuser": "0", "cookie": "VISITOR_INFO1_LIVE=_6_cl6hzr..."}
    """
    try:
        file_headers = open("headers_auth.json")
        headers = json.load(file_headers)

        if not "x-goog-authuser" in headers or not "cookie" in headers:
            raise Exception("Error: Could not get the auth headers")

        return headers
    except Exception as e:
        raise Exception("Error: Could not get the auth headers")


def create_instance_youtube_music_api():
    """
    Create instance Unofficial Youtube Music API (https://github.com/sigma67/ytmusicapi)
    :return: Authenticated Class YTMusic instance
    """
    headers = get_headers_auth()

    # Please consult the YTMusic library documentation for obtain
    x_goog_authuser = headers["x-goog-authuser"]
    cookie = headers["cookie"]

    try:
        # :auth: required parameter in constructor though it's not used
        yt_music = YTMusic(auth="headers_auth.json")

        # :headers_raw: it's contains the necessary information to do the authentication
        yt_music.setup(headers_raw=f"x-goog-authuser: {x_goog_authuser}\ncookie: {cookie}")
    except Exception as e:
        raise Exception("YTMusicError: Error to create instance")

    return yt_music


if __name__ == '__main__':
    ytmusic_instance = create_instance_youtube_music_api()
    # search_results = ytmusic_instance.get_library_playlists()
    playlist_items = ytmusic_instance.get_playlist(playlistId="LM")  # Get playlist with likes

    for item in playlist_items["tracks"]:
        if item["videoId"] == "EZLZDhg1ZhY":
            break

        url_resource = f'https://www.youtube.com/watch?v={item["videoId"]}'

        pprint.pprint("Downloading -> " + item["title"])
        pprint.pprint("To URL: " + url_resource)
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url_resource])

        # pprint.pprint(f'https://www.youtube.com/watch?v={item["videoId"]}')
        # pprint.pprint(item)

    # https://www.youtube.com/watch?v=tlwZ4mdzN-M
    # Save downloads
    # pprint.pprint(search_results)
    # print(search_results)
