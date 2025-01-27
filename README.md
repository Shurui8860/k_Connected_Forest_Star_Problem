# $\kappa$ connected Forest Star_Problem

This project implements a system that integrates data management, modeling, and visualization for solving optimization problems using the CPLEX environment. Below is an overview of the project's structure and functionality.

## Table of Contents
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Modules Overview](#modules-overview)
  - [plot_class.py](#plot_classpy)
  - [callback.py](#callbackpy)
  - [main.py](#mainpy)
  - [data_class.py](#data_classpy)
  - [model_class.py](#model_classpy)
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
This module contains utility functions for visualization:
- **Functions**:
  - `plot_solution`: Plots the solution of the optimization problem.
  - `create_network`: Generates a network visualization.
  - `plot_graph`: Creates a graph representation of the data.
- **Note**: This module lacks a detailed docstring.

### `callback.py`
Defines callback classes for integrating custom logic with the CPLEX environment:
- **Classes**:
  - `Callback_lazy`: A callback for lazy constraint generation.
  - `Callback_user`: A callback for user-defined logic.
  - `HeuristicsCallback`: Implements heuristics-based callbacks.
- **Functions**:
  - `__init__`: Initializes the callbacks.
  - `__call__`: Executes the callback logic.

### `main.py`
The main entry point of the project:
- **Purpose**:
  - Orchestrates the execution of the program by importing and calling functions from other modules.
- **Note**: The module does not contain any classes or functions.

### `data_class.py`
Manages data creation and manipulation:
- **Class**:
  - `Data`: Handles data storage and preprocessing.
- **Functions**:
  - `__init__`: Initializes the data object.
  - `create_data`: Creates and processes the data.
- **Note**: This module lacks a detailed docstring.

### `model_class.py`
Defines the optimization model:
- **Class**:
  - `KfspModel`: Implements the optimization logic.
- **Functions**:
  - `__init__`: Initializes the model with required parameters.
  - `solve`: Solves the optimization problem.
- **Note**: This module lacks a detailed docstring.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add a meaningful message"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

