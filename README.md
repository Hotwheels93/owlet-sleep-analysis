# owlet-sleep-analysis
Script to aggregate and analyze sleep data from the Owlet Smart Sock 3

# Features
- Plots sleep cycles, output are images with plots for each day in a month
- Generating reports to do further investigation.
  Reports have the following structure: Date, Weekday, Duraiton awake, Duration of light sleep, Duration of deep sleep, Sum Duration light & deep sleep

# Requirements: 

- Dataset with the data measured by the Smart Sock in csv format. The structure of the dataset should look like this

  "id";"userID";"heartRate";"oxygenSaturation";"battery";"skin_temperature";"sock_disconnected";"sock_off";"battery_minutes";"signal_strength";"base_station_on";"sock_connection";"sleep_state";"movement";"movement_bucket";"charging";"monitor_start_time";"base_battery_status";"last_updated";"importDate"
"1";"3";"0";"0";"100";"0";"0";"0";"0";"41";"1";"2";"0";"0";"0";"2";"0";"4";"2023-07-13 22:16:26";"2023-07-14 00:21:04"

# FAQ: How to get the data measured by the Owlet Smart Sock 3?

- There a different wrappers available which have alreay implemented the API protocol to communicate with the sock, for example you can use https://github.com/ryanbdclark/pyowletapi

- It is recommended to store the data measured by the sock in a database or file. In the Owlet app data currently is only available for 30 days. After this time they will be deleted automatically
