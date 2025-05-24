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
    # Iterate through 'Stop number' values in the group
    part_number = 1
    for stop_id in group['Stop:Number']:
        whole_entry = group.loc[group["Stop:Number"] == stop_id]
        if (len(group['Stop:Number']) <= 1):
            break
        
        if departure_column.empty:
            departure_column = whole_entry
        elif arrival_column.empty and not departure_column.empty:
            arrival_column = whole_entry
            ###Merge merge merge!
            is_cancelled_val = -1
            if (departure_column['Stop:Departure cancelled'].iloc[0] == False and arrival_column['Stop:Arrival cancelled'].iloc[0] == False):
                is_cancelled_val = False
            elif (departure_column['Stop:Departure cancelled'].iloc[0] == True and arrival_column['Stop:Arrival cancelled'].iloc[0] == True):
                is_cancelled_val = True
            else:
                is_cancelled_val = True
            new_entries.append(
                {
                'Journey id': departure_column['Service:RDT-ID'].iloc[0],
                'Train type': departure_column['Service:Type'].iloc[0],
                'Departure station code': departure_column['Stop:Station code'].iloc[0],
                'Arrival station code': arrival_column['Stop:Station code'].iloc[0],
                'Departure station name': departure_column['Stop:Station name'].iloc[0],
                'Arrival station name': arrival_column['Stop:Station name'].iloc[0],
                'Departure time': departure_column['Stop:Departure time'].iloc[0],
                'Arrival time': arrival_column['Stop:Arrival time'].iloc[0],
                'Departure delay': departure_column["Stop:Departure delay"].iloc[0],
                "Arrival delay": arrival_column["Stop:Arrival delay"].iloc[0],
                'Part number': part_number,
                'Cancelled': is_cancelled_val,
                "Departure platform changed": departure_column["Stop:Platform change"].iloc[0],
                "Arrival platform changed": arrival_column["Stop:Platform change"].iloc[0]
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