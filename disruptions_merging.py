import numpy as np
import pandas as pd
from datetime import datetime
import pytz

tz = pytz.timezone("Europe/Amsterdam")
disruptions_dataset = pd.read_csv("preprocessed_data/disruptions_p.csv")
engineering_works = pd.read_csv("preprocessed_data/engineering_works_p.csv")

def merge_disruptions(one_row_encoded_as_dict):
    
    for _, row in disruptions_dataset.iterrows():
        station_codes = row["rdt_station_codes"].split(", ")
        if (len(station_codes) == 1):
            if (one_row_encoded_as_dict["Departure station code"] in station_codes or one_row_encoded_as_dict["Arrival station code"] in station_codes):
                if (compare_times_singular(one_row_encoded_as_dict["Departure time"], row["start_time"], row["end_time"]) or 
                compare_times_singular(one_row_encoded_as_dict["Arrival time"], row["start_time"], row["end_time"])):
                    one_row_encoded_as_dict["Disruptions"] = True
                    return one_row_encoded_as_dict
        else:
            if ((one_row_encoded_as_dict["Departure station code"] in station_codes and one_row_encoded_as_dict["Arrival station code"] in station_codes)):
                if (compare_times_multiple(one_row_encoded_as_dict["Departure time"], one_row_encoded_as_dict["Arrival time"], row["start_time"], row["end_time"])):
                    one_row_encoded_as_dict["Disruptions"] = True
                    return one_row_encoded_as_dict
                
    one_row_encoded_as_dict["Disruptions"] = False
    return one_row_encoded_as_dict
                    
def merge_maintenance(one_row_encoded_as_dict):
    
    for _, row in disruptions_dataset.iterrows():
        station_codes = row["rdt_station_codes"].split(", ")
        
        if ((one_row_encoded_as_dict["Departure station code"] in station_codes and one_row_encoded_as_dict["Arrival station code"] in station_codes)):
            if (compare_times_multiple(one_row_encoded_as_dict["Departure time"], one_row_encoded_as_dict["Arrival time"], row["start_time"], row["end_time"])):
                one_row_encoded_as_dict["Maintenance"] = True
                return one_row_encoded_as_dict
                
    one_row_encoded_as_dict["Maintenance"] = False
    return one_row_encoded_as_dict
                    
            
def compare_times_singular(main_dataset_time, start_time_disruptions, end_time_disruptions):
    
    main_time = datetime.fromisoformat(main_dataset_time)
    start_time = datetime.strptime(start_time_disruptions, "%Y-%m-%d %H:%M:%S")  # naive
    end_time = datetime.strptime(end_time_disruptions, "%Y-%m-%d %H:%M:%S") # naive
    
    #make this timezone-aware
    start_time = tz.localize(start_time)
    end_time = tz.localize(end_time)
    
    #disruption has occured
    if (start_time < main_time and end_time > main_time):
        return True
    
    return False


def compare_times_multiple(main_dep_time, main_arr_time, start_time_disruptions, end_time_disruptions):
    
    dep_time = datetime.fromisoformat(main_dep_time)
    arr_time = datetime.fromisoformat(main_arr_time)
    
    start_time = datetime.strptime(start_time_disruptions, "%Y-%m-%d %H:%M:%S")  # naive
    end_time = datetime.strptime(end_time_disruptions, "%Y-%m-%d %H:%M:%S")  # naive
    
    #make this timezone-aware
    start_time = tz.localize(start_time)
    end_time = tz.localize(end_time)
    
    if (end_time < dep_time or start_time > arr_time):
        return False
    return True