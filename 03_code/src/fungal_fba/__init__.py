"""Fungal GEM project: minimal FBA harness built on cobrapy.

Mirrors the ``labUtils.fba.fba_tools`` API (rpazuki/lab_utils) so the lab's
pipelines drop in, while remaining usable standalone.
"""

from .cobra_env import prepare, quiet_load, quiet_read_sbml
from .fba import (
    biomass_yield_on_carbon,
    check_energy_generating_cycles,
    close_free_boundary,
    exchange_summary,
    find_biomass_reactions,
    find_maintenance_reactions,
    maintenance_profile,
    reversibility_profile,
    load_model,
    map_medium_to_model,
    apply_medium,
    set_biomass_objective,
    solve_fba,
    solve_fba_and_flux,
)
from .media import MINIMAL_GLUCOSE, build_uptake, resolve_roles

__all__ = [
    "prepare", "quiet_load", "quiet_read_sbml",
    "load_model", "solve_fba", "solve_fba_and_flux",
    "find_biomass_reactions", "set_biomass_objective",
    "apply_medium", "map_medium_to_model",
    "exchange_summary", "biomass_yield_on_carbon",
    "close_free_boundary", "check_energy_generating_cycles",
    "reversibility_profile", "find_maintenance_reactions", "maintenance_profile",
    "MINIMAL_GLUCOSE", "build_uptake", "resolve_roles",
]
