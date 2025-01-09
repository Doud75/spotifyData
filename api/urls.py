from django.urls import path
from . import views
from . import ageStats
from . import top10
from . import genderStats
from . import popularity
from . import yearStats
from . import premiumStats
from . import languageStats
from . import summaryStats

urlpatterns = [
    path('get-filtered-data/', views.get_filtered_data, name='get_filtered_data'),
    path('age-stats/', ageStats.get_age_stats, name='get_age_stats'),
    path('top-stats/', top10.get_top_stats_api, name='get_top_stats'),
    path('gender-stats/', genderStats.get_gender_stats, name='get_gender_stats'),
    path('stats-by-popularity/', popularity.stats_by_popularity, name='stats_by_popularity'),
    path('premium-stats/', premiumStats.get_premium_stats, name='get_premium_stats'),
    path('stats-by-language/', languageStats.get_stats_by_language_api, name='get_stats_by_language'),
    path('year/summary/', yearStats.get_year_summary_stats, name='year_summary_stats'),
    path('year/distribution/', yearStats.get_yearly_distribution_stats, name='yearly_distribution_stats'),
    path('year/top-artists/', yearStats.get_top_artists_by_year_and_decade, name='top_artists_by_year_decade'),
    path('year/popularity/', yearStats.get_average_popularity_stats, name='average_popularity_stats'),
    path('year/artist-diversity/', yearStats.get_artist_diversity_stats, name='artist_diversity_stats'),
    path('year/feature-averages/', yearStats.get_feature_averages_by_year, name='feature_averages_by_year'),
    path('summary-stats/', summaryStats.get_summary_stats, name='get_summary_stats')
    ]
