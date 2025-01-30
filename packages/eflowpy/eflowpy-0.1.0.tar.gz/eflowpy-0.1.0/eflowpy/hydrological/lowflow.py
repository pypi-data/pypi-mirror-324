from eflowpy.core import EnvironmentalFlow

class LowFlowQ90(EnvironmentalFlow):
    """
    A class to calculate low flow indices like Q90.
    Inherits from the EnvironmentalFlow base class.
    """

    def calculate_q90(self):
        """
        Calculate the Q90 flow (flow exceeded 90% of the time).

        Returns:
        float: The Q90 flow value.
        """
        self.validate_data()  # Ensure the data is valid

        # Sort the flow data in descending order
        sorted_flows = self.flow_data.sort_values(ascending=False).reset_index(drop=True)

        # Calculate the position of Q90 (90% exceedance)
        n = len(sorted_flows)
        q90_index = int(n * 0.9) - 1  # 90% exceedance index (zero-based)

        # Return the flow value at the Q90 index
        return sorted_flows.iloc[q90_index]
