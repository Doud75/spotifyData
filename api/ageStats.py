from django.http import JsonResponse
from csvmanager.fileHandler import read_file
from django.conf import settings
from . import utils
import os

def calculate_gender_distribution(data):
    if not data:
        return {}

    gender_distribution = {}
    total_users = len(data)

    for record in data:
        gender = record.get('Gender')
        if gender:
            gender_distribution[gender] = gender_distribution.get(gender, 0) + 1

    for gender, count in gender_distribution.items():
        gender_distribution[gender] = (count / total_users) * 100

    return gender_distribution


def calculate_premium_percentage(data):
    if not data:
        return 0
    premium_count = 0
    for record in data:
        if record.get('premium_sub_willingness') == "Yes":
            premium_count += 1
    return utils.percentage(premium_count, len(data))

def get_age_stats(request):
    file_path = os.path.join(settings.BASE_DIR, 'csvmanager', 'files', 'Spotify_data_user.xlsx')

    try:
        all_data = read_file(file_path)
        total_users_global = len(all_data)

        age_groups = ["12-20", "20-35", "35-60"]
        age_stats = {}

        for age_group in age_groups:
            filters = {'Age': age_group}
            age_group_data = read_file(file_path, filters=filters)
            total_users_age_group = len(age_group_data)

            age_stats[age_group] = {
                "global_percentage": utils.percentage(total_users_age_group, total_users_global),
                "gender_distribution": calculate_gender_distribution(age_group_data),
                "premium_percentage": calculate_premium_percentage(age_group_data),
            }

        data = {
            "age_stats": age_stats,
        }
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
