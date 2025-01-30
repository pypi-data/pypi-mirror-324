import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

def plot_fdc(flow_duration_curve_df, q_values=None):
    """
    Plots the Flow Duration Curve (FDC) with an optional feature to highlight specific Q-values.

    Parameters:
    - flow_duration_curve_df (pd.DataFrame): A DataFrame with 'Exceedance Probability (%)' and flow values.
    - q_values (list, optional): A list of exceedance percentiles to highlight (e.g., [1, 5, 10, 50, 90, 95]).
                                  If None, the plot is generated without additional markers.
    """
    print("\nPlotting FDC - Available Columns:", flow_duration_curve_df.columns)

    # Ensure correct column selection
    exceedance_probs = flow_duration_curve_df["Exceedance Probability (%)"]
    flow_values = flow_duration_curve_df["Flow (m^3/s)"]

    # Create figure
    plt.figure(figsize=(8, 5))

    # Plot the main FDC curve
    plt.plot(exceedance_probs, flow_values, marker="o", linestyle="-", label="Flow Duration Curve")

    # If q_values is provided, plot markers for each specified Q-value
    if q_values:
        # Interpolation function for flow at specific percentiles
        interp_func = interp1d(exceedance_probs, flow_values, kind="linear", fill_value="extrapolate")

        for q in q_values:
            if min(exceedance_probs) <= q <= max(exceedance_probs):  # Ensure within range
                q_flow = float(interp_func(q))  # Get interpolated flow value
                plt.scatter(q, q_flow, color="red", zorder=3)  # Highlight Q-values with a red marker
                plt.text(q, q_flow, f"Q{q}\n{q_flow:.2f}", fontsize=10, verticalalignment="bottom", horizontalalignment="right")

    # Set axis labels and title
    plt.xlabel("Exceedance Probability (%)")
    plt.ylabel("Flow (m³/s)")
    plt.title("Flow Duration Curve (FDC)")
    
    # Set log scale for y-axis (Flow) - if necessary
    #plt.yscale("log")  
    #plt.gca().invert_xaxis()  # Exceedance probability should decrease from left to right

    # Improve grid visibility
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.legend()

    # Show plot
    plt.show()




def plot_7q10(annual_min_flows):
    """
    Plots the annual minimum 7-day flow trend used in 7Q10 calculation.
    
    Parameters:
    annual_min_flows (pd.Series): A Pandas Series where the index is the year and values are the annual minimum 7-day flows.
    """
    plt.figure(figsize=(8, 5))
    plt.plot(annual_min_flows.index, annual_min_flows.values, marker="o", linestyle="-", label="Annual Min 7-day Flow")
    
    plt.xlabel("Year")
    plt.ylabel("7-day Minimum Flow (m³/s)")
    plt.title("Annual Minimum 7-day Flow (7Q10)")
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_tennant(minimum_flow, optimum_flow):
    """
    Plots a bar chart comparing minimum and optimum flow values from Tennant Method.

    Parameters:
    minimum_flow (float): The minimum flow value from Tennant Method.
    optimum_flow (float): The optimum flow value from Tennant Method.
    """
    plt.figure(figsize=(6, 4))
    plt.bar(["Minimum Flow", "Optimum Flow"], [minimum_flow, optimum_flow], color=["blue", "green"])
    
    plt.ylabel("Flow (m³/s)")
    plt.title("Tennant Method Flow Recommendations")
    plt.grid(axis="y")
    plt.show()
