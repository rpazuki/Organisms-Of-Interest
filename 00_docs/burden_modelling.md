# Burden modelling: three approaches, and which to use first

## The problem

Plain FBA maximising growth reports a production strain growing exactly as fast
as its parent. Nothing in the stoichiometric matrix knows that recombinant
product consumes precursors, ATP and ribosomal capacity that would otherwise
have made biomass. Every in-silico design that ignores this overestimates yield,
and the error grows with titre — which is precisely the regime strain design
targets.

## Approach 1 — Fixed growth-rate penalty

Constrain the biomass reaction to a fraction of the wild-type rate measured for
the production strain.

- **Needs:** one growth-rate measurement per construct.
- **Gives:** a correctly-sized flux redistribution at that operating point.
- **Does not give:** any prediction of *why* growth fell, so it cannot rank two
  constructs you have not yet built. It encodes the answer rather than deriving
  it.
- **Use when:** you already have the strain and want realistic flux maps.

## Approach 2 — Explicit product sink and growth-coupled sweep (recommended start)

Add a reaction consuming the product's precursors (amino acids for protein,
pathway intermediates for a metabolite) plus the polymerisation ATP, then sweep
enforced product flux and re-maximise growth. This is implemented in
`src/fungal_fba/burden.py` and demonstrated in `burden_envelopes.csv`.

- **Needs:** only the product's composition. Known for every target these hosts
  are used for.
- **Gives:** a production envelope; its slope is a single number — growth rate
  lost per unit product — that ranks hosts and constructs before anything is
  built. Measured slopes for hen lysozyme across this organism set span
  -11.3 to -14.8 h^-1 per mmol gDW^-1 h^-1.
- **Critical detail:** the ATP term is what makes this a burden rather than a
  relabelled biomass drain. Without it the model makes protein from free amino
  acids and the penalty largely vanishes. It contributes 6.5-21.7% of total
  burden in the models where it can be evaluated at all.
- **Known underestimate:** ribosome and tRNA machinery are not in any of these
  GEMs, so translation apparatus cost is absent. Reported burden is therefore a
  lower bound.

## Approach 3 — Enzyme-constrained (GECKO) models

Enzyme-constrained reconstructions add a shared protein-pool constraint, so
expressing a heterologous enzyme genuinely competes with native enzymes for
finite proteome capacity.

- **Needs:** kcat values and a parameterised ec-model.
- **Gives:** the mechanistically correct account of proteome burden, including
  the overflow and Crabtree behaviour that stoichiometric models cannot produce.
- **Availability in this organism set:** ecYeastGEM (*S. cerevisiae*) and
  eciYali5-GEM (*Y. lipolytica*) only. For the other six hosts this would mean
  building an ec-model first, which is a project in itself.
- **Use when:** the design is enzyme-expression-limited, and only for those two
  hosts.

## Recommended sequence for this project

1. Run approach 2 for all eight hosts to rank them and to size the trade-off.
   Already done; see `fig_selection_burden.png` panel d.
2. For the two hosts with ec-models, repeat under approach 3 and compare. The
   gap between the two estimates is itself informative — it quantifies how much
   burden is proteome-mediated rather than precursor-mediated.
3. Calibrate approach 1 against measured growth once strains exist, and use the
   residual to check whether approaches 2/3 captured the real cost.

## Hard caveat: two hosts cannot support this yet

`iJB1325` (*A. niger*) and `iWV1346` (*A. oryzae*) both contain
energy-generating cycles — they produce 49 and 102 ATP per glucose against a
thermodynamic maximum near 32. Any ATP cost imposed on these models is absorbed
by the cycle at zero cost to growth, which is exactly why *A. oryzae* shows a
0% ATP contribution to burden while every well-behaved model shows 6-22%.
Burden numbers for these two hosts are precursor-only and should not be compared
against the others until the cycles are found and removed.

`CoReCo T. reesei` has no genes at all, so no knockout or overexpression design
is possible regardless of burden formulation.

## Demonstration product

Hen egg-white lysozyme (UniProt P00698), mature chain residues 19-147 after
signal-peptide removal, 129 residues. Chosen because it is the classic secreted
model protein for *K. phaffii* and its composition is unambiguous. Sequence
retrieved from UniProt, not reconstructed from memory; see
`product_lysozyme_P00698.fasta`.
