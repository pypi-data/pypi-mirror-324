# cg_r_pathway

`cg_r_pathway` is a comprehensive protein reaction coordinate optimization framework that integrates:

- **Physics-based Modeling:** Residue-specific parameters (mass, charge, ε, σ, hydrophobicity), bonds, angles, nonbonded interactions.
- **Advanced Optimization:** Global path optimization using Adaptive PSO+SA and local refinement using Double-Nested Simulated Annealing (DSA-ASA).
- **Self-Learning ML Model:** A placeholder neural network force field for continuous improvement.
- **Coarse-Graining and Backmapping:** Converting full-atom PDB structures to a coarse-grained model and reconstructing all-atom models via rigid-body transformation.
- **Advanced Visualization:** Reaction coordinate (RMSD vs Energy) plots and 3D path visualization.

## Installation

Clone the repository and install with pip:

```bash
pip install .

