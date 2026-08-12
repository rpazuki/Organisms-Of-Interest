"""Model-selection metric for choosing one GEM per organism.

The problem this solves: several of these organisms have a dozen candidate
reconstructions (K. phaffii has 10, Y. lipolytica 12) spanning 2010-2026, and
"most recent" and "largest" both pick the wrong model in at least one case. The
metric below scores each candidate on six axes and is deliberately transparent
so a lab can re-weight it: the weights encode a *purpose* (strain design with
gene knockouts), not a universal notion of model quality.

Weights and why:

  fba_ready   0.30  A hard gate in practice. A model that does not load, has no
                    exchanges, or solves to an implausible growth rate cannot
                    answer a design question at all. Weighted highest because
                    every other virtue is worthless without it.
  gpr         0.25  Fraction of reactions with gene-protein-reaction rules.
                    Directly bounds what fraction of the metabolic map is
                    reachable by a genetic intervention. A gene-less draft
                    (CoReCo) can predict flux but cannot rank a knockout, which
                    is the actual deliverable here.
  mass_bal    0.15  Fraction of reactions that are elementally balanced. An
                    unbalanced reaction is a route to free mass; a model with
                    many of them will overpredict yield in ways that look
                    plausible.
  scope       0.15  Reaction count, log-scaled and normalised within organism.
                    Bigger is better only weakly and only up to a point, hence
                    log: iJB1325's 2400 reactions genuinely cover more
                    secondary metabolism than iMA871's 1200, but a 5000-reaction
                    automated draft is not 4x better than either.
  curation    0.10  Provenance tier: consensus/community > manual single-lab >
                    semi-automated > fully automated draft. Encodes the strong
                    empirical pattern that curation effort predicts predictive
                    accuracy better than any structural statistic.
  recency     0.05  Publication year, normalised. Deliberately the smallest
                    weight: yeast-GEM 9.1 (2026) and iMA871 (2008) differ by
                    18 years, but iLC915 (2012) outranks two later K. phaffii
                    models on every axis that matters. Recency is a weak proxy
                    at best and is included only as a tiebreaker.
"""

from __future__ import annotations

import math
import re

import pandas as pd

WEIGHTS = {
    "fba_ready": 0.30,
    "gpr": 0.25,
    "mass_bal": 0.15,
    "scope": 0.15,
    "curation": 0.10,
    "recency": 0.05,
}

# Provenance tiers. Matched against the model_id and publication string.
CURATION_TIERS = {
    "consensus": 1.00,   # community-maintained, versioned, CI-tested
    "manual": 0.75,      # single-lab manual reconstruction, peer-reviewed
    "semi_auto": 0.45,   # automated draft with reported manual gap-filling
    "auto": 0.15,        # fully automated (CoReCo, RAVEN/ModelSEED draft)
}

_CONSENSUS = re.compile(r"yeast-gem|consensus|pan-gem|community", re.I)
_AUTO = re.compile(r"coreco|modelseed|carveme|raven draft|automat", re.I)
_SEMI = re.compile(r"draft|template|homolog", re.I)

# Enzyme-constrained (GECKO) models. ecYeastGEM reports 8144 reactions against
# yeast-GEM's 4102, but the extra 4000 are per-isozyme arm reactions and enzyme
# usage pseudo-reactions wrapping the SAME metabolic map, not additional
# biochemistry. Scoring them on raw reaction count ranked ecYeastGEM above the
# consensus model it is derived FROM, which is backwards.
_EC_MODEL = re.compile(r"^ec[A-Zi]|gecko|enzyme-constrain", re.I)


def is_enzyme_constrained(model_id: str, publication: str = "") -> bool:
    """Whether a candidate is a GECKO-style enzyme-constrained expansion."""
    return bool(_EC_MODEL.search(f"{model_id} {publication or ''}"))


def curation_tier(model_id: str, publication: str = "") -> tuple[str, float]:
    """Classify reconstruction provenance from its identifier and citation."""
    blob = f"{model_id} {publication or ''}"
    if _CONSENSUS.search(blob):
        return "consensus", CURATION_TIERS["consensus"]
    if _AUTO.search(blob):
        return "auto", CURATION_TIERS["auto"]
    if _SEMI.search(blob):
        return "semi_auto", CURATION_TIERS["semi_auto"]
    return "manual", CURATION_TIERS["manual"]


def fba_readiness(row) -> float:
    """Graded, not binary: a model can be partly usable.

    Loads (0.25) + has exchanges (0.25) + objective defined (0.25) + solves to a
    plausible growth rate (0.25). 'Plausible' is 0.01-2.0 /h: below that the
    model is effectively dead, above it the medium is unconstrained and the
    number is an artefact rather than a prediction.
    """
    score = 0.0
    if row.get("load_ok"):
        score += 0.25
    if (row.get("n_exchanges") or 0) > 0:
        score += 0.25
    obj = str(row.get("objective_expression") or "").strip()
    if obj and obj.lower() not in {"nan", "0", "0.0", "none"}:
        score += 0.25
    growth = row.get("default_fba_growth")
    if growth is not None and not pd.isna(growth) and 0.01 <= float(growth) <= 2.0:
        score += 0.25
    return score


def biomass_carbon_check(pct_c_biomass: float | None) -> dict:
    """Empirical gate the structural score cannot substitute for.

    Fungal dry weight is 42-53% carbon. Simulating the model on a defined
    medium and asking how much carbon ends up in biomass per unit of objective
    flux tests whether the biomass reaction is normalised to one gram dry
    weight at all -- which no structural statistic reveals.

    This is not redundant with the score. For R. microsporus the structural
    metric ranks iHol first (1461 genes, GPR 0.81) over iCV785 (787 genes,
    GPR 0.75), but iHol reports 59.4% C under its holobiont objective and
    118.8% under the fungal one, meaning neither is per-gDW; iCV785 gives
    46.8%. Growth rates and yields from iHol are therefore not comparable to
    any other model in the set, while iCV785's are.
    """
    if pct_c_biomass is None or pd.isna(pct_c_biomass):
        return {"pct_c_biomass": None, "normalised_per_gdw": None,
                "note": "not computable (no elemental formulas)"}
    ok = 42.0 <= float(pct_c_biomass) <= 53.0
    return {
        "pct_c_biomass": round(float(pct_c_biomass), 1),
        "normalised_per_gdw": bool(ok),
        "note": ("consistent with per-gDW normalisation" if ok else
                 "biomass reaction is NOT per-gDW; growth rate and g/g yield "
                 "are not comparable across models"),
    }


def atp_yield_check(max_atp_per_glucose: float | None) -> dict:
    """Second empirical gate: does the model make ATP out of nothing?

    Complete oxidation of one glucose yields at most ~32 ATP; a model that
    exceeds this contains an energy-generating cycle (EGC) -- a thermodynamically
    infeasible loop, usually a reversible transporter paired with a proton pump,
    that regenerates ATP for free.

    This matters specifically for burden and strain design. Any ATP cost you
    impose on a model with an EGC is absorbed by the cycle at zero cost to
    growth, so the energy component of burden silently evaluates to zero, and
    ATP-consuming pathway designs look free. Measured here on the same defined
    medium as everything else: constrain glucose, maximise a synthetic
    ATP-hydrolysis drain, divide by glucose uptake.
    """
    if max_atp_per_glucose is None or pd.isna(max_atp_per_glucose):
        return {"max_atp_per_glucose": None, "egc_free": None,
                "note": "not computable"}
    v = float(max_atp_per_glucose)
    ok = v <= 35.0
    return {
        "max_atp_per_glucose": round(v, 1),
        "egc_free": bool(ok),
        "note": ("within thermodynamic bound" if ok else
                 "ENERGY-GENERATING CYCLE: ATP costs are absorbed for free, so "
                 "burden and ATP-consuming designs are unreliable"),
    }


def score_candidates(census: pd.DataFrame) -> pd.DataFrame:
    """Score every candidate model; scope and recency normalise within organism.

    Normalising within organism rather than globally is deliberate: the question
    is 'which model for THIS organism', and a global normalisation would let
    S. cerevisiae's exceptionally well-served model set drag down every
    Mucoromycota candidate on axes where no better option exists.
    """
    df = census.copy()

    df["s_fba_ready"] = df.apply(fba_readiness, axis=1)
    df["s_gpr"] = df["gpr_coverage"].fillna(0.0).clip(0, 1)
    # mass_balance_frac in the census is the VIOLATION fraction; invert it.
    # Missing means not checkable (no formulas at all), which is itself a
    # defect, so it scores 0 rather than being dropped.
    df["s_mass_bal"] = (1.0 - df["mass_balance_frac"]).where(
        df["mass_balance_frac"].notna(), 0.0
    ).clip(0, 1)

    tiers = df.apply(
        lambda r: curation_tier(str(r["model_id"]), str(r.get("publication", ""))),
        axis=1,
    )
    df["curation_tier"] = [t[0] for t in tiers]
    df["s_curation"] = [t[1] for t in tiers]

    def _norm_within(group, col, log=False):
        vals = group[col].astype(float)
        if log:
            vals = vals.apply(lambda v: math.log10(v) if v and v > 0 else 0.0)
        lo, hi = vals.min(), vals.max()
        if not (hi > lo):
            return pd.Series(1.0, index=group.index)
        return (vals - lo) / (hi - lo)

    # Score scope on the underlying metabolic map. For an ec-model that is the
    # gene-associated core, approximated by n_genes-scaled reaction count of its
    # parent; without the parent in hand, discount the raw count to the median
    # non-ec count for that organism so the ec expansion neither helps nor hurts.
    df["is_ec"] = df.apply(
        lambda r: is_enzyme_constrained(str(r["model_id"]), str(r.get("publication", ""))),
        axis=1,
    )
    df["scope_basis"] = df["n_reactions"].astype(float)
    for org, grp in df.groupby("organism"):
        non_ec = grp.loc[~grp["is_ec"], "n_reactions"].dropna()
        if len(non_ec) and grp["is_ec"].any():
            df.loc[grp.index[grp["is_ec"]], "scope_basis"] = float(non_ec.median())

    df["s_scope"] = (
        df.groupby("organism", group_keys=False)
        .apply(lambda g: _norm_within(g, "scope_basis", log=True))
        .reindex(df.index)
        .fillna(0.0)
    )
    df["s_recency"] = (
        df.groupby("organism", group_keys=False)
        .apply(lambda g: _norm_within(g, "year"))
        .reindex(df.index)
        .fillna(0.0)
    )

    df["score"] = sum(
        WEIGHTS[k] * df[f"s_{k}"] for k in WEIGHTS
    ).round(4)
    df["rank_in_organism"] = (
        df.groupby("organism")["score"].rank(ascending=False, method="min").astype(int)
    )
    return df.sort_values(["organism", "score"], ascending=[True, False])
