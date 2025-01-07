from django.urls import path
from . import views
from . import ageStats

urlpatterns = [
    path('get-filtered-data/', views.get_filtered_data, name='get_filtered_data'),
    path('age-stats/', ageStats.get_age_stats, name='get_age_stats'),
]
