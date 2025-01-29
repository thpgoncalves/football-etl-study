import pandas as pd
from typing import List

def read_csv(df: str) -> pd.DataFrame:
    """
    """
    data_frame = pd.read_csv(f'../data/{df}.csv')
    return data_frame

def add_year(df: pd.DataFrame, date_collumn: str) -> pd.DataFrame:
    result_df = df.copy()
    result_df[f'{date_collumn}'] = pd.to_datetime(result_df[f'{date_collumn}'], dayfirst=True, format='mixed')
    result_df['Year'] = result_df[f'{date_collumn}'].dt.year
    return result_df 

def create_classification_table(df: pd.DataFrame, year: str) -> pd.DataFrame:
    """
    """
    return 

def calculate_points(df: pd.DataFrame) -> pd.DataFrame:
    """
    """
    result_df = df.copy()
    
    result_df['home_team_points'] = 0
    result_df['away_team_points'] = 0

    result_df.loc[result_df['FTR'] == 'H', 'home_team_points'] = 3
    result_df.loc[result_df['FTR'] == 'D', ['home_team_points', 'away_team_points']] = 1
    result_df.loc[result_df['FTR'] == 'A', 'away_team_points'] = 3

    return result_df

def calculate_goals_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    yet to finish the logics
    """
    result_df = df.copy()

    result_df['goals_for'] = 0
    result_df['goals_against'] = 0
    result_df['goals_diff'] = 0