import pandas as pd
import time
import datetime
from datetime import datetime

#for journey, group in grouped_data:
def merge_func(args):
    journey_id, group = args
    new_entries = []
    departure_column = pd.Series([])
    arrival_column = pd.Series([])
    # Iterate through 'Stop id' values in the group
    part_number = 1
    for stop_id in group['Stop id']:
        whole_entry = group.loc[group["Stop id"] == stop_id]
        if departure_column.empty:
            departure_column = whole_entry
        elif arrival_column.empty and not departure_column.empty:
            arrival_column = whole_entry
            ###Merge merge merge!
            total_delay = departure_column['Arrival delay'].iloc[0] + departure_column['Departure delay'].iloc[0]
            if stop_id == len(group):
                total_delay = total_delay + arrival_column['Arrival delay'].iloc[0]
            new_entries.append(
                {
                'Journey id': departure_column['Journey id'].iloc[0],
                'Train type': departure_column['Train type'].iloc[0],
                'Railroad company': departure_column['Railroad company'].iloc[0],
                'Train number': departure_column['Train number'].iloc[0],
                'Departure station code': departure_column['Station code'].iloc[0],
                'Arrival station code': arrival_column['Station code'].iloc[0],
                'Departure station name': departure_column['Station name'].iloc[0],
                'Arrival station name': arrival_column['Station name'].iloc[0],
                'Total journey delay': total_delay,
                'Departure time': departure_column['Departure time'].iloc[0],
                'Arrival time': arrival_column['Arrival time'].iloc[0],
                'Is weekend': arrival_column['Is_weekend'].iloc[0],
                'Is holiday': arrival_column['Is_holiday'].iloc[0],
                'Part number': part_number,
                'Cancelled': departure_column['Departure cancelled'].iloc[0]
                }
            ) 
            departure_column = arrival_column
            part_number = part_number + 1
        arrival_column = pd.Series([])
    return pd.DataFrame(new_entries)

def unify_date_time_format(df):
    new_dataframe = df
    result = pd.DataFrame(new_dataframe)
    result["Departure time"] = result["Departure time"].apply(lambda x: pd.to_datetime(x).strftime('%Y-%m-%d %H:%M:%S'))
    return result

def check_for_disruptions(df):
    df['Disruptions'] = df.apply(lambda row: check_for_disruptions(row['Departure station code'], row['Arrival station code'], row['Departure time'], row['Arrival time']), axis=1)
    return df