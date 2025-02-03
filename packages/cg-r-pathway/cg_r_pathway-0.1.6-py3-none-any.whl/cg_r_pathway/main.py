#!/usr/bin/env python3
"""
Entry point for cg_r_pathway when run as a module.

Usage:
    python -m cg_r_pathway --bound A.pdb --unbound B.pdb --steps 40
"""

from cg_r_pathway.cli import main

if __name__ == '__main__':
    main()
