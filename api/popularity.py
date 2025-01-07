import os
import pandas as pd
from django.http import JsonResponse
from django.conf import settings
from csvmanager.fileHandler import read_file

def stats_by_popularity(request):
    
    # Chemin vers le fichier CSV
    file_path = os.path.join(settings.BASE_DIR, 'csvmanager', 'files', 'spotify_tracks.csv')

    # Lecture des filtres depuis les paramètres GET (optionnel)
    filters = {key: value for key, value in request.GET.items()}

    try:
        # Lecture des données et application des filtres
        data = read_file(file_path, filters)

        # Conversion en DataFrame
        df = pd.DataFrame(data)

        # Liste des métriques pour l'analyse
        metrics = ["danceability", "duration_ms", "energy", "acousticness", "tempo", "valence"]

        # Vérifier que les colonnes nécessaires existent
        required_columns = metrics + ["popularity"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return JsonResponse({
                "status": "error",
                "message": f"Les colonnes suivantes sont manquantes : {', '.join(missing_columns)}"
            }, status=400)

        # Normalisation des données
        df[metrics + ["popularity"]] = df[metrics + ["popularity"]].apply(
            lambda x: (x - x.min()) / (x.max() - x.min())
        )

        # Grouper par plages de popularité (ex. : 0-20, 20-40, etc.)
        df['popularity_range'] = pd.cut(
            df['popularity'], bins=[0, 0.2, 0.4, 0.6, 0.8, 1.0], 
            labels=["0-20", "20-40", "40-60", "60-80", "80-100"]
        )

        # Calculer les moyennes des métriques pour chaque plage de popularité
        grouped = df.groupby('popularity_range')[metrics].mean()

        global_metrics = df[metrics].mean()
        grouped.loc["0-100"] = global_metrics

        # Convertir les résultats en dictionnaire
        result = grouped.to_dict(orient='index')

        # Retourner les résultats sous forme JSON
        return JsonResponse({
            "status": "success",
            "data": result,
        })

    except ValueError as e:
        # Gestion des erreurs
        return JsonResponse({
            "status": "error",
            "message": str(e),
        }, status=400)
