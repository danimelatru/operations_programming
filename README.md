# Hybrid Flow Shop Scheduling Optimization

This repository contains a Python project for solving the **Hybrid Flow Shop Scheduling Problem (HFSP)**. The primary objective of the implemented algorithms is to find an optimal or near-optimal job sequence to **minimize the total weighted tardiness ($\sum w_j T_j$)**.

The project implements, compares, and evaluates a variety of algorithms, ranging from simple dispatching rules to more complex metaheuristics.

## Algorithms Implemented

The solution is approached using three categories of algorithms, which are benchmarked against each other:

### 1. Dispatching Rules
Simple rules used to prioritize jobs:
* **EDD (Earliest Due Date)**
* **LPT (Longest Processing Time)**
* **WSPT (Weighted Shortest Processing Time)**

### 2. Constructive Heuristics
More advanced heuristics to build a complete solution iteratively:
* **MS (Minimum Slack)**
* **CI (Cheapest Insertion)**
* **ATC (Apparent Tardiness Cost)**

### 3. Metaheuristics
High-level optimization algorithms used to find high-quality solutions in a large search space:
* **Iterated Greedy (IG)**: A metaheuristic that iteratively destructs and reconstructs solutions.
* **Hybrid Genetic Algorithm (GA)**: A population-based algorithm that mimics natural selection.

---

## Workflow

The main execution script (`Main.py`) runs a comprehensive benchmark:

1.  **Instance Generation**: It generates 30 test instances with varying job sizes (10, 20, and 30 jobs).
2.  **Algorithm Execution**: For *each* instance, it runs all nine algorithms (3 dispatching rules, 3 heuristics, 2 metaheuristics).
3.  **Benchmarking**: It compares the performance ($\sum w_j T_j$) of all algorithms within their respective categories.
4.  **Result Storage**: All results, including the best algorithm, the best objective value, and the final job sequence, are compiled and saved to an Excel file (`Datos_PO.xlsx`) for analysis.

---

## 📂 Repository Structure

.
├── Main.py                     # Main script to run the full experiment
├── FlowShopHibrido.py          # Class defining the HFS environment and problem logic
├── Generador_de_instancias.py  # Utility to generate test problems
├── Dispatching_rules.py        # Module for EDD, LPT, WSPT
├── Heuristicas_constructivas.py  # Module for MS, CI, ATC
├── Metaheuristicas.py          # Module for Iterated Greedy (IG) and Genetic Algorithm (GA)
├── Datos_PO.xlsx               # Input data (also used for output results)
├── Analisis_def.xlsx           # Excel file for final analysis
├── Comparaciones.xlsx          # Excel file for algorithm comparisons
└── Correcciones.pdf            # Project documentation or problem statement

---

## 🛠️ How to Use

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/danimelatru/operations_programming.git](https://github.com/danimelatru/operations_programming.git)
    cd operations_programming
    ```

2.  **Install dependencies:**
    This project requires `pandas` to handle Excel files.
    ```bash
    pip install pandas
    ```

3.  **Run the experiment:**
    ```bash
    python Main.py
    ```
    The script will print the progress for each instance to the console and save the final results in the Excel files.
