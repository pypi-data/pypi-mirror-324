from eflowpy.core import EnvironmentalFlow
import pandas as pd

class FlowDurationCurve(EnvironmentalFlow):
    """
    A class to calculate environmental flows using the Flow Duration Curve (FDC) Shifting Method.
    Inherits from the EnvironmentalFlow base class.
    """

    def calculate_fdc(self):
        """
        Calculate the Flow Duration Curve (FDC).

        Returns:
        pd.DataFrame: A DataFrame containing sorted flow values and exceedance probabilities.
        """
        self.validate_data()  # Ensure the data is valid

        # Sort the flow data in descending order
        sorted_flows = self.flow_data.sort_values(ascending=False).reset_index(drop=True)

        # Fix exceedance probability calculation (ensure it goes from 100% to near 0%)
        exceedance_probabilities = [(100 * (i) / (len(sorted_flows) - 1)) for i in range(len(sorted_flows))]

        # Combine into a DataFrame
        fdc = pd.DataFrame({
            "Exceedance Probability (%)": exceedance_probabilities,
            "Flow (m^3/s)": sorted_flows
        })

        return fdc


    

    def get_flow_at_percentile(self, percentile):
        """
        Get the flow value at a specified exceedance percentile.

        Parameters:
        percentile (float): The target exceedance percentile (e.g., 10 for Q10).

        Returns:
        float: The flow value corresponding to the target percentile.
        """
        fdc = self.calculate_fdc()

        # Debugging: Print available columns and percentile range
        print("\nAvailable Columns in FDC DataFrame:", fdc.columns)
        print(f"Percentile Requested: {percentile}, Min Exceedance: {fdc['Exceedance Probability (%)'].min()}, Max: {fdc['Exceedance Probability (%)'].max()}")

        # Extract exceedance probabilities and corresponding flow values
        exceedance_probs = fdc["Exceedance Probability (%)"].values
        flow_values = fdc["Flow (m^3/s)"].values

        # Ensure the requested percentile is within the valid range
        if percentile < min(exceedance_probs) or percentile > max(exceedance_probs):
            raise ValueError(f"Percentile {percentile} is out of range! Allowed range: {min(exceedance_probs)}% to {max(exceedance_probs)}%.")

        # Interpolate to get an accurate flow estimate at the given percentile
        from scipy.interpolate import interp1d
        interp_func = interp1d(exceedance_probs, flow_values, kind="linear", fill_value="extrapolate")
        return float(interp_func(percentile))

