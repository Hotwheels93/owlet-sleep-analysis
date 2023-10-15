import pandas as pd
import matplotlib.pyplot as plt
from tkinter import filedialog, Tk
from os.path import dirname, join
from datetime import time

root = Tk()
root.withdraw()
csv_file_path = filedialog.askopenfilename(title="Choose your dataset")
root.destroy()

if not csv_file_path:
    print("No file choosen.")
    exit()


df = pd.read_csv(csv_file_path, delimiter=";")
df['last_updated'] = pd.to_datetime(df['last_updated'])
df['day'] = df['last_updated'].dt.date
df['month'] = df['last_updated'].dt.to_period('M')

color_map = {0: 'white', 1: 'red', 8: 'blue', 15: 'yellow'}
label_map = {0: 'Unknown', 1: 'Awake', 8: 'LightSleep', 15: 'DeepSleep'}
labels_added = set()

for month, month_df in df.groupby('month'):
    plt.figure(figsize=(20, 20))
    unique_days = sorted(month_df['day'].unique())

    for idx, day in enumerate(unique_days):
        day_df = month_df[month_df['day'] == day]
        day_df = day_df.sort_values('last_updated')
        
        prev_minutes = None
        for _, row in day_df.iterrows():
            current_minutes = row['last_updated'].hour * 60 + row['last_updated'].minute
            label = None
            if row['sleep_state'] not in labels_added:
                label = label_map.get(row['sleep_state'], 'Unknown')
                labels_added.add(row['sleep_state'])
            if prev_minutes is not None:
                plt.fill_betweenx([idx * 1.2, (idx + 1) * 1.2], prev_minutes, current_minutes, color=color_map[row['sleep_state']], label=label)
            prev_minutes = current_minutes

    plt.legend(title="Phases", loc="upper right")
    plt.yticks([idx * 1.2 for idx in range(len(unique_days))], unique_days)
    plt.title(f'Sleepcycles month: {month}')
    plt.xlabel('Time')
    plt.xlim(0, 23 * 60 + 59)
    plt.xticks([0, 360, 720, 1080, 1440], ['00:00', '06:00', '12:00', '18:00', '24:00'])
    
    plt.savefig(join(dirname(csv_file_path), f'sleep_plot_month_{month}.png'))
    plt.close()

print(f"Plots saved in {dirname(csv_file_path)}")
