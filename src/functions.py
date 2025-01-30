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

def create_classification_table(df: pd.DataFrame, year: int) -> pd.DataFrame:
    """
    """
    result_df = df.copy()

    collumns_order = ['Team', 'Total Points', 'Wins', 'Draws', 'Loses', 'Goals Diff', 'Goals For', 'Goals Against']

    result_df = add_year(result_df, 'Date')
    filtered_df = result_df[result_df['Year'] == year]

    filtered_agg = calculate_goals_statistics(calculate_points(filtered_df))
    filtered_agg['Total Points'] = filtered_agg['home_team_points'] + filtered_agg['away_team_points']
    filtered_agg['Wins'] = filtered_agg['home_win'] + filtered_agg['away_win']
    filtered_agg['Loses'] = filtered_agg['home_lose'] + filtered_agg['away_lose']
    filtered_agg = filtered_agg[collumns_order]
    return filtered_agg.sort_values(by='Total Points', ascending=False)

def calculate_points(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the points and statistics (wins, losses, draws) for teams
    based on match results ('FTR').

    Args:
        df (pd.DataFrame): A DataFrame containing the 'FTR' column indicating results:
                           - 'H': Home team wins
                           - 'D': Draw
                           - 'A': Away team wins

    Returns:
        pd.DataFrame: A new DataFrame with additional columns:
                      - 'home_team_points', 'away_team_points'
                      - 'home_win', 'home_lose', 'away_win', 'away_lose', 'draw'
    """
    result_df = df.copy()
    
    # Initialize new columns for points and statistics
    result_df['home_team_points'] = 0
    result_df['away_team_points'] = 0
    result_df['home_win'] = 0
    result_df['home_lose'] = 0
    result_df['Draws'] = 0
    result_df['away_lose'] = 0
    result_df['away_win'] = 0

    # Assign points and statistics based on match results ('FTR')
    # Home team wins ('H')
    result_df.loc[result_df['FTR'] == 'H', 'home_team_points'] = 3  # Home team gets 3 points
    result_df.loc[result_df['FTR'] == 'H', 'home_win'] = 1          # Home win count
    result_df.loc[result_df['FTR'] == 'H', 'away_lose'] = 1         # Away loss count

    # Draw ('D')
    result_df.loc[result_df['FTR'] == 'D', 'home_team_points'] = 1  # Home team gets 1 point
    result_df.loc[result_df['FTR'] == 'D', 'away_team_points'] = 1  # Away team gets 1 point
    result_df.loc[result_df['FTR'] == 'D', 'Draws'] = 1              # Draw count

    # Away team wins ('A')
    result_df.loc[result_df['FTR'] == 'A', 'away_team_points'] = 3  # Away team gets 3 points
    result_df.loc[result_df['FTR'] == 'A', 'home_lose'] = 1         # Home loss count
    result_df.loc[result_df['FTR'] == 'A', 'away_win'] = 1          # Away win count

    return result_df

def calculate_goals_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    yet to finish the logics
    """
    result_df = df.copy()

    result_df_agg_home = result_df.groupby('HomeTeam', as_index=False).agg({
        'FTHG': 'sum',
        'FTAG': 'sum',
        'home_team_points': 'sum',
        'home_win': 'sum',
        'home_lose': 'sum',
        'Draws': 'sum',
        })
    result_df_agg_home.rename(columns={
        'HomeTeam': 'Team',
        'FTHG': 'Goals For',
        'FTAG': 'Goals Against'
        }, inplace=True)

    result_df_agg_away = result_df.groupby('AwayTeam', as_index=False).agg({
    'FTHG': 'sum',
    'FTAG': 'sum',
    'away_team_points': 'sum',
    'away_win': 'sum',
    'away_lose': 'sum',
    'Draws': 'sum',
    })
    result_df_agg_away.rename(columns={
        'AwayTeam': 'Team',
        'FTHG': 'Goals Against',
        'FTAG': 'Goals For'
        }, inplace=True)

    combined_df = pd.concat([result_df_agg_away, result_df_agg_home], ignore_index=True)

    final_df = combined_df.groupby('Team', as_index=False).sum()
    final_df['Goals Diff'] = final_df['Goals For'] - final_df['Goals Against']
    return final_df