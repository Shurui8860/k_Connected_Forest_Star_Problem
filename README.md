# $\kappa$ connected Forest Star Problem

This project implements a system that integrates data management, optimization modeling, and visualization for solving complex optimization problems using the CPLEX environment. It utilizes Python and the `docplex` library to build and solve optimization models, along with custom visualization tools to interpret results.

## Table of Contents

- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Modules Overview](#modules-overview)
  - [plot\_class.py](#plot_classpy)
  - [callback.py](#callbackpy)
  - [main.py](#mainpy)
  - [data\_class.py](#data_classpy)
  - [model\_class.py](#model_classpy)
- [Contributing](#contributing)
- [License](#license)

## Project Structure

```
.
├── plot_class.py     # Functions for plotting solutions and graphs
├── callback.py       # Callback classes for CPLEX optimization
├── main.py           # Entry point of the program
├── data_class.py     # Data management and creation
├── model_class.py    # Optimization model and solving logic
```

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd <project-directory>
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the main script to execute the program:

```bash
python main.py
```

## Modules Overview

### `plot_class.py`

This module provides utility functions to visualize optimization results. It helps in interpreting the data and solution through graphs and plots.

- **Functions**:
  - `plot_solution(data, model)`: Plots the solution of the optimization problem, including routes and assignments.
  - `create_network(data, model)`: Generates a network graph representing the relationships between nodes and edges.
  - `plot_graph(data, model)`: Visualizes the graph with nodes, edges, and their attributes.

### `callback.py`

Implements callback classes to enhance the optimization process by adding custom constraints and heuristics during the solving phase.

- **Classes**:
  - `Callback_lazy`: Handles lazy constraint generation to ensure solutions meet specified conditions.
  - `Callback_user`: Applies user-defined constraints dynamically during the solving process.
  - `HeuristicsCallback`: Incorporates heuristic methods to improve solution quality and reduce solving time.

### `main.py`

The entry point of the program, orchestrating data generation, model setup, and solution visualization.

- **Key Workflow**:
  1. Creates data using the `Data` class.
  2. Initializes the `KfspModel` optimization model.
  3. Registers callbacks (`Callback_lazy`, `Callback_user`).
  4. Solves the model and visualizes the results using `plot_graph`.

### `data_class.py`

Handles data creation and preprocessing for the optimization model.

- **Class**:
  - `Data(n, m)`: Manages the set of roots and customers, their locations, and edge attributes.
- **Methods**:
  - `create_data(width, const, seed)`: Generates random locations for roots and customers, calculates distance matrices, and defines edges.

### `model_class.py`

Defines and solves the optimization model using the `docplex` library.

- **Class**:
  - `KfspModel(name, data, k)`: Represents the optimization problem with decision variables, constraints, and the objective function.
- **Methods**:
  - `__init__`: Initializes the model with the data and connectedness constraints.
  - `solve(log)`: Solves the optimization problem and retrieves the solution.



## License

This project is licensed under the MIT License. See the LICENSE file for more details.

