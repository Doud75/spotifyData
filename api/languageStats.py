import pandas as pd
from django.http import JsonResponse
from django.conf import settings
import os


def get_stats_by_language():
    file_path = os.path.join(settings.BASE_DIR, 'csvmanager', 'files', 'spotify_tracks.csv')

    df = pd.read_csv(file_path)

    required_columns = ['language', 'popularity', 'danceability']
    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"La colonne '{column}' est manquante dans le fichier CSV.")

    grouped = df.groupby('language').agg(
        average_popularity=('popularity', 'mean'),
        average_danceability=('danceability', 'mean')
    ).reset_index()

    stats_by_language = grouped.set_index('language').T.to_dict()

    return stats_by_language


def get_stats_by_language_api(request):
    try:
        data = get_stats_by_language()
        return JsonResponse({'stats_by_language': data}, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


if __name__ == "__main__":
    try:
        result = get_stats_by_language()
        print("Statistiques par langue :")
        for lang, stats in result.items():
            print(
                f"{lang}: Popularité moyenne: {stats['average_popularity']:.2f}, Dansabilité moyenne: {stats['average_danceability']:.2f}")
    except Exception as e:
        print(f"Erreur : {e}")