#!/usr/bin/env python3
"""
Command-Line Interface for cg_r_pathway.

Usage:
    cg-r-pathway --bound A.pdb --unbound B.pdb --steps 40
"""

import argparse
from cg_r_pathway import core

def main():
    parser = argparse.ArgumentParser(
        description="cg_r_pathway: Protein Reaction Coordinate Optimization Framework"
    )
    parser.add_argument('--bound', required=True,
                        help="Path to the folded (bound) PDB file, e.g., A.pdb")
    parser.add_argument('--unbound', required=True,
                        help="Path to the unfolded (unbound) PDB file, e.g., B.pdb")
    parser.add_argument('--steps', type=int, default=40,
                        help="Number of interpolation steps (default: 40)")
    args = parser.parse_args()

    # Call the main workflow from core.py
    core.main(bound_pdb=args.bound, unbound_pdb=args.unbound, steps=args.steps)

if __name__ == '__main__':
    main()
