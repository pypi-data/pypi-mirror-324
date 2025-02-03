#!/usr/bin/env python3
"""
cg_r_pathway.core

This module contains the full simulation logic for the protein reaction coordinate optimization framework.
It includes:
- PDB parsing and coarse-graining functions.
- Energy function definitions (bonds, angles, nonbonded, quantum hotspot).
- Global optimization (Adaptive PSO+SA) and local refinement (DSA-ASA).
- Visualization functions.
- Backmapping functions.
- The main workflow function.
"""

import os, math
import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.autograd as autograd
from numba import njit
from math import erf
from copy import deepcopy
import multiprocessing

# --- Section 1: Constants & Conversions ---
AVOGADRO          = 6.02214076e23
BOLTZMANN         = 1.380649e-23
AMU_TO_KG         = 1.66053906660e-27
J_TO_KCAL_PER_MOL = AVOGADRO / 4184.0

@njit
def my_erfc(x):
    return 1.0 - erf(x)

# --- Section 2: Residue Parameters & Hydrophobicity Scale ---
RESIDUE_PARAMS = {
    "ALA": {"mass":  89.0, "charge":  0.00, "epsilon": 0.2, "sigma": 4.5},
    "ARG": {"mass": 174.2, "charge": +0.15, "epsilon": 0.25, "sigma": 5.0},
    "ASN": {"mass": 132.1, "charge": -0.10, "epsilon": 0.2, "sigma": 4.7},
    "ASP": {"mass": 133.1, "charge": -0.15, "epsilon": 0.25, "sigma": 4.8},
    "CYS": {"mass": 121.2, "charge": -0.05, "epsilon": 0.25, "sigma": 4.7},
    "GLN": {"mass": 146.2, "charge": -0.10, "epsilon": 0.2, "sigma": 4.7},
    "GLU": {"mass": 147.1, "charge": -0.15, "epsilon": 0.25, "sigma": 4.8},
    "GLY": {"mass": 75.07, "charge":  0.00, "epsilon": 0.2, "sigma": 4.5},
    "HIS": {"mass": 155.2, "charge": +0.10, "epsilon": 0.25, "sigma": 4.8},
    "ILE": {"mass": 131.2, "charge":  0.00, "epsilon": 0.2, "sigma": 4.8},
    "LEU": {"mass": 131.2, "charge":  0.00, "epsilon": 0.2, "sigma": 4.8},
    "LYS": {"mass": 146.2, "charge": +0.15, "epsilon": 0.25, "sigma": 5.0},
    "MET": {"mass": 149.2, "charge":  0.00, "epsilon": 0.25, "sigma": 4.8},
    "PHE": {"mass": 165.2, "charge":  0.00, "epsilon": 0.3, "sigma": 5.0},
    "PRO": {"mass": 115.1, "charge":  0.00, "epsilon": 0.2, "sigma": 4.5},
    "SER": {"mass": 105.1, "charge": -0.05, "epsilon": 0.2, "sigma": 4.6},
    "THR": {"mass": 119.1, "charge": -0.05, "epsilon": 0.2, "sigma": 4.7},
    "TRP": {"mass": 204.2, "charge":  0.00, "epsilon": 0.3, "sigma": 5.1},
    "TYR": {"mass": 181.2, "charge":  0.00, "epsilon": 0.3, "sigma": 5.0},
    "VAL": {"mass": 117.1, "charge":  0.00, "epsilon": 0.2, "sigma": 4.8},
}
for res in RESIDUE_PARAMS:
    RESIDUE_PARAMS[res]["sigma"] /= 10.0

HYDRO_SCALE = {
    "ALA":0.5, "VAL":0.7, "ILE":0.8, "LEU":0.8, "MET":0.7,
    "PHE":1.0, "TYR":0.9, "TRP":1.0,
    "ARG":0.2, "LYS":0.2, "ASP":0.1, "GLU":0.1,
    "SER":0.4, "THR":0.4, "ASN":0.3, "GLN":0.3, "PRO":0.5,
    "HIS":0.6, "CYS":0.6, "GLY":0.5
}

# --- Section 3: PDB Parsing and CG Conversion Functions ---
def parse_pdb_as_cg(file_path):
    positions = []
    residue_names = []
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith("ATOM") and line[12:16].strip() == "CA":
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])
                res_name = line[17:20].strip()
                positions.append([x, y, z])
                residue_names.append(res_name)
    return np.array(positions), residue_names

def parse_full_pdb(pdb_file):
    residues_data = []
    current_atoms = []
    current_ca_pos = None
    last_res_seq = None
    def store_res(res_seq, atoms, ca):
        if atoms:
            residues_data.append({'res_id': res_seq, 'atoms': atoms.copy(), 'ca_pos': ca})
    with open(pdb_file, 'r') as f:
        for line in f:
            if not line.startswith(("ATOM", "HETATM")):
                continue
            res_seq_str = line[22:26].strip()
            try:
                res_seq = int(res_seq_str)
            except:
                continue
            atom_name = line[12:16].strip()
            x = float(line[30:38])
            y = float(line[38:46])
            z = float(line[46:54])
            if last_res_seq is None or res_seq != last_res_seq:
                if last_res_seq is not None:
                    store_res(last_res_seq, current_atoms, current_ca_pos)
                current_atoms = []
                current_ca_pos = None
                last_res_seq = res_seq
            current_atoms.append({'line': line, 'x': x, 'y': y, 'z': z, 'atom_name': atom_name})
            if atom_name == "CA":
                current_ca_pos = np.array([x, y, z], dtype=float)
    if current_atoms:
        store_res(last_res_seq, current_atoms, current_ca_pos)
    for res in residues_data:
        if res['ca_pos'] is None:
            raise ValueError(f"No CA found in residue {res['res_id']}.")
    return residues_data

def parse_pdb_to_cg(file_path):
    positions, residue_names = parse_pdb_as_cg(file_path)
    charges, masses, epsilons, sigmas, hydrophobicities = [], [], [], [], []
    for res in residue_names:
        if res not in RESIDUE_PARAMS:
            raise ValueError(f"Residue '{res}' not found in RESIDUE_PARAMS.")
        params = RESIDUE_PARAMS[res]
        charges.append(params["charge"])
        masses.append(params["mass"])
        epsilons.append(params["epsilon"])
        sigmas.append(params["sigma"])
        hydrophobicities.append(HYDRO_SCALE[res])
    return positions, np.array(charges), np.array(masses), np.array(epsilons), np.array(sigmas), np.array(hydrophobicities)

def format_pdb_line(orig_line, newx, newy, newz):
    return (orig_line[:30] + f"{newx:8.3f}{newy:8.3f}{newz:8.3f}" + orig_line[54:])

def write_frame_pdb(filename, residues_data):
    with open(filename, 'w') as fp:
        for res in residues_data:
            for atom in res['atoms']:
                new_line = format_pdb_line(atom['line'], atom['x'], atom['y'], atom['z'])
                fp.write(new_line)
        fp.write("END\n")

# --- Section 4: Energy Functions ---
def compute_bond_energy_and_forces(positions, bond_list, k_bond=300.0, r0=4.0):
    E = 0.0
    forces = np.zeros_like(positions)
    for (i, j) in bond_list:
        diff = positions[i] - positions[j]
        r = np.linalg.norm(diff)
        if r < 1e-12:
            continue
        dr = r - r0
        E += 0.5 * k_bond * dr**2
        fmag = -k_bond * dr
        unit = diff / r
        forces[i] += fmag * unit
        forces[j] -= fmag * unit
    return E, forces

def compute_angle_energy_and_forces(positions, angle_list, k_angle=40.0, theta0=math.radians(120.0)):
    E = 0.0
    forces = np.zeros_like(positions)
    for (i1, i2, i3) in angle_list:
        r1 = positions[i1] - positions[i2]
        r2 = positions[i3] - positions[i2]
        n1 = np.linalg.norm(r1)
        n2 = np.linalg.norm(r2)
        if n1 < 1e-12 or n2 < 1e-12:
            continue
        cos_th = np.dot(r1, r2) / (n1 * n2)
        cos_th = np.clip(cos_th, -1.0, 1.0)
        th = math.acos(cos_th)
        dth = th - theta0
        E += 0.5 * k_angle * dth**2
    return E, forces

def compute_nonbonded_energy_and_forces(positions, charges, pairs_array,
                                          epsilon=0.2, sigma=5.0, alpha=0.3,
                                          debye_length=10.0):
    E = 0.0
    forces = np.zeros_like(positions)
    for pair in pairs_array:
        i, j = pair
        diff = positions[i] - positions[j]
        r = np.linalg.norm(diff)
        if r < 1e-12:
            continue
        sr = sigma / r
        sr6 = sr**6
        sr12 = sr6**2
        E_lj = 4.0 * epsilon * (sr12 - sr6)
        dE_lj_dr = 4.0 * epsilon * (-12.0 * sr12 + 6.0 * sr6) / r
        E_coul = charges[i]*charges[j] * my_erfc(alpha*r) / r * math.exp(-r/debye_length)
        dE_coul_dr = -charges[i]*charges[j] * math.exp(-r/debye_length) * (
                        my_erfc(alpha*r)/r**2 + (2*alpha/np.sqrt(np.pi))*np.exp(-(alpha*r)**2)/r)
        E_pair = E_lj + E_coul
        dE_pair_dr = dE_lj_dr + dE_coul_dr
        fvec = -dE_pair_dr * (diff / r)
        forces[i] += fvec
        forces[j] -= fvec
        E += E_pair
    return E, forces

def total_energy(positions, charges, hydrophobicities, epsilons, sigmas):
    E_total = 0.0
    N = len(positions)
    for i in range(N):
        for j in range(i+1, N):
            rij = positions[j] - positions[i]
            r = np.linalg.norm(rij)
            if r < 3.0 and r > 1e-6:
                epsilon_ij = np.sqrt(epsilons[i] * epsilons[j])
                sigma_ij = (sigmas[i] + sigmas[j]) / 2.0
                inv_r6 = (sigma_ij / r) ** 6
                inv_r12 = inv_r6 ** 2
                LJ = 4 * epsilon_ij * (inv_r12 - inv_r6)
                Coulomb = (charges[i] * charges[j]) / (4 * np.pi * 8.85e-12 * r)
                Hydro = -0.1 * (hydrophobicities[i] * hydrophobicities[j]) / r
                Steric = 5000 if r < 0.3 else 0
                E_total += LJ + Coulomb + Hydro + Steric
    return E_total

def compute_classical_energy_and_forces(positions, cg_system):
    E_bond, f_bond = compute_bond_energy_and_forces(positions, cg_system.bond_list)
    E_angle, f_angle = compute_angle_energy_and_forces(positions, cg_system.angle_list)
    E_nb, f_nb = compute_nonbonded_energy_and_forces(positions, cg_system.charges,
                                                       cg_system.neighbor_list.pairs_array)
    return E_bond + E_angle + E_nb, f_bond + f_angle + f_nb

# --- Section 5: Quantum Hotspot Correction ---
def quantum_hotspot(positions, hotspot_indices=None):
    if not hotspot_indices:
        return 0.0, np.zeros_like(positions)
    A = 0.1
    B = 1.0
    E_corr = 0.0
    f_corr = np.zeros_like(positions)
    for i in range(len(hotspot_indices)):
        for j in range(i+1, len(hotspot_indices)):
            idx_i = hotspot_indices[i]
            idx_j = hotspot_indices[j]
            r_vec = positions[idx_i] - positions[idx_j]
            r = np.linalg.norm(r_vec)
            if r < 1e-6:
                continue
            E_pair = A * np.exp(-B * r)
            E_corr += E_pair
            force_mag = A * B * np.exp(-B * r)
            f_vec = force_mag * (r_vec / r)
            f_corr[idx_i] += f_vec
            f_corr[idx_j] -= f_vec
    return E_corr, f_corr

# --- Section 6: Double-Nested Adaptive Simulated Annealing (DSA-ASA) ---
def double_nested_simulated_annealing(positions, charges, hydrophobicities, epsilons, sigmas,
                                      outer_steps=5, inner_steps=2000):
    best_positions = positions.copy()
    best_energy = total_energy(best_positions, charges, hydrophobicities, epsilons, sigmas)
    for outer in range(outer_steps):
        T_outer = 300 * (0.9 ** outer)
        positions_inner = positions.copy()
        for inner in range(inner_steps):
            T_inner = T_outer * (0.95 ** inner)
            new_positions = positions_inner + np.random.normal(0, 0.1, positions_inner.shape)
            delta_E = total_energy(new_positions, charges, hydrophobicities, epsilons, sigmas) - \
                      total_energy(positions_inner, charges, hydrophobicities, epsilons, sigmas)
            if delta_E < 0 or np.random.rand() < np.exp(-delta_E / (1.38e-23 * T_inner)):
                positions_inner = new_positions
        current_energy = total_energy(positions_inner, charges, hydrophobicities, epsilons, sigmas)
        if current_energy < best_energy:
            best_energy = current_energy
            best_positions = positions_inner.copy()
        print(f"[DSA-ASA] Outer step {outer+1}/{outer_steps}, Energy = {current_energy:.4e}")
    return best_positions

# --- Section 7: Advanced Visualization ---
def plot_reaction_coordinate(trajectory, reference, charges, hydrophobicities, epsilons, sigmas):
    rmsd_values = []
    energy_values = []
    for pos in trajectory:
        rmsd = np.sqrt(np.mean(np.sum((pos - reference)**2, axis=1)))
        rmsd_values.append(rmsd)
        energy_values.append(total_energy(pos, charges, hydrophobicities, epsilons, sigmas))
    plt.figure(figsize=(10,6))
    plt.plot(rmsd_values, energy_values, '-o', color='blue')
    plt.xlabel("Reaction Coordinate (RMSD) (nm)")
    plt.ylabel("Energy (arb. units)")
    plt.title("Reaction Coordinate vs Energy")
    plt.grid()
    plt.show()

def plot_3d_path(folded, unfolded, trajectory, hotspot_indices=None, skip_frames=10):
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
    fig = plt.figure(figsize=(18,6))
    ax1 = fig.add_subplot(131, projection='3d')
    ax1.plot(folded[:,0], folded[:,1], folded[:,2], '-o', color='blue')
    ax1.set_title("Folded (Blue)")
    ax2 = fig.add_subplot(132, projection='3d')
    ax2.plot(unfolded[:,0], unfolded[:,1], unfolded[:,2], '-o', color='red')
    ax2.set_title("Unfolded (Red)")
    ax3 = fig.add_subplot(133, projection='3d')
    steps = trajectory.shape[0]
    step_skip = max(1, steps // skip_frames)
    for s in range(0, steps, step_skip):
        coords = trajectory[s]
        ax3.plot(coords[:,0], coords[:,1], coords[:,2], '-o', color='green', alpha=0.6)
        if hotspot_indices is not None:
            hx = coords[hotspot_indices, 0]
            hy = coords[hotspot_indices, 1]
            hz = coords[hotspot_indices, 2]
            ax3.scatter(hx, hy, hz, color='red', s=50, marker='^', alpha=0.9)
    ax3.set_title("Trajectory (Green) + Hotspots (Red)")
    plt.tight_layout()
    plt.show()

# --- Section 8: Neural Network Force Field (ML Model Placeholder) ---
class CGNet(nn.Module):
    def __init__(self, input_dim, hidden_dim=64):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1)
        )
    def forward(self, x):
        return self.net(x)

class CGNetworkForceField:
    def __init__(self, n_beads, model_path=None):
        in_dim = 3 * n_beads
        self.model = CGNet(in_dim, hidden_dim=64)
        if model_path and os.path.exists(model_path):
            self.model.load_state_dict(torch.load(model_path))
        self.model.eval()
        self.n_beads = n_beads
    def compute_energy_forces(self, positions):
        pos_t = torch.tensor(positions.flatten(), dtype=torch.float32).unsqueeze(0)
        pos_t.requires_grad_(True)
        e_t = self.model(pos_t)
        grad = autograd.grad(e_t, pos_t, grad_outputs=torch.ones_like(e_t), create_graph=False)[0]
        e_val = e_t.item()
        grad_np = grad.detach().numpy().reshape(self.n_beads, 3)
        forces = -grad_np
        return e_val, forces

def update_ml_model(new_data):
    """
    This function is a placeholder for on-the-fly training/updating of the ML model.
    For now, it does nothing.
    """
    # In a full implementation, this function would use 'new_data' to update the model.
    print("ML model update not implemented. Skipping update.")

# --- Section 9: Coarse-Grained System and Neighbor List ---
def flatten_neighbor_list(nested_list):
    pairs = []
    for i, neighs in enumerate(nested_list):
        for j in neighs:
            if j > i:
                pairs.append((i, j))
    return pairs

class NeighborList:
    def __init__(self, cutoff=12.0, skin=1.0):
        self.cutoff = cutoff
        self.skin = skin
        self.build_cut2 = (cutoff + skin) ** 2
        self.verlet_list = None
        self.pairs_array = None
        self.last_positions = None
    def build(self, positions):
        n = len(positions)
        raw_list = [[] for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                diff = positions[i] - positions[j]
                r2 = diff.dot(diff)
                if r2 < self.build_cut2:
                    raw_list[i].append(j)
                    raw_list[j].append(i)
        self.verlet_list = raw_list
        self.pairs_array = np.array(flatten_neighbor_list(raw_list), dtype=np.int64)
        self.last_positions = positions.copy()
    def update(self, positions):
        if self.last_positions is None or np.max(np.linalg.norm(positions - self.last_positions, axis=1)) > 0.5:
            self.build(positions)

def clone_cg_system(template, new_positions):
    new_sys = CGSystem(positions=new_positions.copy(),
                       charges=template.charges,
                       bond_list=template.bond_list,
                       angle_list=template.angle_list,
                       hotspot_indices=template.hotspot)
    new_sys.nn_force = template.nn_force
    new_sys.neighbor_list = template.neighbor_list
    return new_sys

class CGSystem:
    def __init__(self, positions, charges, bond_list, angle_list,
                 hotspot_indices=None, model_path=None):
        self.positions = positions
        self.charges = charges
        self.bond_list = bond_list
        self.angle_list = angle_list
        self.hotspot = hotspot_indices if hotspot_indices is not None else []
        self.neighbor_list = NeighborList(cutoff=12.0, skin=1.0)
        self.neighbor_list.build(positions)
        n_beads = positions.shape[0]
        self.nn_force = CGNetworkForceField(n_beads, model_path=model_path)
        self.k_bond = 300.0
        self.r0 = 4.0
        self.k_angle = 40.0
        self.theta0 = math.radians(120.0)
        self.epsilon = 0.2
        self.sigma = 5.0
        self.alpha = 0.3
    def compute_energy_forces(self):
        E_classical, f_classical = compute_classical_energy_and_forces(self.positions, self)
        e_nn, f_nn = self.nn_force.compute_energy_forces(self.positions)
        e_qm, f_qm = quantum_hotspot(self.positions, self.hotspot)
        E_total = E_classical + e_nn + e_qm
        total_forces = f_classical + f_nn + f_qm
        return E_total, total_forces

def compute_classical_energy_and_forces(positions, cg_system):
    E_bond, f_bond = compute_bond_energy_and_forces(positions, cg_system.bond_list)
    E_angle, f_angle = compute_angle_energy_and_forces(positions, cg_system.angle_list)
    E_nb, f_nb = compute_nonbonded_energy_and_forces(positions, cg_system.charges,
                                                       cg_system.neighbor_list.pairs_array)
    return E_bond + E_angle + E_nb, f_bond + f_angle + f_nb

# --- Section 10: Kinetic Energy & Action Calculation ---
@njit
def kinetic_energy_numba(path, mass_array, dt):
    steps = path.shape[0]
    velocities = (path[1:] - path[:-1]) / dt
    totalKE = 0.0
    mass_kg = mass_array * AMU_TO_KG
    for s in range(steps - 1):
        KE_j = 0.0
        for i in range(mass_array.shape[0]):
            vx, vy, vz = velocities[s, i]
            vsq = vx*vx + vy*vy + vz*vz
            KE_j += 0.5 * mass_kg[i] * vsq
        KE_kcal = KE_j * J_TO_KCAL_PER_MOL
        totalKE += KE_kcal * dt
    return totalKE

def potential_sum(path, cg_system, dt):
    steps = path.shape[0]
    V_sum = 0.0
    for s in range(steps - 1):
        system = clone_cg_system(cg_system, path[s])
        e_val, _ = system.compute_energy_forces()
        V_sum += e_val * dt
    return V_sum

def compute_action(path, mass_array, dt, cg_system):
    KE = kinetic_energy_numba(path, mass_array, dt)
    PE = potential_sum(path, cg_system, dt)
    return KE + PE

# --- Section 11: Global Path Optimization using PSO+SA ---
def _parallel_eval(args):
    idx, path_candidate, mass_array, dt, cg_system = args
    val = compute_action(path_candidate, mass_array, dt, cg_system)
    return (idx, val)

def parallel_pso_sa_optimize(initial_path, mass_array, dt, template_cgsys,
                             num_particles=5, max_iters=20, T0=10.0, cooling=0.95,
                             w_init=0.9, w_final=0.4, c1=1.0, c2=1.0,
                             clamp_velocity=True, velocity_limit=0.5, nprocs=4):
    from multiprocessing import Pool
    def cost_fn(pth):
        return compute_action(pth, mass_array, dt, template_cgsys)
    swarm = []
    velocities = []
    pbest = []
    pbest_scores = []
    for _ in range(num_particles):
        pert = np.random.normal(scale=0.1, size=initial_path.shape)
        candidate = initial_path + pert
        candidate[0] = initial_path[0]
        candidate[-1] = initial_path[-1]
        sc = cost_fn(candidate)
        swarm.append(candidate)
        velocities.append(np.zeros_like(candidate))
        pbest.append(candidate.copy())
        pbest_scores.append(sc)
    g_idx = np.argmin(pbest_scores)
    g_best = pbest[g_idx].copy()
    g_best_score = pbest_scores[g_idx]
    T = T0
    with Pool(nprocs) as pool:
        for it in range(max_iters):
            w = w_init - (w_init - w_final) * (it / (max_iters - 1)) if max_iters > 1 else w_final
            for i in range(num_particles):
                r1, r2 = np.random.rand(), np.random.rand()
                velocities[i] = (w * velocities[i] +
                                 c1 * r1 * (pbest[i] - swarm[i]) +
                                 c2 * r2 * (g_best - swarm[i]))
                if clamp_velocity:
                    np.clip(velocities[i], -velocity_limit, velocity_limit, out=velocities[i])
                swarm[i] += velocities[i]
                swarm[i][0] = initial_path[0]
                swarm[i][-1] = initial_path[-1]
            tasks = [(i, swarm[i], mass_array, dt, template_cgsys) for i in range(num_particles)]
            results = pool.map(_parallel_eval, tasks)
            for idx, val in results:
                dE = val - pbest_scores[idx]
                if dE < 0:
                    pbest[idx] = swarm[idx].copy()
                    pbest_scores[idx] = val
                else:
                    if np.random.rand() < np.exp(-dE / (T + 1e-12)):
                        pbest[idx] = swarm[idx].copy()
                        pbest_scores[idx] = val
                    else:
                        swarm[idx] = pbest[idx].copy()
                        velocities[idx] *= 0.0
            loc_idx = np.argmin(pbest_scores)
            if pbest_scores[loc_idx] < g_best_score:
                g_best = pbest[loc_idx].copy()
                g_best_score = pbest_scores[loc_idx]
            print(f"[PSO+SA] Iter {it}/{max_iters}, T={T:.3f}, BestAction={g_best_score:.4e}")
            T *= cooling
    return g_best

# --- Section 12: Backmapping to All-Atom Structures ---
def kabsch_rotation(P, Q):
    P_cent = np.mean(P, axis=0)
    Q_cent = np.mean(Q, axis=0)
    P_centered = P - P_cent
    Q_centered = Q - Q_cent
    H = P_centered.T @ Q_centered
    U, S, Vt = np.linalg.svd(H)
    R = Vt.T @ U.T
    if np.linalg.det(R) < 0:
        Vt[-1,:] *= -1
        R = Vt.T @ U.T
    return R

def backmap_path_to_allatom(ref_pdb, path, prefix="frame_", start_idx=1):
    residues_data = parse_full_pdb(ref_pdb)
    n_res = len(residues_data)
    frames = path.shape[0]
    if path.shape[1] != n_res:
        raise ValueError("Mismatch in residue count between path and reference PDB.")
    for f in range(frames):
        new_res = []
        for r in range(n_res):
            ref_r = residues_data[r]
            orig_ca = ref_r['ca_pos']
            new_ca = path[f, r]
            R = np.eye(3)  # Identity rotation (can be replaced with kabsch_rotation if desired)
            new_atoms = []
            for atom in ref_r['atoms']:
                orig_pos = np.array([atom['x'], atom['y'], atom['z']])
                new_pos = new_ca + (R @ (orig_pos - orig_ca))
                new_atom = atom.copy()
                new_atom['x'], new_atom['y'], new_atom['z'] = new_pos
                new_atoms.append(new_atom)
            new_res.append({'res_id': ref_r['res_id'], 'atoms': new_atoms, 'ca_pos': new_ca})
        frame_idx = f + start_idx
        out_filename = f"{prefix}{frame_idx:04d}.pdb"
        write_frame_pdb(out_filename, new_res)
        print(f"Backmapped frame written to {out_filename}")

# --- Section 13: Full Simulation Workflow (Main) ---
def main(bound_pdb, unbound_pdb, steps=40):
    # 1. Parse bound and unbound PDB files; convert to CG properties.
    if not os.path.exists(bound_pdb) or not os.path.exists(unbound_pdb):
        print("Error: Required PDB files not found.")
        return

    folded_pos, _ = parse_pdb_as_cg(bound_pdb)
    try:
        folded_pos, folded_charges, folded_masses, folded_epsilons, folded_sigmas, folded_hydro = parse_pdb_to_cg(bound_pdb)
    except Exception as e:
        print(f"Error parsing bound PDB: {e}")
        return

    unbound_pos, _ = parse_pdb_as_cg(unbound_pdb)
    if folded_pos.shape[0] != unbound_pos.shape[0]:
        raise ValueError("Bound and unbound structures must have the same number of CA atoms.")
    n_beads = folded_pos.shape[0]

    # 2. Build initial CG path via linear interpolation.
    path_init = np.linspace(folded_pos, unbound_pos, steps)

    # 3. Define bonds and angles (assume a linear chain).
    bond_list = [(i, i+1) for i in range(n_beads-1)]
    angle_list = [(i, i+1, i+2) for i in range(n_beads-2)]
    rand_charges = 0.02 * (2 * np.random.rand(n_beads) - 1.0)
    rand_charges -= np.mean(rand_charges)
    hotspot = list(range(n_beads-3, n_beads)) if n_beads >= 3 else []

    # 4. Build the CG system using bound structure properties.
    cg_system = CGSystem(positions=folded_pos.copy(), charges=rand_charges,
                         bond_list=bond_list, angle_list=angle_list,
                         hotspot_indices=hotspot, model_path=None)

    # 5. Global Path Optimization using PSO+SA.
    mass_array = folded_masses
    dt = 1e-15
    print("Starting global PSO+SA optimization of the CG path...")
    global_path = parallel_pso_sa_optimize(initial_path=path_init,
                                           mass_array=mass_array,
                                           dt=dt,
                                           template_cgsys=cg_system,
                                           num_particles=5,
                                           max_iters=20,
                                           T0=10.0,
                                           cooling=0.95,
                                           w_init=0.9,
                                           w_final=0.4,
                                           c1=1.0,
                                           c2=1.0,
                                           clamp_velocity=True,
                                           velocity_limit=0.5,
                                           nprocs=4)
    print("Global optimization complete.")

    # 6. Local Refinement on each frame using DSA-ASA.
    print("Starting local refinement (DSA-ASA) on each frame...")
    refined_path = []
    for i in range(global_path.shape[0]):
        frame = global_path[i]
        refined_frame = double_nested_simulated_annealing(frame, folded_charges, folded_hydro, folded_epsilons, folded_sigmas,
                                                          outer_steps=3, inner_steps=500)
        refined_path.append(refined_frame)
    refined_path = np.array(refined_path)
    print("Local refinement complete.")

    # 7. Advanced Visualization.
    plot_reaction_coordinate(refined_path, folded_pos, folded_charges, folded_hydro, folded_epsilons, folded_sigmas)
    plot_3d_path(folded_pos, unbound_pos, refined_path, hotspot_indices=hotspot)

    # 8. Update ML model (placeholder).
    update_ml_model(refined_path)

    # 9. Backmapping: Reconstruct full-atom PDBs using the bound PDB as reference.
    print("Starting backmapping to all-atom PDB files...")
    backmap_path_to_allatom(bound_pdb, refined_path, prefix="frame_")

    # 10. Compute and report final action.
    def compute_whole_action(path):
        KE = kinetic_energy_numba(path, mass_array, dt)
        PE = 0.0
        for s in range(path.shape[0]-1):
            system = clone_cg_system(cg_system, path[s])
            e_val, _ = system.compute_energy_forces()
            PE += e_val * dt
        return KE + PE
    final_action = compute_whole_action(refined_path)
    print(f"Final CG Path Action = {final_action:.4e}")

# Allow main() to be called from the command line or by the CLI module.
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="cg_r_pathway: Protein Reaction Coordinate Optimization Framework"
    )
    parser.add_argument('--bound', required=True, help="Path to the folded (bound) PDB file, e.g., A.pdb")
    parser.add_argument('--unbound', required=True, help="Path to the unfolded (unbound) PDB file, e.g., B.pdb")
    parser.add_argument('--steps', type=int, default=40, help="Number of interpolation steps (default: 40)")
    args = parser.parse_args()
    main(bound_pdb=args.bound, unbound_pdb=args.unbound, steps=args.steps)
