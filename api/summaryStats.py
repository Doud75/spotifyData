import os
from django.http import JsonResponse
from django.conf import settings
from csvmanager.fileHandler import read_file
from api.utils import percentage

def get_summary_stats(request):
    file_path = os.path.join(settings.BASE_DIR, 'csvmanager', 'files', 'Spotify_data_user.xlsx')
    try:
        data = read_file(file_path)
        total = len(data)
        
        satisfaction_counts = {}
        content_counts = {}
        usage_period_counts = {}

        for record in data:
            satisfaction = record.get('pod_variety_satisfaction')
            if satisfaction:
                satisfaction_counts[satisfaction] = satisfaction_counts.get(satisfaction, 0) + 1

            content = record.get('preferred_listening_content')
            if content:
                content_counts[content] = content_counts.get(content, 0) + 1

            usage = record.get('spotify_usage_period')
            if usage:
                usage_period_counts[usage] = usage_period_counts.get(usage, 0) + 1

        satisfaction_percentage = {
            k: percentage(v, total) for k, v in satisfaction_counts.items()
        }

        content_percentage = {
            k: percentage(v, total) for k, v in content_counts.items()
        }

        most_common_usage_period = None
        if usage_period_counts:
            most_common_usage_period = max(usage_period_counts, key=usage_period_counts.get)

        result = {
            "satisfaction_distribution": satisfaction_percentage,
            "listening_content_ratio": content_percentage,
            "most_common_usage_period": most_common_usage_period
        }
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
