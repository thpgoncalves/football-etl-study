import pandas as pd
from typing import List

def read_csv(df: str) -> pd.DataFrame:
    """
    """
    data_frame = pd.read_csv(f'../data/{df}.csv')
    return data_frame