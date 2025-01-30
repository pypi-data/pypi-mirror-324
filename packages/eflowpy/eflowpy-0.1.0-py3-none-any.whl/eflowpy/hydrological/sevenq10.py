import numpy as np
import pandas as pd
from eflowpy.core import EnvironmentalFlow
from scipy.stats import lognorm

class SevenQ10Method(EnvironmentalFlow):
    """
    A class to estimate the 7Q10 low-flow using the 7-day, 10-year return period method.
    """

    def calculate_7q10(self):
        """
        Estimate the 7Q10 flow, which is the lowest 7-day average flow expected once every 10 years.

        Returns:
        float: Estimated 7Q10 flow value.
        """
        self.validate_data()  # Ensure the data is valid

        # Ensure data is in a Pandas Series with a datetime index (for yearly grouping)
        if not isinstance(self.flow_data.index, pd.DatetimeIndex):
            raise ValueError("Flow data must have a datetime index for annual analysis.")

        # Compute the 7-day moving average
        rolling_7day_avg = self.flow_data.rolling(window=7, min_periods=7).mean()

        # Extract the minimum 7-day average flow per year
        min_annual_flows = rolling_7day_avg.groupby(self.flow_data.index.year).min().dropna()

        # Fit a log-normal distribution to estimate the 10-year return period
        shape, loc, scale = lognorm.fit(min_annual_flows, floc=0)
        q10_flow = lognorm.ppf(0.1, shape, loc, scale)  # 10% probability (10-year return)

        return q10_flow
