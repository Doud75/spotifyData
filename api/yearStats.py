from django.http import JsonResponse
from django.conf import settings
import os
import pandas as pd

def year_stats(request):
    # Chemin vers le fichier CSV
    file_path = os.path.join(settings.BASE_DIR, 'csvmanager', 'files', 'spotify_tracks.csv')

    try:
        # Charger les données
        df = pd.read_csv(file_path)
        
        # Nettoyer et convertir la colonne 'year'
        df['year'] = pd.to_numeric(df['year'], errors='coerce')
        df = df.dropna(subset=['year'])
        df['year'] = df['year'].astype(int)
        
        total_tracks = len(df)

        # Filtrer pour l'année 2024
        year2024_df = df[df['year'] == 2024]
        year2024_count = year2024_df.shape[0]
        percentage_2024 = (year2024_count / total_tracks * 100) if total_tracks > 0 else 0

        # Groupement général par année
        group = df.groupby('year')

        # Statistiques de base par année
        counts_by_year = group.size().to_dict()
        avg_popularity_by_year = group['popularity'].mean().to_dict()
        avg_duration_by_year = group['duration_ms'].mean().to_dict()
        avg_energy_by_year = group['energy'].mean().to_dict() if 'energy' in df.columns else {}
        avg_danceability_by_year = group['danceability'].mean().to_dict() if 'danceability' in df.columns else {}

        # Calcul des top artistes et diversité par année
        top_artists_by_year = {}
        diversity_by_year = {}
        for yr, group_year in df.groupby('year'):
            artist_counts = group_year['artist_name'].value_counts()
            top_artists_by_year[yr] = artist_counts.head(3).to_dict()  # Top 3 artistes
            diversity_by_year[yr] = group_year['artist_name'].nunique()

        # Création de la colonne 'decade'
        df['decade'] = (df['year'] // 10) * 10
        
        # Calcul des statistiques par décennie
        decade_group = df.groupby('decade')
        

        # Popularité moyenne par décennie
        avg_popularity_by_decade = decade_group['popularity'].mean().to_dict()

        # Top artistes par décennie
        top_artists_by_decade = {}
        for dec, group_decade in df.groupby('decade'):
            artist_counts_dec = group_decade['artist_name'].value_counts()
            top_artists_by_decade[dec] = artist_counts_dec.head(3).to_dict()

        # Préparation de la réponse
        data = {
            "total_tracks": total_tracks,
            "year2024_count": year2024_count,
            "year2024_percentage": percentage_2024,
            "counts_by_year": counts_by_year,
            "avg_popularity_by_year": avg_popularity_by_year,
            "avg_duration_by_year": avg_duration_by_year,
            "avg_energy_by_year": avg_energy_by_year,
            "avg_danceability_by_year": avg_danceability_by_year,
            "top_artists_by_year": top_artists_by_year,
            "diversity_by_year": diversity_by_year,
            "avg_popularity_by_decade": avg_popularity_by_decade,
            "top_artists_by_decade": top_artists_by_decade
        }

        return JsonResponse(data, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
