from django.urls import path
from . import views
from . import ageStats
from . import top10  # Importer le fichier top10

from . import genderStats
from . import popularity
from . import yearStats
from . import premiumStats

urlpatterns = [
    path('get-filtered-data/', views.get_filtered_data, name='get_filtered_data'),
    path('age-stats/', ageStats.get_age_stats, name='get_age_stats'),
    path('top-stats/', top10.get_top_stats_api, name='get_top_stats'),
    path('gender-stats/', genderStats.get_gender_stats, name='get_gender_stats'),
    path('stats-by-popularity/', popularity.stats_by_popularity, name='stats_by_popularity'),
    path('year-stats/', yearStats.get_year_stats, name='get_year_stats'),
    path('premium-stats/', premiumStats.get_premium_stats, name='get_premium_stats')
]
