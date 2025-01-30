from eflowpy.hydrological.fdc import FlowDurationCurve

class GEFCMethod(FlowDurationCurve):
    """
    A class to estimate environmental flows using the Global Environmental Flow Calculator (GEFC) method.
    Inherits from the FlowDurationCurve class.
    """

    def calculate_gefc_flows(self):
        """
        Estimate environmental flow thresholds based on EMC classes.

        Returns:
        dict: Environmental flow thresholds for different EMC classes.
        """
        self.validate_data()  # Ensure the data is valid

        # Get flow values at specific exceedance percentiles
        q50 = self.get_flow_at_percentile(50)  # EMC A
        q70 = self.get_flow_at_percentile(70)  # EMC B
        q80 = self.get_flow_at_percentile(80)  # EMC C
        q90 = self.get_flow_at_percentile(90)  # EMC D

        return {
            "EMC_A (Natural Flow - Q50)": q50,
            "EMC_B (Slightly Modified - Q70)": q70,
            "EMC_C (Moderately Modified - Q80)": q80,
            "EMC_D (Heavily Modified - Q90)": q90
        }
