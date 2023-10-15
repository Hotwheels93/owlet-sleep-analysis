import pandas as pd
from datetime import datetime
from os.path import dirname, join
import locale

try:
    locale.setlocale(locale.LC_ALL, 'de_DE.utf8')
except locale.Error:
    print("German lang file not found. Default is English")

def minutes_to_hh_mm(minutes):
    hours, remainder = divmod(minutes, 60)
    return f"{hours:02d}:{remainder:02d}"

# Change filepath for your dataset here
df = pd.read_csv('owlet_smart_sock3_events-2.csv', delimiter=";")
df['last_updated'] = pd.to_datetime(df['last_updated'])
df['day'] = df['last_updated'].dt.date
df['weekday'] = df['last_updated'].dt.day_name()
df['month'] = df['last_updated'].dt.to_period('M')

csv_data = []

# Kopfzeile hinzufügen
csv_data.append(['Date', 'Weekday', 'Duration awake', 'Duration lightsleep', 'Duration deepsleep', 'Total Duration sleep'])

# Analyse
print(f"{'Datum':<20}{'Weekday':<20}{'Duration awake':<20}{'Duration lightsleep':<25}{'Duration deepsleep':<25}{'Total Duration sleep':<25}")

for month, month_df in df.groupby('month'):
    for day, day_df in month_df.groupby('day'):
        day_df = day_df.sort_values('last_updated')

        # Initialisieren
        counts = {1: 0, 8: 0, 15: 0}
        durations = {1: 0, 8: 0, 15: 0}
        prev_time = None
        total_sleep = 0

        for _, row in day_df.iterrows():
            current_time = row['last_updated'].hour * 60 + row['last_updated'].minute
            weekday = row['weekday']
            
            if prev_time is not None:
                duration = current_time - prev_time
                if row['sleep_state'] in [1, 8, 15]:
                    counts[row['sleep_state']] += 1
                    durations[row['sleep_state']] += duration
                    if row['sleep_state'] in [8, 15]:
                        total_sleep += duration
            prev_time = current_time

        # Daten formatieren
        sum_wake = minutes_to_hh_mm(durations[1])
        sum_light_sleep = minutes_to_hh_mm(durations[8])
        sum_deep_sleep = minutes_to_hh_mm(durations[15])
        sum_total_sleep = minutes_to_hh_mm(total_sleep)
        formatted_day = str(day)

        print(f"{formatted_day:<20}{weekday:<20}{sum_wake:<20}{sum_light_sleep:<25}{sum_deep_sleep:<25}{sum_total_sleep:<25}")

        # Zeile zur Liste hinzufügen
        csv_row = [formatted_day, weekday, sum_wake, sum_light_sleep, sum_deep_sleep, sum_total_sleep]
        csv_data.append(csv_row)

# Liste von Listen in einen DataFrame umwandeln
csv_df = pd.DataFrame(csv_data, columns=['Date', 'Weekday', 'Duration awake', 'Duration lightsleep', 'Duration deepsleep', 'Total Duration sleep'])

# DataFrame als CSV-Datei speichern
csv_df.to_csv('reports.csv', index=False, sep=';')
