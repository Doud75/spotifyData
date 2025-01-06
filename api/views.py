from django.http import JsonResponse
from csvmanager.fileHandler import read_file
from django.conf import settings
import os

def get_filtered_data(request):
    file_path = os.path.join(settings.BASE_DIR, 'csvmanager', 'files', 'Spotify_data_song.csv')

    filters = {key: value for key, value in request.GET.items()}

    try:
        data = read_file(file_path, filters)
        return JsonResponse(len(data), safe=False)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
