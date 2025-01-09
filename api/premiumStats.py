import os
import logging
from django.conf import settings
from django.http import JsonResponse
from csvmanager.fileHandler import read_file
from api.utils import percentage

logger = logging.getLogger(__name__)

try:
    file_path = os.path.join(settings.BASE_DIR, 'csvmanager', 'files', 'Spotify_data_user.xlsx')
    datas = read_file(file_path)
    total_users = len(datas)
except Exception as e:
    logger.error(f"Error reading data file: {e}")
    datas = []
    total_users = 0

def counts_and_percentage(counts, local_total):
    if local_total == 0:
        return {}
    
    return {
        item: {
            "count": count,
            "local_percentage": percentage(count, local_total),
            "global_percentage": percentage(count, total_users)
            
        }
        for item, count in counts.items()
    }

def _get_plan_distribution(data):
    if not data:
        return {}

    plan_count = {}

    for record in data:
        plan = record.get('spotify_subscription_plan', 'Unknown') 
        plan_count[plan] = plan_count.get(plan, 0) + 1

    return counts_and_percentage(plan_count, total_users)

def _plan_vs_usage_period(data):
    if not data:
        return {}

    results = {}
    for record in data:
        period = record.get('spotify_usage_period', 'Unknown')
        plan = record.get('spotify_subscription_plan', 'Unknown')
        if period not in results:
            results[period] = {}
        results[period][plan] = results[period].get(plan, 0) + 1

    for period, plan_dict in results.items():
        local_total = sum(plan_dict.values())
        results[period] = counts_and_percentage(plan_dict, local_total)

    return results



def _plan_vs_age(data):
    if not data:
        return {}

    results = {}
    for record in data:
        age_group = record.get('Age', 'Unknown')
        plan = record.get('spotify_subscription_plan', 'Unknown')
        if age_group not in results:
            results[age_group] = {}
        results[age_group][plan] = results[age_group].get(plan, 0) + 1

    for age_group, plan_dict in results.items():
        local_total = sum(plan_dict.values())
        results[age_group] = counts_and_percentage(plan_dict, local_total)

    return results

def _plan_vs_satisfaction(data):
    if not data:
        return {}

    results = {}
    for record in data:
        satisfaction = record.get('pod_variety_satisfaction', 'Unknown')
        plan = record.get('spotify_subscription_plan', 'Unknown')
        if satisfaction not in results:
            results[satisfaction] = {}
        results[satisfaction][plan] = results[satisfaction].get(plan, 0) + 1

    for satisfaction, plan_dict in results.items():
        local_total = sum(plan_dict.values())
        results[satisfaction] = counts_and_percentage(plan_dict, local_total)

    return results


def _plan_vs_content_type(data):
    if not data:
        return {}

    results = {}
    for record in data:
        content_type = record.get('preferred_listening_content', 'Unknown')
        plan = record.get('spotify_subscription_plan', 'Unknown')
        if content_type not in results:
            results[content_type] = {}
        results[content_type][plan] = results[content_type].get(plan, 0) + 1

    for content_type, plan_dict in results.items():
        local_total = sum(plan_dict.values())
        results[content_type] = counts_and_percentage(plan_dict, local_total)

    return results


def get_premium_stats(request):
    
    try : 
        response_data = {
            "plan_distribution": _get_plan_distribution(datas),
            "plan_vs_usage_period": _plan_vs_usage_period(datas),
            "plan_vs_age": _plan_vs_age(datas),
            "plan_vs_satisfaction": _plan_vs_satisfaction(datas),
            "plan_vs_content_type": _plan_vs_content_type(datas)
        }
        return JsonResponse(response_data, safe=False)
    except ValueError as e:
        logger.exception("Une erreur est survenue pendant la récupération des statistiques liées aux abonnements premium")
        return JsonResponse({'error': str(e)}, status=400)
