import pypsa
import pandas as pd

def run_pypsa_model(demand_Copenhagen, demand_Aarhus, demand_Aalborg,
                    capacity_wind, cost_wind,
                    capacity_solar, cost_solar,
                    capacity_gas, cost_gas):
    # Create a network and define one snapshot (time step)
    network = pypsa.Network()
    network.set_snapshots([0])
    
    # Define buses with coordinates (approximate lat/lon for Danish cities)
    buses = {
        'Copenhagen': {'lat': 55.6761, 'lon': 12.5683},
        'Aarhus': {'lat': 56.1629, 'lon': 10.2039},
        'Aalborg': {'lat': 57.0488, 'lon': 9.9217}
    }
    
    for bus, coords in buses.items():
        network.add("Bus", bus, x=coords['lon'], y=coords['lat'])
    
    # Add generators with user-defined capacities (MW) and marginal costs (€/MWh)
    # Copenhagen: Wind generator
    network.add("Generator", "wind_Copenhagen",
                bus="Copenhagen",
                p_nom=capacity_wind,
                marginal_cost=cost_wind,
                carrier="wind",
                p_max_pu=1.0)
    
    # Aarhus: Solar generator
    network.add("Generator", "solar_Aarhus",
                bus="Aarhus",
                p_nom=capacity_solar,
                marginal_cost=cost_solar,
                carrier="solar",
                p_max_pu=1.0)
    
    # Aalborg: Gas generator
    network.add("Generator", "gas_Aalborg",
                bus="Aalborg",
                p_nom=capacity_gas,
                marginal_cost=cost_gas,
                carrier="gas",
                p_max_pu=1.0)
    
    # Add loads at each bus (load provided in MW)
    network.add("Load", "load_Copenhagen",
                bus="Copenhagen",
                p_set=demand_Copenhagen)
    network.add("Load", "load_Aarhus",
                bus="Aarhus",
                p_set=demand_Aarhus)
    network.add("Load", "load_Aalborg",
                bus="Aalborg",
                p_set=demand_Aalborg)
    
    # Define transmission lines connecting the nodes (using a simplified impedance factor)
    lines = [
        ("Copenhagen", "Aarhus", 150),  # (from, to, length in km)
        ("Aarhus", "Aalborg", 100),
        ("Aalborg", "Copenhagen", 200)
    ]
    
    for bus1, bus2, length in lines:
        network.add("Line", f"{bus1}_{bus2}",
                    bus0=bus1,
                    bus1=bus2,
                    x=length * 0.01,
                    s_nom=100)
    
    # Solve the linear optimal power flow problem.
    # network.optimize(network.snapshots,)
    network.optimize(solver_name="glpk")
    
    # Retrieve results: generator outputs and line flows.
    results = {}
    results["generators"] = network.generators_t.p.iloc[0].to_dict()
    results["lines"] = network.lines_t.p0.iloc[0].to_dict()
    results["buses"] = buses
    return results

# # For testing the module independently.
# if __name__ == "__main__":
#     # Example test parameters:
#     res = run_pypsa_model(
#         demand_Copenhagen=50, demand_Aarhus=50, demand_Aalborg=50,
#         capacity_wind=100, cost_wind=20,
#         capacity_solar=80, cost_solar=25,
#         capacity_gas=120, cost_gas=50
#     )
#     print(res)
