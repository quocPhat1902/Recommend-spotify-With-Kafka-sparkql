

#get_ipython().run_line_magic('matplotlib', 'inline')

import os
#import my_spotify_credentials as credentials
import numpy as np
import pandas as pd
import ujson
import spotipy
import spotipy.util
import seaborn as sns


# use your credentials
os.environ["SPOTIPY_CLIENT_ID"] = '73f68e0b4a9b4569b9f1ac2f4dadee9d'
os.environ["SPOTIPY_CLIENT_SECRET"] = '7c5addae32234e4db9ed865e20ff9c0f'
os.environ["SPOTIPY_REDIRECT_URI"] = 'http://mysite.com/callback/'




def save_only_some_fields(track_response):
    return {        
        'id': str(track_response['track']['id']),
        'name': str(track_response['track']['name']),
        'artists': [artist['name'] for artist in track_response['track']['artists']],
        'duration_ms': track_response['track']['duration_ms'],
        'popularity': track_response['track']['popularity'],
        'added_at': track_response['added_at']
    }
def get_new():
    scope = 'user-library-read'
    username = 'nqphat1902@gmail.com'

    token = spotipy.util.prompt_for_user_token(username, scope)

    if token:
        spotipy_obj = spotipy.Spotify(auth=token)
        saved_tracks_resp = spotipy_obj.current_user_saved_tracks(limit=50)
    else:
        print('Couldn\'t get token for that username')
    number_of_tracks = saved_tracks_resp['total']
    print('%d tracks' % number_of_tracks)
    tracks = [save_only_some_fields(track) for track in saved_tracks_resp['items']]

    while saved_tracks_resp['next']:
        saved_tracks_resp = spotipy_obj.next(saved_tracks_resp)
        tracks.extend([save_only_some_fields(track) for track in saved_tracks_resp['items']])


    tracks_df = pd.DataFrame(tracks)
    pd.set_option('display.max_rows', len(tracks))


    tracks_df['artists'] = tracks_df['artists'].apply(lambda artists: artists[0])
    tracks_df['duration_ms'] = tracks_df['duration_ms'].apply(lambda duration: duration/1000)

    tracks_df = tracks_df.rename(columns = {'duration_ms':'duration_s'})


    audio_features = {}

    for idd in tracks_df['id'].tolist():
        audio_features[idd] = spotipy_obj.audio_features(idd)[0]
        
    tracks_df['acousticness'] = tracks_df['id'].apply(lambda idd: audio_features[idd]['acousticness'])
    tracks_df['speechiness'] = tracks_df['id'].apply(lambda idd: audio_features[idd]['speechiness'])
    tracks_df['key'] = tracks_df['id'].apply(lambda idd: str(audio_features[idd]['key']))
    tracks_df['liveness'] = tracks_df['id'].apply(lambda idd: audio_features[idd]['liveness'])
    tracks_df['instrumentalness'] = tracks_df['id'].apply(lambda idd: audio_features[idd]['instrumentalness'])
    tracks_df['energy'] = tracks_df['id'].apply(lambda idd: audio_features[idd]['energy'])
    tracks_df['tempo'] = tracks_df['id'].apply(lambda idd: audio_features[idd]['tempo'])
    tracks_df['time_signature'] = tracks_df['id'].apply(lambda idd: audio_features[idd]['time_signature'])
    tracks_df['loudness'] = tracks_df['id'].apply(lambda idd: audio_features[idd]['loudness'])
    tracks_df['danceability'] = tracks_df['id'].apply(lambda idd: audio_features[idd]['danceability'])
    tracks_df['valence'] = tracks_df['id'].apply(lambda idd: audio_features[idd]['valence'])
    return tracks_df



class getSong(): # cnn to rnn is hooked here.
    def __init__(self):
        super(getSong, self).__init__()
        
    def passs():
        tracks_df=get_new()
        return tracks_df


# 'name', 'artists', 'duration_ms', 'explicit', 'danceability', 'energy',
#        'key', 'loudness', 'mode', 'speechiness', 'acousticness',
#        'instrumentalness', 'liveness', 'valence', 'tempo'
