from django.urls import path
from . import views

urlpatterns = [
    path('get-filtered-data/', views.get_filtered_data, name='get_filtered_data'),
]
