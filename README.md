# Spotify Data

## Run docker !! Run !!!

``` bash
    docker compose up -d --build
```

# documentation des routes de l'api 

Toutes les routes sont préfixées par `/api/`.
Par exemple, l'endpoint pour les statistiques générales pour l'année 2024 sera accessible via `/api/year/summary/`.

---

## 1. Résumé des statistiques générales de l'année 2024
**Endpoint** : `/api/year/summary/`  
**Méthode HTTP** : GET  
**Description** : Renvoie un résumé général des statistiques pour l'année 2024, incluant le nombre total de pistes, le nombre de pistes de 2024 et le pourcentage que cela représente par rapport au total.  
**Réponse** (exemple) :
```json
{
  "total_tracks": 10000,
  "year2024_count": 200,
  "year2024_percentage": 2.0
}
```
---

## 2. répartition des morceaux par année avec pourcentages
**Endpoint** : `/api/year/distribution/`  
**Méthode HTTP** : GET  
**Description** : Retourne la répartition des pistes par année ainsi que le pourcentage que chaque année représente sur le total des pistes.  
**Réponse** (exemple) :
```json
{
  "counts_by_year": { "2020": 1200, "2021": 1500, "2022": 1300 },
  "percentage_by_year": { "2020": 12.0, "2021": 15.0, "2022": 13.0 }
}
```

---

## 3. top artistes par année et par décennie
**Endpoint** : `/api/year/top-artists/`  
**Méthode HTTP** : GET  
**Description** : Fournit les trois artistes les plus populaires pour chaque année et pour chaque décennie. 
Fournit le nombre de morceaux pour chaque artiste. 
**Réponse** (exemple) :
```json
{
  "top_artists_by_year": {
    "2020": { "Artist1": 150, "Artist2": 140, "Artist3": 130 },
    "2021": { "Artist4": 160, "Artist5": 155, "Artist6": 145 }
  },
  "top_artists_by_decade": {
    "2020": { "ArtistA": 500, "ArtistB": 490, "ArtistC": 480 },
    "2010": { "ArtistD": 450, "ArtistE": 440, "ArtistF": 430 }
  }
}
```

---

## 4. popularité moyenne par année et par décennie
**Endpoint** : `/api/year/popularity/`  
**Méthode HTTP** : GET  
**Description** : Renvoie la popularité moyenne des pistes regroupées par année et par décennie.  
**Réponse** (exemple) :
```json
{
  "avg_popularity_by_year": { "2020": 75.3, "2021": 82.1 },
  "avg_popularity_by_decade": { "1990": 67.5, "2000": 73.2 }
}
```

---

## 5. diversité des artistes par année
**Endpoint** : `/api/year/artist-diversity/`  
**Méthode HTTP** : GET  
**Description** : Fournit le nombre d'artistes uniques par année, mesurant ainsi la diversité des artistes pour chaque année.  
**Réponse** (exemple) :
```json
{
  "diversity_by_year": { "2020": 400, "2021": 500 }
}
```

---

## 6. moyennes des caractéristiques par année
**Endpoint** : `/api/year/feature-averages/`  
**Méthode HTTP** : GET  
**Description** : Renvoie la durée moyenne, l'énergie moyenne et la danceabilité moyenne des pistes pour chaque année.  
**Réponse** (exemple) :
```json
{
  "avg_duration_by_year": { "2020": 210000, "2021": 205000 },
  "avg_energy_by_year": { "2020": 0.65, "2021": 0.68 },
  "avg_danceability_by_year": { "2020": 0.71, "2021": 0.73 }
}
```