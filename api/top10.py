import pandas as pd
from django.http import JsonResponse
from django.conf import settings
import os


def get_top_stats():
    file_path = os.path.join(settings.BASE_DIR, 'csvmanager', 'files', 'spotify_tracks.csv')
    df = pd.read_csv(file_path)

    if 'popularity' not in df.columns or 'track_name' not in df.columns or 'artist_name' not in df.columns or 'artwork_url' not in df.columns:
        raise ValueError("Les colonnes nécessaires sont manquantes dans le fichier CSV.")

    # Top 10 chansons
    top_10_songs = df.nlargest(10, 'popularity')[[
        'track_name', 'artist_name', 'album_name', 'popularity',
        'year', 'duration_ms', 'artwork_url', 'track_url'
    ]].to_dict(orient='records')

    # Top 10 artistes
    artist_popularity = df.groupby('artist_name')['popularity'].sum().reset_index()
    top_10_artists = artist_popularity.nlargest(10, 'popularity')

    artist_artwork_map = df.groupby('artist_name').first()['artwork_url']
    top_10_artists['artwork_url'] = top_10_artists['artist_name'].map(artist_artwork_map)

    top_10_artists = top_10_artists.to_dict(orient='records')

    top_10_danceable_songs = df.nlargest(10, 'danceability')[[
        'track_name', 'artist_name', 'album_name', 'danceability',
        'year', 'duration_ms', 'artwork_url', 'track_url'
    ]].to_dict(orient='records')

    return {
        "top_10_songs": top_10_songs,
        "top_10_artists": top_10_artists,
        "top_10_danceable_songs": top_10_danceable_songs
    }


def get_top_stats_api(request):
    try:
        data = get_top_stats()
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
