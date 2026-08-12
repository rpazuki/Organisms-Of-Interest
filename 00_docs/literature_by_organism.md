# Literature by organism: key reconstructions and best current model

Derived from the curated corpus (`publications.csv`, n = 242). **Model status lines cite this project's own round-0 SBML probe** of the eight downloaded models; literature lines cite retrieved bibliographic records only. Preprints are marked `[PREPRINT - NOT PEER REVIEWED]`. Citation counts are OpenAlex `cited_by_count` at retrieval time — a popularity signal, not a quality judgement.

Organisms are ordered by GEM readiness, best first.

## *Saccharomyces cerevisiae*

**Curated works:** 46 | **GEM availability:** excellent

**Best current model.** yeast-GEM v9.1.0 — 4102 rxns / 2748 mets / 1143 genes / 14 compartments, default growth 0.0809 h⁻¹. The reference-quality GEM of the eight.

**Key reconstruction / model papers.**

- *Evaluation of enzyme-constrained genome-scale model through metabolic engineering of anaerobic co-production of 2,3-butanediol and glycerol by Saccharomyces cerevisiae.* — Metabolic engineering (2024, 9 citations). [doi:10.1016/j.ymben.2024.01.007](https://doi.org/10.1016/j.ymben.2024.01.007)
    - Applies an enzyme-constrained S. cerevisiae GEM to guide metabolic engineering for anaerobic co-production, directly relevant as a template for ecGEM validation and enzyme-constraint methodology in this project's yeast workflows.
- *A consensus S. cerevisiae metabolic model Yeast8 and its ecosystem for comprehensively probing cellular metabolism.* — Nature communications (2019, 400 citations). [doi:10.1038/s41467-019-11581-3](https://doi.org/10.1038/s41467-019-11581-3)
    - Provides Yeast8, a well-curated consensus GEM for S. cerevisiae, directly supporting GEM selection and reproducible FBA baseline for this organism, and as a template for proxy-host modelling of related fungi.
- *Identification of novel metabolic engineering targets for S-adenosyl-L-methionine production in Saccharomyces cerevisiae via genome-scale engineering* — Metabolic Engineering (2021, 36 citations). [doi:10.1016/j.ymben.2021.03.005](https://doi.org/10.1016/j.ymben.2021.03.005)
    - Genome-scale strain-design study for SAM overproduction in S. cerevisiae; useful reference for FBA-based target identification methods and reconstruction approaches applicable to this project's S. cerevisiae GEM workflows.
- *Reconstruction and validation of Saccharomyces cerevisiae iND750, a fully compartmentalized genome-scale metabolic model.* — Genome research (2004, 656 citations). [doi:10.1101/gr.2250904](https://doi.org/10.1101/gr.2250904)
    - Foundational compartmentalized GEM for S. cerevisiae; useful as a candidate reference model for GEM selection and as a baseline for minimal reproducible FBA workflows in this project.
- *Reconstruction of cytosolic fumaric acid biosynthetic pathways in Saccharomyces cerevisiae.* — Microbial cell factories (2012, 89 citations). [doi:10.1186/1475-2859-11-24](https://doi.org/10.1186/1475-2859-11-24)
    - Describes engineered cytosolic fumarate pathway construction in S. cerevisiae; relevant as a product-target case study for pathway reconstruction/metabolic-burden modelling atop the yeast GEM rather than for GEM selection itself.
- *Yeast9: a consensus genome-scale metabolic model for S. cerevisiae curated by the community.* — Molecular systems biology (2024, 58 citations). [doi:10.1038/s44320-024-00060-7](https://doi.org/10.1038/s44320-024-00060-7)
    - Community-consensus GEM for S. cerevisiae; a strong candidate as the canonical model for this organism in the project's GEM-selection step and baseline for reproducible FBA workflows.
- *A genome-scale metabolic model of Saccharomyces cerevisiae that integrates expression constraints and reaction thermodynamics.* — Nature communications (2021, 107 citations). [doi:10.1038/s41467-021-25158-6](https://doi.org/10.1038/s41467-021-25158-6)
    - Provides an expression- and thermodynamics-constrained S. cerevisiae GEM, useful as a candidate reference model and template for enzyme-constrained extensions in the S. cerevisiae workflow.

**Supporting literature** (applications, burden, omics, product formation).

- *Genome-scale metabolic models reveal determinants of phenotypic differences in non-Saccharomyces yeasts.* — BMC bioinformatics (2023) [reconstruction]. [doi:10.1186/s12859-023-05506-7](https://doi.org/10.1186/s12859-023-05506-7)
- *Yeast9: A Consensus Yeast Metabolic Model Enables Quantitative Analysis of Cellular Metabolism By Incorporating Big Data* — bioRxiv (Cold Spring Harbor Laboratory) (2023) [reconstruction]. [doi:10.1101/2023.12.03.569754](https://doi.org/10.1101/2023.12.03.569754) `[PREPRINT - NOT PEER REVIEWED]`
- *Genome-scale modeling drives 70-fold improvement of intracellular heme production in Saccharomyces cerevisiae .* — Proceedings of the National Academy of Sciences of the United States of America (2022) [reconstruction]. [doi:10.1073/pnas.2108245119](https://doi.org/10.1073/pnas.2108245119)
- *Genome-Scale Reconstruction of the Saccharomyces cerevisiae Metabolic Network* — Genome Research (2003) [reconstruction]. [doi:10.1101/gr.234503](https://doi.org/10.1101/gr.234503)
- *Evaluating proteome allocation of Saccharomyces cerevisiae phenotypes with resource balance analysis.* — Metabolic engineering (2022) [ecmodel, omics]. [doi:10.1016/j.ymben.2023.04.009](https://doi.org/10.1016/j.ymben.2023.04.009)
- *Dynamic genome-scale modeling of Saccharomyces cerevisiae unravels mechanisms for ester formation during alcoholic fermentation.* — Biotechnology and bioengineering (2023) [reconstruction]. [doi:10.1002/bit.28421](https://doi.org/10.1002/bit.28421)
- *Two Decades of Genome-Scale Metabolic Modeling for Saccharomyces cerevisiae* — GAZI UNIVERSITY JOURNAL OF SCIENCE (2026) [reconstruction]. [doi:10.35378/gujs.1840536](https://doi.org/10.35378/gujs.1840536)
- *Improving the flux distributions simulated with genome-scale metabolic models of Saccharomyces cerevisiae.* — Metabolic engineering communications (2016) [reconstruction]. [doi:10.1016/j.meteno.2016.05.002](https://doi.org/10.1016/j.meteno.2016.05.002)
- *The genome-scale metabolic model iIN800 of Saccharomyces cerevisiae and its validation: a scaffold to query lipid metabolism.* — BMC systems biology (2008) [reconstruction]. [doi:10.1186/1752-0509-2-71](https://doi.org/10.1186/1752-0509-2-71)

## *Yarrowia lipolytica*

**Curated works:** 21 | **GEM availability:** good

**Best current model.** iYali (Sánchez et al. consensus lineage) — FBA-capable in this project's probe: 1924 rxns / 1671 mets / 848 genes / 14 compartments, default growth 0.1057 h⁻¹.

**Key reconstruction / model papers.**

- *Enzyme-constrained genome-scale model of Yarrowia lipolytica predicts growth-phase specific metabolic engineering targets.* — Applied microbiology and biotechnology (2026, 0 citations). [doi:10.1007/s00253-026-13791-4](https://doi.org/10.1007/s00253-026-13791-4)
    - Directly relevant: an enzyme-constrained GEM for Y. lipolytica supports this project's ecModel and strain-design workflows, potentially informing growth-phase-aware FBA and metabolic-burden analyses for this target organism.
- *Genome-scale model-driven strain design for dicarboxylic acid production in Yarrowia lipolytica.* — BMC systems biology (2018, 89 citations). [doi:10.1186/s12918-018-0542-5](https://doi.org/10.1186/s12918-018-0542-5)
    - Directly relevant GEM-driven strain design work in Y. lipolytica; useful reference for reconstruction/curation choices and FBA-guided strain-design methodology applicable to this organism's model.
- *Metabolic model-guided strain design for improved succinic acid production in Yarrowia lipolytica.* — Bioresource technology (2026, 2 citations). [doi:10.1016/j.biortech.2025.133508](https://doi.org/10.1016/j.biortech.2025.133508)
    - Directly relevant example of GEM-guided strain design in Y. lipolytica; useful reference for reconstruction/curation practices and FBA-driven strain design workflows applicable to this species' model.
- *Integrated knowledge mining, genome-scale modeling, and machine learning for predicting Yarrowia lipolytica bioproduction.* — Metabolic engineering (2021, 67 citations). [doi:10.1016/j.ymben.2021.07.003](https://doi.org/10.1016/j.ymben.2021.07.003)
    - Combines GEM reconstruction, knowledge mining, and machine learning to predict Y. lipolytica bioproduction, directly informing GEM selection and reconstruction strategy for this organism in the project's FBA workflows.
- *In silico identification of metabolic engineering strategies for improved lipid production in Yarrowia lipolytica by genome-scale metabolic modeling.* — Biotechnology for biofuels (2019, 60 citations). [doi:10.1186/s13068-019-1518-4](https://doi.org/10.1186/s13068-019-1518-4)
    - Directly relevant: uses a Y. lipolytica GEM to derive engineering strategies for lipid production, offering a template for FBA-based strain-design workflows and GEM selection for this species.
- *Heterologous Biosynthesis of Taxifolin in Yarrowia lipolytica: Metabolic Engineering and Genome-Scale Metabolic Modeling.* — Applied biochemistry and biotechnology (2024, 5 citations). [doi:10.1007/s12010-024-05099-8](https://doi.org/10.1007/s12010-024-05099-8)
    - Directly relevant Y. lipolytica GEM reconstruction paired with heterologous pathway engineering; useful reference for GEM selection and FBA workflow design in this host.
- *Optimization of lipid production with a genome-scale model of Yarrowia lipolytica.* — BMC systems biology (2015, 141 citations). [doi:10.1186/s12918-015-0217-4](https://doi.org/10.1186/s12918-015-0217-4)
    - Directly relevant as a candidate GEM for Y. lipolytica; useful for model selection and as a basis for FBA-based lipid-production optimization workflows in this project.

**Supporting literature** (applications, burden, omics, product formation).

- *A genome-scale metabolic model of the lipid-accumulating yeast Yarrowia lipolytica.* — BMC systems biology (2012) [reconstruction]. [doi:10.1186/1752-0509-6-35](https://doi.org/10.1186/1752-0509-6-35)
- *Reconstruction of genome-scale metabolic model of Yarrowia lipolytica and its application in overproduction of triacylglycerol* — Bioresources and Bioprocessing (2017) [product_target, reconstruction]. [doi:10.1186/s40643-017-0180-6](https://doi.org/10.1186/s40643-017-0180-6)
- *Dissecting carbon metabolism of Yarrowia lipolytica type strain W29 using genome-scale metabolic modelling.* — Computational and structural biotechnology journal (2022) [reconstruction]. [doi:10.1016/j.csbj.2022.05.018](https://doi.org/10.1016/j.csbj.2022.05.018)
- *Mapping of Nonhomologous End Joining-Mediated Integration Facilitates Genome-Scale Trackable Mutagenesis in Yarrowia lipolytica.* — ACS synthetic biology (2022) [reconstruction]. [doi:10.1021/acssynbio.1c00390](https://doi.org/10.1021/acssynbio.1c00390)
- *Comparison and Analysis of Published Genome-scale Metabolic Models of Yarrowia lipolytica* — Biotechnology and Bioprocess Engineering (2020) [reconstruction]. [doi:10.1007/s12257-019-0208-1](https://doi.org/10.1007/s12257-019-0208-1)
- *Reconstruction and in silico analysis of metabolic network for an oleaginous yeast, Yarrowia lipolytica.* — PloS one (2012) [reconstruction]. [doi:10.1371/journal.pone.0051535](https://doi.org/10.1371/journal.pone.0051535)
- *Ameliorating the Metabolic Burden of the Co-expression of Secreted Fungal Cellulases in a High Lipid-Accumulating Yarrowia lipolytica Strain by Medium C/N Ratio and a Chemical Chaperone.* — Frontiers in microbiology (2018) [burden, product_target]. [doi:10.3389/fmicb.2018.03276](https://doi.org/10.3389/fmicb.2018.03276)
- *Genome-scale transcriptional activation by non-homologous end joining-mediated integration in Yarrowia lipolytica.* — Biotechnology for biofuels and bioproducts (2024) [reconstruction]. [doi:10.1186/s13068-024-02472-x](https://doi.org/10.1186/s13068-024-02472-x)
- *Disruption of the Snf1 Gene Enhances Cell Growth and Reduces the Metabolic Burden in Cellulase-Expressing and Lipid-Accumulating Yarrowia lipolytica* — Frontiers in Microbiology (2021) [burden, product_target]. [doi:10.3389/fmicb.2021.757741](https://doi.org/10.3389/fmicb.2021.757741)

## *Komagataella phaffii*

**Curated works:** 56 | **GEM availability:** good

**Best current model.** iMT1026 (MODEL1508040001) — 2220 rxns / 2764 mets / 9 compartments; gene associations absent from the SBML and the objective is unset, so a biomass reaction must be selected explicitly (candidates found: `growth`, `BIOMASS`, `BIOMASS8020`, `BIOMASS6040`, `BIOMASS4060`).

**Key reconstruction / model papers.**

- *Genome-scale metabolic model of methylotrophic yeast Pichia pastoris and its use for in silico analysis of heterologous protein production.* — Biotechnology journal (2010, 130 citations). [doi:10.1002/biot.201000078](https://doi.org/10.1002/biot.201000078)
    - Foundational GEM for K. phaffii (P. pastoris), directly supporting model selection and providing a basis for in silico metabolic-burden analysis of heterologous protein production in this host.
- *Recombinant protein production in Pichia pastoris : from transcriptionally redesigned strains to bioprocess optimization and metabolic modelling* — FEMS Yeast Research (2021, 77 citations). [doi:10.1093/femsyr/foab057](https://doi.org/10.1093/femsyr/foab057)
    - Reviews strain engineering, bioprocess optimization, and metabolic modelling for recombinant protein production in Pichia (Komagataella phaffii), relevant to metabolic-burden modelling and GEM-based strategies for this host.
- *Developing a metabolic model-based fed-batch feeding strategy for Pichia pastoris fermentation through fine-tuning of the methanol utilization pathway.* — Microbial biotechnology (2023, 19 citations). [doi:10.1111/1751-7915.14264](https://doi.org/10.1111/1751-7915.14264)
    - Applies a metabolic-model-guided fed-batch feeding strategy targeting the methanol utilization pathway in P. pastoris (K. phaffii); useful for FBA-informed feeding/culture design and metabolic-burden considerations for recombinant protein production.
- *Fine-tuning the P. pastoris iMT1026 genome-scale metabolic model for improved prediction of growth on methanol or glycerol as sole carbon sources.* — Microbial biotechnology (2018, 107 citations). [doi:10.1111/1751-7915.12871](https://doi.org/10.1111/1751-7915.12871)
    - Refines the iMT1026 GEM for K. phaffii growth on methanol/glycerol, directly informing GEM selection and FBA carbon-source predictions for the proxy-host/production strain in this fungal panel.
- *Genome-scale metabolic model of Pichia pastoris with native and humanized glycosylation of recombinant proteins.* — Biotechnology and bioengineering (2016, 70 citations). [doi:10.1002/bit.25863](https://doi.org/10.1002/bit.25863)
    - Directly relevant GEM for Komagataella phaffii (as Pichia pastoris); useful base model for FBA workflows and for modelling metabolic burden from recombinant protein glycosylation and secretion.
- *Genome-scale analysis of library sorting (GALibSo): Isolation of secretion enhancing factors for recombinant protein production in Pichia pastoris.* — Biotechnology and bioengineering (2010, 38 citations). [doi:10.1002/bit.22573](https://doi.org/10.1002/bit.22573)
    - Relevant to metabolic-burden modelling for K. phaffii: describes a genome-scale approach to identifying secretion-enhancing factors for recombinant protein production, informative for host-engineering strategies tied to secretory/burden constraints in ecGEM workflows.
- *Comparative genome-scale analysis of Pichia pastoris variants informs selection of an optimal base strain.* — Biotechnology and bioengineering (2019, 70 citations). [doi:10.1002/bit.27209](https://doi.org/10.1002/bit.27209)
    - Comparative genome-scale analysis across Pichia pastoris/K. phaffii strain variants directly informs base-strain and GEM selection for this organism, supporting reconstruction choices ahead of FBA and recombinant-protein burden modeling.

**Supporting literature** (applications, burden, omics, product formation).

- *Genome-scale metabolic reconstruction and in silico analysis of methylotrophic yeast Pichia pastoris for strain improvement.* — Microbial cell factories (2010) [reconstruction]. [doi:10.1186/1475-2859-9-50](https://doi.org/10.1186/1475-2859-9-50)
- *Metabolic flux analysis for recombinant protein production by Pichia pastoris using dual carbon sources: Effects of methanol feeding rate.* — Biotechnology and bioengineering (2009) [burden, mfa_13c, product_target]. [doi:10.1002/bit.22543](https://doi.org/10.1002/bit.22543)
- *Protein expression in Pichia pastoris: recent achievements and perspectives for heterologous protein production.* — Applied microbiology and biotechnology (2014) [burden, review]. [doi:10.1007/s00253-014-5732-5](https://doi.org/10.1007/s00253-014-5732-5)
- *Metabolic flux profiling of recombinant protein secreting Pichia pastoris growing on glucose:methanol mixtures.* — Microbial cell factories (2012) [burden, product_target]. [doi:10.1186/1475-2859-11-57](https://doi.org/10.1186/1475-2859-11-57)
- *Integration and Validation of the Genome-Scale Metabolic Models of Pichia pastoris: A Comprehensive Update of Protein Glycosylation Pathways, Lipid and Energy Metabolism.* — PloS one (2016) [reconstruction]. [doi:10.1371/journal.pone.0148031](https://doi.org/10.1371/journal.pone.0148031)
- *Genome-scale metabolic model analysis of Pichia pastoris for enhancing the production of S-adenosyl-L-methionine.* — Bioprocess and biosystems engineering (2023) [reconstruction]. [doi:10.1007/s00449-023-02913-1](https://doi.org/10.1007/s00449-023-02913-1)
- *Dynamic genome-scale metabolic modeling of the yeast Pichia pastoris.* — BMC systems biology (2017) [reconstruction]. [doi:10.1186/s12918-017-0408-2](https://doi.org/10.1186/s12918-017-0408-2)
- *Enabling growth-decoupled Komagataella phaffii recombinant protein production based on the methanol-free P DH promoter.* — Frontiers in bioengineering and biotechnology (2023) [burden, product_target]. [doi:10.3389/fbioe.2023.1130583](https://doi.org/10.3389/fbioe.2023.1130583)
- *Metabolic modeling to identify engineering targets for Komagataella phaffii: The effect of biomass composition on gene target identification.* — Biotechnology and bioengineering (2017) [reconstruction]. [doi:10.1002/bit.26380](https://doi.org/10.1002/bit.26380)

## *Aspergillus niger*

**Curated works:** 13 | **GEM availability:** moderate

**Best current model.** iMA871 (MODEL1507180047) — 1400 rxns / 1900 mets / 3 compartments, 0 genes in the SBML; unbounded default objective (27.79), so exchange bounds must be constrained before use. Later reconstructions are reported in the literature below.

**Key reconstruction / model papers.**

- *Metabolic model integration of the bibliome, genome, metabolome and reactome of Aspergillus niger.* — Molecular systems biology (2008, 199 citations). [doi:10.1038/msb.2008.12](https://doi.org/10.1038/msb.2008.12)
    - Foundational multi-omics reconstruction of an A. niger GEM, directly relevant to model selection and as a curated baseline network for FBA and enzyme-constrained extensions in this species.
- *Multi-omics integrative analysis with genome-scale metabolic model simulation reveals global cellular adaptation of Aspergillus niger under industrial enzyme production condition.* — Scientific reports (2018, 63 citations). [doi:10.1038/s41598-018-32341-1](https://doi.org/10.1038/s41598-018-32341-1)
    - Directly relevant: applies GEM simulation with multi-omics to A. niger under enzyme-production conditions, informing metabolic-burden modelling and enzyme-constrained approaches for recombinant protein production in this species.
- *A community-driven reconstruction of the Aspergillus niger metabolic network.* — Fungal biology and biotechnology (2018, 39 citations). [doi:10.1186/s40694-018-0060-7](https://doi.org/10.1186/s40694-018-0060-7)
    - Directly relevant as a candidate curated GEM for A. niger, one of the eight target fungi; a community reconstruction likely provides the reaction/gene network foundation for FBA workflows.
- *Integration of enzyme constraints in a genome-scale metabolic model of Aspergillus niger improves phenotype predictions.* — Microbial cell factories (2021, 32 citations). [doi:10.1186/s12934-021-01614-2](https://doi.org/10.1186/s12934-021-01614-2)
    - Directly relevant: presents an enzyme-constrained GEM for A. niger, valuable for improving phenotype prediction accuracy and informing enzyme-constrained modelling approaches across the fungal panel.
- *The genome-scale sugar metabolic model from Neurospora crassa reveals lower gene redundancy than that of Aspergillus niger.* — Current research in microbial sciences (2026, 0 citations). [doi:10.1016/j.crmicr.2026.100596](https://doi.org/10.1016/j.crmicr.2026.100596)
    - Comparative sugar-metabolism GEM analysis relevant to A. niger; may inform GEM selection/curation and gene-redundancy considerations for FBA reconstructions, though Neurospora is not a target organism.
- *Comprehensive reconstruction and in silico analysis of Aspergillus niger genome-scale metabolic network model that accounts for 1210 ORFs.* — Biotechnology and bioengineering (2016, 42 citations). [doi:10.1002/bit.26195](https://doi.org/10.1002/bit.26195)
    - Direct candidate GEM for A. niger in this project's scope; a published reconstruction like this could serve as the baseline model for FBA workflows and enzyme-constrained extensions without needing a proxy host.
- *Integration of Aspergillus niger transcriptomic profile with metabolic model identifies potential targets to optimise citric acid production from lignocellulosic hydrolysate.* — Biotechnology for biofuels and bioproducts (2022, 6 citations). [doi:10.1186/s13068-021-02099-2](https://doi.org/10.1186/s13068-021-02099-2)
    - Directly relevant: integrates transcriptomics with an A. niger GEM to identify targets for citric acid production, informing model refinement and product-yield-oriented FBA strategies for this project organism.

**Supporting literature** (applications, burden, omics, product formation).

- *An accurate description of Aspergillus niger organic acid batch fermentation through dynamic metabolic modelling.* — Biotechnology for biofuels (2017) [reconstruction]. [doi:10.1186/s13068-017-0950-6](https://doi.org/10.1186/s13068-017-0950-6)
- *Quality Assessment of a Metabolic Model and Systems Analysis of Citric Acid Production by Aspergillus Niger* — Modern Trends in Biothermokinetics (1993) [product_target, reconstruction]. [doi:10.1007/978-1-4615-2962-0_20](https://doi.org/10.1007/978-1-4615-2962-0_20)
- *Genome-Scale Metabolic Model's multi-objective solving algorithm based on the inflexion point of Pareto front including maximum energy utilization and its application in Aspergillus niger DS03043.* — Biotechnology and bioengineering (2022) [reconstruction]. [doi:10.1002/bit.28078](https://doi.org/10.1002/bit.28078)
- *The Sugar Metabolic Model of Aspergillus niger Can Only Be Reliably Transferred to Fungi of Its Phylum.* — Journal of fungi (Basel, Switzerland) (2022) [reconstruction]. [doi:10.3390/jof8121315](https://doi.org/10.3390/jof8121315)
- *Genomic analysis of the secretion stress response in the enzyme-producing cell factory Aspergillus niger.* — BMC genomics (2007) [burden]. [doi:10.1186/1471-2164-8-158](https://doi.org/10.1186/1471-2164-8-158)
- *Optimization of the citric acid production by Aspergillus niger through a metabolic flux balance model* — Americanae (AECID Library) (2001) [fba, product_target]. [doi:10.4067/s0717-34582001000100001](https://doi.org/10.4067/s0717-34582001000100001)

## *Aspergillus oryzae*

**Curated works:** 7 | **GEM availability:** moderate

**Best current model.** iWV1314 (MODEL1507180056) — 2361 rxns / 1104 mets / 1346 genes / 4 compartments; unbounded default objective (25.68), requires medium constraints.

**Key reconstruction / model papers.**

- *Reconstruction of a Genome-Scale Metabolic Model for Aspergillus oryzae Engineered Strain: A Potent Computational Tool for Enhancing Cordycepin Production.* — International journal of molecular sciences (2025, 1 citations). [doi:10.3390/ijms26146906](https://doi.org/10.3390/ijms26146906)
    - Directly relevant GEM reconstruction for A. oryzae, one of the eight target fungi; useful reference for model selection and as a template for FBA-based recombinant/engineered-strain production studies.
- *Improved annotation through genome-scale metabolic modeling of Aspergillus oryzae.* — BMC genomics (2008, 94 citations). [doi:10.1186/1471-2164-9-245](https://doi.org/10.1186/1471-2164-9-245)
    - Foundational GEM reconstruction for A. oryzae with genome annotation refinement; likely a key candidate for GEM selection and a baseline model for downstream FBA and enzyme-constrained extensions for this host.
- *Genome-scale analysis of the high-efficient protein secretion system of Aspergillus oryzae.* — BMC systems biology (2014, 49 citations). [doi:10.1186/1752-0509-8-73](https://doi.org/10.1186/1752-0509-8-73)
    - Genome-scale reconstruction analyzing A. oryzae's protein secretion machinery, directly relevant to GEM selection and metabolic-burden modelling for recombinant protein production in this edible fungus.
- *pAo: a consensus genome-scale metabolic model for Aspergillus oryzae capturing intra-species diversity* — Computational and Structural Biotechnology Journal (2026, 0 citations). [doi:10.34133/csbj.0173](https://doi.org/10.34133/csbj.0173)
    - Provides a ready-made consensus GEM for A. oryzae, directly supporting model selection and minimal FBA setup for this organism, and its pan-species framing may inform reconciling intra-species variability during reconstruction.
- *Impacts of Aspergillus Oryzae 3.042 on the Metabolic Network Formation of Cantonese Soy Sauce Koji in Industrial-Scale Traditional Fermentation* — Elsevier BV (2023, 0 citations). [doi:10.2139/ssrn.4616968](https://doi.org/10.2139/ssrn.4616968) `[PREPRINT - NOT PEER REVIEWED]`
    - Provides fermentation-condition metabolic network data for A. oryzae relevant to model reconstruction, but focuses on industrial koji ecology rather than a curated GEM; limited direct FBA utility.

**Supporting literature** (applications, burden, omics, product formation).

- *Isolation of Aspergillus oryzae mutants for heterologous protein production from a double proteinase gene disruptant.* — Applied microbiology and biotechnology (2009) [burden]. [doi:10.1007/s00253-008-1851-1](https://doi.org/10.1007/s00253-008-1851-1)
- *Optimizing Mycoprotein Production by Aspergillus oryzae Using Soy Whey as a Substrate* — Journal of Fungi (2025) [scp_food]. [doi:10.3390/jof11050349](https://doi.org/10.3390/jof11050349)

## *Trichoderma reesei*

**Curated works:** 17 | **GEM availability:** draft only

**Best current model.** Only an automated CoReCo draft (MODEL1302010019: 2145 rxns, 0 genes, 1 compartment, 0 exchange reactions) — **not FBA-capable as distributed**.

**Key reconstruction / model papers.**

- *Whole-genome metabolic model of Trichoderma reesei built by comparative reconstruction.* — Biotechnology for biofuels (2016, 29 citations). [doi:10.1186/s13068-016-0665-0](https://doi.org/10.1186/s13068-016-0665-0)
    - Directly relevant GEM source for T. reesei; a comparative genome-scale reconstruction could serve as the baseline model for FBA workflows and enzyme-constrained extensions for this organism.

**Supporting literature** (applications, burden, omics, product formation).

- *Common features and interesting differences in transcriptional responses to secretion stress in the fungi Trichoderma reesei and Saccharomyces cerevisiae.* — BMC Genomics (2006) [burden]. [doi:10.1186/1471-2164-7-32](https://doi.org/10.1186/1471-2164-7-32)
- *Protein Production—Quality Control and Secretion Stress Responses in Trichoderma reesei* — Biotechnology and Biology of Trichoderma (2014) [burden]. [doi:10.1016/b978-0-444-59576-8.00006-0](https://doi.org/10.1016/b978-0-444-59576-8.00006-0)
- *Metabolic engineering strategies for the improvement of cellulase production by Hypocrea jecorina.* — Biotechnology for biofuels (2009) [product_target]. [doi:10.1186/1754-6834-2-19](https://doi.org/10.1186/1754-6834-2-19)
- *Cellulases and beyond: the first 70 years of the enzyme producer Trichoderma reesei.* — Microbial cell factories (2016) [product_target]. [doi:10.1186/s12934-016-0507-6](https://doi.org/10.1186/s12934-016-0507-6)
- *Efficient genome editing in filamentous fungus Trichoderma reesei using the CRISPR/Cas9 system.* — Cell discovery (2015) [general]. [doi:10.1038/celldisc.2015.7](https://doi.org/10.1038/celldisc.2015.7)
- *From induction to secretion: a complicated route for cellulase production in Trichoderma reesei* — Bioresources and Bioprocessing (2021) [product_target]. [doi:10.1186/s40643-021-00461-8](https://doi.org/10.1186/s40643-021-00461-8)
- *Cellulase hyper-production by Trichoderma reesei mutant SEU-7 on lactose.* — Biotechnology for Biofuels (2017) [product_target]. [doi:10.1186/s13068-017-0915-9](https://doi.org/10.1186/s13068-017-0915-9)
- *Single Mutation in Transcriptional Activator Xyr1 Enhances Cellulase and Xylanase Production in Trichoderma reesei on Glucose.* — Journal of agricultural and food chemistry (2023) [product_target]. [doi:10.1021/acs.jafc.3c03466](https://doi.org/10.1021/acs.jafc.3c03466)
- *Re-annotation of the CAZy genes of Trichoderma reesei and transcription in the presence of lignocellulosic substrates.* — Microbial Cell Factories (2012) [omics]. [doi:10.1186/1475-2859-11-134](https://doi.org/10.1186/1475-2859-11-134)

## *Rhizopus microsporus var. oligosporum*

**Curated works:** 14 | **GEM availability:** draft only

**Best current model.** Only an automated CoReCo draft for *R. oryzae* (MODEL1302010018: 2124 rxns, 0 genes, 1 compartment, 0 exchange reactions) — **not FBA-capable as distributed**, and for a different species.

**Key reconstruction papers: none retrieved.** No genome-scale reconstruction for this organism was found in any of the five sources. The literature below is the physiology, genome and omics foundation that a de novo reconstruction or a proxy-host correction would have to be anchored in.

**Supporting literature** (applications, burden, omics, product formation).

- *Genomic analysis of the basal lineage fungus Rhizopus oryzae reveals a whole-genome duplication.* — PLoS genetics (2009) [general]. [doi:10.1371/journal.pgen.1000549](https://doi.org/10.1371/journal.pgen.1000549)
- *Dynamic Optimization of Lactic Acid Production from Grape Stalk Solid-State Fermentation with Rhizopus oryzae Applying a Variable Temperature Profile* — Fermentation (2024) [product_target]. [doi:10.3390/fermentation10020101](https://doi.org/10.3390/fermentation10020101)
- *Ferulic acid triggering a co-production of 4-vinyl guaiacol and fumaric acid from lignocellulose-based carbon source by Rhizopus oryzae.* — Food chemistry (2024) [product_target]. [doi:10.1016/j.foodchem.2024.140799](https://doi.org/10.1016/j.foodchem.2024.140799)
- *Lactic acid fermentation using Rhizopus spp.: current insights and future prospects.* — Bioresources and bioprocessing (2025) [product_target]. [doi:10.1186/s40643-025-00982-6](https://doi.org/10.1186/s40643-025-00982-6)
- *Potato peel waste fermentation by Rhizopus oryzae to produce lactic acid and ethanol.* — Food science & nutrition (2023) [product_target]. [doi:10.1002/fsn3.3670](https://doi.org/10.1002/fsn3.3670)
- *Cellulase and β-glucosidase activity of crude enzyme extracted from fresh and expired soybean tempeh.* — Iranian journal of microbiology (2026) [product_target]. [doi:10.18502/ijm.v18i3.21671](https://doi.org/10.18502/ijm.v18i3.21671)
- *Carbohydrate-active enzymes from the zygomycete fungus Rhizopus oryzae: a highly specialized approach to carbohydrate degradation depicted at genome level.* — BMC genomics (2011) [general]. [doi:10.1186/1471-2164-12-38](https://doi.org/10.1186/1471-2164-12-38)
- *Transcriptome analysis of Rhizopus oryzae seed pellet formation using triethanolamine.* — Biotechnology for biofuels (2021) [omics]. [doi:10.1186/s13068-021-02081-y](https://doi.org/10.1186/s13068-021-02081-y)
- *Complete genome sequence of Burkholderia rhizoxinica, an Endosymbiont of Rhizopus microsporus.* — Journal of bacteriology (2011) [omics]. [doi:10.1128/jb.01318-10](https://doi.org/10.1128/jb.01318-10)

## *Fusarium venenatum*

**Curated works:** 14 | **GEM availability:** absent

**Best current model.** **No GEM exists** — verified absent across BioModels, BiGG and many query forms. Requires a proxy host or de novo reconstruction.

**Key reconstruction papers: none retrieved.** No genome-scale reconstruction for this organism was found in any of the five sources. The literature below is the physiology, genome and omics foundation that a de novo reconstruction or a proxy-host correction would have to be anchored in.

**Supporting literature** (applications, burden, omics, product formation).

- *Efficient Mycoprotein Production with Low CO(2) Emissions through Metabolic Engineering and Fermentation Optimization of Fusarium venenatum.* — Journal of agricultural and food chemistry (2023) [scp_food]. [doi:10.1021/acs.jafc.3c08509](https://doi.org/10.1021/acs.jafc.3c08509)
- *The interaction of α-amylase with mycoprotein: Diffusion through the fungal cell wall, enzyme entrapment, and potential physiological implications* — Food Hydrocolloids (2020) [product_target, scp_food]. [doi:10.1016/j.foodhyd.2020.106018](https://doi.org/10.1016/j.foodhyd.2020.106018)
- *Mutation of the LRG1 Rho-GAP gene is responsible for the hyper branching C-variant phenotype in the quorn mycoprotein fungus Fusarium venenatum A3/5.* — Fungal biology and biotechnology (2024) [scp_food]. [doi:10.1186/s40694-025-00195-8](https://doi.org/10.1186/s40694-025-00195-8)
- *Mycoprotein Production by Submerged Fermentation of the Edible Mushroom Pleurotus ostreatus in a Batch Stirred Tank Bioreactor Using Agro-Industrial Hydrolysate.* — Foods (Basel, Switzerland) (2023) [scp_food]. [doi:10.3390/foods12122295](https://doi.org/10.3390/foods12122295)
- *Enhancing Mycoprotein Yield: Metabolic Modulation of Chitin Synthase in Fusarium venenatum.* — Journal of agricultural and food chemistry (2024) [scp_food]. [doi:10.1021/acs.jafc.4c07105](https://doi.org/10.1021/acs.jafc.4c07105)
- *Safety assays and nutritional values of mycoprotein produced by Fusarium venenatum IR372C from date waste as substrate.* — Journal of the science of food and agriculture (2020) [scp_food]. [doi:10.1002/jsfa.10483](https://doi.org/10.1002/jsfa.10483)
- *Cell wall engineering-guided strategy for high-efficiency biosynthesis of nutrient-fortified Fusarium venenatum mycoprotein.* — Bioresource technology (2025) [scp_food]. [doi:10.1016/j.biortech.2025.133005](https://doi.org/10.1016/j.biortech.2025.133005)
- *Dual enhancement of mycoprotein nutrition and sustainability via CRISPR-mediated metabolic engineering of Fusarium venenatum.* — Trends in biotechnology (2026) [scp_food]. [doi:10.1016/j.tibtech.2025.09.016](https://doi.org/10.1016/j.tibtech.2025.09.016)
- *Enhanced mycoprotein extraction via cell wall disruption: A promising alternative protein with preferable digestibility and lubrication over soy protein.* — Food chemistry (2025) [scp_food]. [doi:10.1016/j.foodchem.2025.146123](https://doi.org/10.1016/j.foodchem.2025.146123)

## Cross-organism methodology and tooling

56 curated works are method or tool papers with no single target organism. These govern *how* the project's models are built, tested, constrained and used. Top 20 by score:

- *MEMOTE for standardized genome-scale metabolic model testing.* — Nature biotechnology (2020, 562 citations) [reconstruction, sbml_release]. [doi:10.1038/s41587-020-0446-y](https://doi.org/10.1038/s41587-020-0446-y)
    - Provides a standardized test suite for GEM quality control (SBML compliance, annotation, consistency), useful for validating and comparing candidate GEMs before FBA workflows across the eight target fungi.
- *Reconstruction of a catalogue of genome-scale metabolic models with enzymatic constraints using GECKO 2.0.* — Nature communications (2021, 151 citations) [ecmodel, reconstruction]. [doi:10.1038/s41467-022-31421-1](https://doi.org/10.1038/s41467-022-31421-1)
    - Directly relevant methods reference for building enzyme-constrained models (GECKO 2.0) applicable across the eight target fungi, supporting ecGEM reconstruction and metabolic-burden analysis for recombinant protein production.
- *Reconstruction, simulation and analysis of enzyme-constrained metabolic models using GECKO Toolbox 3.0.* — Nature protocols (2024, 107 citations) [ecmodel, reconstruction]. [doi:10.1038/s41596-023-00931-7](https://doi.org/10.1038/s41596-023-00931-7)
    - Provides the updated GECKO 3.0 pipeline for building and simulating enzyme-constrained models, directly applicable methodology for adding enzyme constraints to the eight fungal GEMs in this project.
- *Enzyme-constrained genome-scale modeling resolves growth-production trade-offs in fermentative biohydrogen production.* — Environmental science and ecotechnology (2026, 0 citations) [ecmodel, reconstruction]. [doi:10.1016/j.ese.2026.100706](https://doi.org/10.1016/j.ese.2026.100706)
    - Demonstrates enzyme-constrained GEM methodology for capturing growth-production trade-offs; methodologically relevant as a template for ecModel construction applicable to recombinant protein burden analysis in the target fungi.
- *WILDkCAT: extract, retrieve, and predict enzyme turnover numbers of constraint-based metabolic models.* — Bioinformatics (Oxford, England) (2026, 0 citations) [ecmodel, fba, reconstruction]. [doi:10.1093/bioinformatics/btag510](https://doi.org/10.1093/bioinformatics/btag510)
    - Tool for extracting/retrieving/predicting enzyme turnover numbers (kcat) for constraint-based models; directly supports building enzyme-constrained GEMs for these fungi where kcat data is sparse.
- *An Improved Systematic Method for Constructing Enzyme-Constrained Genome-Scale Metabolic Models Using a Protein-Chemical Transformer* — bioRxiv (Cold Spring Harbor Laboratory) (2025, 0 citations) [ecmodel, reconstruction]. [doi:10.1101/2025.10.29.684458](https://doi.org/10.1101/2025.10.29.684458) `[PREPRINT - NOT PEER REVIEWED]`
    - Presents an automated pipeline for building enzyme-constrained GEMs, directly relevant to enzyme-constrained modeling for the eight target fungi and could streamline ecGEM construction where full GEMs already exist.
- *Improving recombinant protein production by yeast through genome-scale modeling using proteome constraints.* — Nature communications (2022, 86 citations) [burden, omics, reconstruction]. [doi:10.1038/s41467-022-30689-7](https://doi.org/10.1038/s41467-022-30689-7)
    - Directly relevant: applies proteome-constrained genome-scale modeling to recombinant protein production burden in yeast, offering a methodological template adaptable to Y. lipolytica, S. cerevisiae, or K. phaffii FBA workflows.
- *Current State, Challenges, and Opportunities in Genome-Scale Resource Allocation Models: A Mathematical Perspective.* — Metabolites (2024, 23 citations) [ecmodel, reconstruction, review]. [doi:10.3390/metabo14070365](https://doi.org/10.3390/metabo14070365)
    - Reviews mathematical foundations and challenges of genome-scale resource allocation models, relevant background for building/interpreting enzyme-constrained models across the eight target fungi.
- *OptRAM: In-silico strain design via integrative regulatory-metabolic network modeling.* — PLoS computational biology (2019, 63 citations) [reconstruction, strain_design]. [doi:10.1371/journal.pcbi.1006835](https://doi.org/10.1371/journal.pcbi.1006835)
    - Presents an integrated regulatory-metabolic strain-design method that could inform metabolic-burden and strain-optimization strategies for recombinant protein production once applied to a species-specific GEM in this project's panel.
- *EnzymeTuning improves enzyme-constrained metabolic modeling and proteome abundance prediction through deep learning.* — Nature communications (2026, 0 citations) [ecmodel, omics, reconstruction]. [doi:10.1038/s41467-026-73744-3](https://doi.org/10.1038/s41467-026-73744-3)
    - Deep-learning method for refining enzyme-constrained models and predicting proteome abundances; directly relevant to building/improving ecGEMs and enzyme-usage constraints for these fungi's FBA and metabolic-burden analyses.
- *Simultaneous application of enzyme and thermodynamic constraints to metabolic models using an updated Python implementation of GECKO.* — Microbiology spectrum (2023, 6 citations) [ecmodel, reconstruction]. [doi:10.1128/spectrum.01705-23](https://doi.org/10.1128/spectrum.01705-23)
    - Directly relevant methodology paper: a Python GECKO update combining enzyme-constrained and thermodynamic constraints, useful for building/refining enzyme-constrained models and burden analysis across the eight target fungi.
- *Genome scale modeling of the protein secretory pathway reveals novel targets for improved recombinant protein production in yeast* — bioRxiv (Cold Spring Harbor Laboratory) (2021, 3 citations) [burden, reconstruction]. [doi:10.1101/2021.10.16.464630](https://doi.org/10.1101/2021.10.16.464630) `[PREPRINT - NOT PEER REVIEWED]`
    - Genome-scale secretory pathway modeling offers a template for extending GEMs beyond core metabolism to capture secretion burden, directly relevant to metabolic-burden modelling of recombinant protein production in yeast-family hosts like S. cerevisiae and K. phaffii.
- *Genome-scale models of metabolism and expression predict the metabolic burden of recombinant protein expression.* — Metabolic engineering (2024, 37 citations) [burden, reconstruction]. [doi:10.1016/j.ymben.2024.06.005](https://doi.org/10.1016/j.ymben.2024.06.005)
    - Directly relevant methodology paper: ME-model framework linking recombinant protein expression to metabolic burden, applicable to modelling production-strain fitness costs across the project's target fungi.
- *Principles of proteome allocation are revealed using proteomic data and genome-scale models.* — Scientific reports (2016, 44 citations) [ecmodel, omics, reconstruction]. [doi:10.1038/srep36734](https://doi.org/10.1038/srep36734)
    - Introduces proteome-allocation analysis integrating proteomics with genome-scale models, informing enzyme-constrained model construction and metabolic-burden considerations relevant to recombinant protein production across the eight target fungi.
- *Transcriptome-guided parsimonious flux analysis improves predictions with metabolic networks in complex environments.* — PLoS computational biology (2019, 100 citations) [fba, omics, reconstruction]. [doi:10.1371/journal.pcbi.1007099](https://doi.org/10.1371/journal.pcbi.1007099)
    - Presents a transcriptome-integrated parsimonious FBA method for constraining metabolic models in complex media; relevant methodological reference for improving flux predictions and reproducible FBA workflows across the eight fungal GEMs.
- *Integrating proteomic or transcriptomic data into metabolic models using linear bound flux balance analysis.* — Bioinformatics (Oxford, England) (2018, 73 citations) [fba, omics, reconstruction]. [doi:10.1093/bioinformatics/bty445](https://doi.org/10.1093/bioinformatics/bty445)
    - Describes a linear-bound FBA method for integrating proteomic/transcriptomic data into GEMs; directly relevant for constraining fungal models with omics data and for burden modelling of recombinant protein production.
- *EnzymeTuning: a Deep-learning-based Toolbox for Optimizing Enzyme-constrained Metabolic Modeling with Enhanced Proteome Abundance Prediction* — openRxiv (2025, 1 citations) [ecmodel, omics, reconstruction]. [doi:10.1101/2025.08.23.670849](https://doi.org/10.1101/2025.08.23.670849) `[PREPRINT - NOT PEER REVIEWED]`
    - Deep-learning tool for tuning enzyme-constrained models via improved proteome abundance prediction; directly relevant to building enzyme-constrained GEMs and proteome-based constraints for metabolic-burden modeling in the target fungi.
- *Efficient cell factory design by combining meta-heuristic algorithm with enzyme-constrained metabolic models.* — Bioresource technology (2026, 1 citations) [ecmodel, reconstruction]. [doi:10.1016/j.biortech.2026.134706](https://doi.org/10.1016/j.biortech.2026.134706)
    - Presents a meta-heuristic approach for strain design using enzyme-constrained models, potentially applicable to guide ecGEM-based flux predictions and target selection for engineering any of the eight fungal hosts.
- *A hybrid machine learning and enzyme-constrained metabolic model for ab initio prediction of proteome reallocation* — openRxiv (2026, 0 citations) [ecmodel, omics, reconstruction]. [doi:10.64898/2026.07.20.739489](https://doi.org/10.64898/2026.07.20.739489) `[PREPRINT - NOT PEER REVIEWED]`
    - Presents a hybrid ML/enzyme-constrained modeling approach for predicting proteome reallocation, directly relevant to this project's enzyme-constrained model and metabolic-burden modelling needs; note it is an unreviewed preprint.
- *EINN: An enzyme-informed neural network guided by an enzyme-constrained genome-scale metabolic model* — Synthetic and Systems Biotechnology (2027, 0 citations) [ecmodel, reconstruction]. [doi:10.1016/j.synbio.2026.07.009](https://doi.org/10.1016/j.synbio.2026.07.009)
    - Presents an enzyme-informed neural network built on an enzyme-constrained GEM; a methodological approach potentially adaptable for enzyme-constrained modelling and metabolic-burden analysis across the project's target fungi.

## Knowledge-gap summary

| Organism | GEM availability | Curated works | Reconstruction/ecModel papers | Gap severity |
|---|---|---|---|---|
| *Saccharomyces cerevisiae* | excellent | 46 | 36 | none |
| *Yarrowia lipolytica* | good | 21 | 14 | low |
| *Komagataella phaffii* | good | 56 | 16 | low |
| *Aspergillus niger* | moderate | 13 | 11 | medium |
| *Aspergillus oryzae* | moderate | 7 | 5 | medium |
| *Trichoderma reesei* | draft only | 17 | 1 | high |
| *Rhizopus microsporus var. oligosporum* | draft only | 14 | 0 | high |
| *Fusarium venenatum* | absent | 14 | 0 | critical |

The three high- and critical-severity organisms — *F. venenatum*, *R. microsporus* var. *oligosporum* and *T. reesei* — are exactly those with no usable published GEM. Their curated entries are therefore weighted toward genome sequencing, re-annotation and fermentation physiology rather than modelling: that is the evidence base any proxy-host correction or de novo reconstruction must rest on, and its depth sets a hard ceiling on how much confidence an FBA prediction for these three organisms can carry.

Note on *F. venenatum*: 14 curated works exist and none is a reconstruction. The retrieved literature is dominated by mycoprotein production, strain morphology and metabolic engineering of the industrial strain — useful as constraint and validation data, but it does not substitute for a network reconstruction.
