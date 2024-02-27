import json
import pandas as pd
from datetime import datetime, timedelta
from common import *

def processJSON(PATH):
    with open(PATH, "r") as f:
        data = json.load(f)
    
    columns = []
    for key, value in data['data'][0].items():
        if isinstance(value, dict):
            for k, v in value.items():
                columns.append(k)
        else:
            columns.append(key)
    
    df = pd.DataFrame(columns = columns)

    for i in range(len(data['data'])):
        row = []
        for key, value in data['data'][i].items():
            if isinstance(value, dict):
                for k, v in value.items():
                    row.append(v)
            else:
                row.append(value)
        df.loc[i] = row

    start = []
    end = []

    for i in range(len(df)):
        time = df.loc[i, "time"].split('-')
        start.append(time[0].strip())
        end.append(time[1].strip())

    df['start_time'] = start
    df['end_time'] = end

    df['weekday'] = df["day"].apply(lambda x: day_mapping[x])

    for col in ["start_time", "end_time"]:
        time = []
        for time_str in df[col]:
            time_obj = datetime.strptime(time_str, "%I:%M")
            if time_obj.hour < 6:
                time_obj = time_obj + timedelta(hours=12)
            time.append(time_obj.strftime("%H:%M"))

        df[col] = time

    df["start_time"] = df["start_time"].apply(lambda x: datetime.strptime(x, "%H:%M").time())
    df["end_time"] = df["end_time"].apply(lambda x: datetime.strptime(x, "%H:%M").time())

    df = df.sort_values(by = ["section", "weekday", "start_time"]).reset_index(drop = True).drop("id", axis = 1)
    cols = ["section", 'weekday', 'day', 'start_time', 'end_time', "pid" , 'course_number', 'course_name', 'instructor_id', 'instructor_name', 'room']
    df = df[cols]

    return df