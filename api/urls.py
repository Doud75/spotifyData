from django.urls import path
from . import views
from . import ageStats
from . import genderStats

urlpatterns = [
    path('get-filtered-data/', views.get_filtered_data, name='get_filtered_data'),
    path('age-stats/', ageStats.get_age_stats, name='get_age_stats'),
    path('gender-stats/', genderStats.get_gender_stats, name='get_gender_stats'),
]
