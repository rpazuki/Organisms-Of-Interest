# Model census — round 1 (fungal GEM project)

Scope: 47 candidate genome-scale models across the 8 target organisms plus deliberate proxy species. Every row in `model_census.csv` was actually downloaded and loaded in cobrapy 0.31.1; no metric in this document is taken from a paper's abstract. `default_fba_growth` is the objective value of `model.optimize()` **as distributed** — no medium was curated, so a large value means the shipped bounds are open, not that the organism grows that fast.

## How to read the verdict column

- **FBA-READY** — loads, has exchange reactions, solves to a plausible growth rate (0 < mu <= 5 /h).
- **objective=0** — loads and solves but the shipped objective is empty or blocked; needs a biomass objective set.
- **unbounded/unconstrained** — solves at an implausible rate (mu > 5 /h); the distributed medium is wide open.
- **no exchange/boundary reactions** — a closed network; FBA is impossible without adding exchanges.
- **NOT LOADABLE** — cobrapy refuses the file as distributed (see the repair section).

## Per-organism assessment

### Saccharomyces cerevisiae

**Best model: yeast-GEM v9.1.0** (4102 rxns, 1143 genes, 14 compartments, mu=0.0809 /h out of the box).

This is the strongest position of any organism in the project: a genuine consensus community model, actively released (v9.1.0 dated 2026-07-01), with the lowest mass-balance violation rate in the whole census (5.5%).

For enzyme-constrained work, **ecYeastGEM** (8143 rxns) and **ecYeastGEM_batch** (8144 rxns) both load and solve directly in cobrapy — the batch variant gives mu=0.377 /h under its single pooled-enzyme constraint, the non-batch gives 0.088 /h. Note their apparent mass-balance violation rate (44-51%) is an artefact of the GECKO formulation: enzyme-usage pseudo-reactions draw on protein pseudo-metabolites that carry no chemical formula, so `check_mass_balance` flags them. It is not evidence of a curation defect in the underlying network.

**Knowledge gap: effectively none.** S. cerevisiae is the reference against which the other seven should be judged, and the natural proxy donor for the gap organisms.


| model_id | year | n_reactions | n_genes | n_compartments | n_exchanges | gpr_coverage | default_fba_growth | verdict |
|---|---|---|---|---|---|---|---|---|
| yeast-GEM v9.1.0 | 2026 | 4102 | 1143 | 14 | 270 | 0.6538 | 0.08094 | FBA-READY (growth 0.0809) |
| ecYeastGEM | 2022 | 8143 | 1148 | 14 | 484 | 0.7056 | 0.08797 | FBA-READY (growth 0.0880) |
| ecYeastGEM_batch | 2022 | 8144 | 1148 | 14 | 484 | 0.7056 | 0.3768 | FBA-READY (growth 0.3768) |
| CoReCo S.cerevisiae | 2016 | 6051 | 0 | 2 | 2737 | 0 | 0.1238 | FBA-READY (growth 0.1238) |


### Yarrowia lipolytica

**Best model: eciYali5-GEM (2026)** for enzyme-constrained work; **iYali (iYali4)** for plain unconstrained FBA.

This organism has the deepest model lineage after S. cerevisiae — 12 candidates spanning 2012-2026. The important correction to the project's earlier assumption: **eciYali5-GEM ships a real SBML file (`model/eciYali5-GEM.xml`, 3.8 MB), not only GECKO `.yml`** — it loads in cobrapy without modification (3968 rxns, 905 genes, mu=0.664 /h). The GECKO `.yml` limitation does not apply here.

Caveats worth carrying forward:
- `iYali5.xml` (the non-enzyme-constrained 2026 parent) solves at **22.4 /h** — its shipped medium is wide open. Usable, but the medium must be closed before any prediction is trusted.
- `eciYali` (Chalmers ecModels) needed an ID repair to load, and even then the LP returns solver status `error` — prefer `eciYali_batch` (mu=0.276 /h) from that pair.
- `iMK735` is **infeasible as distributed** — do not use without diagnosing its bounds.
- `Loira2012` solves at 3.89 /h (open medium).

**Knowledge gap: small.** Lipid/acetyl-CoA metabolism is well covered; the main risk is medium definition, not network scope.


| model_id | year | n_reactions | n_genes | n_compartments | n_exchanges | gpr_coverage | default_fba_growth | verdict |
|---|---|---|---|---|---|---|---|---|
| eciYali5-GEM | 2026 | 3968 | 905 | 14 | 153 | 0.6653 | 0.6638 | FBA-READY (growth 0.6638) |
| iYali5 | 2026 | 1986 | 904 | 14 | 153 | 0.6521 | 22.35 | Solves but growth 22.35/h implausible -> unbounded/unconstrained medium |
| eciYali | 2022 | n/a | n/a | n/a | n/a | n/a | n/a | NOT LOADABLE in cobrapy |
| eciYali [ID-repaired] | 2022 | 4022 | 847 | 14 | 318 | 0.6798 | n/a | NOT FBA-ready: solver status error |
| eciYali_batch | 2022 | n/a | n/a | n/a | n/a | n/a | n/a | NOT LOADABLE in cobrapy |
| eciYali_batch [ID-repaired] | 2022 | 4023 | 847 | 14 | 318 | 0.6796 | 0.2761 | FBA-READY (growth 0.2761) |
| Lu2021 Y.lipolytica pan-GEM | 2021 | 3814 | 1103 | 14 | 243 | 0.6411 | 0.08478 | FBA-READY (growth 0.0848) |
| CoReCo Y.lipolytica | 2016 | 6181 | 0 | 2 | 2788 | 0 | 0.1318 | FBA-READY (growth 0.1318) |
| iYali (iYali4) | 2016 | 1924 | 848 | 14 | 159 | 0.6622 | 0.1057 | FBA-READY (growth 0.1057) |
| iYali4 | 2016 | 1985 | 901 | 14 | 153 | 0.6514 | 0.05664 | FBA-READY (growth 0.0566) |
| iMK735 | 2015 | 1464 | 735 | 8 | 127 | 0.5676 | 0 | NOT FBA-ready: solver status infeasible |
| Loira2012 (iNL895) | 2012 | 2262 | 899 | 13 | 260 | 0.5279 | 3.888 | FBA-READY (growth 3.8879) |


### Komagataella phaffii (Pichia pastoris)

**Best model: iMT1026 v3** (BioModels MODEL1612130000; 2237 rxns, 1026 genes, mu=0.0578 /h).

This directly resolves the round-0 blocker. The round-0 file (`iMT1026` v1, MODEL1508040001) carries **0 genes and an empty objective**; v3 carries **1026 genes, 66% GPR coverage, and a working biomass objective that solves out of the box**. v3 supersedes v1 for every purpose in this project.

Other options and their traps:
- **Torres2019 contextualized iMT1026v3** — needed an ID repair to load, and is then **infeasible** as shipped (its contextualizing constraints are mutually inconsistent without the accompanying medium). Not recommended as a base model.
- **Lu2021 K. pastoris pan-GEM** (3811 rxns) is larger and solves at 0.093 /h — good cross-organism comparability since it was built by the same pipeline as the Y. lipolytica and F. graminearum pan-GEMs.
- **ihGlycopastoris** (Irani2015) adds N-glycosylation detail, solves at 0.080 /h — the right choice specifically for glycoprotein/secretion questions.
- `iLC915` (79.0 /h), `PpaMBEL1254` (78.7 /h, 1 compartment, 0 genes) and `iPP668` (3.89 /h, 0 genes) are all open-medium and/or gene-free; treat as historical.
- `PpaCore_3HP` (MODEL2210090004) is **not a GEM** — it is a `.ftbl` 13C-MFA core model. Excluded from the census by design.

**Knowledge gap: small-to-moderate.** Central metabolism and methanol utilisation are covered; secretion-pathway burden is the weak spot, which is exactly the burden-modelling target.


| model_id | year | n_reactions | n_genes | n_compartments | n_exchanges | gpr_coverage | default_fba_growth | verdict |
|---|---|---|---|---|---|---|---|---|
| Lu2021 K.pastoris pan-GEM | 2021 | 3811 | 910 | 14 | 243 | 0.6408 | 0.09286 | FBA-READY (growth 0.0929) |
| iMT1026v3 contextualized | 2019 | n/a | n/a | n/a | n/a | n/a | n/a | NOT LOADABLE in cobrapy |
| iMT1026v3 contextualized [ID-repaired] | 2019 | 2246 | 1026 | 9 | 176 | 0.6572 | 0 | NOT FBA-ready: solver status infeasible |
| Cetinkaya2017 | 2017 | 2382 | 861 | 9 | 908 | 0.4769 | 0.157 | FBA-READY (growth 0.1570) |
| iMT1026 (v1) | 2016 | 2220 | 0 | 9 | 175 | 0 | 0 | Loads+solves but objective=0 (needs biomass objective / medium set) |
| iMT1026 v3 | 2016 | 2237 | 1026 | 9 | 175 | 0.6598 | 0.05775 | FBA-READY (growth 0.0578) |
| ihGlycopastoris | 2015 | 1595 | 916 | 7 | 73 | 0.6658 | 0.08024 | FBA-READY (growth 0.0802) |
| iLC915 | 2012 | 1423 | 915 | 7 | 54 | 0.7154 | 79.02 | Solves but growth 79.02/h implausible -> unbounded/unconstrained medium |
| PpaMBEL1254 | 2010 | 1254 | 0 | 1 | 59 | 0 | 78.7 | Solves but growth 78.70/h implausible -> unbounded/unconstrained medium |
| iPP668 | 2010 | 1361 | 0 | 8 | 149 | 0 | 3.891 | FBA-READY (growth 3.8915) |


### Aspergillus niger

**Best model: iJB1325** (Brandl et al. 2018, community-driven; 2320 rxns, 1325 genes, 7 compartments).

A large improvement over the round-0 `iMA871`, which has **0 genes** and solves at an implausible 27.8 /h. iJB1325 has full GPRs (57% coverage), the **lowest mass-balance violation rate of any filamentous model in the census (4.0%)**, and 662 blocked reactions out of 2320 (29%) — a real, quantified curation gap but a normal one for a filamentous fungus.

One caveat to flag clearly: iJB1325 solves at **0.94 /h**, which is far above a realistic A. niger growth rate (~0.1-0.25 /h). This is an open-medium artefact, not a network error — the medium must be constrained before use.

`An_curated.xml` is a MEMOTE-ready curated derivative of iJB1325 and is numerically identical on every metric measured here; either file works.

I could **not** retrieve the two enzyme-constrained/expanded A. niger models — see the 'found but not retrieved' section.

**Knowledge gap: moderate.** Organic-acid overflow metabolism is the best-documented part; secretion and morphology-linked maintenance costs are not represented.


| model_id | year | n_reactions | n_genes | n_compartments | n_exchanges | gpr_coverage | default_fba_growth | verdict |
|---|---|---|---|---|---|---|---|---|
| iJB1325 (curated) | 2026 | 2320 | 1325 | 7 | 375 | 0.5737 | 0.9399 | FBA-READY (growth 0.9399) |
| iJB1325 | 2018 | 2320 | 1325 | 7 | 375 | 0.5737 | 0.9399 | FBA-READY (growth 0.9399) |
| CoReCo A.niger (Castillo) | 2016 | 7091 | 0 | 2 | 3211 | 0 | 0 | Loads+solves but objective=0 (needs biomass objective / medium set) |
| CoReCo A.niger (Pitkanen) | 2014 | 2249 | 0 | 1 | 0 | 0 | 0 | NOT FBA-ready: no exchange/boundary reactions |
| iMA871 | 2008 | 1400 | 0 | 3 | 166 | 0 | 27.79 | Solves but growth 27.79/h implausible -> unbounded/unconstrained medium |


### Aspergillus oryzae

**Best model: iWV1346 / sysbiomics A. oryzae** (2360 rxns, 1346 genes, **83.9% GPR coverage — the highest of any filamentous model in this census**, mu=0.138 /h).

The 2025 engineered-strain paper (PMID 40725156, DOI 10.3390/ijms26146906) **does have a retrievable model file** — `newOryzae2.xml` in the `nachonase/corOryzae` repository. It required an ID repair to load (see below), after which it gives 2025 rxns, 1781 genes (the largest gene set of any A. oryzae model here) and mu=0.0326 /h. It is the most recent option; `iWV1346` is the safer default because it loads unmodified.

The round-0 `iWV1314` solves at 25.7 /h (open medium) and is superseded.

**Knowledge gap: moderate**, but this organism is in better shape than T. reesei or Rhizopus — it has both high GPR coverage and a 2025 model.


| model_id | year | n_reactions | n_genes | n_compartments | n_exchanges | gpr_coverage | default_fba_growth | verdict |
|---|---|---|---|---|---|---|---|---|
| corOryzae (newOryzae2) | 2025 | n/a | n/a | n/a | n/a | n/a | n/a | NOT LOADABLE in cobrapy |
| corOryzae (newOryzae2) [ID-repaired] | 2025 | 2025 | 1781 | 4 | 139 | 0.798 | 0.03259 | FBA-READY (growth 0.0326) |
| iWV1346 | 2019 | 2360 | 1346 | 4 | 82 | 0.839 | 0.1381 | FBA-READY (growth 0.1381) |
| sysbiomics A.oryzae | 2019 | 2360 | 1346 | 4 | 82 | 0.839 | 0.1381 | FBA-READY (growth 0.1381) |
| CoReCo A.oryzae (Castillo) | 2016 | 7263 | 0 | 2 | 3279 | 0 | 0.09074 | FBA-READY (growth 0.0907) |
| iWV1314 | 2008 | 2361 | 1346 | 4 | 82 | 0.8391 | 25.68 | Solves but growth 25.68/h implausible -> unbounded/unconstrained medium |


### Trichoderma reesei

**Best model: Castillo2016 CoReCo T. reesei** (BioModels MODEL1604280024) — and this is a **material correction to the round-0 conclusion**.

Round-0 recorded T. reesei as having only a non-FBA-capable CoReCo draft. That is true of the *Pitkanen2014* draft (MODEL1302010019: 0 exchanges, 1 compartment — FBA impossible). But the **Castillo2016** model from the 'whole-genome metabolic model built by comparative reconstruction' paper is a different, later file: 7296 reactions, 3289 exchange reactions, 2 compartments, and it **solves to mu=0.0899 /h**. T. reesei is therefore FBA-capable today, which it was not thought to be.

The hard limitation remains: **0 genes and 0% GPR coverage**. With no gene-protein-reaction associations there is **no way to simulate a gene knockout or a heterologous-enzyme burden** on this model. It supports flux-space and yield questions only.

**Knowledge gap: large.** No manually curated, gene-associated T. reesei GEM was found anywhere. For any gene-level strain-design question, a proxy host (A. oryzae or A. niger, both gene-complete) is required.


| model_id | year | n_reactions | n_genes | n_compartments | n_exchanges | gpr_coverage | default_fba_growth | verdict |
|---|---|---|---|---|---|---|---|---|
| CoReCo T.reesei (Castillo) | 2016 | 7296 | 0 | 2 | 3289 | 0 | 0.0899 | FBA-READY (growth 0.0899) |
| CoReCo T.reesei (Pitkanen) | 2014 | 2145 | 0 | 1 | 0 | 0 | 0 | NOT FBA-ready: no exchange/boundary reactions |


### Rhizopus microsporus var. oligosporus

**Best model: iHol** (Gonzalez-Hernandez et al. 2024, PMID 38072824; 2478 rxns, 1461 genes, 80.9% GPR coverage, mu=0.112 /h) — a **major upgrade over the round-0 position** and the single most valuable find of this round.

Round-0 recorded Rhizopus as having only an automated CoReCo draft with 0 genes and no exchanges. iHol is a manually built, gene-associated, FBA-ready model of **R. microsporus specifically — the project's actual target species**, not a substitute. Its mass-balance violation rate (3.0%) is the lowest of any filamentous model here.

iHol is a *holobiont* model: it represents the fungus together with its *Mycetohabitans* bacterial endosymbiont and a viral partner. The repository also ships the members separately — **iCV785** (1359 rxns, 787 genes, mu=0.116 /h) is the fungal/cured member and is the right file for questions about the fungus alone; **iCV675** (1125 rxns, 677 genes) is the bacterial symbiont and solves at 1.23 /h.

Two caveats: the strain is *R. microsporus*, not specifically var. *oligosporus* (the tempeh variety), so variety-level differences are uncharacterised; and the holobiont framing means iHol's biomass includes symbiont demands. For var. *oligosporus* work, use **iCV785** and treat the variety difference as an explicit correction term.

**Knowledge gap: moderate** (was: severe). Now gene-level tractable, which it was not before.


| model_id | year | n_reactions | n_genes | n_compartments | n_exchanges | gpr_coverage | default_fba_growth | verdict |
|---|---|---|---|---|---|---|---|---|
| iCV675 | 2024 | 1125 | 677 | 3 | 48 | 0.8844 | 1.228 | FBA-READY (growth 1.2283) |
| iCV785 | 2024 | 1359 | 787 | 6 | 104 | 0.7476 | 0.1157 | FBA-READY (growth 0.1157) |
| iHol (holobiont) | 2024 | 2478 | 1461 | 8 | 144 | 0.8091 | 0.1125 | FBA-READY (growth 0.1125) |


### Rhizopus / Mucoromycota (other)

The two CoReCo *R. oryzae* drafts are retained for completeness only. Pitkanen2014 (MODEL1302010018) has **0 exchanges** and cannot do FBA at all; Castillo2016 (MODEL1604280023) has exchanges but an **empty objective** (solves to 0). Both have 0 genes. Superseded by iHol/iCV785 for every purpose.


| model_id | year | n_reactions | n_genes | n_compartments | n_exchanges | gpr_coverage | default_fba_growth | verdict |
|---|---|---|---|---|---|---|---|---|
| CoReCo R.oryzae (Castillo) | 2016 | 6715 | 0 | 2 | 3030 | 0 | 0 | Loads+solves but objective=0 (needs biomass objective / medium set) |
| CoReCo R.oryzae (Pitkanen) | 2014 | 2124 | 0 | 1 | 0 | 0 | 0 | NOT FBA-ready: no exchange/boundary reactions |


### Fusarium venenatum — proxy: F. graminearum

**No genome-scale metabolic model of *Fusarium venenatum* exists.** This is a confirmed negative, not a retrieval failure. Checked this round: BioModels full-text search for `venenatum`, `Fusarium venenatum`, `mycoprotein` and `Quorn` returns **0 matches each**; GitHub repository search for `venenatum` returns 2 repositories, both genome-annotation work (`harrisonlab/fusarium_venenatum`) with no metabolic model; Europe PMC returns no reconstruction paper. Round-0 reached the same conclusion by different query forms.

**Best proxy: Lu2021 F. graminearum** (4093 rxns, 1611 genes, 66.6% GPR coverage, mu=0.0904 /h), extracted from the Lu2021 `outgroup.zip` archive. Two properties make it the right choice: it is the same genus as the target, and it was built by the **same pan-GEM pipeline** as the Lu2021 Y. lipolytica and K. phaffii models — so proxy-vs-host differences reflect biology rather than differing reconstruction conventions.

The CoReCo F. graminearum draft (MODEL1302010026) has 0 exchanges and 0 genes; unusable.


| model_id | year | n_reactions | n_genes | n_compartments | n_exchanges | gpr_coverage | default_fba_growth | verdict |
|---|---|---|---|---|---|---|---|---|
| Lu2021 F.graminearum | 2021 | 4093 | 1611 | 14 | 243 | 0.6663 | 0.09036 | FBA-READY (growth 0.0904) |
| CoReCo F.graminearum | 2014 | 2182 | 0 | 1 | 0 | 0 | 0 | NOT FBA-ready: no exchange/boundary reactions |


### Fusarium venenatum — proxy: F. fujikuroi

**Second proxy option: iCY1235** (PMID 37931026, 2023; 1753 rxns, 1235 genes, 82.9% GPR coverage, mu=0.166 /h).

This is a *manually curated* Fusarium GEM — higher GPR coverage and a far lower mass-balance violation rate (10.8%) than the Lu2021 pan-GEM (41.2%). The trade-off: *F. fujikuroi* is a gibberellin producer, phylogenetically further from *F. venenatum* than *F. graminearum*, and the model is tuned toward terpenoid production.

Recommendation: use **Lu2021 F. graminearum** as the primary proxy (phylogeny + pipeline consistency) and **iCY1235** as a cross-check. Agreement between two independent proxies is the only available confidence signal for F. venenatum predictions.


| model_id | year | n_reactions | n_genes | n_compartments | n_exchanges | gpr_coverage | default_fba_growth | verdict |
|---|---|---|---|---|---|---|---|---|
| iCY1235 | 2023 | 1753 | 1235 | 4 | 89 | 0.8289 | 0.1659 | FBA-READY (growth 0.1659) |


## Models that needed repair to load

Four files fail in cobrapy as distributed. The cause in every case is the same and is worth recording, because the error message cobrapy surfaces ("model is not valid") points at SBML validity and is misleading:

These files encode identifiers using COBRA character escapes — `__32__` for a space, `__160__` for a non-breaking space. cobrapy decodes those escapes back into literal whitespace, then hands the result to optlang, which rejects variable names containing whitespace. The SBML itself is structurally fine (libSBML reports 0 errors for the Torres2019 file). The fix is to replace whitespace-producing escapes with `_` across identifier attributes only, leaving human-readable `name` and `chemicalFormula` attributes untouched.

Repaired copies are included in the tarball with an `_idfix.xml` suffix, alongside `REPAIR_LOG.json`. **Both the original and repaired file are shipped** so the modification is auditable.

| original file | escaped-space occurrences | loads after repair | reactions |
|---|---|---|---|
| eciYali.xml | 6 | True | 4022 |
| eciYali_batch.xml | 6 | True | 4023 |
| corOryzae_newOryzae2.xml | 274 | True | 2025 |
| Torres2019_iMT1026v3_ctx_MODEL1910040001.xml | 6 | True | 2246 |


After repair: `eciYali_batch` and `corOryzae (newOryzae2)` become FBA-ready. `eciYali` loads but its LP returns solver status `error`, and `Torres2019 iMT1026v3 contextualized` loads but is infeasible — those two are genuinely unusable as distributed, for reasons beyond the ID encoding.

## Models found in the literature but NOT retrieved

Recorded as retrieval failures, **not** as evidence the models do not exist:

- **ec_iJB1325** — enzyme-constrained A. niger (Ozturk/Upton et al. 2021, PMID 34193117, DOI 10.1186/s12934-021-01614-2). The paper is indexed and open-access, but Europe PMC returns HTTP 404 for its `supplementaryFiles` endpoint and no GitHub repository search surfaced the model. Very likely obtainable from the journal's own supplementary-file URLs (not on the network allowlist) or by emailing the authors.
- **iHL1210** — expanded A. niger reconstruction (Lu et al. 2017, PMID 27696371, DOI 10.1002/bit.26195). Same situation: Europe PMC `supplementaryFiles` 404s, and Wiley supplementary hosting is not reachable from here. Note iJB1325 (2018) is newer and is in hand, so this is a low-priority gap.
- **eciYali5 GECKO `.yml` context-specific variants** — 12 condition-specific `.yml` files exist in the `bioengtaltech/eciYali5-GEM` repository. These are GECKO/RAVEN YAML, which cobrapy cannot parse; they would need MATLAB+RAVEN or a YAML-to-SBML conversion. Not a blocker, because the repository's own `eciYali5-GEM.xml` SBML export covers the base model.
- **A. niger 2021 enzyme-constrained model via BiGG** — not applicable. The BiGG API was queried directly and contains **no filamentous fungal models at all**; its only relevant entries are `iMM904` and `iND750` (S. cerevisiae). BiGG is not a source for this project.

## Cross-cutting observations

1. **The CoReCo family splits into two generations that behave very differently.** The Pitkanen2014 drafts (T. reesei, R. oryzae, A. niger, F. graminearum) have 0 exchange reactions and cannot do FBA at all. The Castillo2016 drafts of the same species have ~3000 exchanges and mostly do solve. Any statement of the form 'only a CoReCo draft exists, so FBA is impossible' must specify which generation — for T. reesei it is wrong.
2. **Gene coverage, not reaction count, is the binding constraint for strain design.** Every CoReCo model in the census reports 0 genes, so none of them can support a knockout or a gene-level burden simulation regardless of how many reactions it contains. On this criterion the organisms sort into gene-complete (S. cerevisiae, Y. lipolytica, K. phaffii, A. niger, A. oryzae, R. microsporus via iHol/iCV785, and both Fusarium proxies) and gene-absent (**T. reesei alone**).
3. **`default_fba_growth` is a diagnostic of the shipped medium, not a biological rate.** Nine models solve above 5 /h. Before any quantitative flux claim, each selected model needs its exchange bounds set deliberately.
4. **Mass-balance violation rates are not comparable across model classes.** Enzyme-constrained (GECKO) models show 35-51% because protein pseudo-metabolites carry no formula; CoReCo models show 0.0% because they carry no formulas to check at all. Only within-class comparison is meaningful — among curated filamentous models, iHol (3.0%), iJB1325 (4.0%) and iCY1235 (10.8%) are the cleanest.
5. **Blocked-reaction counts are mostly absent by design.** `find_blocked_reactions` was capped at 2500 reactions; it completed for iJB1325 (662 blocked / 2320 = 28.5%) but did not converge within a 30-minute budget on the enzyme-constrained and repaired models, where it was deliberately skipped and recorded as such rather than left to hang.

## Recommended base model per organism

| organism | recommended model | why | FBA-ready as shipped |
|---|---|---|---|
| S. cerevisiae | yeast-GEM v9.1.0 | consensus, current, cleanest balance | yes (0.081 /h) |
| S. cerevisiae (enzyme-constrained) | ecYeastGEM_batch | loads in cobrapy directly | yes (0.377 /h) |
| Y. lipolytica | iYali (iYali4) | loads unmodified, plausible rate | yes (0.106 /h) |
| Y. lipolytica (enzyme-constrained) | eciYali5-GEM | 2026, SBML provided, no repair needed | yes (0.664 /h) |
| K. phaffii | iMT1026 v3 | 1026 genes + working objective vs v1's 0 genes | yes (0.058 /h) |
| A. niger | iJB1325 | community model, full GPRs, 4% imbalance | yes (0.940 /h, open medium) |
| A. oryzae | iWV1346 | 83.9% GPR coverage, loads unmodified | yes (0.138 /h) |
| T. reesei | Castillo2016 CoReCo | only FBA-capable T. reesei model; **0 genes** | yes (0.090 /h) |
| R. microsporus | iCV785 (fungus) / iHol (holobiont) | 2024, gene-associated, correct species | yes (0.116 / 0.112 /h) |
| F. venenatum | **none exists** — proxy Lu2021 F. graminearum | same genus, same pipeline as other pan-GEMs | proxy yes (0.090 /h) |
