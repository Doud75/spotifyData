from django.http import JsonResponse
from csvmanager.fileHandler import read_file
from django.conf import settings
from . import utils
import os


def calculate_listening_time_slots(data):
    if not data:
        return {}

    time_slots = {}
    total_users = len(data)

    for record in data:
        slot = record.get('music_time_slot')
        if slot:
            time_slots[slot] = time_slots.get(slot, 0) + 1

    for slot, count in time_slots.items():
        time_slots[slot] = utils.percentage(count, total_users)

    return time_slots


def calculate_mood_influences(data):
    if not data:
        return {}

    moods = {}
    total_users = len(data)

    for record in data:
        mood = record.get('music_Influencial_mood')
        if mood:
            mood_list = [m.strip() for m in mood.split(',')]
            for m in mood_list:
                moods[m] = moods.get(m, 0) + 1

    for mood, count in moods.items():
        moods[mood] = utils.percentage(count, total_users)

    return moods


def calculate_podcast_preferences(data):
    if not data:
        return {}

    podcast_stats = {
        'genres': {},
        'formats': {},
        'host_preferences': {},
        'durations': {}
    }

    total_podcast_users = sum(1 for record in data if record.get('pod_lis_frequency') != 'Never')

    if total_podcast_users == 0:
        return podcast_stats

    for record in data:
        if record.get('pod_lis_frequency') != 'Never':
            genre = record.get('fav_pod_genre')
            if genre and genre != 'None':
                podcast_stats['genres'][genre] = podcast_stats['genres'].get(genre, 0) + 1

            format_type = record.get('preffered_pod_format')
            if format_type and format_type != 'None':
                podcast_stats['formats'][format_type] = podcast_stats['formats'].get(format_type, 0) + 1

            host = record.get('pod_host_preference')
            if host and host != 'None':
                podcast_stats['host_preferences'][host] = podcast_stats['host_preferences'].get(host, 0) + 1

            duration = record.get('preffered_pod_duration')
            if duration and duration != 'None':
                podcast_stats['durations'][duration] = podcast_stats['durations'].get(duration, 0) + 1

    for category in podcast_stats:
        for key in podcast_stats[category]:
            podcast_stats[category][key] = utils.percentage(podcast_stats[category][key], total_podcast_users)

    return podcast_stats


def calculate_usage_patterns(data):
    if not data:
        return {}

    patterns = {
        'usage_period': {},
        'listening_frequency': {},
        'exploration_methods': {},
        'satisfaction_levels': {}
    }
    total_users = len(data)

    for record in data:
        period = record.get('spotify_usage_period')
        if period:
            patterns['usage_period'][period] = patterns['usage_period'].get(period, 0) + 1

        frequency = record.get('music_lis_frequency')
        if frequency:
            frequency_list = [f.strip() for f in frequency.split(',')]
            for f in frequency_list:
                patterns['listening_frequency'][f] = patterns['listening_frequency'].get(f, 0) + 1

        exploration = record.get('music_expl_method')
        if exploration:
            exploration_list = [e.strip() for e in exploration.split(',')]
            for e in exploration_list:
                patterns['exploration_methods'][e] = patterns['exploration_methods'].get(e, 0) + 1

        satisfaction = record.get('pod_variety_satisfaction')
        if satisfaction:
            patterns['satisfaction_levels'][satisfaction] = patterns['satisfaction_levels'].get(satisfaction, 0) + 1

    for category in patterns:
        for key in patterns[category]:
            patterns[category][key] = utils.percentage(patterns[category][key], total_users)

    return patterns


def get_gender_stats(request):
    file_path = os.path.join(settings.BASE_DIR, 'csvmanager', 'files', 'Spotify_data_user.xlsx')

    try:
        all_data = read_file(file_path)
        total_users = len(all_data)

        genders = ["Male", "Female", "Others"]
        gender_stats = {}

        for gender in genders:
            filters = {'Gender': gender}
            gender_data = read_file(file_path, filters=filters)
            total_users_gender = len(gender_data)

            gender_stats[gender] = {
                "global_percentage": utils.percentage(total_users_gender, total_users),
                "listening_time_preferences": calculate_listening_time_slots(gender_data),
                "mood_influences": calculate_mood_influences(gender_data),
                "podcast_preferences": calculate_podcast_preferences(gender_data),
                "usage_patterns": calculate_usage_patterns(gender_data)
            }

        data = {
            "gender_stats": gender_stats,
        }
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)