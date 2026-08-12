"""Defined minimal media, and cross-model exchange-ID resolution.

Published fungal GEMs use mutually incompatible exchange naming schemes
(``r_1714`` in yeast-GEM, ``y001714`` in iYali, ``Ex_glc`` in iMT1026,
``EX_glc(e)`` in BiGG-derived files). A single medium therefore cannot be
expressed as literal reaction IDs; it is defined here as *chemical roles*
which are resolved per model by metabolite-name matching.
"""

from __future__ import annotations

import re
from typing import Iterable

# Glucose-limited defined minimal medium, aerobic, ammonium as N source.
# Values are uptake bound magnitudes in mmol gDW^-1 h^-1.
# 10 mmol/gDW/h glucose with unconstrained O2 is the conventional reference
# condition for yeast GEMs and gives growth rates comparable to published
# aerobic batch values.
MINIMAL_GLUCOSE = {
    "glucose": 10.0,
    # Vitamin, not a bulk nutrient: supplied at a low bound so it can satisfy
    # an auxotrophy without becoming an alternative carbon source. Models whose
    # organism is a biotin prototroph simply have no matching exchange and are
    # unaffected.
    "biotin": 0.01,
    "oxygen": 1000.0,
    "ammonium": 1000.0,
    "phosphate": 1000.0,
    "sulphate": 1000.0,
    "water": 1000.0,
    "proton": 1000.0,
    "iron2": 1000.0,
    "potassium": 1000.0,
    "sodium": 1000.0,
    "chloride": 1000.0,
    "magnesium": 1000.0,
    "calcium": 1000.0,
    "copper": 1000.0,
    "manganese": 1000.0,
    "zinc": 1000.0,
    "molybdate": 1000.0,
    # Dissolved CO2 is present in any real aerobic culture and several models
    # require CO2 uptake for anaplerotic carboxylation (iMA871 cannot grow at
    # all without it). It is fully oxidised carbon, so allowing it does not
    # create a free energy source.
    # Export-only. A zero here caps UPTAKE at zero while leaving the export
    # direction untouched, which is the correct heterotrophic convention: these
    # organisms cannot fix CO2 net, and leaving uptake open let iCV785 run a
    # CO2-out/bicarbonate-in cycle at ~420 mmol gDW^-1 h^-1 that made carbon
    # bookkeeping unreadable.
    "co2": 0.0,
    "bicarbonate": 0.0,
    "nitrate": 0.0,        # explicitly closed: ammonium is the N source
    "ethanol": 0.0,
    "acetate": 0.0,
    "glycerol": 0.0,
}

# Synonyms used to identify the exchanged metabolite of each role. Matching is
# done on metabolite name (lowercased); the first alternative that matches wins.
ROLE_SYNONYMS: dict[str, tuple[str, ...]] = {
    # iCV785 (MetaCyc-derived) names glucose by anomer and keeps separate alpha
    # and beta extracellular pools; both are legitimate uptake forms.
    "glucose":    ("d-glucose", "glucose", "glc__d", "glc-d",
                   "alpha-d-glucose", "beta-d-glucose"),
    "oxygen":     ("oxygen", "o2", "dioxygen"),
    "ammonium":   ("ammonium", "ammonia", "nh4", "nh3", "nh4+"),
    "phosphate":  ("phosphate", "orthophosphate", "pi", "hydrogenphosphate"),
    # Some reconstructions offer sulfite rather than sulfate as the S source
    # (iMA871, iWV1314 both do), so both are accepted.
    "sulphate":   ("sulphate", "sulfate", "so4", "sulfite", "sulphite", "h2so3", "so3"),
    "water":      ("water", "h2o"),
    "proton":     ("proton", "h+", "hydrogen ion"),
    "iron2":      ("fe2+", "iron(2+)", "ferrous", "iron(ii)"),
    "potassium":  ("potassium", "k+"),
    "sodium":     ("sodium", "na+"),
    "chloride":   ("chloride", "cl-"),
    "magnesium":  ("magnesium", "mg2+", "mg(2+)"),
    "calcium":    ("calcium", "ca2+", "ca(2+)"),
    "copper":     ("cu2+", "copper", "cupric"),
    "manganese":  ("mn2+", "manganese"),
    "zinc":       ("zn2+", "zinc"),
    "molybdate":  ("molybdate", "moo4"),
    # Kept as separate roles: bicarbonate is a distinct extracellular pool in
    # MetaCyc-derived models (iCV785), and lumping it with CO2 meant one medium
    # entry silently opened two carbon routes.
    "co2":         ("co2", "carbondioxide", "carbon dioxide"),
    "bicarbonate": ("hco3", "bicarbonate", "hydrogencarbonate"),
    "nitrate":    ("nitrate", "no3"),
    "ethanol":    ("ethanol",),
    "acetate":    ("acetate",),
    "glycerol":   ("glycerol",),
    # K. phaffii cannot synthesise biotin de novo and requires it supplied in
    # defined media (this is why BSM/FM22 carry biotin; prototrophy has to be
    # engineered in). iMT1026v3 encodes the auxotrophy faithfully and gives
    # exactly zero growth without Ex_btn, so biotin belongs in the minimal
    # medium as a real nutritional requirement, not as a modelling fudge.
    "biotin":     ("biotin", "btn", "d-biotin"),
}

_COMPARTMENT_TAG = re.compile(r"\s*[\[\(][a-z_ ]{1,20}[\]\)]$")
_CHARGE_PARENS = re.compile(r"\((\d*[+-])\)")
# Several BioModels-hosted reconstructions (iMA871, iWV1314, iLC915) append the
# molecular formula to the metabolite name: "D-glucose_C6H12O6", "oxygen_",
# "Biomass_", "NH3_H3N". The suffix must be stripped before role matching.
_FORMULA_SUFFIX = re.compile(
    r"_(?:[A-Z][a-z]?\d*)*$"  # e.g. _C6H12O6, _H3N, _HSR, or an empty tail
)


def _norm(name: str) -> str:
    """Canonicalise a metabolite name for role matching.

    Strips a trailing compartment tag and normalises parenthesised charges so
    that ``Cu2(+)``, ``Mn(2+)`` and ``iron(2+)`` compare equal to ``cu2+``,
    ``mn2+`` and ``iron2+`` respectively -- the naming varies between models
    and even between species within one model.
    """
    raw = (name or "").strip()
    # Strip the formula suffix on the *original* casing, since the pattern
    # relies on formulas being capitalised (C6H12O6) unlike ordinary words.
    if "_" in raw:
        stripped = _FORMULA_SUFFIX.sub("", raw)
        if stripped:                       # never reduce a name to nothing
            raw = stripped
    s = raw.lower()
    s = _COMPARTMENT_TAG.sub("", s).strip()
    s = _CHARGE_PARENS.sub(r"\1", s)      # mn(2+) -> mn2+ ; cu2(+) -> cu2+
    return s.replace(" ", "")


def _norm_synonyms(role: str) -> frozenset[str]:
    """Role synonyms passed through :func:`_norm`, so both sides compare alike."""
    return frozenset(_norm(s) for s in ROLE_SYNONYMS[role])


_EMBEDDED_FORMULA = re.compile(r"_([A-Z][a-z]?\d*(?:[A-Z][a-z]?\d*)*)$")


def recover_formulas_from_names(model) -> dict:
    """Populate empty ``metabolite.formula`` from a formula embedded in the name.

    iYali4 ships every one of its 1683 metabolites with no formula attribute but
    encodes it in the name ('(R)-carnitine_C7H15NO3'). Without this, no
    mass-balance or carbon-balance check can run on the model at all.

    Reports rather than silently skipping the failures, because they are
    informative: 104 iYali4 metabolite names carry a literal
    'ActiveX VT_ERROR:' string, an Excel export artefact baked into the
    published SBML, and those species genuinely have no recoverable formula.
    """
    recovered = failed = 0
    corrupted: list[str] = []
    for met in model.metabolites:
        if met.formula:
            continue
        name = (met.name or "").strip()
        if "VT_ERROR" in name or "ActiveX" in name:
            corrupted.append(met.id)
            failed += 1
            continue
        match = _EMBEDDED_FORMULA.search(name)
        candidate = match.group(1) if match else None
        if not candidate or len(candidate) > 40:
            failed += 1
            continue
        try:
            met.formula = candidate
            recovered += 1
        except Exception:
            failed += 1
    return {
        "recovered": recovered,
        "failed": failed,
        "n_excel_corrupted": len(corrupted),
        "excel_corrupted_ids": corrupted,
    }


def import_capacity(rxn) -> float:
    """Uptake capacity a boundary reaction permits *as shipped*.

    A boundary reaction carries one metabolite. With coefficient -1 (the usual
    ``A_e -->`` form) import is negative flux, so capacity is ``-lower_bound``;
    with coefficient +1 (``--> A_e``) import is positive flux and capacity is
    ``upper_bound``. Reconstructions that split each transport into two
    irreversible half-reactions (``*_L2R`` / ``*_R2L``) rely on this: the export
    half is structurally incapable of uptake, and opening it does nothing.
    """
    if not rxn.metabolites:
        return 0.0
    coef = next(iter(rxn.metabolites.values()))
    if coef < 0:
        return max(-rxn.lower_bound, 0.0)
    return max(rxn.upper_bound, 0.0)


def resolve_roles(model, roles: Iterable[str] | None = None) -> dict[str, list[str]]:
    """Map each chemical role to the exchange reaction IDs that carry it.

    Works by inspecting the metabolite behind every exchange reaction and
    matching its name against :data:`ROLE_SYNONYMS`. Returns role -> list of
    candidate exchange reaction IDs (empty list when the model has none).
    """
    roles = list(roles) if roles is not None else list(ROLE_SYNONYMS)
    found: dict[str, list[str]] = {r: [] for r in roles}

    # Scan model.boundary, not model.exchanges. cobrapy classifies a boundary
    # reaction by ID prefix and direction, so genuine nutrient supplies land in
    # .sinks or .demands in models that do not use the EX_ convention: iCV785's
    # only ammonia supply is AMMONIA_TRANS_RXN_R2L, classified as a sink. Left
    # out of the medium it is then clamped as a free-carbon route, starving the
    # model of nitrogen and giving a spurious zero growth.
    for rxn in model.boundary:
        for met in rxn.metabolites:
            nm = _norm(met.name) or _norm(met.id)
            mid = _norm(met.id)
            for role in roles:
                # Exact match only. A prefix rule would wrongly capture
                # derivatives -- "d-glucose 6-phosphate exchange" starts with
                # "d-glucose " and would silently triple available carbon.
                syns = _norm_synonyms(role)
                if nm in syns or mid in syns:
                    found[role].append(rxn.id)

    # Rank candidates so an import-capable reaction always precedes an
    # export-only one. iCV785 splits every transport into irreversible
    # *_L2R / *_R2L halves; the export half matches the role name just as well
    # but can never carry uptake, so name matching alone silently starves the
    # model. Ordering is stable within each group.
    out: dict[str, list[str]] = {}
    for role, ids in found.items():
        uniq = list(dict.fromkeys(ids))
        uniq.sort(key=lambda rid: import_capacity(model.reactions.get_by_id(rid)) <= 0)
        out[role] = uniq
    return out


def build_uptake(
    model, medium: dict[str, float] | None = None, verbose: bool = False
) -> tuple[dict[str, float], list[str]]:
    """Translate a role-based medium into ``{exchange_id: bound}`` for a model.

    Returns the uptake dict and the list of roles the model could not supply.
    When a role maps to several exchanges the bound is applied to each; this is
    intentional for redundant transporters, and the returned mapping is
    reported so the choice stays auditable.
    """
    medium = MINIMAL_GLUCOSE if medium is None else medium
    resolved = resolve_roles(model, medium.keys())
    uptake: dict[str, float] = {}
    unmatched: list[str] = []

    for role, bound in medium.items():
        ids = resolved.get(role, [])
        # Drop export-only halves: opening them cannot supply the nutrient, and
        # including them would misreport the medium actually applied.
        importable = [
            rid for rid in ids
            if import_capacity(model.reactions.get_by_id(rid)) > 0
        ]
        ids = importable or ids
        if not ids:
            if bound > 0:
                unmatched.append(role)
            continue
        for rxn_id in ids:
            uptake[rxn_id] = float(bound)
        if verbose:
            print(f"{role:<12} -> {ids}")
    return uptake, unmatched
