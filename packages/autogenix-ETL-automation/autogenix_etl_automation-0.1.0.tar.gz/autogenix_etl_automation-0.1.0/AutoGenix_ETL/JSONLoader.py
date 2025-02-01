import pandas as pd
import json
from .determine_orient import determine_orient


def JSONLoader(file_path, **kwargs):
    with open(file_path, "r") as file:
        json_data = json.load(file)

    orient = determine_orient(json_data)
    print(f"Detected orient: {orient}")
    df = pd.read_json(file_path, orient=orient, **kwargs)
    df_head = df.head()
    return df_head
