import requests
from datetime import datetime, timedelta
import os
import csv

# Vos identifiants
ACCESS_TOKEN = 'AQVkNYir6uErOUGbFLdhnVltwMr7Q8VRU6DW2ATl44x7IJWK1RqdTH0BGUKr0Dz8TUB7Ex5KadgMdllZDT-QQnOI0h62AC5zdzEVplZeSXVOvlCdi_nI5pwmqY3X7cCH0oWorXVcqvrxXuD6D7DeqLJRnguwmU8JlyqFv3dL1UjSEjUhny1TqkAazP0Y8o9nOQIuujIugeCfWBbGsWmM219YtMS3QG-N-gjx5bzdIevhTyYGjccMQw1Rma5pKxYzrfdauzUr5QCxw7HxITcN1_X14zfO6GvOZcBn7kfrB2IUBZfhbo3dKVseXOKmBFo-bXmyBi2p0gChSEmP4JkrienksD1v-w'  # Remplacez par votre token d'accès valide

# URL de l'API
url = 'https://api.linkedin.com/v2/organizationalEntityShareStatistics'

# En-têtes
headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Content-Type': 'application/json'
}

# ID de l'organisation
ORGANIZATION_ID = '70415423'  # Assurez-vous que cet ID est correct


# Fonction pour récupérer les statistiques pour une journée
def get_statistics_for_day(date):
    params = {
        'q': 'organizationalEntity',
        'organizationalEntity': f'urn:li:organization:{ORGANIZATION_ID}',
        'timeIntervals.timeGranularityType': 'DAY',
        'timeIntervals.timeRange.start': int(date.timestamp() * 1000),  # En millisecondes
        'timeIntervals.timeRange.end': int((date + timedelta(days=1)).timestamp() * 1000) - 1  # En millisecondes
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erreur {response.status_code}: {response.text}")
        return None


# Fonction principale
def main():
    # Date de début
    start_date = datetime(2023, 12, 30)
    end_date = datetime.today()

    # Récupérer les statistiques pour chaque jour
    current_date = start_date
    all_statistics = []

    while current_date <= end_date:
        print(f"Récupération des données pour le {current_date.strftime('%d/%m/%Y')}...")
        stats = get_statistics_for_day(current_date)
        if stats and 'elements' in stats and stats['elements']:
            all_statistics.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'impressions': stats['elements'][0]['totalShareStatistics'].get('impressionCount', 0),
                'clicks': stats['elements'][0]['totalShareStatistics'].get('clickCount', 0),
                'likes': stats['elements'][0]['totalShareStatistics'].get('likeCount', 0),
                'shares': stats['elements'][0]['totalShareStatistics'].get('shareCount', 0),
                'comments': stats['elements'][0]['totalShareStatistics'].get('commentCount', 0),
                'engagement': stats['elements'][0]['totalShareStatistics'].get('engagement', 0)
            })
        current_date += timedelta(days=1)
    # Chemin du fichier CSV dans le dossier du script
    script_dir = os.path.dirname(__file__)  # Dossier du script
    csv_file = os.path.join(script_dir, 'linkedin_statistics.csv')  # Chemin complet du fichier CSV

    # Sauvegarder les données dans un fichier CSV
    csv_columns = ['date', 'impressions', 'clicks', 'likes', 'shares', 'comments', 'engagement']

    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=csv_columns)
        writer.writeheader()
        writer.writerows(all_statistics)

    print(f"Les statistiques ont été sauvegardées dans le fichier '{csv_file}'.")


# Point d'entrée du script
if __name__ == "__main__":
    main()
