# R_microsporus — selected model and QC

**Adopted model:** iCV785  (1359 reactions, 787 genes)
**Rationale:** metric rank 3 but ADOPTED: iHol (rank 1) fails the biomass-carbon gate (59.4% C under System_growth, 118.8% under fungal biomass) so its rates are not per-gDW. iCV785 gives 46.8%. Use iHol only for gene-level coverage (1461 vs 787 genes).

## Quantitative QC (defined glucose medium, 10 mmol gDW-1 h-1)

| check | value | verdict |
|---|---|---|
| growth rate | 1.1113 /h | — |
| carbon in biomass | 46.8 % | PASS (valid 42-53%) |
| max ATP per glucose | 34.8 | PASS (max ~32) |
| unmatched medium roles | 5 | — |
| burden slope (lysozyme) | -14.02 /h per mmol gDW-1 h-1 | — |

**Usable for quantitative burden / strain design:** YES
