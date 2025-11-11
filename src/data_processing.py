"""
Module for cleaning and preprocessing solar farm measurement data.
"""

import pandas as pd

class SolarDataCleaner:
    """
    Class responsible for cleaning solar data measurements.
    """

    def __init__(self, df: pd.DataFrame):
        """
        :param df: Input raw measurements DataFrame
        """
        self.df = df

    def drop_high_missing(self, threshold: float = 0.05) -> pd.DataFrame:
        """
        Drop columns with missing-value fraction > threshold.

        :param threshold: max allowed fraction of missing data per column
        :return: cleaned DataFrame
        """
        missing_frac = self.df.isna().mean()
        cols_to_drop = missing_frac[missing_frac > threshold].index.tolist()
        return self.df.drop(columns=cols_to_drop)
