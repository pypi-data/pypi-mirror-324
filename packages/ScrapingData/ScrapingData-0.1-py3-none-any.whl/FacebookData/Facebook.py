
import csv
import requests
from datetime import datetime, timedelta
import pytz
import os

# Configuration globale
BASE_URL = "https://graph.facebook.com/v21.0"
PAGE_ID = "Rsolution.by.Recinov"  # Remplacez par l'ID de votre page
ACCESS_TOKEN = "EAB9kU0ZCfDWEBO0YwOsZCrY6tlmPcm8kBaaudnjjqcCm4GGFVIkfgSbr9RhX3tifUjGUcq3DTOJqfyWsomMkfblLw0ODG8EdTWZB2SuOXwboXfZBWCGI5BmJwmxQ2nfGlt37PM881vMIgR9CGjUJrzDUMgRae54WJs5MkMHd3Uqfk7xYQiDzVF7wgFHHXL6PSZAhGdAePugLKikZBQZBgwR2KgBOuZCTt7ZCgAoSAqhcZC"


# Fonction pour récupérer les données de type "day"
def fetch_day_metrics(metric, start_date, end_date):
    data_by_date = {}
    current_start_date = start_date

    while current_start_date < end_date:
        current_end_date = min(current_start_date + timedelta(days=90), end_date)

        params = {
            'metric': metric,
            'period': 'day',
            'since': current_start_date.strftime('%Y-%m-%d'),
            'until': current_end_date.strftime('%Y-%m-%d'),
            'access_token': ACCESS_TOKEN
        }

        response = requests.get(f"{BASE_URL}/{PAGE_ID}/insights", params=params)

        if response.status_code == 200:
            data = response.json().get('data', [])
            for entry in data:
                for value in entry.get('values', []):
                    date = value['end_time'].split('T')[0]
                    if date not in data_by_date:
                        data_by_date[date] = {'date': date}
                    data_by_date[date][metric] = value.get('value', 0)
        else:
            print(f"Erreur pour {metric}: {response.status_code} - {response.text}")

        current_start_date = current_end_date

    return data_by_date


# Fonction pour récupérer les données de type "lifetime"
def fetch_lifetime_metrics(post_id, metrics):
    insights_url = f"{BASE_URL}/{post_id}/insights"
    params = {
        'metric': ','.join(metrics),
        'period': 'lifetime',
        'access_token': ACCESS_TOKEN
    }
    response = requests.get(insights_url, params=params)

    if response.status_code == 200:
        return response.json().get('data', [])
    else:
        print(f"Erreur pour {post_id}: {response.status_code} - {response.text}")
        return []


# Fonction pour récupérer les publications
def fetch_posts(start_date, end_date):
    posts_url = f"{BASE_URL}/{PAGE_ID}/posts"
    posts_data = []
    current_start_date = start_date

    while current_start_date < end_date:
        current_end_date = min(current_start_date + timedelta(days=90), end_date)

        params = {
            'fields': 'id,created_time,attachments{media_type}',
            'since': current_start_date.strftime('%Y-%m-%d'),
            'until': current_end_date.strftime('%Y-%m-%d'),
            'access_token': ACCESS_TOKEN
        }

        response = requests.get(posts_url, params=params)
        if response.status_code == 200:
            posts_data.extend(response.json().get('data', []))
        else:
            print(f"Erreur lors de la récupération des publications: {response.status_code} - {response.text}")

        current_start_date = current_end_date

    return posts_data


# Fonction pour générer le fichier Facebook_page_insights.csv
def generate_page_insights_csv():
    metrics = [
        'page_daily_follows',
        'page_follows', 'page_impressions',
        'page_fans', 'page_views_total',
    ]

    start_date = datetime(2024, 5, 12)
    end_date = datetime.now()

    data_by_date = {}
    for metric in metrics:
        metric_data = fetch_day_metrics(metric, start_date, end_date)
        for date, values in metric_data.items():
            if date not in data_by_date:
                data_by_date[date] = {'date': date}
            data_by_date[date].update(values)

    # Chemin du fichier CSV dans le dossier du script
    csv_file = os.path.join(os.path.dirname(__file__), 'Facebook_page_insights.csv')
    with open(csv_file, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['date'] + metrics
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for date, row in data_by_date.items():
            writer.writerow(row)


# Fonction pour générer le fichier Facebook_post.csv
def generate_post_csv():
    metrics = [
        'post_impressions',
        'post_impressions_unique',
        'post_reactions_like_total',
        'post_video_views',
        'post_video_avg_time_watched',
        'post_clicks',
    ]

    tz = pytz.timezone('UTC')
    start_date = tz.localize(datetime(2024, 5, 12))
    end_date = datetime.now(tz)

    posts = fetch_posts(start_date, end_date)

    # Chemin du fichier CSV dans le dossier du script
    csv_file = os.path.join(os.path.dirname(__file__), 'Facebook_post.csv')

    with open(csv_file, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['date', 'post_id', 'post_type'] + metrics
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for post in posts:
            post_id = post.get('id')
            created_time = post.get('created_time')
            post_date = datetime.strptime(created_time, '%Y-%m-%dT%H:%M:%S%z')

            if start_date <= post_date <= end_date:
                attachments = post.get('attachments', {}).get('data', [{}])
                post_type = attachments[0].get('media_type', 'post') if attachments else 'post'

                insights_data = fetch_lifetime_metrics(post_id, metrics)
                row = {'date': created_time, 'post_id': post_id, 'post_type': post_type}

                for entry in insights_data:
                    metric_name = entry.get('name')
                    metric_value = entry.get('values', [{}])[0].get('value', 0)
                    row[metric_name] = metric_value

                writer.writerow(row)


# Fonction pour générer le fichier Facebook_fans.csv
def generate_fans_csv():
    metrics = ['page_fans', 'page_fans_city', 'page_fans_country', 'page_fans_locale']

    start_date = datetime(2024, 5, 12)
    end_date = datetime.now()

    data_by_date = {}
    for metric in metrics:
        metric_data = fetch_day_metrics(metric, start_date, end_date)
        for date, values in metric_data.items():
            if date not in data_by_date:
                data_by_date[date] = {
                    'page_fans': 0,
                    'cities': {},
                    'countries': {},
                    'languages': {}
                }
            if metric == 'page_fans':
                data_by_date[date]['page_fans'] = values.get(metric, 0)
            elif metric == 'page_fans_city':
                data_by_date[date]['cities'] = values.get(metric, {})
            elif metric == 'page_fans_country':
                data_by_date[date]['countries'] = values.get(metric, {})
            elif metric == 'page_fans_locale':
                data_by_date[date]['languages'] = values.get(metric, {})

    # Chemin du fichier CSV dans le dossier du script
    csv_file = os.path.join(os.path.dirname(__file__), 'Facebook_fans.csv')

    with open(csv_file, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['date', 'page_fans', 'city', 'country', 'language', 'fans_count']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for date, data in data_by_date.items():
            page_fans = data['page_fans']
            cities = data.get('cities', {})
            countries = data.get('countries', {})
            locales = data.get('languages', {})

            for city, city_count in cities.items():
                for country, country_count in countries.items():
                    for locale, locale_count in locales.items():
                        writer.writerow({
                            'date': date,
                            'page_fans': page_fans,
                            'city': city,
                            'country': country,
                            'language': locale,
                            'fans_count': min(city_count, country_count, locale_count)
                        })


# Fonction principale
def main():
    print("Exécution de Facebook.py...")
    generate_page_insights_csv()
    generate_post_csv()
    generate_fans_csv()
    print("Les fichiers CSV ont été générés avec succès.")


# Point d'entrée du script
if __name__ == "__main__":
    main()
