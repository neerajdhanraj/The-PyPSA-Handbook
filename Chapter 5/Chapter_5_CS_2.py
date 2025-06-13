# ==============================================================================
# Case Study 2: Chapter 5 - Windhaven – Integrating Wind Energy and Storage Units 
#   into the Grid
#
# Authors:   Neeraj Dhanraj Bokde  (www.neerajbokde.in)
#            Carlo Fanara
# Affiliation: Renewable & Sustainable Energy Research Center, TII, Abu Dhabi
# Corresponding author: neeraj.bokde@tii.ae / neerajdhanraj@gmail.com
#
# Description:
#   This script models the impact of adding wind generation and battery storage
#   to a conventionally fossil-based grid using PyPSA. Two networks are compared:
#   (1) baseline fossil system, (2) system with wind farm and battery.
#   Economic, operational, storage, and emissions results are calculated and visualized.
#
# Book Reference:
#   Bokde, N. D., & Fanara, C. (2025). Decarbonization and Renewable Integration.
#   In: The PyPSA Handbook: Integrated Power System Analysis and Renewable 
#   Energy Modeling, Chapter 5. 
#   Publisher: Elsevier Science
#   ISBN: 044326631X, 9780443266317
#
# Software Dependencies:
#   - Python 3.8+
#   - pypsa (v0.21+ recommended)
#   - numpy, pandas, matplotlib
#
# License: MIT
# Version: 1.0
# Date: June 2025
# ==============================================================================

import pypsa
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------
# PART 1: Baseline Fossil Fuel-Based Grid
# -------------------------------------------

# Step 1: Initialize the PyPSA network (baseline)
network_old = pypsa.Network()
network_old.set_snapshots(range(24))

# Step 2: Add a main bus
network_old.add("Bus", "Main Bus")

# Step 3: Add conventional generators (coal and gas)
network_old.add("Generator", "Coal Plant",
                bus="Main Bus",
                p_nom=150,
                marginal_cost=70,
                carrier="coal",
                p_max_pu=[1.0]*24)
network_old.add("Generator", "Gas Plant",
                bus="Main Bus",
                p_nom=100,
                marginal_cost=50,
                carrier="gas",
                p_max_pu=[1.0]*24)

# Step 4: Define a dynamic daily load profile
dynamic_load = [100, 120, 140, 160, 180, 200, 220, 200, 180,
                160, 140, 120, 110, 100, 110, 120, 140, 160,
                180, 200, 220, 200, 180, 140]
network_old.add("Load", "City Load", bus="Main Bus", p_set=dynamic_load)

# Step 5: Optimize baseline network
network_old.optimize(solver_name='glpk')

# Step 6: Output baseline cost
print("\n====== Windhaven Fossil Baseline ======")
print(f"Total System Cost (OPEX): {network_old.objective:.2f}")

# -------------------------------------------
# PART 2: Wind and Storage Integration
# -------------------------------------------

# Step 1: Initialize new network
network_new = pypsa.Network()
network_new.set_snapshots(range(24))

# Step 2: Replicate bus structure
network_new.add("Bus", "Main Bus")

# Step 3: Copy fossil generators (ensure robust copy)
for gen in network_old.generators.index:
    gen_data = network_old.generators.loc[gen]
    # If capital_cost column is missing (PyPSA default), set to 0
    capital_cost = gen_data.capital_cost if 'capital_cost' in gen_data.index else 0
    network_new.add("Generator", gen, 
                    bus=gen_data.bus, 
                    p_nom=gen_data.p_nom, 
                    marginal_cost=gen_data.marginal_cost, 
                    capital_cost=capital_cost, 
                    carrier=gen_data.carrier,
                    p_max_pu=[1.0]*24)

# Step 4: Add dynamic load
network_new.add("Load", "City Load", bus="Main Bus", p_set=dynamic_load)

# Step 5: Define wind pattern over 24 hours
wind_pattern = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.85,
                0.8, 0.75, 0.7, 0.65, 0.6, 0.55, 0.5, 0.45,
                0.4, 0.35, 0.3, 0.25, 0.2, 0.15, 0.1, 0.05]

# Step 6: Add wind generator (100 MW, capital and marginal cost)
network_new.add("Generator", "Wind Farm",
                bus="Main Bus",
                p_nom=100,
                capital_cost=600,
                marginal_cost=10,
                carrier="wind",
                p_max_pu=wind_pattern)

# Step 7: Add battery storage unit
network_new.add("StorageUnit", "Battery Storage",
                bus="Main Bus",
                p_nom=40,
                capital_cost=200,
                marginal_cost=0.01,
                efficiency_store=0.95,
                efficiency_dispatch=0.95,
                state_of_charge_initial=0.1)

# Step 8: Optimize new network
network_new.optimize(solver_name='glpk')

# Step 9: Output results (cost, wind use, storage)
print("\n====== Windhaven with Wind and Storage ======")
print(f"Total System Cost (OPEX + CAPEX): {network_new.objective:.2f}")

# -------------------------------------------
# PART 3: Storage Unit Analysis
# -------------------------------------------

print("\nBattery Storage Charging (MW):")
print(network_new.storage_units_t.p_store["Battery Storage"].round(2))

print("\nBattery Storage Discharging (MW):")
print(network_new.storage_units_t.p_dispatch["Battery Storage"].round(2))

print("\nBattery State of Charge (MWh):")
print(network_new.storage_units_t.state_of_charge["Battery Storage"].round(2))

# -------------------------------------------
# PART 4: Generation Dispatch Plots
# -------------------------------------------

# Step 1: Organize data for plotting
hours = range(24)
generation = network_new.generators_t.p
storage_charging = network_new.storage_units_t.p_store["Battery Storage"]
storage_discharging = network_new.storage_units_t.p_dispatch["Battery Storage"]
storage_soc = network_new.storage_units_t.state_of_charge["Battery Storage"]

# Prepare DataFrames
df_generation = pd.DataFrame(generation, index=hours)
df_generation['Storage Discharge'] = storage_discharging  # Show on bar

df_storage = pd.DataFrame({
    'Charging': storage_charging,
    'Discharging': storage_discharging,
    'SOC': storage_soc
}, index=hours)

# Step 2: Plot generation and storage operations
fig, ax1 = plt.subplots(figsize=(15, 7))

# Consistent color codes for generators and storage
color_map = {
    'Coal Plant': 'royalblue',        
    'Gas Plant': 'darkorange',
    'Wind Farm': 'seagreen',          
    'Storage Discharge': 'crimson'    
}

# Plot columns in preferred order
plot_columns = [col for col in ['Coal Plant', 'Gas Plant', 'Wind Farm', 'Storage Discharge'] if col in df_generation.columns]
bar_colors = [color_map[c] for c in plot_columns]

df_generation[plot_columns].plot(
    ax=ax1,
    kind='bar',
    stacked=True,
    width=0.9,
    color=bar_colors
)

ax1.set_title("Power Generation and Storage Operations")
ax1.set_xlabel("Hour")
ax1.set_ylabel("Generation (MW)")
ax1.set_xticks(range(24))
ax1.legend(title="Generation Source", loc='upper left', ncols=2)
ax1.set_ylim(0, 250)
ax1.grid(axis='y', linestyle=':', alpha=0.6)

# Step 3: Overlay storage charging, discharging, SOC on secondary y-axis
ax2 = ax1.twinx()

df_storage['Charging'].plot(
    ax=ax2,
    color='green',
    marker='^',
    linestyle='-',
    linewidth=1.5,
    label='Charging'
)
df_storage['Discharging'].plot(
    ax=ax2,
    color='red',
    marker='v',
    linestyle='-',
    linewidth=1.5,
    label='Discharging'
)
df_storage['SOC'].plot(
    ax=ax2,
    color='blue',
    marker='x',
    linestyle='--',
    linewidth=2,
    label='SOC'
)

ax2.set_ylabel("Storage Charging/Discharging (MW) & SOC (MWh)")
ax2.set_ylim(0, 50)
ax2.legend(title="Storage Ops", loc='upper right', ncols=1)
ax2.grid(axis='y', linestyle=':', alpha=0.4)

plt.tight_layout()
plt.show()

# -------------------------------------------
# PART 5: Cost and Emissions Analysis
# -------------------------------------------

# Step 1: Compute average energy cost
old_total_load = sum(network_old.loads_t.p_set["City Load"])
new_total_load = sum(network_new.loads_t.p_set["City Load"])
old_avg_cost = network_old.objective / old_total_load
new_avg_cost = network_new.objective / new_total_load

print("\n--- Energy Cost Comparison ---")
print(f"Average Energy Cost Before (Fossil): {old_avg_cost:.2f}")
print(f"Average Energy Cost After (Wind+Storage): {new_avg_cost:.2f}")

# Step 2: Assign emission factors and calculate total emissions
emission_factors = {
    "Coal Plant": 0.9,    # tons CO2/MWh
    "Gas Plant": 0.4,
    "Wind Farm": 0
}

def assign_emissions(network, efactors):
    for gen, ef in efactors.items():
        if gen in network.generators.index:
            network.generators.loc[gen, "emission_factor"] = ef

assign_emissions(network_old, emission_factors)
assign_emissions(network_new, emission_factors)

def calculate_total_emissions(network):
    total = 0
    for gen_name, gen_data in network.generators.iterrows():
        generation = network.generators_t.p[gen_name]
        ef = gen_data.get("emission_factor", 0)
        total += sum(generation * ef)
    return total

old_emissions = calculate_total_emissions(network_old)
new_emissions = calculate_total_emissions(network_new)

print("\n--- Emissions Comparison ---")
print(f"Total Emissions Before Integration: {old_emissions:.1f} tons CO2")
print(f"Total Emissions After Integration: {new_emissions:.1f} tons CO2")

# ==============================================================================
# End of Windhaven Case Study Script
# ==============================================================================

