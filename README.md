# The PyPSA Handbook – Code Repository

**Authors**: Dr. Neeraj Dhanraj Bokde (www.neerajbokde.in) and Dr. Carlo Fanara

**Affiliation**: Renewable and Sustainable Energy Research Center, Technology Innovation Institute (TII), Abu Dhabi

**Contact**: [neeraj.bokde@tii.ae](mailto:neeraj.bokde@tii.ae) | [neerajdhanraj@gmail.com](mailto:neerajdhanraj@gmail.com)

## Overview

*The PyPSA Handbook: Integrated Power System Analysis and Renewable Energy Modeling* is a comprehensive reference for modeling, simulation, and optimization of power systems using [PyPSA](https://pypsa.org/). This repository provides all supplementary materials for the book, including reproducible code, input datasets, and visualizations for the case studies discussed in each chapter.

The materials are structured to support both self-paced learning and formal teaching, and may be used in conjunction with the published text to implement and extend energy system models using open-source tools.

## Repository Structure

The repository is organized by chapter. Each folder contains:

* Python scripts (`.py`) and Jupyter notebooks (`.ipynb`) for case studies
* Input datasets (`.csv`, where applicable)
* Supporting scripts for simulation and visualization
* R Shiny files for the interactive application in Chapter 9

All scripts are documented and correspond directly to specific case studies described in the book.

## Chapter Index

### Chapter 4 – Advanced Modeling Techniques in PyPSA

Time series modeling, solver configuration, and OPF/SCOPF/LOPF workflows

**Files**: `Chapter_4_CS_1.py`, `Chapter_4_CS_1.ipynb`

### Chapter 5 – Decarbonization and Renewable Integration

Sector coupling, combined heat and power, and demand-supply balancing

**Files**: `Chapter_5_CS_1.py`, `Chapter_5_CS_2.py`, and notebook variants

### Chapter 6 – Microgrids and Distributed Energy Resources

Rural electrification with renewables, storage systems, and demand response

**Files**: `Chapter_6_CS_1.py`, `microgrid_input_timeseries_2020.csv`

### Chapter 7 – Transmission Planning and Expansion

Spatial transmission corridor planning with investment co-optimization

**Files**: `Chapter_7_CS_1.py`, `Chapter_7_CS_1.ipynb`

### Chapter 8 – Reliability and Resilience in Power Systems

Stress-testing and security-constrained optimization scenarios

**Files**: `Chapter_8_CS_1.py`, `Chapter_8_CS_2.py`, and notebook variants

### Chapter 9 – Integrating PyPSA with Other Tools

Interactive modeling interface using R, Shiny, and Python integration

**Files**: `app.R`, `pypsa_model.py`, `Chapter_9.Rproj`

## Software Requirements

To execute the examples in this repository, the following software is recommended:

* Python 3.8 or later
* PyPSA (version 0.21 or later)
* Required Python packages: `numpy`, `pandas`, `matplotlib`, `pyomo`, `linopy`
* R 4.2 or later (for Chapter 9) with packages: `shiny`, `reticulate`
* Jupyter Notebook (for interactive notebooks)

Environment setup instructions are detailed in Chapter 2 of the book.

## License

This repository is licensed under the **MIT License**. See the `LICENSE` file for details.

## Citation

If you use this repository or the book in your academic or professional work, please cite as follows:

```bibtex
@book{bokde2025pypsa,
  title     = {The PyPSA Handbook: Integrated Power System Analysis and Renewable Energy Modeling},
  author    = {Bokde, Neeraj Dhanraj and Fanara, Carlo},
  year      = {2025},
  publisher = {Elsevier Science},
  isbn      = {9780443266317}
}
```


