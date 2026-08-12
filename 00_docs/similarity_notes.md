# Cross-organism similarity: method, results, and top-3 proxy candidates

Ranked **by similarity score alone**. Model quality, FBA-capability and curation depth are a
separate track's concern; where the score-optimal neighbour has no usable GEM I flag it but do
not down-rank it.

## Method

Combined score for each of the 28 pairs, from four independent evidence sources:

| Component | Weight | Source | Definition |
|---|---|---|---|
| Taxonomic shared-rank depth | 0.40 | NCBI Taxonomy (E-utilities `esearch`+`efetch`, `LineageEx`) | Deepest rank on the ladder kingdom -> phylum -> subphylum -> class -> order -> family -> genus at which both lineages still agree, requiring agreement at every coarser rank; divided by 7. |
| KEGG metabolic-KO Jaccard | 0.30 | KEGG REST `/link/ko/<org>` intersected with the metabolic-map KO universe (`/link/pathway/ko`, maps < 2000; 6932 KOs) | \|A∩B\| / \|A∪B\| over metabolic KOs. |
| UniProt EC overlap coefficient | 0.20 | UniProt `/uniprotkb/stream?query=proteome:<UPID>&fields=ec` | \|A∩B\| / min(\|A\|,\|B\|) over unique EC numbers. Overlap coefficient rather than Jaccard because reference proteomes differ ~2.8x in size and Jaccard penalises the smaller set for annotation depth it cannot have. |
| KEGG pathway-set Jaccard | 0.05 | KEGG REST `/list/pathway/<org>` | Coarse (only 142-156 pathways per organism, range 0.885-0.972) so weighted low. |
| Proteome size ratio | 0.05 | UniProt reference proteome protein counts | min/max. Proxy for genome-scale comparability, not homology. |

Weights are renormalised over available components, so a missing component does not bias the
score downward — it widens the uncertainty. `weight_coverage` in `similarity_pairs_wide.csv`
records how much weight each pair actually carried: **1.00 for the 21 Ascomycota pairs, 0.65 for
the 7 *R. microsporus* pairs** (KEGG components unavailable — see below). Every component value
is in `similarity_components.csv` in long form so the weighting can be re-run.

### Honest coverage statement
- **KEGG has no *Rhizopus* genome.** Verified by exhaustive search of `/list/genome` (all 481 kB)
  for `Rhizopus`, `Mucor`, `Phycomyces`, `Rhizomucor`, `Lichtheimia`, `Parasitella`, `Absidia`,
  `Syncephalastrum`, `Benjaminiella` — **zero Mucoromycota hits**. `/list/organism` returns HTTP 400
  on the current API; `/list/genome` is the working endpoint. The seven *R. microsporus* pairs
  therefore score on taxonomy + UniProt EC + proteome scale only (0.65 weight coverage), and
  fall back exactly as the task specified.
- KEGG codes resolved for the other seven: `yli`, `sce`, `fvn` (*F. venenatum* **is** in KEGG,
  T09539), `tre` (QM6a), `ppa`, `ang`, `aor`.
- *R. microsporus* still receives a full metabolic-content score via the UniProt EC axis
  (673 unique ECs from reference proteome UP000242254, *R. microsporus* ATCC 52813, 97.1% BUSCO).

## Taxonomic structure — verified against NCBI

Confirmed by `efetch` on the eight taxids (`organism_taxonomy_genomics.csv`):

- ***R. microsporus* (taxid 58291) is Mucoromycota**; all seven others are Ascomycota. It shares
  only **kingdom (Fungi)** with every other organism — shared-rank depth **1/7**. Lineage:
  Mucoromycota / Mucoromycotina / Mucoromycetes / Mucorales / Rhizopodaceae / *Rhizopus*.
  (The lab's variety *R. microsporus* var. *oligosporus* is NCBI taxid 4847, a child node.)
- ***F. venenatum* and *T. reesei* are both Hypocreales** (Sordariomycetes, Pezizomycotina) —
  shared-rank depth **5/7** (order), the second-deepest pair in the panel and the only cross-genus
  order-level match.
- ***A. niger* and *A. oryzae* are congeneric** *Aspergillus* (Eurotiales, Eurotiomycetes) —
  depth **7/7**, the only genus-level pair.
- ***S. cerevisiae*, *Y. lipolytica*, *K. phaffii* are all Saccharomycotina** but NCBI's current
  taxonomy splits them across three *classes*: Saccharomycetes (*S. cerevisiae*),
  **Dipodascomycetes** (*Y. lipolytica*), Pichiomycetes (*K. phaffii*) — depth **3/7** for all
  three pairwise combinations. This corroborates the expected divergence of *Y. lipolytica*: it is
  no longer placed in the same class as *S. cerevisiae* at all, and its class-level separation is
  identical in depth to *K. phaffii*'s. The metabolic axes then separate them — *Y. lipolytica*
  scores 0.688 to *S. cerevisiae* and 0.689 to
  *K. phaffii*, while *S. cerevisiae*-*K. phaffii* is 0.693.

## Combined matrix, clustered

The dendrogram (average linkage on 1 - similarity) recovers taxonomy without being given it:
`R_microsporus | A_niger | A_oryzae | F_venenatum | T_reesei | Y_lipolytica | S_cerevisiae | K_phaffii`. *R. microsporus* joins last and at the greatest height; the two
Aspergillus species and the two Hypocreales species form the two tightest clades; the three
yeasts form a third.

Range: **0.389** (*R. microsporus*-*K. phaffii*, and *R. microsporus*-*S. cerevisiae*
at 0.389) to **0.931** (*A. niger*-*A. oryzae*).
Every one of *R. microsporus*'s seven scores (0.389-0.426) is below every one of the 21
Ascomycota-Ascomycota scores (0.521-0.931) — the phylum boundary is the dominant signal in the
matrix, with no overlap between the two distributions.

## Top-3 proxy candidates

### *Fusarium venenatum* (no GEM found anywhere)
1. ***Trichoderma reesei*** — 0.827 (no usable GEM)
2. ***Aspergillus niger*** — 0.711
3. ***Aspergillus oryzae*** — 0.691

Restricted to organisms with an FBA-capable model:
1. ***Aspergillus niger*** — 0.711
2. ***Aspergillus oryzae*** — 0.691
3. ***Yarrowia lipolytica*** — 0.572

**Caveat:** the score-optimal proxy (*T. reesei*, same order Hypocreales, 0.827) has only a
CoReCo draft — 0 genes, 1 compartment, 0 exchange reactions, not FBA-capable. This is the
"nearest relative may itself lack a good model" case in its sharpest form: the gap between the
best-by-similarity (0.827) and best-by-availability (*A. niger*, 0.711) is 0.116, and it crosses
a class boundary (Sordariomycetes -> Eurotiomycetes).

### *Trichoderma reesei* (CoReCo draft only, not FBA-capable)
1. ***Fusarium venenatum*** — 0.827 (no usable GEM)
2. ***Aspergillus niger*** — 0.685
3. ***Aspergillus oryzae*** — 0.678

Restricted to organisms with an FBA-capable model:
1. ***Aspergillus niger*** — 0.685
2. ***Aspergillus oryzae*** — 0.678
3. ***Yarrowia lipolytica*** — 0.586

**Caveat:** same problem mirrored — the top neighbour is *F. venenatum*, which has no GEM at all.
Both Hypocreales members are model-poor, so neither can rescue the other, and the forced fallback
to *A. niger* (0.685) is precisely the transfer direction that the phylum-transfer study measured
as already diverged (see `metabolic_differences.md` §3.1).

### *Rhizopus microsporus* var. *oligosporus* (CoReCo draft only, not FBA-capable)
1. ***Aspergillus niger*** — 0.426
2. ***Aspergillus oryzae*** — 0.422
3. ***Fusarium venenatum*** — 0.419 (no usable GEM)

Restricted to organisms with an FBA-capable model:
1. ***Aspergillus niger*** — 0.426
2. ***Aspergillus oryzae*** — 0.422
3. ***Yarrowia lipolytica*** — 0.395

**Caveat — the strongest one in this track:** all seven candidates cluster in a
**0.389-0.426** band, a spread of only 0.037. The ranking is therefore *not meaningful* —
picking *A. niger* (0.426) over *K. phaffii* (0.393) is not a defensible biological choice, it is
noise on a cross-phylum comparison. Two consequences:

1. **Do not treat the top-ranked Ascomycota proxy as a recommendation.** Report it as "least-bad
   within a uniformly unsuitable set".
2. **Look outside the eight-organism panel.** *Mucor circinelloides* **iWV1213** [Vongsangnak W et al., Gene, 2016; PMID:26911256 doi:10.1016/j.gene.2016.02.028]
   is a published, compartmentalised, FBA-validated Mucoromycota GEM (1213 genes, 1326 reactions)
   in the same subphylum *and* the same order (Mucorales) as *R. microsporus*. On the taxonomy
   axis it would score 3/7 shared-rank depth against *R. microsporus* versus 1/7 for every
   Ascomycota candidate — a three-fold better taxonomic match than anything in the panel.
   **This should be evaluated before any Ascomycota proxy is assigned to *R. microsporus*.**

## Files
- `similarity_matrix.csv` — 8x8 combined score, symmetric, diagonal 1.0
- `similarity_components.csv` — long form, one row per pair x component, with weights
- `similarity_pairs_wide.csv` — 28 pairs, all components + `weight_coverage`
- `organism_taxonomy_genomics.csv` — taxid, full lineage, proteome ID/size/BUSCO, KEGG code/counts
- `marker_enzyme_presence.csv` / `marker_ko_presence.csv` — 19 marker enzymes (EC) and 20 KOs x 8 organisms
- `marker_annotation_concordance.csv` — EC-vs-KO agreement, 98 observations, 19.4% discordant
- `similarity_citations.csv` / `.bib` — 78 PubMed-verified references
- `similarity_heatmap.png` — clustered heatmap, phylum-annotated
- `metabolic_differences.md` — transfer-blocker catalogue
