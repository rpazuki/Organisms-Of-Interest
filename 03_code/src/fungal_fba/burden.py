"""Burden modelling: the metabolic cost of expressing a heterologous product.

Why this is needed. Plain FBA maximises growth and will happily report that a
production strain grows exactly as fast as its parent, because nothing in the
stoichiometric matrix knows that making a gram of recombinant protein consumes
precursors, ATP and ribosomes that would otherwise have made biomass. Every
in-silico design that ignores this overestimates yield, and the error grows with
titre. The three approaches below are ordered by how much information they
require, so a lab can start with the first on day one and move to the third when
enzyme data exists.

Recommendation for this project: start with (2) explicit product sink and a
growth-coupled sweep, because it needs only the product's amino-acid or
elemental composition, which is known for every target these organisms are used
for. Escalate to (3) enzyme-constrained models where a GECKO reconstruction
already exists -- which in this organism set means S. cerevisiae and
Y. lipolytica only.
"""

from __future__ import annotations

import re

import pandas as pd

# Mean ATP cost of polymerising one amino acid into protein: 4 high-energy
# phosphate bonds (2 for aminoacyl-tRNA charging, 2 for elongation). Standard
# across the bacterial and fungal literature; the dominant term in protein
# burden and the reason protein products are far costlier than small molecules.
ATP_PER_PEPTIDE_BOND = 4.0


def protein_burden_reaction(model, aa_composition: dict, atp_per_aa: float = ATP_PER_PEPTIDE_BOND):
    """Build a drain representing synthesis of one mmol of a protein product.

    ``aa_composition`` maps model metabolite IDs for the charged amino acids to
    their stoichiometric counts in the product. The ATP term is what makes this
    a burden rather than a relabelled biomass drain: without it the model can
    make protein from amino acids for free and the growth penalty vanishes.

    Deliberately does NOT add the ribosome/tRNA machinery: those are not in any
    of these GEMs, so including a nominal cost would be inventing a constraint.
    The consequence is that this UNDERESTIMATES true protein burden, which is
    stated in the report rather than hidden.
    """
    from cobra import Reaction

    rxn = Reaction("PRODUCT_SYNTHESIS")
    rxn.name = "heterologous protein synthesis (burden)"
    rxn.lower_bound = 0.0
    rxn.upper_bound = 1000.0

    stoich = {}
    for met_id, count in aa_composition.items():
        stoich[model.metabolites.get_by_id(met_id)] = -float(count)

    n_residues = sum(aa_composition.values())
    if atp_per_aa:
        missing = [r for r in ("atp", "adp", "pi", "h2o")
                   if _find_metabolite(model, r) is None]
        if missing:
            # Raising rather than skipping: a silently dropped ATP term yields a
            # burden that looks valid but understates cost, which is worse than
            # no answer.
            raise ValueError(
                f"cannot build ATP burden term, unresolved cofactors: {missing}"
            )
        for role, coef in [("atp", -atp_per_aa * n_residues),
                           ("h2o", -atp_per_aa * n_residues),
                           ("adp", atp_per_aa * n_residues),
                           ("pi", atp_per_aa * n_residues)]:
            met = _find_metabolite(model, role)
            stoich[met] = stoich.get(met, 0.0) + coef

    rxn.add_metabolites(stoich)
    return rxn


_COMPARTMENT_SUFFIX = re.compile(r"\s*\[[^\]]+\]\s*$")

# Formula is the tiebreaker when names disagree. Matching on name alone picked
# the wrong metabolite in the pan-GEMs, whose names carry a compartment suffix
# ("ATP [cytoplasm]"), and would silently return None -- which does not error,
# it just drops the ATP term and reports a burden that is precursor-only.
_COFACTOR = {
    "atp": (("atp", "adenosine triphosphate"), "C10H12N5O13P3"),
    "adp": (("adp", "adenosine diphosphate"), "C10H12N5O10P2"),
    "pi": (("pi", "phosphate", "orthophosphate"), "HO4P"),
    "h2o": (("h2o", "water"), "H2O"),
}


def _find_metabolite(model, role: str):
    """Locate a cytosolic cofactor across inconsistent naming conventions.

    Tries exact name (compartment suffix stripped), then chemical formula, then
    ID prefix. Returns None only when the metabolite is genuinely absent, which
    callers must treat as a failure rather than a zero cost.
    """
    aliases, formula = _COFACTOR[role]
    cytosolic = [m for m in model.metabolites
                 if (m.compartment or "").lower().startswith("c")]
    if not cytosolic:
        cytosolic = list(model.metabolites)

    for alias in aliases:
        for met in cytosolic:
            name = _COMPARTMENT_SUFFIX.sub("", (met.name or "").strip()).lower()
            if name == alias.lower():
                return met
    for met in cytosolic:
        if (met.formula or "") == formula:
            return met
    for alias in aliases:
        for met in cytosolic:
            if met.id.lower().startswith(alias.lower()):
                return met
    return None


def growth_coupled_sweep(model, product_rxn_id: str, biomass_rxn_id: str,
                         levels=None) -> pd.DataFrame:
    """Trace the growth-production trade-off: the production envelope.

    Forces product flux to each level and re-maximises growth. The slope of the
    resulting line IS the burden -- how many hours of growth rate are paid per
    unit of product. A flat line means the model cannot see the cost and the
    burden formulation is incomplete; a cliff means the product competes for a
    genuinely limiting precursor.
    """
    if levels is None:
        levels = [0.0, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0]

    rows = []
    for level in levels:
        with model as m:
            rxn = m.reactions.get_by_id(product_rxn_id)
            rxn.bounds = (float(level), float(level))
            m.objective = biomass_rxn_id
            growth = m.slim_optimize()
            rows.append({
                "product_flux": float(level),
                "growth": float(growth) if growth is not None and growth == growth else 0.0,
                "feasible": growth is not None and growth == growth and growth > 1e-9,
            })
    df = pd.DataFrame(rows)
    base = df.loc[df.product_flux == 0, "growth"]
    if len(base) and base.iloc[0] > 0:
        df["growth_frac_of_wt"] = (df.growth / base.iloc[0]).round(4)
    return df


def burden_slope(envelope: pd.DataFrame) -> float:
    """Growth rate lost per unit product flux, over the feasible region.

    Reported as a single number so strains and hosts can be ranked. Fitted only
    on feasible points, because the infeasible tail is a wall rather than a
    slope and including it would flatten the estimate.
    """
    feas = envelope[envelope.feasible]
    if len(feas) < 2:
        return float("nan")
    x = feas.product_flux.to_numpy()
    y = feas.growth.to_numpy()
    n = len(x)
    denom = (n * (x * x).sum() - x.sum() ** 2)
    if abs(denom) < 1e-12:
        return float("nan")
    return float((n * (x * y).sum() - x.sum() * y.sum()) / denom)
