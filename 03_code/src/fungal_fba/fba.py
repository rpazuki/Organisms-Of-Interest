"""Minimal FBA harness for the fungal GEM project.

API-compatible with ``labUtils.fba.fba_tools`` (rpazuki/lab_utils) so that the
lab's existing pipelines drop in, but it works standalone when ``labUtils`` is
not installed.

The ``solve_fba`` contract follows lab_utils exactly:

* ``df`` — one row per condition. Columns are **exchange reaction IDs**; each
  cell is the uptake bound for that exchange in that condition.
* Every exchange in ``model.medium`` is first zeroed, then only the columns
  present in ``df_medium_columns`` are opened. This makes the medium fully
  explicit — nothing is inherited from the model file's default medium.
* ``scaled_columns`` / ``scale_factor`` rescale selected columns (used when
  medium concentrations need converting to flux units).
* ``zero_uptake_columns`` force specific exchanges shut after scaling.
* ``use_sfba=True`` selects pFBA (parsimonious FBA) instead of plain FBA.

Everything runs inside ``with model:`` so bounds are always restored.
"""

from __future__ import annotations

from typing import Iterable, Sequence

import pandas as pd

from .cobra_env import prepare, quiet_load

prepare()

import cobra  # noqa: E402  (must follow prepare())
from cobra.exceptions import Infeasible, OptimizationError  # noqa: E402
from cobra.flux_analysis import pfba  # noqa: E402


# ----------------------------------------------------------------------------
# model loading
# ----------------------------------------------------------------------------

def load_model(path: str):
    """Load a COBRA model from SBML or JSON.

    Same signature as ``labUtils.fba.fba_tools.load_model``, with the SBML
    warning flood suppressed.
    """
    return quiet_load(path)


# ----------------------------------------------------------------------------
# objective handling
# ----------------------------------------------------------------------------

BIOMASS_PATTERNS = (
    "biomass", "growth", "bio1", "xbiomass", "r_2111", "added_biomass",
)


def find_biomass_reactions(model: "cobra.Model") -> list[str]:
    """Return reaction IDs that look like a biomass/growth objective.

    Several published fungal GEMs ship with **no** objective set (e.g. iMT1026)
    or with an objective that leaves growth unbounded, so the objective must be
    chosen explicitly rather than trusted from the file.
    """
    hits = []
    for rxn in model.reactions:
        text = f"{rxn.id} {rxn.name or ''}".lower()
        if any(pat in text for pat in BIOMASS_PATTERNS):
            hits.append(rxn.id)
    return hits


def set_biomass_objective(model: "cobra.Model", reaction_id: str) -> None:
    """Set the model objective to a single biomass reaction, maximised."""
    if reaction_id not in model.reactions:
        raise KeyError(f"{reaction_id!r} not in model {model.id!r}")
    model.objective = reaction_id
    model.objective_direction = "max"


# ----------------------------------------------------------------------------
# medium handling
# ----------------------------------------------------------------------------

def apply_medium(
    model: "cobra.Model",
    uptake: dict[str, float],
    zero_uptake_columns: Iterable[str] = (),
) -> dict[str, float]:
    """Zero every exchange in the model medium, then open only ``uptake``.

    ``uptake`` maps exchange reaction ID -> uptake bound (positive magnitude,
    matching the cobrapy ``model.medium`` convention). Returns the medium dict
    actually applied. Unknown reaction IDs are ignored so a single medium
    definition can be reused across models with different naming schemes; use
    :func:`map_medium_to_model` first to see what matched.
    """
    # A few reconstructions ship exchanges with a NEGATIVE upper bound, i.e. a
    # forced minimum uptake. cobrapy's own `model.medium` setter assigns lb
    # before ub and raises on the transient lb > ub, so raise those ceilings to
    # zero first. This only removes a forced uptake, never adds capacity.
    for rxn in model.exchanges:
        if rxn.upper_bound < 0:
            rxn.bounds = (rxn.lower_bound, 0.0)
        # The mirror case: a POSITIVE lower bound is a forced minimum flux.
        # cobrapy's medium setter writes the upper bound first and raises on the
        # transient lb > ub, so the floor has to come down first. As above this
        # only removes a forced flux, never adds capacity.
        if rxn.lower_bound > 0:
            rxn.bounds = (0.0, rxn.upper_bound)

    medium = {rxn_id: 0.0 for rxn_id in model.medium}
    # Boundary reactions cobrapy classifies as sinks/demands are absent from
    # model.medium and its setter rejects them, so their bounds are set
    # directly. Direction matters: for `A_e -->` (coef -1) uptake is negative
    # flux and the bound goes on the lower bound; for `--> A_e` (coef +1) it is
    # positive flux and goes on the upper bound.
    exchange_ids = {rxn.id for rxn in model.exchanges}
    direct: dict[str, float] = {}
    for rxn_id, value in uptake.items():
        if rxn_id not in model.reactions:
            continue
        if rxn_id in exchange_ids or rxn_id in medium:
            medium[rxn_id] = float(value)
        else:
            direct[rxn_id] = float(value)
    for rxn_id in zero_uptake_columns:
        if rxn_id in medium:
            medium[rxn_id] = 0.0
        direct.pop(rxn_id, None)
    model.medium = medium

    for rxn_id, value in direct.items():
        rxn = model.reactions.get_by_id(rxn_id)
        coef = next(iter(rxn.metabolites.values()), -1.0)
        if coef < 0:
            rxn.bounds = (-abs(value), max(rxn.upper_bound, 0.0))
        else:
            rxn.bounds = (min(rxn.lower_bound, 0.0), abs(value))
    medium.update(direct)
    return medium


def _is_extracellular(model, met) -> bool:
    """Whether a metabolite sits in the extracellular compartment.

    Compartment IDs are not standardised across reconstructions ('e', 'C_ex',
    'CCO-EXTRACELLULAR'), so match the declared compartment NAME as well.
    """
    comp = (met.compartment or "").lower()
    if comp in {"e", "ex", "extracellular", "c_ex", "s", "e0"}:
        return True
    name = (model.compartments.get(met.compartment, "") or "").lower()
    return "extracellular" in name or "extra-organism" in name


def _is_free_carbon_route(model, met) -> bool:
    """Whether an unclamped boundary on ``met`` could supply real nutrient.

    True for extracellular metabolites (genuine transport boundaries) and for
    any metabolite whose formula contains carbon (an intracellular sink that
    can still inject carbon). False for formula-less intracellular pool
    pseudo-metabolites, which exist only to assemble biomass.
    """
    if _is_extracellular(model, met):
        return True
    formula = met.formula or ""
    return "C" in (met.elements or {}) if formula else False


def close_free_boundary(
    model: "cobra.Model", allowed: Iterable[str] = ()
) -> list[str]:
    """Shut reverse (inward) flux on every boundary reaction except ``allowed``.

    ``model.medium`` covers only reactions cobrapy classifies as *exchanges*.
    Reversible **sink** and **demand** reactions are invisible to it, so a model
    carrying reversible sinks can import metabolites for free no matter how
    carefully the medium is set. iWV1314 (A. oryzae) has 79 such sinks with a
    lower bound of -10, which is enough to make growth effectively unbounded.

    Returns the IDs of the boundary reactions that were clamped.
    """
    allowed = set(allowed)
    clamped = []
    for rxn in model.boundary:
        if rxn.id in allowed:
            continue
        met = next(iter(rxn.metabolites), None)
        if met is not None and not _is_free_carbon_route(model, met):
            # Formula-less intracellular pool pseudo-metabolites ("biomass",
            # "cofactor", "lipid backbone") are biomass-assembly scaffolding,
            # not nutrient routes. Clamping them removes a biomass precursor:
            # closing yeast-GEM's r_4598 cofactor pseudoreaction drops growth
            # to exactly zero. They cannot supply carbon, so exempt them.
            continue
        coef = next(iter(rxn.metabolites.values()), -1.0)
        if coef < 0:
            # `A_e -->`: uptake is negative flux, so the floor is the free door.
            if rxn.lower_bound < 0:
                # Both bounds at once; see check_energy_generating_cycles.
                rxn.bounds = (0.0, max(rxn.upper_bound, 0.0))
                clamped.append(rxn.id)
        else:
            # `--> A_e`: the reaction PRODUCES the extracellular metabolite, so
            # uptake is POSITIVE flux and the ceiling is the free door. Clamping
            # only the lower bound here closes nothing: iCV785 writes every
            # supply this way and kept drawing citrate and xylitol, pulling in
            # 478 mmol C when the medium supplied 60.
            if rxn.upper_bound > 0:
                rxn.bounds = (min(rxn.lower_bound, 0.0), 0.0)
                clamped.append(rxn.id)
    return clamped


def find_maintenance_reactions(model: "cobra.Model") -> list[str]:
    """Find non-growth-associated maintenance (NGAM) ATP-hydrolysis reactions.

    Matching is done on whole words plus a check that the reaction really
    hydrolyses ATP. A naive substring search for "gam" matches every
    "gamma-glutamyl..." enzyme in the model, so word boundaries matter.
    """
    import re as _re

    word = _re.compile(r"\b(maintenance|atpm|ngam|gam)\b", _re.I)
    hits = []
    for rxn in model.reactions:
        if not word.search(f"{rxn.id} {rxn.name or ''}"):
            continue
        # Match on metabolite NAME as well as ID: yeast-GEM and iYali use
        # opaque identifiers (s_0434 = ATP), so an ID-only check misses them.
        blob = " ".join(
            f"{m.id} {m.name or ''}" for m in rxn.metabolites
        ).lower()
        if "atp" in blob and ("adp" in blob or "amp" in blob):
            hits.append(rxn.id)
    return hits


def maintenance_profile(model: "cobra.Model") -> dict:
    """Report whether a maintenance-energy constraint is actually enforced.

    An unenforced NGAM (bounds ``(0, 1000)``) or a missing one lets the model
    spend nothing on maintenance, which inflates biomass yield. This is a
    common cause of a GEM predicting a yield above the ~0.5 gDW/g glucose
    biochemical ceiling for aerobic growth.
    """
    ids = find_maintenance_reactions(model)
    if not ids:
        return {"maintenance_reactions": [], "ngam_enforced": False,
                "ngam_lower_bound": None,
                "note": "no NGAM reaction found; maintenance cost is unmodelled"}
    rxn = model.reactions.get_by_id(ids[0])
    enforced = rxn.lower_bound > 1e-9
    return {
        "maintenance_reactions": ids,
        "ngam_reaction": rxn.id,
        "ngam_lower_bound": float(rxn.lower_bound),
        "ngam_enforced": bool(enforced),
        "note": ("NGAM pinned/floored, maintenance cost enforced" if enforced
                 else "NGAM present but lower bound is 0, so maintenance is optional"),
    }


def check_energy_generating_cycles(
    model: "cobra.Model", atp_reaction_hint: str | None = None
) -> dict:
    """Test whether the model can make ATP with no substrate uptake.

    The standard thermodynamic sanity check: close every uptake, then maximise
    an ATP-hydrolysing reaction. A correctly constrained model returns 0. A
    nonzero value means an energy-generating cycle exists, which inflates every
    predicted growth rate and makes yield predictions meaningless.

    Models whose directionality constraints were lost on SBML export (all
    reactions reversible) fail this test systematically.
    """
    result = {"atp_reaction": None, "max_atp_no_uptake": None, "has_egc": None}
    candidates = []
    if atp_reaction_hint and atp_reaction_hint in model.reactions:
        candidates.append(atp_reaction_hint)
    candidates.extend(find_maintenance_reactions(model))
    if not candidates:
        return result

    rxn_id = candidates[0]
    result["atp_reaction"] = rxn_id
    with model:
        # Maintenance reactions are often pinned to a fixed nonzero flux (yeast-GEM
        # fixes NGAM at 0.7). That pinned value would be reported as a spurious
        # energy-generating cycle, so free the bound before maximising it.
        target = model.reactions.get_by_id(rxn_id)
        target.bounds = (0.0, 1000.0)
        for rxn in model.boundary:
            # Assign both bounds together: some models force uptake with a
            # negative upper bound, and setting lb alone would transiently
            # violate lb <= ub and raise.
            rxn.bounds = (0.0, max(rxn.upper_bound, 0.0))
        model.objective = rxn_id
        model.objective_direction = "max"
        sol = model.optimize()
        value = 0.0 if sol.objective_value is None else float(sol.objective_value)
    result["max_atp_no_uptake"] = value
    result["has_egc"] = bool(value > 1e-6)
    return result


def reversibility_profile(model: "cobra.Model") -> dict:
    """Summarise directionality constraints, which gate prediction quality.

    ``frac_fully_open`` near 1.0 indicates the SBML lost its flux bounds, so
    the model is thermodynamically unconstrained and its FBA output cannot be
    trusted quantitatively.
    """
    n = len(model.reactions)
    if n == 0:
        return {"n_reactions": 0}
    reversible = sum(1 for r in model.reactions if r.lower_bound < 0 < r.upper_bound)
    wide = sum(
        1 for r in model.reactions if r.lower_bound <= -1000 and r.upper_bound >= 1000
    )
    return {
        "n_reactions": n,
        "n_reversible": reversible,
        "frac_reversible": round(reversible / n, 4),
        "n_fully_open": wide,
        "frac_fully_open": round(wide / n, 4),
        "bounds_likely_lost": bool(wide / n > 0.95),
    }


def map_medium_to_model(
    model: "cobra.Model", uptake: dict[str, float]
) -> tuple[dict[str, float], list[str]]:
    """Split ``uptake`` into components the model has and those it lacks."""
    present = {k: v for k, v in uptake.items() if k in model.reactions}
    missing = [k for k in uptake if k not in model.reactions]
    return present, missing


# ----------------------------------------------------------------------------
# lab_utils-compatible solvers
# ----------------------------------------------------------------------------

def _growth_from(solution, model: "cobra.Model") -> float:
    """Extract the growth rate from a cobrapy solution.

    ``pfba`` minimises total flux subject to the objective being held at its
    optimum, so ``solution.objective_value`` is the **flux sum**, not growth.
    The growth rate must therefore be read from the objective reaction's own
    flux. Plain FBA is handled by the same code path.
    """
    ids = [r.id for r in model.reactions if r.objective_coefficient != 0]
    if ids:
        try:
            return float(sum(solution.fluxes[i] for i in ids))
        except (KeyError, TypeError):
            pass
    return 0.0 if solution.objective_value is None else float(solution.objective_value)


def solve_fba(
    df: pd.DataFrame,
    model: "cobra.Model",
    df_medium_columns: Sequence[str] | None = None,
    scaled_columns: Sequence[str] = (),
    scale_factor: float = 1.0,
    zero_uptake_columns: Sequence[str] = (),
    use_sfba: bool = False,
    close_sinks: bool = True,
    gr_column: str = "mv_mu_max",
    solution_column_name: str = "fba_growth",
    solution_status_column_name: str = "fba_status",
) -> pd.DataFrame:
    """Solve FBA for every row of ``df``. Mirrors ``lab_utils.solve_fba``.

    Returns a copy of ``df`` with predicted growth and solver status appended.
    """
    df = df.copy()
    df[solution_column_name] = 0.0
    df[solution_status_column_name] = ""

    if df_medium_columns is None:
        df_medium_columns = [
            c for c in df.columns
            if c not in (solution_column_name, solution_status_column_name, gr_column)
        ]

    for idx, row in df.iterrows():
        with model:
            uptake = {}
            for rxn_id in df_medium_columns:
                value = float(row.get(rxn_id, 0.0) or 0.0)
                if rxn_id in scaled_columns:
                    value *= scale_factor
                uptake[rxn_id] = value
            apply_medium(model, uptake, zero_uptake_columns)
            if close_sinks:
                # Reversible sinks/demands bypass model.medium entirely and can
                # supply free carbon; clamp all inward boundary flux except the
                # medium components we deliberately opened.
                close_free_boundary(model, allowed={
                    k for k, v in uptake.items() if v > 0
                })
            try:
                solution = pfba(model) if use_sfba else model.optimize()
            except (Infeasible, OptimizationError) as exc:
                # pfba raises on an infeasible LP instead of returning a status.
                # Infeasibility is a real result (e.g. a model whose maintenance
                # ATP demand is pinned nonzero cannot survive zero carbon), so it
                # is recorded rather than aborting the sweep.
                df.loc[idx, solution_column_name] = 0.0
                df.loc[idx, solution_status_column_name] = (
                    "infeasible" if isinstance(exc, Infeasible) else "error"
                )
                continue
            df.loc[idx, solution_column_name] = _growth_from(solution, model)
            df.loc[idx, solution_status_column_name] = solution.status
    return df


def solve_fba_and_flux(
    df: pd.DataFrame,
    model: "cobra.Model",
    df_medium_columns: Sequence[str] | None = None,
    scaled_columns: Sequence[str] = (),
    scale_factor: float = 1.0,
    zero_uptake_columns: Sequence[str] = (),
    use_sfba: bool = False,
    close_sinks: bool = True,
    gr_column: str = "mv_mu_max",
    solution_column_name: str = "fba_growth",
    solution_status_column_name: str = "fba_status",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """As :func:`solve_fba`, but also return the full flux matrix.

    Second return value is a DataFrame of fluxes, one row per condition
    (index aligned to ``df``), one column per reaction.
    """
    df = df.copy()
    df[solution_column_name] = 0.0
    df[solution_status_column_name] = ""
    flux_rows = []

    if df_medium_columns is None:
        df_medium_columns = [
            c for c in df.columns
            if c not in (solution_column_name, solution_status_column_name, gr_column)
        ]

    for idx, row in df.iterrows():
        with model:
            uptake = {}
            for rxn_id in df_medium_columns:
                value = float(row.get(rxn_id, 0.0) or 0.0)
                if rxn_id in scaled_columns:
                    value *= scale_factor
                uptake[rxn_id] = value
            apply_medium(model, uptake, zero_uptake_columns)
            if close_sinks:
                # Reversible sinks/demands bypass model.medium entirely and can
                # supply free carbon; clamp all inward boundary flux except the
                # medium components we deliberately opened.
                close_free_boundary(model, allowed={
                    k for k, v in uptake.items() if v > 0
                })
            try:
                solution = pfba(model) if use_sfba else model.optimize()
            except (Infeasible, OptimizationError) as exc:
                df.loc[idx, solution_column_name] = 0.0
                df.loc[idx, solution_status_column_name] = (
                    "infeasible" if isinstance(exc, Infeasible) else "error"
                )
                continue
            df.loc[idx, solution_column_name] = _growth_from(solution, model)
            df.loc[idx, solution_status_column_name] = solution.status
            flux_rows.append(solution.fluxes.rename(idx))

    fluxes = pd.DataFrame(flux_rows) if flux_rows else pd.DataFrame()
    return df, fluxes


# ----------------------------------------------------------------------------
# reporting helpers
# ----------------------------------------------------------------------------

def exchange_summary(
    solution_fluxes: pd.Series,
    model: "cobra.Model",
    threshold: float = 1e-6,
) -> pd.DataFrame:
    """Tabulate non-trivial exchange fluxes, split into uptake and secretion."""
    rows = []
    for rxn in model.exchanges:
        flux = float(solution_fluxes.get(rxn.id, 0.0))
        if abs(flux) < threshold:
            continue
        rows.append({
            "reaction": rxn.id,
            "name": rxn.name or "",
            "flux": flux,
            "direction": "uptake" if flux < 0 else "secretion",
        })
    out = pd.DataFrame(rows)
    return out.sort_values("flux") if len(out) else out


def biomass_yield_on_carbon(
    growth_rate: float, carbon_uptake_flux: float
) -> float | None:
    """gDW per mmol carbon source. ``carbon_uptake_flux`` may be signed."""
    denom = abs(carbon_uptake_flux)
    if denom < 1e-9:
        return None
    return growth_rate / denom
