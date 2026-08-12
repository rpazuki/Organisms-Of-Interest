# Literature coverage: what would PubMed alone have missed?

Round-1 multi-source retrieval for the fungal GEM/FBA project. All five required sources were queried with a shared query battery so per-source coverage is comparable. Merged pool: **3822** deduplicated works; curated set: **242** works (`publications.csv`, `references.bib`).

Deduplication key: normalised DOI, falling back to PMID, then to a normalised (case-, punctuation- and diacritic-stripped) title used only when ≥25 characters. Records were merged with a union-find pass, so a work found under three different identifiers collapses to one row and every identifier is retained.

## 1. Headline answer

Of the 242 curated works, **134 (55.4%)** were returned by our PubMed queries; **108 (44.6%, 45% rounded) were not.** That gap splits into two effects which must not be conflated:

1. **36 works are not indexed in PubMed at all.** Verified by re-querying PubMed for each DOI directly (`"<doi>"[AID]`). These are structurally invisible to PubMed: bioRxiv/openRxiv preprints, and articles in engineering and computational journals outside MEDLINE coverage. No amount of PubMed query tuning recovers them.
2. **72 works are indexed in PubMed but were not surfaced by our PubMed query set.** They were recovered only because Crossref, OpenAlex or Europe PMC matched them under different term weighting. This is a recall limitation of any single query formulation — and it is the larger of the two effects.

(134 + 72 + 36 = 242.)

Both matter. The first is a hard coverage boundary of PubMed as a database. The second shows that multi-source querying also buys robustness against query wording — the failure mode a single-database review cannot detect from the inside, because a query that returns plausible results gives no signal about what it silently omitted.

Of the 108 works PubMed did not return, **79 are key papers** (reconstructions, ecModels, model-quality tools or genome/annotation papers for the gap organisms) — so the omission is not confined to peripheral literature.

## 2. Per-source contribution (curated set, n = 242)

| Source | Works returned | % of curated set | Unique to this source | % unique |
|---|---|---|---|---|
| PubMed/PMC | 134 | 55.4% | 30 | 12.4% |
| Europe PMC | 89 | 36.8% | 8 | 3.3% |
| Crossref | 111 | 45.9% | 38 | 15.7% |
| OpenAlex | 124 | 51.2% | 13 | 5.4% |
| bioRxiv/medRxiv | 11 | 4.5% | 2 | 0.8% |

"Unique to this source" = returned by that source and by no other. Columns do not sum to the corpus size because most works were returned by two to four sources.

Overlap profile: **91** works found by 1 source, **90** works found by 2 sources, **46** works found by 3 sources, **15** works found by 4 sources. The 91 single-source works are the concrete cost of dropping any one database.

## 3. Per-source contribution (full merged pool, n = 3822)

Raw retrieval breadth, before topical curation.

| Source | Works returned | % of pool | Unique to this source | % unique |
|---|---|---|---|---|
| PubMed/PMC | 1059 | 27.7% | 745 | 19.5% |
| Europe PMC | 1355 | 35.5% | 998 | 26.1% |
| Crossref | 970 | 25.4% | 795 | 20.8% |
| OpenAlex | 1069 | 28.0% | 617 | 16.1% |
| bioRxiv/medRxiv | 118 | 3.1% | 84 | 2.2% |

In the raw pool 2763 of 3822 works (72.3%) were not returned by PubMed. The curated percentage is lower because curation selects for well-indexed modelling literature — which is itself a mild bias toward what PubMed covers well.

## 4. What each source contributed that the others did not

| Source | Distinctive contribution observed in this run |
|---|---|
| PubMed/PMC | Largest single contributor (134 works) and the source of PMIDs/PMCIDs used as dedup keys and as MeSH-quality provenance. Blind to preprints and to non-MEDLINE engineering venues. |
| Europe PMC | Indexes preprints (`PPR` source) alongside journal articles, and returns `commentCorrectionList` — the field that detected all three errata in this corpus. |
| Crossref | Largest source of single-database works (38). Publisher-deposited and DOI-level, so it reaches engineering/computational journals, book chapters and theses that have no PMID. |
| OpenAlex | Supplied citation counts for 239 curated works plus `is_retracted` flags, and its topic index surfaced cross-organism methodology papers that organism-keyword queries missed. |
| bioRxiv/medRxiv | The only route to unpublished preprints and to preprint→published linkage. Contributed 11 curated works, 2 found by no other source. |

## 5. Works genuinely absent from PubMed (n = 36)

Verified DOI-by-DOI. Venue distribution:

| Venue | Works |
|---|---|
| bioRxiv (Cold Spring Harbor Laboratory) | 4 |
| openRxiv | 3 |
| Biochemical Engineering Journal | 2 |
| bioRxiv | 2 |
| New Biotechnology | 2 |
| Bioresources and Bioprocessing | 1 |
| GAZI UNIVERSITY JOURNAL OF SCIENCE | 1 |
| Biotechnology and Bioprocess Engineering | 1 |
| Synthetic and Systems Biotechnology | 1 |
| Modern Trends in Biothermokinetics | 1 |
| Computational and Structural Biotechnology Journal | 1 |
| Elsevier BV | 1 |
| Processes | 1 |
| Springer Science and Business Media LLC | 1 |
| Biocomputing 2005 | 1 |
| Industrial Biotechnology | 1 |
| Pontificia Universidad Catolica de Chile | 1 |
| Office of Scientific and Technical Information (OSTI) | 1 |
| Yarrowia Lipolytica Yeast | 1 |
| 4ID | 1 |
| Biotechnology and Biology of Trichoderma | 1 |
| Vilnius University Press | 1 |
| Americanae (AECID Library) | 1 |
| Advances in Intelligent Systems and Computing | 1 |
| Food Hydrocolloids | 1 |
| Fermentation | 1 |
| Journal of Proteome Research | 1 |
| (unknown) | 1 |

Highest-scoring examples:

| Year | Sources | Title | DOI |
|---|---|---|---|
| 2025 | bioRxiv/medRxiv, Crossref, OpenAlex | An Improved Systematic Method for Constructing Enzyme-Constrained Genome-Scale Metabolic... | 10.1101/2025.10.29.684458 |
| 2023 | bioRxiv/medRxiv, Crossref, OpenAlex | Yeast9: A Consensus Yeast Metabolic Model Enables Quantitative Analysis of Cellular Meta... | 10.1101/2023.12.03.569754 |
| 2021 | bioRxiv/medRxiv, Crossref, OpenAlex | Genome scale modeling of the protein secretory pathway reveals novel targets for improve... | 10.1101/2021.10.16.464630 |
| 2017 | Crossref, OpenAlex | Reconstruction of genome-scale metabolic model of Yarrowia lipolytica and its applicatio... | 10.1186/s40643-017-0180-6 |
| 2026 | Crossref, OpenAlex | Two Decades of Genome-Scale Metabolic Modeling for Saccharomyces cerevisiae | 10.35378/gujs.1840536 |
| 2020 | Crossref, OpenAlex | Comparison and Analysis of Published Genome-scale Metabolic Models of Yarrowia lipolytic... | 10.1007/s12257-019-0208-1 |
| 2025 | Crossref | EnzymeTuning: a Deep-learning-based Toolbox for Optimizing Enzyme-constrained Metabolic ... | 10.1101/2025.08.23.670849 |
| 2026 | Crossref | A hybrid machine learning and enzyme-constrained metabolic model for ab initio predictio... | 10.64898/2026.07.20.739489 |
| 2027 | Crossref | EINN: An enzyme-informed neural network guided by an enzyme-constrained genome-scale met... | 10.1016/j.synbio.2026.07.009 |
| 2018 | bioRxiv/medRxiv, OpenAlex | Memote: A community driven effort towards a standardized genome-scale metabolic model te... | 10.1101/350991 |
| 1993 | Crossref | Quality Assessment of a Metabolic Model and Systems Analysis of Citric Acid Production b... | 10.1007/978-1-4615-2962-0_20 |
| 2026 | Crossref | Modeling meets metabolic engineering: The iPichia consensus model as basis for metabolic... | 10.1016/j.bej.2025.109940 |
| 2026 | Crossref | pAo: a consensus genome-scale metabolic model for Aspergillus oryzae capturing intra-spe... | 10.34133/csbj.0173 |
| 2023 | Crossref | Impacts of Aspergillus Oryzae 3.042 on the Metabolic Network Formation of Cantonese Soy ... | 10.2139/ssrn.4616968 |
| 2024 | bioRxiv/medRxiv | A continuous dynamic genome-scale model explains batch fermentations led by species of t... | 10.1101/2024.05.03.592398 |

## 6. Preprints and peer-review status

12 curated works are preprints and are **not peer reviewed**. Each is marked `PREPRINT - NOT PEER REVIEWED` in the `peer_review_status` column of `publications.csv`, carries the same string at the head of its `note` field in `references.bib`, is entered as `@misc` rather than `@article`, and is tagged `[PREPRINT - NOT PEER REVIEWED]` wherever it appears in `literature_by_organism.md`.

| Preprint DOI | Server | Published version found | Published version in corpus |
|---|---|---|---|
| 10.1101/350991 | bioRxiv (Cold Spring Harbor Laboratory) | 10.1038/s41587-020-0446-y | yes |
| 10.1101/2021.10.16.464630 | bioRxiv (Cold Spring Harbor Laboratory) | 10.1038/s41467-022-30689-7 | yes |
| 10.1101/2022.02.11.479986 | openRxiv | none found | — |
| 10.1101/2023.12.03.569754 | bioRxiv (Cold Spring Harbor Laboratory) | none found | — |
| 10.2139/ssrn.4616968 | Elsevier BV | none found | — |
| 10.1101/2024.05.03.592398 | bioRxiv | none found | — |
| 10.1101/2025.10.29.684458 | bioRxiv (Cold Spring Harbor Laboratory) | none found | — |
| 10.1101/2025.08.23.670849 | openRxiv | none found | — |
| 10.20944/preprints202510.0516.v1 | ? | none found | — |
| 10.64898/2026.07.20.739489 | openRxiv | none found | — |
| 10.21203/rs.3.rs-9453242/v1 | Springer Science and Business Media LLC | none found | — |
| 10.64898/2026.04.09.717583 | bioRxiv | none found | — |

Resolution used the bioRxiv API `published_doi` field first, then Crossref and OpenAlex title matching restricted to non-preprint record types. Where no published version is listed, none was found at retrieval time; absence of a link is not evidence the work is unpublished. Both resolved published versions were already present in the corpus as separate records — they are retained as distinct rows with the link recorded, rather than merged, so a citation to either version resolves.

## 7. Retractions, errata and integrity flags

**No retracted or withdrawn work is present in the curated set.** OpenAlex `is_retracted` was false for all 242 works, and no PubMed publication type contained "Retract". 3 works carry an erratum notice — the article stands, a correction was published alongside it:

| Work | Flag |
|---|---|
| A consensus S. cerevisiae metabolic model Yeast8 and its ecosystem for comprehen | epmc:Erratum in:33093448 |
| MEMOTE for standardized genome-scale metabolic model testing. | epmc:Erratum in:32265554 |
| The ModelSEED Biochemistry Database for the integration of metabolic annotations | epmc:Erratum in:33179751 |

Detection used four independent signals: OpenAlex `is_retracted`, PubMed publication types, Europe PMC `commentCorrectionList`, and Crossref `update-to`. Any one firing sets `integrity_flag` in the CSV. Note that erratum detection depends on the correcting notice being indexed; a very recent correction may not yet be visible in any of the four.

## 8. Query design and reproducibility

- **PubMed/PMC** — 31 round-0 query sets (420 records, reused) + 38 shared topic queries + 14 broad organism queries + 28 gap-organism queries, via E-utilities.
- **Europe PMC** — 66 queries, REST `search`, `resultType=core`, cited-by sort.
- **Crossref** — 66 queries via `query.bibliographic`. Practical note: combining `select` with `query.bibliographic` returned HTTP 400 for some term combinations; queries were re-issued without `select`, and residual failures resolved after stripping punctuation or falling back to the general `query` parameter.
- **OpenAlex** — 38 queries via the connector, plus batched DOI-filter enrichment (40 DOIs per request) for citation counts, retraction flags and missing PMIDs. An API key is mandatory; keyless requests are rejected.
- **bioRxiv/medRxiv** — the API exposes **no keyword or free-text search**, only subject category plus a date window, and cursor paging does not extend the per-window result cap. Coverage was therefore obtained two ways: (a) sweeping monthly windows from 2023-01 across systems biology, bioengineering and synthetic biology, scanning ~3957 preprint records and keyword-filtering titles and abstracts locally; and (b) direct DOI confirmation of every `10.1101/` and `10.64898/` DOI seen in the other four sources.

**Known limitations.**

- The bioRxiv category sweep is bounded to 2023-01 onward and to three categories, so earlier or differently-categorised preprints may be missed. Preprints already cited by the other four sources were captured regardless of date via route (b).
- Citation counts are OpenAlex `cited_by_count` at retrieval time; they drift and are a popularity signal, not a quality judgement.
- The curated set is a topical selection from the merged pool, not the pool itself. Inclusion rules are recorded in the `tier` column: `A_organism_model` (target organism + a core modelling topic), `C_methodology` (cross-organism tool/method papers, no competing organism), `D_gap_foundation` (genome, annotation and fermentation-physiology literature for the three organisms with no usable GEM). Works whose title named a non-target organism were excluded unless a target organism was also named.
