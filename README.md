# 🔌 The PyPSA Handbook – Code Repository

**Authors**: Neeraj Dhanraj Bokde (www.neerajbokde.in), Carlo Fanara  
**Affiliation**: Renewable and Sustainable Energy Research Center, TII, Abu Dhabi  
**Contact**: neeraj.bokde@tii.ae / neerajdhanraj@gmail.com  

---

## 📖 About the Handbook

_The PyPSA Handbook: Integrated Power System Analysis and Renewable Energy Modeling_ is a comprehensive guide for building, analyzing, and visualizing energy systems using [PyPSA](https://pypsa.org/). The handbook bridges theory with practice through reproducible case studies covering topics such as optimal dispatch, transmission expansion, microgrids, and interactive modeling via Shiny.

This repository contains all code, datasets, and notebooks used in the book, structured chapter-wise.

---

## 📁 Repository Structure

Each chapter folder contains:

- 📘 `.py` or `.ipynb` files for case study code
- 📊 Input datasets if applicable
- 🔧 Scripts for simulation and visualization
- 📱 R Shiny files (Chapter 9 only)

---

## 📚 Chapter Overview

### ✅ **Chapter 4 – Advanced Modeling Techniques in PyPSA**
> Explores time-series modeling, solver configuration, OPF/SCOPF/LOPF workflows with code-driven examples.

**Files**:
- `Chapter_4_CS_1.py`: PyPSA LOPF demonstration
- `Chapter_4_CS_1.ipynb`: Interactive notebook version

---

### ✅ **Chapter 5 – Decarbonization and Renewable Integration**
> Covers CHP modeling, heat pumps, and basic sector coupling via Links and Stores in PyPSA.

**Files**:
- `Chapter_5_CS_1.py` / `.ipynb`: CHP-based heat-power system
- `Chapter_5_CS_2.py` / `.ipynb`: Electrification and demand-supply coordination

---

### ✅ **Chapter 6 – Microgrids and Distributed Energy Resources**
> Designs a rural electrification system with RE, batteries, and demand response.

**Files**:
- `Chapter_6_CS_1.py` / `.ipynb`: Full microgrid model
- `microgrid_input_timeseries_2020.csv`: Hourly input data

---

### ✅ **Chapter 7 – Transmission Planning and Expansion**
> Models a greenfield power system with North–South spatial separation. Co-optimizes generation, storage, and corridor investments.

**Files**:
- `Chapter_7_CS_1.py` / `.ipynb`: Full LOPF and investment planning model

---

### ✅ **Chapter 8 – Reliability and Resilience in Power Systems**
> Stress-tests the Chapter 7 system with multiple disruption scenarios.

**Files**:
- `Chapter_8_CS_1.py` / `.ipynb`: Scenarios A–D (weather, outage, failure)
- `Chapter_8_CS_2.py` / `.ipynb`: Strict SCOPF modeling across contingencies

---

### ✅ **Chapter 9 – Integrating PyPSA with Other Tools**
> Demonstrates PyPSA–Shiny integration with a real-time dispatch simulator.

**Files**:
- `app.R`: R Shiny frontend for interactive modeling
- `pypsa_model.py`: Python backend model executed via `reticulate`
- `Chapter_9.Rproj`: RStudio project for structured development

---

## ⚙️ Software Requirements

- Python 3.8+
- PyPSA v0.21+  
- pandas, numpy, matplotlib
- R (v4.2+) + shiny, reticulate (for Chapter 9)
- Jupyter Notebook (for `.ipynb` files)

---

## 📜 License

This repository is released under the **MIT License**. See `LICENSE` for more details.

---

## 📌 Citation

If you use this repository or book in your research, please cite:

```bibtex
@book{bokde2025pypsa,
  title     = {The PyPSA Handbook: Integrated Power System Analysis and Renewable Energy Modeling},
  author    = {Bokde, Neeraj Dhanraj and Fanara, Carlo},
  year      = {2025},
  publisher = {Elsevier Science},
  isbn      = {9780443266317}
}
