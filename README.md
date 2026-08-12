# Fungal GEM curation and strain-design project — round 1

Eight industrial fungal hosts: *Y. lipolytica*, *S. cerevisiae*, *F. venenatum*,
*R. microsporus* var. *oligosporus*, *T. reesei*, *K. phaffii*, *A. niger*, *A. oryzae*.

Round 1 delivers: model census and selection metric, the adopted GEM per organism,
a minimum FBA simulation on a defined medium, and a working burden model.

## Layout

```
00_docs/              selection metric, burden strategy, literature and census notes
01_organisms/NN_*/    per organism: models/, fba/, qc/, literature/
02_comparative/       cross-organism tables and figures
03_code/              src/fungal_fba (importable), figure builders, product sequence
```

## Headline results

| organism | adopted model | %C biomass | ATP/glc | trustworthy |
|---|---|---|---|---|
| *S cerevisiae* | yeast-GEM v9.1.0 | 49.4 | 19.1 | yes |
| *Y lipolytica* | Lu2021 Y.lipolytica pan-GEM | 50.7 | 22.2 | yes |
| *K phaffii* | Lu2021 K.pastoris pan-GEM | 49.0 | 22.2 | yes |
| *A niger* | iJB1325 (curated) | 53.2 | 49.1 | no |
| *A oryzae* | iWV1346 | 52.2 | 101.9 | no |
| *R microsporus* | iCV785 | 46.8 | 34.8 | yes |
| *F venenatum* | Lu2021 F. graminearum (PROXY) | 49.0 | 19.8 | yes |
| *T reesei* | CoReCo Castillo2016 | nan | 1.8 | no |

Five of eight models are trustworthy for quantitative FBA. *A. niger* and
*A. oryzae* carry energy-generating cycles (49 and 102 ATP/glucose against a
thermodynamic ceiling near 32) that silently absorb any imposed ATP cost.
*T. reesei*'s only model has zero genes, so no gene-level design is possible.

## Literature

242 works curated across PubMed/PMC, Europe PMC, Crossref, OpenAlex and
bioRxiv. 45% of the corpus was not returned by PubMed queries alone — see
`00_docs/literature_coverage.md`.

## Reproducing

```bash
pip install cobrapy pandas matplotlib
export PYTHONPATH=03_code/src
python -c "import fungal_fba.fba as f; m=f.load_model('01_organisms/02_saccharomyces_cerevisiae/models/curated/yeast-GEM.xml'); print(f.solve_fba(m))"
```

Round 2 candidates: remove the two energy-generating cycles; growth-coupled
knockout screening on the five clean models; ec-model burden comparison for
*S. cerevisiae* and *Y. lipolytica*.
