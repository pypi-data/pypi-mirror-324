"""
Parse periodic structures, assign Wannier centres and identify interactions.

This module contains the functions necessary to parse the geometry of the target system
and from this identify relevant interatomic/on-site interactions from which to compute
descriptors of bonding and local electronic structure.
"""

# Copyright (C) 2024-2025 Patrick J. Taylor

# This file is part of pengWann.
#
# pengWann is free software: you can redistribute it and/or modify it under the terms
# of the GNU General Public License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# pengWann is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with pengWann.
# If not, see <https://www.gnu.org/licenses/>.

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike
from pengwann.interactions import (
    AtomicInteractionContainer,
    AtomicInteraction,
    WannierInteraction,
)
from pengwann.io import read_xyz
from pengwann.utils import get_atom_indices
from pymatgen.core import Structure


def build_geometry(path: str, cell: ArrayLike) -> Structure:
    """
    Parse a seedname_centres.xyz file, add PBCs and assign Wannier centres.

    This function will parse a Wannier90 seedname_centres.xyz file and by combining
    this data with the `cell` vectors, generate a Pymatgen Structure object with
    periodic boundary conditions and a :code:`wannier_centres` site property. This
    latter data is required to identify interatomic and on-site interactions in terms
    of Wannier functions.

    Parameters
    ----------
    path : str
        Filepath to the seedname_centres.xyz file output by Wannier90.
    cell : array_like
        The cell vectors associated with the structure.

    Returns
    -------
    geometry : Structure
        The Pymatgen Structure with a :code:`"wannier_centres"` site property.

    See Also
    --------
    assign_wannier_centres
    """
    symbols, coords = read_xyz(path)

    geometry = Structure(cell, symbols, coords, coords_are_cartesian=True)

    assign_wannier_centres(geometry)

    return geometry


def assign_wannier_centres(geometry: Structure) -> None:
    """
    Assign Wannier centres to atoms based on a closest distance criterion.

    A :code:`"wannier_centres"` site property will be assigned in-place to the input
    `geometry`, associating each atom in the structure with a sequence of indices. These
    indices refer to the order of atoms in `geometry` and associate each atom with the
    Wannier centres to which it is closer than any other atom.

    Parameters
    ----------
    geometry : Structure
        A Pymatgen Structure object containing the structure itself as well as the
        positions of the Wannier centres (as "X" atoms).

    Returns
    -------
    None
    """
    wannier_indices, atom_indices = [], []
    for idx in range(len(geometry)):
        symbol = geometry[idx].species_string

        if symbol == "X0+":
            wannier_indices.append(idx)

        else:
            atom_indices.append(idx)

    if not wannier_indices:
        raise ValueError(
            'No Wannier centres ("X" atoms) found in the input Structure object.'
        )

    distance_matrix = geometry.distance_matrix

    wannier_centres_list = [[] for site in geometry]
    for i in wannier_indices:
        min_distance, min_idx = np.inf, 2 * len(geometry)

        for j in atom_indices:
            distance = distance_matrix[i, j]

            if distance < min_distance:
                min_distance = distance
                min_idx = j

        wannier_centres_list[i].append(min_idx)
        wannier_centres_list[min_idx].append(i)

    wannier_centres = tuple([tuple(indices) for indices in wannier_centres_list])
    geometry.add_site_property("wannier_centres", wannier_centres)


def identify_onsite_interactions(
    geometry: Structure, symbols: tuple[str, ...]
) -> AtomicInteractionContainer:
    """
    Identify all on-site interactions for a set of atomic species.

    Parameters
    ----------
    geometry : Structure
            A Pymatgen Structure object with a :code:`"wannier_centres"` site property
            that associates each atom with the indices of its Wannier centres.
    symbols : tuple of str
            The atomic species to return interactions for. These should match one or
            more of the species present in `geometry`.

    Returns
    -------
    interactions : AtomicInteractionContainer
            The on-site/diagonal AtomicInteraction objects associated with each symbol
            in `symbols`.

    Notes
    -----
    In the context of pengwann, an on-site/diagonal interaction is simply a 2-body
    interaction between atoms or individual Wannier functions in which
    atom i == atom j or Wannier function i == Wannier function j.
    """
    bl_0 = np.array([0, 0, 0])
    wannier_centres = geometry.site_properties["wannier_centres"]

    interactions = []
    for idx in range(len(geometry)):
        symbol = geometry[idx].species_string
        if symbol in symbols:
            wannier_interactions = []
            for i in wannier_centres[idx]:
                wannier_interaction = WannierInteraction(i, i, bl_0, bl_0)

                wannier_interactions.append(wannier_interaction)

            interaction = AtomicInteraction(
                idx, idx, symbol, symbol, tuple(wannier_interactions)
            )

            interactions.append(interaction)

    if not interactions:
        raise ValueError(f"No atoms matching symbols in {symbols} found.")

    return AtomicInteractionContainer(sub_interactions=tuple(interactions))


def identify_interatomic_interactions(
    geometry: Structure, radial_cutoffs: dict[tuple[str, str], float]
) -> AtomicInteractionContainer:
    """
    Identify interatomic interactions according to a set of radial distance cutoffs.

    Parameters
    ----------
    geometry : Structure
        A Pymatgen Structure object with a :code:`"wannier_centres"` site property that
        associates each atom with the indices of its Wannier centres.
    radial_cutoffs : dict of {2-length tuple of str : float} pairs
        A dictionary defining radial cutoffs for pairs of atomic species e.g
        :code:`{("C", "C"): 1.6, ("C", "O"): 1.5}`.

    Returns
    -------
    interactions : AtomicInteractionContainer
        The interactions identified according to the `radial_cutoffs`.

    See Also
    --------
    build_geometry
    pengwann.descriptors.DescriptorCalculator.assign_descriptors :
        Compute bonding descriptors for a set of interatomic interactions.
    """
    if "wannier_centres" not in geometry.site_properties.keys():
        raise ValueError('Input geometry is missing a "wannier_centres" site property.')

    num_wann = len([site for site in geometry if site.species_string == "X0+"])

    if num_wann == 0:
        raise ValueError(
            'Input geometry contains no Wannier centres (i.e. no "X" atoms).'
        )

    symbols_list: list[str] = []
    for pair in radial_cutoffs.keys():
        for symbol in pair:
            if symbol not in symbols_list:
                symbols_list.append(symbol)

    symbols = tuple(symbols_list)

    atom_indices = get_atom_indices(geometry, symbols)

    wannier_centres = geometry.site_properties["wannier_centres"]
    interactions = []
    for pair, cutoff in radial_cutoffs.items():
        symbol_i, symbol_j = pair

        possible_interactions = []
        if symbol_i != symbol_j:
            for i in atom_indices[symbol_i]:
                for j in atom_indices[symbol_j]:
                    possible_interactions.append((i, j))

        # Exclude self-interactions
        else:
            for idx, i in enumerate(atom_indices[symbol_i]):
                for j in atom_indices[symbol_j][idx + 1 :]:
                    possible_interactions.append((i, j))

        for i, j in possible_interactions:
            distance = geometry.get_distance(i, j)

            if distance < cutoff:
                wannier_interactions_list = []
                for m in wannier_centres[i]:
                    for n in wannier_centres[j]:
                        _, bl_1 = geometry[i].distance_and_image(geometry[m])
                        _, bl_2 = geometry[j].distance_and_image(geometry[n])

                        wannier_interaction = WannierInteraction(m, n, bl_1, bl_2)
                        wannier_interactions_list.append(wannier_interaction)

                wannier_interactions = tuple(wannier_interactions_list)
                interaction = AtomicInteraction(
                    i, j, symbol_i, symbol_j, wannier_interactions
                )
                interactions.append(interaction)

    return AtomicInteractionContainer(sub_interactions=tuple(interactions))
