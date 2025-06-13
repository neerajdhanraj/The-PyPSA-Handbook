# ==============================================================================
# Case Study: Chapter 4 - Time Series and Snapshots for Renewable Integration 
#
# Authors:   Neeraj Dhanraj Bokde  (www.neerajbokde.in)
#            Carlo Fanara          
# Affiliation: Renewable & Sustainable Energy Research Center, TII, Abu Dhabi
# Corresponding author: neeraj.bokde@tii.ae/neerajdhanraj@gmail.com
#
# Description:
#   This script models a two-bus power system using PyPSA, illustrating how to
#   represent time-varying renewable generation (solar, wind) and flexible gas
#   backup using hourly snapshots and time series.
#   Dispatch is solved using Linear Optimal Power Flow (LOPF), and results
#   are visualized for teaching and benchmarking purposes.
#
# Book Reference:
#   Bokde, N. D., & Fanara, C. (2025). Advanced Modeling Techniques in PyPSA.
#   In: The PyPSA Handbook: Integrated Power System Analysis and Renewable 
#   Energy Modeling, Chapter 4.
#   Publisher	Elsevier Science
#   ISBN	044326631X, 9780443266317
#
# Software Dependencies:
#   - Python 3.8+
#   - pypsa (v0.21+ recommended)
#   - numpy, pandas, matplotlib
#
# License: MIT
#
# Version: 1.0
# Date: June 2025
# ==============================================================================

import pypsa
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---------------------
# Step 1: Network Setup
# ---------------------
# Create the PyPSA network
network = pypsa.Network()

# Add buses
network.add("Bus", "Bus 1", carrier="AC")
network.add("Bus", "Bus 2", carrier="AC")

# Add transmission line
network.add("Line", "Line 1",
            bus0="Bus 1", bus1="Bus 2",
            x=0.1, r=0.01, s_nom=200, carrier="AC")

# Add static load to Bus 2
network.add("Load", "Load 1", bus="Bus 2", p_set=50)

# Add generators to Bus 1 (gas, solar, wind)
network.add("Generator", "Natural Gas Plant",
            bus="Bus 1", p_nom=40,
            carrier="gas", marginal_cost=50)
network.add("Generator", "Solar Plant",
            bus="Bus 1", p_nom=200,
            carrier="solar", marginal_cost=0)
network.add("Generator", "Wind Farm",
            bus="Bus 1", p_nom=120,
            carrier="wind", marginal_cost=0)

# --------------------------------------------------
# Step 2: Define Hourly Snapshots (Time Resolution)
# --------------------------------------------------
# Simulate 24 hours at hourly intervals
hours = pd.date_range('2024-01-01 00:00', '2024-01-01 23:00', freq='h')
network.set_snapshots(hours)

# ----------------------------------------
# Step 3: Assign Time Series (Availability)
# ----------------------------------------
# Synthetic solar profile: sinusoidal, peaks at midday
angle_range = np.linspace(-np.pi/2, 3*np.pi/2, len(hours))
solar_output = np.maximum(0, np.sin(angle_range))  # [0, 1]

# Synthetic wind profile: random, 0.2-1.0 p.u.
np.random.seed(0)  # Reproducibility
wind_output = np.random.normal(0.5, 0.2, len(hours))
wind_output = np.clip(wind_output, 0.2, 1.0)

# Assign per-unit availabilities (p_max_pu) for each generator
network.generators_t.p_max_pu = pd.DataFrame({
    'Solar Plant': solar_output,
    'Wind Farm': wind_output
}, index=hours)

# -------------------------------------------------
# Step 4: Solve LOPF (Linear Optimal Power Flow)
# -------------------------------------------------
network.optimize(network.snapshots, solver_name='glpk')

# --------------------------------------------
# Step 5: Extract and Print Dispatch Results
# --------------------------------------------
results = network.generators_t.p
print("Generator Dispatch (MW):")
print(results)

# ---------------------------------
# Step 6: Plot Results for Analysis
# ---------------------------------
plt.figure(figsize=(12, 6))
plt.plot(results.index, results["Natural Gas Plant"], label='Natural Gas Plant')
plt.plot(results.index, results["Solar Plant"], label='Solar Plant')
plt.plot(results.index, results["Wind Farm"], label='Wind Farm')
plt.xlabel('Time')
plt.ylabel('Power Output (MW)')
plt.title('Generator Dispatch Over 24 Hours')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# ==============================================================================
# End of Case Study: Chapter 4
# ==============================================================================
