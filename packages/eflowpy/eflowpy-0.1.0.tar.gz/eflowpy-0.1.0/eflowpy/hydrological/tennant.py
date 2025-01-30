from eflowpy.core import EnvironmentalFlow

class TennantMethod(EnvironmentalFlow):
    """
    A class to calculate environmental flows using the Tennant Method.
    Inherits from the EnvironmentalFlow base class.
    """

    def calculate_flows(self):
        """
        Calculate minimum and optimum flows based on the Tennant Method.

        Returns:
        dict: A dictionary with minimum and optimum environmental flows.
        """
        self.validate_data()  # Ensure the data is valid

        minimum_flow = 0.1 * self.average_flow  # 10% of average flow
        optimum_flow = 0.3 * self.average_flow  # 30% of average flow

        return {
            "minimum_flow": minimum_flow,
            "optimum_flow": optimum_flow
        }
