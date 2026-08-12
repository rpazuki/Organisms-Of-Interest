# Model selection: metric, results, and where the metric was overruled

47 candidate reconstructions were scored across the eight organisms
(`model_selection_scores.csv`). *K. phaffii* has 10 candidates and
*Y. lipolytica* 12, spanning 2010-2026, so an ad-hoc "use the newest" or "use
the biggest" rule was not defensible.

## The composite score

Six weighted axes, implemented in `src/fungal_fba/select.py`. The weights encode
a purpose — strain design with gene knockouts — and are meant to be re-weighted
if the purpose changes.

| axis | weight | rationale |
|---|---|---|
| FBA readiness | 0.30 | graded, not binary: loads / has exchanges / objective defined / solves to a plausible rate. Everything else is worthless without it. |
| GPR coverage | 0.25 | bounds what fraction of the map a genetic intervention can reach. A gene-less draft cannot rank a knockout. |
| mass balance | 0.15 | unbalanced reactions are routes to free mass and inflate yield plausibly. |
| scope | 0.15 | reaction count, log-scaled, normalised within organism. |
| curation tier | 0.10 | consensus > manual > semi-automated > automated draft. |
| recency | 0.05 | deliberately smallest: iLC915 (2012) outranks two later *K. phaffii* models on every axis that matters. |

Scope and recency normalise **within organism**, not globally, so that
*S. cerevisiae*'s unusually rich model set cannot depress candidates for
organisms where no better option exists.

### One correction made during development

The first scoring run ranked ecYeastGEM *above* yeast-GEM, the consensus model it
is derived from, because its 8144 reactions scored maximum on scope against
yeast-GEM's 4102. Those extra reactions are per-isozyme arm reactions and
enzyme-usage pseudoreactions wrapping the same metabolic map, not additional
biochemistry. Enzyme-constrained models are now detected and their scope basis
discounted to the median non-ec count for that organism, so the expansion
neither helps nor hurts. yeast-GEM then ranks first, as it should.

## Two empirical gates the score cannot replace

A structural score reads the SBML. It cannot tell you whether the model behaves
physically. Both gates below are computed by simulation on the same defined
glucose medium.

**Gate 1 — biomass normalisation.** Fungal dry weight is 42-53% carbon. Ask how
much carbon ends up in biomass per unit objective flux; if it falls outside that
band the biomass reaction is not per gram dry weight, and growth rates and g/g
yields are not comparable to any other model.

**Gate 2 — energy-generating cycles.** Complete glucose oxidation yields at most
~32 ATP. A model exceeding this contains a thermodynamically infeasible loop
that regenerates ATP for free, which silently zeroes any ATP cost you impose —
including the energy term of burden.

## Final selections

| organism | model | metric rank | verdict |
|---|---|---|---|
| *S. cerevisiae* | yeast-GEM v9.1.0 | 1 | trustworthy |
| *Y. lipolytica* | Lu2021 pan-GEM | 1 | trustworthy |
| *K. phaffii* | Lu2021 pan-GEM | 1 | trustworthy |
| *A. niger* | iJB1325 (curated) | 1 | **EGC present** — burden unreliable |
| *A. oryzae* | iWV1346 | 1 | **EGC present** — burden unreliable |
| *R. microsporus* | iCV785 | 3 | trustworthy — **metric overruled**, see below |
| *F. venenatum* | Lu2021 *F. graminearum* | 1 | proxy host; no *F. venenatum* GEM exists |
| *T. reesei* | CoReCo Castillo2016 | 1 | **0 genes** — no gene-level design possible |

Three selections changed from the round-0 set on empirical evidence: the
*Y. lipolytica* and *K. phaffii* pan-GEMs replaced iYali4 and iMT1026 v3 because
they leave 1 rather than 10 and 7 medium roles unmatched, and close carbon
better; iJB1325's curated revision replaced the 2018 original.

### Where the metric was overruled: *R. microsporus*

The metric ranks `iHol` first — 1461 genes against iCV785's 787, GPR 0.81 vs
0.75. `iHol` is a holobiont reconstruction of the fungus with its bacterial
endosymbiont. Its objective, `System_growth`, proved to be a fixed-ratio
composite:

```
0.5 FUNGAL_BIOMASS + 0.15 Bact_BIOMASS + 0.1 20S + 0.1 23S + 0.15 Rhizoxin -->
```

Solving for the fungal biomass reaction alone returns exactly half the
`System_growth` rate, matching the 0.5 coefficient — confirming the objective is
a composite, not a per-gDW fungal growth rate. Neither objective passes gate 1
(59.4% C under `System_growth`, 118.8% under fungal biomass); iCV785 gives
46.8%.

**iCV785 adopted despite ranking third.** `iHol` is retained as the better
source of gene-level coverage, and remains the right model for any question
about the endosymbiosis itself — but its rates are not comparable to the other
seven hosts.

This case is the reason gate 1 exists in the module: no structural statistic
reveals whether a biomass reaction is normalised per gram dry weight. Only
simulation does.
