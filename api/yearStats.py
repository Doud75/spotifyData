from django.http import JsonResponse
from django.conf import settings
import pandas as pd
import os


def load_and_prepare_df():
    file_path = os.path.join(settings.BASE_DIR, 'csvmanager', 'files', 'spotify_tracks.csv')
    df = pd.read_csv(file_path)
    # Nettoyage et préparation de la colonne 'year'
    df['year'] = pd.to_numeric(df['year'], errors='coerce')
    df.dropna(subset=['year'], inplace=True)
    df['year'] = df['year'].astype(int)
    # Création de la colonne 'decade'
    df['decade'] = (df['year'] // 10) * 10
    return df


def get_year_summary_stats(request):
    """Route pour les statistiques générales de l'année 2024."""
    try:
        df = load_and_prepare_df()
        total_tracks = len(df)
        year2024_df = df[df['year'] == 2024]
        year2024_count = len(year2024_df)
        percentage_2024 = (year2024_count / total_tracks * 100) if total_tracks > 0 else 0

        data = {
            "total_tracks": total_tracks,
            "year2024_count": year2024_count,
            "year2024_percentage": percentage_2024
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_yearly_distribution_stats(request):
    """Route pour obtenir la répartition des morceaux par année avec pourcentages."""
    try:
        df = load_and_prepare_df()
        total_tracks = len(df)
        group = df.groupby('year')
        counts_by_year = group.size().to_dict()
        percentage_by_year = {
            year: (count / total_tracks * 100) if total_tracks > 0 else 0 
            for year, count in counts_by_year.items()
        }
        data = {
            "counts_by_year": counts_by_year,
            "percentage_by_year": percentage_by_year
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_top_artists_by_year_and_decade(request):
    """Route pour obtenir les top artistes par année et par décennie."""
    try:
        df = load_and_prepare_df()
        top_artists_by_year = {}
        top_artists_by_decade = {}

        for year, group_year in df.groupby('year'):
            artist_counts = group_year['artist_name'].value_counts()
            top_artists_by_year[year] = artist_counts.head(3).to_dict()

        for dec, group_decade in df.groupby('decade'):
            artist_counts_dec = group_decade['artist_name'].value_counts()
            top_artists_by_decade[dec] = artist_counts_dec.head(3).to_dict()

        data = {
            "top_artists_by_year": top_artists_by_year,
            "top_artists_by_decade": top_artists_by_decade
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_average_popularity_stats(request):
    """Route pour obtenir la popularité moyenne par année et par décennie."""
    try:
        df = load_and_prepare_df()
        group_by_year = df.groupby('year')
        group_by_decade = df.groupby('decade')
        avg_popularity_by_year = group_by_year['popularity'].mean().to_dict()
        avg_popularity_by_decade = group_by_decade['popularity'].mean().to_dict()

        data = {
            "avg_popularity_by_year": avg_popularity_by_year,
            "avg_popularity_by_decade": avg_popularity_by_decade
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_artist_diversity_stats(request):
    """Route pour obtenir la diversité des artistes par année."""
    try:
        df = load_and_prepare_df()
        diversity_by_year = {}
        for year, group_year in df.groupby('year'):
            diversity_by_year[year] = group_year['artist_name'].nunique()

        data = {
            "diversity_by_year": diversity_by_year
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_feature_averages_by_year(request):
    """Route pour obtenir la durée, l'énergie et la danceabilité moyennes par année."""
    try:
        df = load_and_prepare_df()
        group_by_year = df.groupby('year')
        avg_duration_by_year = group_by_year['duration_ms'].mean().to_dict()
        avg_energy_by_year = group_by_year['energy'].mean().to_dict() if 'energy' in df.columns else {}
        avg_danceability_by_year = group_by_year['danceability'].mean().to_dict() if 'danceability' in df.columns else {}

        data = {
            "avg_duration_by_year": avg_duration_by_year,
            "avg_energy_by_year": avg_energy_by_year,
            "avg_danceability_by_year": avg_danceability_by_year
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
