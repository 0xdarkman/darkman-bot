import pandas as pd


def load_pickle(file_path: str) -> pd.DataFrame:
    return pd.read_pickle(file_path)


def filter_frame_by_dt_range(df, start, end):
    return df.loc[(df["Date"] > start) & (df["Date"] < end)].reset_index(drop=True)


def change_col_type(df, col: str, set_type: str):
    df[col] = df[col].astype(eval(set_type))
    return df
