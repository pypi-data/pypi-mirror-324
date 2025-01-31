import numpy as np
import pandas as pd
import os
from datetime import datetime, timedelta
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest, OrderBy

# Variables globales
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(os.path.dirname(__file__), 'ExtractData-f88dd607777a.json')
property_id = '350317823'
client = BetaAnalyticsDataClient()


# Fonction pour formater le rapport
def format_report(response):
    # Index des lignes
    row_index_names = [header.name for header in response.dimension_headers]
    row_header = []
    for i in range(len(row_index_names)):
        row_header.append([row.dimension_values[i].value for row in response.rows])

    row_index_named = pd.MultiIndex.from_arrays(np.array(row_header), names=np.array(row_index_names))

    # Données des métriques
    metric_names = [header.name for header in response.metric_headers]
    data_values = []
    for i in range(len(metric_names)):
        data_values.append([row.metric_values[i].value for row in response.rows])

    # Création du DataFrame
    output = pd.DataFrame(data=np.transpose(np.array(data_values, dtype='f')),
                          index=row_index_named, columns=metric_names)
    return output


# Fonction pour extraire les données par segments de temps
def fetch_data_in_segments(start_date, end_date, dimensions, metrics, order_by, segment_days=30):
    all_data = pd.DataFrame()
    current_start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    while current_start_date < end_date:
        current_end_date = min(current_start_date + timedelta(days=segment_days), end_date)
        date_range = DateRange(start_date=current_start_date.strftime("%Y-%m-%d"),
                               end_date=current_end_date.strftime("%Y-%m-%d"))

        request = RunReportRequest(
            property='properties/' + property_id,
            dimensions=[Dimension(name=dim) for dim in dimensions],
            metrics=[Metric(name=metric) for metric in metrics],
            order_bys=[OrderBy(dimension={'dimension_name': order_by})],
            date_ranges=[date_range],
        )

        response = client.run_report(request)
        segment_data = format_report(response)
        all_data = pd.concat([all_data, segment_data], axis=0)

        # Passer au segment suivant
        current_start_date = current_end_date + timedelta(days=1)

    return all_data


# Fonction principale
def main():
    print("Exécution de GoogleAnalyticsFor3Data.py...")

    # Définir les dates de début et de fin
    start_date = "2023-01-20"  # Date de création du site
    end_date = datetime.today().strftime("%Y-%m-%d")  # Aujourd'hui

    # UserData
    user_data_dimensions = ["date", "sessionMedium", "sessionSource", "newVsReturning", "audienceId", "signedInWithUserId", "region", "browser"]
    user_data_metrics = ["activeUsers", "newUsers", "engagedSessions", "totalUsers", "firstTimePurchasers", "purchaseRevenue", "averageSessionDuration", "bounceRate", "sessionsPerUser"]
    user_data = fetch_data_in_segments(start_date, end_date, user_data_dimensions, user_data_metrics, order_by="date")

    # CityData
    city_data_dimensions = ["date", "city", "region", "continent", "country"]
    city_data_metrics = ["activeUsers", "totalUsers", "newUsers"]
    city_data = fetch_data_in_segments(start_date, end_date, city_data_dimensions, city_data_metrics, order_by="city")

    # DeviceData
    device_data_dimensions = ["date", "deviceCategory", "language", "browser", "appVersion", "country"]
    device_data_metrics = ["activeUsers", "totalUsers", "newUsers"]
    device_data = fetch_data_in_segments(start_date, end_date, device_data_dimensions, device_data_metrics, order_by="deviceCategory")

    # Exporter les données vers des fichiers CSV dans le dossier du script
    script_dir = os.path.dirname(__file__)  # Dossier où se trouve ce script

    user_data_csv_path = os.path.join(script_dir, 'user_data_GA.csv')
    user_data.to_csv(user_data_csv_path)

    city_data_csv_path = os.path.join(script_dir, 'city_data_GA.csv')
    city_data.to_csv(city_data_csv_path)

    device_data_csv_path = os.path.join(script_dir, 'device_data_GA.csv')
    device_data.to_csv(device_data_csv_path)

    print(f"Les données Google Analytics ont été extraites et sauvegardées avec succès dans le dossier : {script_dir}")


# Point d'entrée du script
if __name__ == "__main__":
    main()
