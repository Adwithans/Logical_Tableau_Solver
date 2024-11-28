# First-Order and Propositional Logic Solver

Welcome to the **First-Order and Propositional Logic Solver**, a versatile application designed to solve complex logic problems efficiently. The solver parses problems defined in an input file and outputs solutions seamlessly to an output file.

## Features

- **Solve Logic Problems**: Handles both first-order and propositional logic problems with ease.
- **Configurable Parameters**:
  - Define the **maximum number of propositions**.
  - Specify the **number of predicates**.
  - Limit the **maximum number of constants** for fine-grained control.
- **File-Based Input and Output**:
  - Input problems are read from `input.txt`.
  - Solutions are written to `output.txt` for easy access and review.

## How It Works

1. **Input File (`input.txt`)**:
   - Define your logic problems in this file using a structured format.
   - Examples:
     - Propositional logic: `(P ∧ Q) → R`
     - First-order logic: `∀x (P(x) → Q(x))`

2. **Configuration**:
   - Customize the solver by adjusting the limits for propositions, predicates, and constants in the configuration settings.

3. **Output File (`output.txt`)**:
   - The solver parses and solves all problems from `input.txt` and writes the solutions to `output.txt`.

## Getting Started

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/logic-solver.git
   cd logic-solver
