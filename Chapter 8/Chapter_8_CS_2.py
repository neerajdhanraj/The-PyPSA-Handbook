# ==============================================================================
# Case Study 2: Chapter 8 – Security-Constrained Optimal Power Flow (SCOPF)
#
# Authors:   Neeraj Dhanraj Bokde  (www.neerajbokde.in)
#            Carlo Fanara
# Affiliation: Renewable & Sustainable Energy Research Center, TII, Abu Dhabi
# Corresponding author: neeraj.bokde@tii.ae / neerajdhanraj@gmail.com
#
# Description:
#   This script implements the SCOPF case study from Chapter 8
#   ("Reliability and Resilience in Power Systems") of The PyPSA Handbook.
#   A 5-bus network is modeled and solved under normal conditions using standard
#   Optimal Power Flow (OPF). A series of N-1 contingency scenarios are introduced,
#   each representing an outage of one transmission line. For each contingency,
#   the network is re-optimized to evaluate operational feasibility and resilience.
#   The maximum generator dispatch across all scenarios is computed to derive a
#   conservative dispatch strategy.
#
#   The results are visualized through comparative dispatch bar plots and
#   summarized in terms of cost and unserved energy. This case highlights how
#   strict SCOPF constraints shape operational planning and provide insights
#   into vulnerability, flexibility, and economic trade-offs under uncertainty.
#
# Book Reference:
#   Bokde, N. D., & Fanara, C. (2025). Reliability and Resilience in Power Systems.
#   In: The PyPSA Handbook: Integrated Power System Analysis and Renewable
#   Energy Modeling, Chapter 8.
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

# -----------------------------
# 1. Create Base Network
# -----------------------------
n = pypsa.Network()
n.set_snapshots(pd.date_range("2025-01-01", periods=1, freq="h"))

# Add 5 buses
for i in range(5):
    n.add("Bus", f"Bus {i}", carrier="AC")

# Add generators (wind, gas, CHP, diesel)
n.add("Generator", "G0", bus="Bus 0", p_nom=100, marginal_cost=0, carrier="wind")
n.add("Generator", "G1", bus="Bus 1", p_nom=80, marginal_cost=50, carrier="gas")
n.add("Generator", "G2", bus="Bus 2", p_nom=40, marginal_cost=40, carrier="chp")
n.add("Generator", "G3", bus="Bus 3", p_nom=100, marginal_cost=200, carrier="diesel")

# Add loads
n.add("Load", "Load1", bus="Bus 1", p_set=50)
n.add("Load", "Load2", bus="Bus 2", p_set=30)
n.add("Load", "Load3", bus="Bus 3", p_set=40)
n.add("Load", "Load4", bus="Bus 4", p_set=80)

# Add transmission lines (loop + radial)
line_params = dict(carrier="AC", x=0.1, r=0.01, s_nom=100)
n.add("Line", "Line_0_1", bus0="Bus 0", bus1="Bus 1", **line_params)
n.add("Line", "Line_1_2", bus0="Bus 1", bus1="Bus 2", **line_params)
n.add("Line", "Line_2_3", bus0="Bus 2", bus1="Bus 3", **line_params)
n.add("Line", "Line_3_0", bus0="Bus 3", bus1="Bus 0", **line_params)
n.add("Line", "Line_1_4", bus0="Bus 1", bus1="Bus 4", **line_params)

# Add high-cost unserved generators at each bus
for i in range(5):
    n.add("Generator", f"Unserved_{i}", bus=f"Bus {i}", p_nom=1e4, marginal_cost=10000, carrier="unserved")

# -----------------------------
# 2. Solve Base OPF & Save to Disk
# -----------------------------
n.optimize(solver_name="glpk")
ofp_dispatch = n.generators_t.p.copy()
ofp_cost = n.objective
n.export_to_netcdf("base_network.nc")

# -----------------------------
# 3. SCOPF Simulation: Outage each line
# -----------------------------
contingency_lines = ["Line_0_1", "Line_1_4", "Line_1_2", "Line_2_3", "Line_3_0"]
scopf_dispatches = []
scopf_costs = []
scopf_unserved = []

for line in contingency_lines:
    m = pypsa.Network("base_network.nc")
    m.lines.at[line, "s_nom"] = 0  # outage the line

    for bus in m.buses.index:
        if f"Unserved_{bus}" not in m.generators.index:
            m.add("Generator", f"Unserved_{bus}", bus=bus, p_nom=1e4, marginal_cost=10000, carrier="unserved")

    status = m.optimize(solver_name="glpk")
    if m.objective is None:
        print(f"Infeasible for outage: {line}")
        continue

    scopf_dispatches.append(m.generators_t.p)
    scopf_costs.append(m.objective)
    unserved_sum = m.generators_t.p.filter(like="Unserved").sum(axis=1).values[0]
    scopf_unserved.append(unserved_sum)

# Conservative dispatch: max output needed across all feasible SCOPF cases
scopf_dispatch = pd.concat(scopf_dispatches).groupby(level=0).max() if scopf_dispatches else ofp_dispatch.copy()

# -----------------------------
# 4. Plot OPF vs. SCOPF Dispatch
# -----------------------------
ofp_dispatch["type"] = "Base OPF"
scopf_dispatch["type"] = "Strict SCOPF"
ofp_dispatch.columns = ofp_dispatch.columns.astype(str)
scopf_dispatch.columns = scopf_dispatch.columns.astype(str)

dispatch_all = pd.concat([ofp_dispatch, scopf_dispatch])
dispatch_all = dispatch_all.reset_index().melt(id_vars=["snapshot", "type"], 
                                               var_name="Generator", 
                                               value_name="Dispatch")

plt.figure(figsize=(7, 4.5))
generators = ["G0", "G1", "G2", "G3"]
colors = {"Base OPF": "#4575b4", "Strict SCOPF": "#d73027"}
hatch = {"Base OPF": "//", "Strict SCOPF": ""}

for i, gen in enumerate(generators):
    for j, mode in enumerate(["Base OPF", "Strict SCOPF"]):
        val = dispatch_all[(dispatch_all["Generator"] == gen) & (dispatch_all["type"] == mode)]["Dispatch"].values[0]
        offset = -0.18 if mode == "Base OPF" else 0.18
        plt.bar(i + offset, val, width=0.36, 
                color=colors[mode], 
                hatch=hatch[mode], 
                edgecolor="k", 
                label=mode if i == 0 else None)

plt.xticks(range(len(generators)), generators, fontsize=12)
plt.ylabel("Dispatch (MW)", fontsize=12)
plt.title("Generator Dispatch: Base OPF vs. Strict SCOPF", fontsize=12, pad=12)
plt.legend(fontsize=12, frameon=False)
plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()

# -----------------------------
# 5. Print Summary Stats
# -----------------------------
print("Base OPF cost:", round(ofp_cost, 2))
print("Average SCOPF contingency cost:", round(np.mean(scopf_costs), 2))
print("Worst-case SCOPF contingency cost:", round(np.max(scopf_costs), 2))
print("Average unserved energy (MW) in SCOPF cases:", round(np.mean(scopf_unserved), 2))
print("Max unserved energy (MW) in SCOPF cases:", round(np.max(scopf_unserved), 2))

# ==============================================================================
# End of Security-Constrained Optimal Power Flow (SCOPF) Case Study (Chapter 8)
# ==============================================================================
