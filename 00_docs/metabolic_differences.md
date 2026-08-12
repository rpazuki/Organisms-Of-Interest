# Metabolic differences that break cross-organism model transfer

Companion to `similarity_matrix.csv` / `similarity_components.csv` / `similarity_heatmap.png`.
Every entry below is a feature that is present (or absent) in the **target** but wired
differently in the **proxy**, so a proxy GEM run unmodified will mispredict. Each entry names
the concrete model surgery needed. Citations are PubMed-verified; DOIs as returned by NCBI ESummary.

## 0. The governing constraint: transfer degrades with taxonomic distance

The central evidence for this whole track is The Sugar Metabolic Model of Aspergillus niger Can Only Be Reliably Transferred to Fungi of Its Phylum [Li J et al., Journal of fungi (Basel, Switzerland), 2022; PMID:36547648 doi:10.3390/jof8121315].
The authors mapped the curated *A. niger* sugar-metabolic network onto five taxonomically
increasingly distant fungi (*A. nidulans*, *Penicillium subrubescens*, *T. reesei*,
*Phanerochaete chrysosporium*, *Dichomitus squalens*) by orthology and validated with
transcriptome, proteome, metabolome and growth profiling. Their conclusion is that pathway
conservation tracks taxonomic distance: near-identical within Eurotiomycetes, measurably
diverged already at *T. reesei* (same phylum, different class), and substantially diverged in
the two Basidiomycetes (different phylum). **Operational reading for this project: an
Ascomycota proxy for an Ascomycota target is defensible with correction; an Ascomycota proxy
for the Mucoromycota target *R. microsporus* is outside the validated envelope of that result
and must be reported as a low-confidence, qualitative-only prediction.**

A second, independent constraint applies to *every* pair below: the biomass equation. Biomass
composition is the least-curated part of most GEMs [Dikicioglu D et al., Metabolomics : Official journal of the Metabolomic Society, 2015; PMID:26491422 doi:10.1007/s11306-015-0819-2], macromolecular composition
shifts with condition so a single fixed biomass equation is questionable across conditions
[Choi YM et al., Computational and structural biotechnology journal, 2023; PMID:37547082 doi:10.1016/j.csbj.2023.07.025], and for *S. cerevisiae* specifically the biomass representation is where
mutant-phenotype prediction fails hardest -- particularly for energy-metabolism genes
[Dikicioglu D et al., Metabolomics : Official journal of the Metabolomic Society, 2015; PMID:26491422 doi:10.1007/s11306-015-0819-2]. A proxy GEM inherits the proxy's biomass equation; this is usually the single
largest source of error in growth-rate transfer, and it is also the easiest thing to correct.

### Annotation-layer disagreement -- a quantified caution

I tested 14 marker enzymes across the 7 organisms with a KEGG genome (98 organism-enzyme
observations) using two independent annotation layers: UniProt EC assignments on the reference
proteome, and KEGG KO assignment. **19 of 98 (19.4%) disagreed** (`marker_annotation_concordance.csv`).
Worst offenders: isocitrate lyase (5 disagreements), dihydroxyacetone synthase (4), alcohol
oxidase (4). This is not a data-cleaning nuisance -- it is the mechanism by which orthology-based
transfer introduces error, and it means **no single-gene presence/absence call below should be
treated as settled without targeted literature or experimental confirmation.** Where a claim
below rests on annotation alone I say so.

---

## 1. *R. microsporus* (target, Mucoromycota) <- any Ascomycota proxy

Similarity to the best Ascomycota candidate is **0.43** (*A. niger*),
against **0.83** for the *F. venenatum*/*T. reesei* pair. This is a
different phylum: NCBI Taxonomy places *R. microsporus* in Mucoromycota / Mucoromycotina /
Mucoromycetes / Mucorales / Rhizopodaceae, sharing with all seven others only the rank
**kingdom (Fungi)** -- shared-rank depth 1/7, versus 3/7 for the deepest cross-class Ascomycota
pairs. **Confidence tier: lowest of the three gap organisms.**

### 1.1 Reductive TCA (rTCA) to fumarate -- a flux mode the proxy will not use
*Rhizopus* produces fumarate via cytosolic CO2 fixation: pyruvate carboxylase carboxylates
pyruvate to oxaloacetate, then malate dehydrogenase and fumarase run reductively to fumarate.
The role of pyruvate carboxylase in *Rhizopus* fumarate production was established early
[Overman SA et al., Biochemical and biophysical research communications, 1969; PMID:5349282 doi:10.1016/0006-291x(69)90937-1] and its subcellular localisation and regulation characterised in *R. arrhizus*
[Osmani SA et al., European journal of biochemistry, 1985; PMID:3971971 doi:10.1111/j.1432-1033.1985.tb08727.x]. Overexpressing *pyc* and *pepc* in *R. oryzae* modulates fumarate biosynthesis,
confirming these as controlling steps [Zhang B et al., Metabolic engineering, 2012; PMID:22814110 doi:10.1016/j.ymben.2012.07.001]; *Rhizopus* rTCA enzymes (pyc, mdh)
are transplantable enough that they have been used to build rTCA C4-acid routes in other hosts
[Chen X et al., Applied microbiology and biotechnology, 2017; PMID:28229207 doi:10.1007/s00253-017-8141-8]. *Rhizopus* is more broadly framed as a platform for C4 platform chemicals
[Meussen BJ et al., Applied microbiology and biotechnology, 2012; PMID:22526790 doi:10.1007/s00253-012-4033-0], and fumarate bioproduction strategy reviews center on it [Sebastian J et al., Critical reviews in biotechnology, 2019; PMID:31138023 doi:10.1080/07388551.2019.1620677].

**Why transfer breaks:** every candidate proxy GEM *has* pyruvate carboxylase, malate
dehydrogenase and fumarase (confirmed in all 8 proteomes, `marker_enzyme_presence.csv`), but
the reactions are compartmentalised and bounded for anaplerosis, not for reductive overflow to
an exported C4 acid. Under FBA the proxy therefore cannot carry high fumarate flux even though
the genes are present.

**Correction protocol:** (i) add or unblock a *cytosolic* pyc-mdh-fumarase branch with reversibility
set for reductive operation; (ii) add a fumarate transport + exchange reaction -- absent as a
secretion route from Ascomycota GEMs; (iii) re-balance cytosolic NADH, since the reductive branch
is an NADH sink competing with ethanol formation; (iv) treat resulting yields as order-of-magnitude only.

### 1.2 L-lactate co-export and the LDH/PDC/ADH branch point
*R. oryzae* is an industrial L-lactate producer; LDH genes were isolated and expressed
[Skory CD et al., Applied and environmental microbiology, 2000; PMID:10831409 doi:10.1128/AEM.66.6.2343-2348.2000], transformants with modified LDH activity shift lactate yield [Skory CD et al., Applied microbiology and biotechnology, 2004; PMID:14624317 doi:10.1007/s00253-003-1480-7],
RNA silencing of LDH redirects flux [Gheinani AH et al., Journal of RNAi and gene silencing : an international journal of RNA and gene targeting research, 2011; PMID:21769297], and in vivo co-regulation of ADH and LDH
sets the lactate/ethanol split [Thitiprasert S et al., Applied biochemistry and biotechnology, 2011; PMID:21416338 doi:10.1007/s12010-011-9214-2]. Manipulating pyruvate decarboxylase changes the
same node [Thitiprasert S et al., Applied biochemistry and biotechnology, 2014; PMID:25149454 doi:10.1007/s12010-014-1155-0], and metabolic control analysis has been applied to the L-lactate
pathway itself [Ke W et al., Bioprocess and biosystems engineering, 2015; PMID:26288952 doi:10.1007/s00449-015-1458-8]. The *Rhizopus* lactate route remains an active platform
[Akter MM et al., Bioresources and bioprocessing, 2025; PMID:41335363 doi:10.1186/s40643-025-00982-6].

**Why transfer breaks:** L-lactate dehydrogenase (EC 1.1.1.27) is present in the
*R. microsporus* reference proteome and **absent from *S. cerevisiae*, *Y. lipolytica*,
*K. phaffii*, *T. reesei* and *A. oryzae*** (`marker_enzyme_presence.csv`; of the eight, only
*R. microsporus* and *A. niger* carry an EC 1.1.1.27 annotation). A proxy GEM built on any of
those five has **no lactate-producing reaction at all** -- the fermentative product spectrum is
structurally wrong, not merely mis-parameterised.

**Correction protocol:** add LDH + lactate transport/exchange; then re-fit the pyruvate node,
because adding an NADH-consuming pyruvate sink alongside PDC/ADH changes the predicted
ethanol:lactate:CO2 split for *every* carbon source, not just the one of interest.

### 1.3 The only Mucoromycota GEMs are for a different genus
No *Rhizopus* GEM was found. The nearest published Mucoromycota reconstruction is
*Mucor circinelloides* **iWV1213** -- 1213 genes, 1413 metabolites, 1326 reactions, compartmentalised,
FBA-validated against growth rates on multiple nutrient sources [Vongsangnak W et al., Gene, 2016; PMID:26911256 doi:10.1016/j.gene.2016.02.028], later used to
study a lipid-overproducing strain [Isarankura Na Ayudhya N et al., PeerJ, 2019; PMID:31316868 doi:10.7717/peerj.7015]. Mucoromycota are actively promoted as
biorefinery chassis [Dzurendova S et al., Applied microbiology and biotechnology, 2022; PMID:34889982 doi:10.1007/s00253-021-11720-1].
**Recommendation for the modelling track: iWV1213 (Mucor -- same subphylum Mucoromycotina, same
order Mucorales) is very likely a better structural starting point for *R. microsporus* than any
Ascomycota GEM, despite scoring outside our 8-organism matrix.** This is the single most
consequential finding of this track and should be checked before proxy assignment is fixed.

### 1.4 Tempeh-relevant physiology is absent from every candidate
The lab's *R. microsporus* var. *oligosporus* is the tempeh organism: solid-substrate growth on
soybean/cereal with extensive proteolytic and lipolytic hydrolysis of the substrate
[Hachmeister KA et al., Critical reviews in microbiology, 1993; PMID:8267862 doi:10.3109/10408419309113527], and in mixed culture with lactic acid bacteria and yeasts during fermentation
[Feng XM et al., International journal of food microbiology, 2005; PMID:15979185 doi:10.1016/j.ijfoodmicro.2005.03.005]. No candidate proxy GEM represents solid-state growth, substrate-bound
hydrolysis, or co-culture. Any FBA here must be interpreted as a submerged-culture idealisation.

---

## 2. *F. venenatum* (target, Hypocreales) <- *T. reesei* (best score) or *A. niger*/*A. oryzae* (best available model)

Similarity: *T. reesei* **0.83** (same order, Hypocreales),
*A. niger* **0.71**, *A. oryzae* **0.69**.
The score-optimal proxy is *T. reesei*, but *T. reesei*'s only GEM is a CoReCo draft
(0 genes, 1 compartment, 0 exchange reactions, not FBA-capable in the probe). **The
score-optimal proxy and the model-optimal proxy differ for this target** -- the modelling track
must reconcile these. Note the phylum-transfer result [Li J et al., Journal of fungi (Basel, Switzerland), 2022; PMID:36547648 doi:10.3390/jof8121315] explicitly measured
*A. niger* -> *T. reesei* as already diverged, so an *A. niger* proxy for a Hypocreales target
inherits that documented divergence.

### 2.1 Mycoprotein biomass composition is the whole point and the whole problem
*F. venenatum* is grown for biomass itself, not a secreted metabolite -- established as a
human-consumption mycoprotein [Wiebe MG et al., Applied microbiology and biotechnology, 2002; PMID:11954786 doi:10.1007/s00253-002-0931-x] and now a target for food-biomanufacturing
engineering [Tong S et al., Metabolic engineering, 2026; PMID:41015229 doi:10.1016/j.ymben.2025.09.009]. Its biomass carries substantial **chitin-rich cell wall / dietary
fibre**: knocking out chitin synthase *FvChs3* cut chitin content 26%, which *by itself* raised
carbon conversion efficiency 16% and protein conversion 36%, and cut fermentation ethanol 47%
[Hong R et al., Journal of agricultural and food chemistry, 2024; PMID:39586715 doi:10.1021/acs.jafc.4c07105]. Cell-wall engineering is an explicit yield lever [Wu X et al., Bioresource technology, 2025; PMID:40680943 doi:10.1016/j.biortech.2025.133005], mycelium
structure is genetically tunable [Wu X et al., Food research international (Ottawa, Ont.), 2025; PMID:41214985 doi:10.1016/j.foodres.2025.117498], and yield/CO2 performance has been improved by
combined metabolic and fermentation engineering [Tong S et al., Journal of agricultural and food chemistry, 2024; PMID:38153978 doi:10.1021/acs.jafc.3c08509]. Biokinetic parameter estimation
with uncertainty quantification has been done for *F. venenatum* A3/5 on lignocellulosic
feedstock [Banks M et al., Current research in food science, 2024; PMID:39555020 doi:10.1016/j.crfs.2024.100908] -- the most directly usable quantitative anchor for calibrating a proxy.

**Why transfer breaks:** *A. niger* and *A. oryzae* GEM biomass equations are tuned for an
organic-acid or enzyme producer. Using them for *F. venenatum* misallocates carbon between
protein, chitin/glucan wall, and lipid -- and because the objective *is* biomass here, that
error propagates directly into the headline number (growth/protein yield). [Hong R et al., Journal of agricultural and food chemistry, 2024; PMID:39586715 doi:10.1021/acs.jafc.4c07105]
quantifies the magnitude: a 26% chitin change moves carbon efficiency by 16%.

**Correction protocol:** this is the highest-value single correction in the whole project.
Replace the proxy biomass equation with an *F. venenatum*-specific one (high protein fraction,
elevated chitin), and -- following [Choi YM et al., Computational and structural biotechnology journal, 2023; PMID:37547082 doi:10.1016/j.csbj.2023.07.025] -- run it as an *ensemble* over plausible
compositions rather than one point estimate, reporting a growth-rate interval instead of a
single value. Calibrate against [Banks M et al., Current research in food science, 2024; PMID:39555020 doi:10.1016/j.crfs.2024.100908].

### 2.2 Ethanol overflow at the pyruvate node
[Hong R et al., Journal of agricultural and food chemistry, 2024; PMID:39586715 doi:10.1021/acs.jafc.4c07105] reports substantial ethanol production during *F. venenatum* fermentation
(reduced 47% on *FvChs3* knockout, and further affected by *FvPDC6* pyruvate decarboxylase
knockout). Aspergillus GEMs are not parameterised for this overflow. Without an unblocked
PDC/ADH branch and a fitted overflow constraint, a proxy will over-predict biomass yield by
assigning to biomass the carbon that in reality leaves as ethanol.

### 2.3 Filamentous morphology and maintenance energy
*F. venenatum* grows as mycelium with texture-relevant morphology [Wu X et al., Food research international (Ottawa, Ont.), 2025; PMID:41214985 doi:10.1016/j.foodres.2025.117498]. Neither
morphology nor its maintenance cost is in any candidate GEM. Maintenance-energy requirements
(ATP for non-growth functions) have been quantified for *S. cerevisiae* at near-zero growth
[Vos T et al., Microbial cell factories, 2016; PMID:27317316 doi:10.1186/s12934-016-0501-z] and for *K. phaffii*, which shows high viability and a notably *low*
maintenance requirement near zero growth [Rebnegger C et al., Applied and environmental microbiology, 2016; PMID:27208115 doi:10.1128/AEM.00638-16] -- i.e. the yeast maintenance values
that a yeast-proxy GEM would carry are not transferable to a filamentous target. Mycelial
networks have distinct transport and architecture [Fricker MD et al., Microbiology spectrum, 2017; PMID:28524023 doi:10.1128/microbiolspec.FUNK-0033-2017], now being modelled explicitly
in 3D [Palmer BJ et al., Physical review. E, 2025; PMID:41116360 doi:10.1103/xbjp-zqj1].

**Correction protocol:** re-fit ATPM (non-growth-associated maintenance) from *F. venenatum*
chemostat data rather than inheriting the proxy's value; report growth-rate predictions as
sensitive to ATPM and show that sensitivity.

---

## 3. *T. reesei* (target, Hypocreales) <- *F. venenatum* (score) / *A. niger* or *A. oryzae* (models)

Similarity: *F. venenatum* **0.83**, *A. niger*
**0.69**, *A. oryzae* **0.68**.
Both top-scoring neighbours lack a usable GEM, so *A. niger*/*A. oryzae* is forced.

### 3.1 This exact transfer has been measured and found lossy
[Li J et al., Journal of fungi (Basel, Switzerland), 2022; PMID:36547648 doi:10.3390/jof8121315] included *T. reesei* as one of the five recipients of the *A. niger* sugar
network and reported a higher level of diversity between *T. reesei* and *A. niger* than among
the three Eurotiomycetes. **The proposed proxy direction for *T. reesei* is therefore a
published negative-control case, not an untested assumption.** Sugar-uptake and catabolic
predictions from an *A. niger* proxy should be flagged as the least reliable class of output.

### 3.2 Massive cellulase secretion is an unmodelled proteome/ATP burden
*T. reesei* is the principal industrial cellulase producer and diverts a large carbon and energy
fraction into secreted hydrolases. Its secretion is regulated by Xyr1 and related activators
[Lv D et al., Journal of agricultural and food chemistry, 2023; PMID:37523749 doi:10.1021/acs.jafc.3c03466], a fusion activator can drive high cellulase/xylanase output even on glucose
[Lv D et al., Bioresource technology, 2023; PMID:36565817 doi:10.1016/j.biortech.2022.128520], regulatory and secretion networks are being dissected mechanistically
[Cui S et al., Biotechnology journal, 2026; PMID:42390029 doi:10.1002/biot.70241], COPII core components are required for secretion [Wang Z et al., International journal of biological macromolecules, 2026; PMID:41478487 doi:10.1016/j.ijbiomac.2025.149971], and
promoter/genetic strategies for enhanced expression are established [Adnan M et al., Microbiological research, 2022; PMID:35339938 doi:10.1016/j.micres.2022.127011]. It is
deployed as an economically competitive enzyme platform [de Lima EA et al., Bioresource technology, 2022; PMID:36162784 doi:10.1016/j.biortech.2022.128019] and can co-produce
carotenoid alongside cellulase [Li J et al., Journal of agricultural and food chemistry, 2023; PMID:37042195 doi:10.1021/acs.jafc.3c00690].

**Why transfer breaks:** stoichiometric FBA has no term for the proteome cost of secreting
grams-per-litre of enzyme. Annotation confirms the capability gap qualitatively -- EC 3.2.1.91
(cellobiohydrolase) appears in the *A. niger* and *A. oryzae* reference proteomes but not in
*T. reesei*'s UniProt EC set, while KEGG *does* assign K01225 to *T. reesei*: one of the 19
discordant calls above, and a direct illustration that annotation-based transfer of secretory
capability is unreliable.

**Correction protocol:** add an explicit secreted-protein sink reaction with amino-acid
stoichiometry and its ATP/GTP translation+translocation cost, then constrain its flux from
measured titres. For a principled version, move to an enzyme-constrained model -- the approach
has been demonstrated for a comparable filamentous fungus, *Myceliophthora thermophila*
[Wang Y et al., Microbial cell factories, 2024; PMID:38750569 doi:10.1186/s12934-024-02415-z]. Without this, a proxy will over-predict growth because secreted-protein carbon
is invisible to it.

### 3.3 Respiratory, not fermentative, central carbon operation
13C flux-ratio and carbon-path analysis showed *T. reesei* uses primarily the respirative
pathway [Jouhten P et al., BMC systems biology, 2009; PMID:19874611 doi:10.1186/1752-0509-3-104], consistent with adaptation to nutrient-poor environments. A
*S. cerevisiae*-derived proxy (Crabtree-positive, fermentative at high glucose
[Malina C et al., Proceedings of the National Academy of Sciences of the United States of America, 2021; PMID:34903663 doi:10.1073/pnas.2112836118]) would predict the wrong product spectrum entirely -- an argument for the
filamentous Aspergillus proxy over the better-curated yeast GEMs.

### 3.4 The existing *T. reesei* GEM and its limits
A whole-genome *T. reesei* model was built by comparative reconstruction with CoReCo, together
with 55 related species, and includes an experimentally measured *T. reesei* biomass equation
[Castillo S et al., Biotechnology for biofuels, 2016; PMID:27895706 doi:10.1186/s13068-016-0665-0]. Our probe of `CoReCo_Treesei` (MODEL1302010019) found 2145 reactions,
1985 metabolites, **0 genes, 1 compartment, 0 exchange reactions** and no FBA capability.
**Actionable:** the publication reports a measured biomass composition -- that biomass equation is
worth extracting from the paper/supplement even if the SBML itself is unusable, because it solves
the section-2.1-type problem for *T. reesei* directly.

---

## 4. Features of the *proxy* organisms that must be switched OFF

A proxy carries its own specialisations into the simulation. These are false-positive
capabilities for the targets.

### 4.1 *Y. lipolytica* -- lipid accumulation and peroxisomal beta-oxidation
*Y. lipolytica* is the model for lipid accumulation [Beopoulos A et al., Biochimie, 2009; PMID:19248816 doi:10.1016/j.biochi.2009.02.004], with GEMs built expressly
around it: the first genome-scale model [Loira N et al., BMC systems biology, 2012; PMID:22558935 doi:10.1186/1752-0509-6-35] (built, notably, on an *S. cerevisiae*
scaffold -- itself a documented cross-species transfer), lipid-production optimisation
[Kavšček M et al., BMC systems biology, 2015; PMID:26503450 doi:10.1186/s12918-015-0217-4], in silico strategies for improved lipid production [Kim M et al., Biotechnology for biofuels, 2019; PMID:31367232 doi:10.1186/s13068-019-1518-4],
model-driven oil engineering [Duman-Özdamar ZE et al., Microbial biotechnology, 2025; PMID:40113666 doi:10.1111/1751-7915.70089], dicarboxylic-acid strain design [Mishra P et al., BMC systems biology, 2018; PMID:29560822 doi:10.1186/s12918-018-0542-5],
and an enzyme-constrained model predicting growth-phase-specific metabolism [De Biaggi JS et al., Applied microbiology and biotechnology, 2026; PMID:41876849 doi:10.1007/s00253-026-13791-4].
Peroxisomal beta-oxidation capacity is central and engineerable [Zhang B et al., Journal of agricultural and food chemistry, 2022; PMID:35763312 doi:10.1021/acs.jafc.2c02242]
[Hanko EKR et al., Metabolic engineering, 2018; PMID:29852272 doi:10.1016/j.ymben.2018.05.018], peroxisome number/size is regulated by beta-oxidation flux [Smith JJ et al., The Journal of biological chemistry, 2000; PMID:10787422 doi:10.1074/jbc.M909285199],
and peroxisomal beta-oxidation activity is directly tied to product formation [Pagot Y et al., Applied microbiology and biotechnology, 1998; PMID:9581293 doi:10.1007/s002530051172];
peroxisome engineering is an active lever [Somasundaram S et al., Biotechnology and bioengineering, 2026; PMID:41627046 doi:10.1002/bit.70166]. It also has a dedicated citrate
exporter, Cex1 [Erian AM et al., FEMS yeast research, 2020; PMID:32990722 doi:10.1093/femsyr/foaa055].
**Transfer consequence:** using iYali as a proxy for a non-oleaginous target will predict lipid
as a carbon sink that the target does not use at that scale. Constrain lipid-body accumulation
and the beta-oxidation cycle down before interpreting yields.

### 4.2 *K. phaffii* -- methanol/AOX metabolism and peroxisome expansion
Methylotrophy is a whole pathway the other seven do not run industrially: alcohol oxidase (AOX)
in an expanded peroxisome, formaldehyde split between assimilation (xylulose-monophosphate
cycle via dihydroxyacetone synthase) and dissimilation. Mit1 mediates methanol signalling and
regulates the AOX1 promoter [Wang X et al., The Journal of biological chemistry, 2016; PMID:26828066 doi:10.1074/jbc.M115.692053]. GEMs exist: iPP668, fully compartmentalised, 1361
reactions / 1177 metabolites [Chung BK et al., Microbial cell factories, 2010; PMID:20594333 doi:10.1186/1475-2859-9-50]; reconstructions of *P. pastoris* alongside
*P. stipitis* with in silico evaluation [Caspeta L et al., BMC systems biology, 2012; PMID:22472172 doi:10.1186/1752-0509-6-24]; industrial-*Pichia* reconstruction and
flux analysis [Chung BK et al., Applied microbiology and biotechnology, 2013; PMID:23339015 doi:10.1007/s00253-013-4702-7]; comparative genome-scale analysis across variants to pick a base
strain [Brady JR et al., Biotechnology and bioengineering, 2020; PMID:31654411 doi:10.1002/bit.27209]; and a model-based fed-batch feeding strategy [Boojari MA et al., Microbial biotechnology, 2023; PMID:37093126 doi:10.1111/1751-7915.14264]. Flux
analysis on glycerol/methanol mixes is available [Jordà J et al., New biotechnology, 2014; PMID:23845285 doi:10.1016/j.nbt.2013.06.007], methanol utilisation is tunable
by reducing AOX activity plus co-substrate [Liu S et al., Journal of fungi (Basel, Switzerland), 2023; PMID:37108877 doi:10.3390/jof9040422], and methanol/formate co-feeding is
being exploited [Ul Z et al., New biotechnology, 2026; PMID:42276244 doi:10.1016/j.nbt.2026.06.004].
**Annotation note:** dihydroxyacetone synthase (EC 2.2.1.3) is annotated **only** in
*K. phaffii* among the eight UniProt reference proteomes -- the cleanest organism-specific marker
in the panel, and consistent with methylotrophy being genuinely restricted here. (KEGG's K17100
is assigned more broadly, another of the 19 discordances.)
**Transfer consequence:** switch off methanol uptake, AOX and the XuMP cycle when using
*K. phaffii* as a proxy. Conversely, *K. phaffii*'s unusually low maintenance-energy requirement
near zero growth [Rebnegger C et al., Applied and environmental microbiology, 2016; PMID:27208115 doi:10.1128/AEM.00638-16] must not be carried into a filamentous target (section 2.3).

### 4.3 *A. niger* / *A. oryzae* -- organic-acid overflow and export
*A. niger*'s citrate overflow is a genuine metabolic peculiarity, identified as such by
comparative metabolic genomics against seven other fungi alongside the first *A. niger*
genome-scale network [Sun J et al., Genome biology, 2007; PMID:17784953 doi:10.1186/gb-2007-8-9-r182]. Citrate uptake and export are reciprocally regulated by
manganese [Netik A et al., Biochimica et biophysica acta, 1997; PMID:9218559 doi:10.1016/s0005-2736(97)00032-1]; disrupting a putative citrate exporter decreases production
[Kirimura K et al., Bioscience, biotechnology, and biochemistry, 2019; PMID:30720390 doi:10.1080/09168451.2019.1574205]; blocking active citrate export produces a global transcriptional response
[Laothanachareon T et al., Journal of fungi (Basel, Switzerland), 2021; PMID:34071072 doi:10.3390/jof7060409]; transporter engineering raises titre [Li J et al., Journal of fungi (Basel, Switzerland), 2026; PMID:42506234 doi:10.3390/jof12070472]. Modelling of citric-acid
production has a long history [Alvarez-Vasquez F et al., Biotechnology and bioengineering, 2000; PMID:10940866 doi:10.1002/1097-0290(20001005)70:1<82::aid-bit10>3.0.co;2-v] and transcriptomic data have been integrated with
the *A. niger* metabolic model to find engineering targets [Upton DJ et al., Biotechnology for biofuels and bioproducts, 2022; PMID:35418297 doi:10.1186/s13068-021-02099-2]. *A. oryzae* has its
own GEM, used to improve genome annotation [Vongsangnak W et al., BMC genomics, 2008; PMID:18500999 doi:10.1186/1471-2164-9-245], with a recent engineered-strain
reconstruction [Raethong N et al., International journal of molecular sciences, 2025; PMID:40725156 doi:10.3390/ijms26146906]; an *A. tubingensis* GEM also exists [Kaushal M et al., Biotechnology for biofuels and bioproducts, 2024; PMID:38807234 doi:10.1186/s13068-024-02506-4].
**Transfer consequence:** an *A. niger* proxy will route carbon into citrate overflow --
a large, easily-flagged artefact when the target is a mycoprotein or enzyme producer. Close the
citrate exchange (and other organic-acid exchanges) before running target simulations, and check
the flux distribution for organic-acid leakage every time.

### 4.4 *S. cerevisiae* -- Crabtree fermentation and the best-curated biomass equation
The consensus models Yeast8 [Lu H et al., Nature communications, 2019; PMID:31395883 doi:10.1038/s41467-019-11581-3] and Yeast9 [Zhang C et al., Molecular systems biology, 2024; PMID:39134886 doi:10.1038/s44320-024-00060-7] are the most curated
GEMs in this panel. But *S. cerevisiae* is Crabtree-positive: metabolic and translational
adaptations give rise to the Crabtree effect [Malina C et al., Proceedings of the National Academy of Sciences of the United States of America, 2021; PMID:34903663 doi:10.1073/pnas.2112836118], and redox balancing differs across
yeast species [Henriques D et al., mSystems, 2021; PMID:34342535 doi:10.1128/mSystems.00260-21]. Its high similarity to *Y. lipolytica* (0.69)
and *K. phaffii* (0.69) makes it a reasonable yeast proxy and a
poor filamentous proxy -- its similarity to *F. venenatum* is only 0.53,
the lowest of any Ascomycota pairing with that target.

---

## 5. Cross-cutting structural mismatches

### 5.1 Compartmentalisation depth
From the probe: yeast-GEM 14 compartments, iYali 14, iMT1026 (*K. phaffii*) 9, iLC915
(*P. pastoris*) 7, iWV1314 (*A. oryzae*) 4, iMA871 (*A. niger*) 3, and both CoReCo drafts
(*T. reesei*, *Rhizopus*) **1**. Compartmentalisation is not cosmetic: it is what makes
cytosolic-vs-mitochondrial rTCA (1.1), peroxisomal beta-oxidation (4.1) and peroxisomal
methanol oxidation (4.2) distinguishable at all. A 1-compartment draft cannot represent any of
them, and a 3-compartment *A. niger* model cannot represent peroxisomal biology that a
14-compartment yeast model can.
**Consequence:** transfer direction matters. Moving a question *from* a well-compartmentalised
proxy *to* a coarse target is safer than the reverse; and a proxy with fewer compartments than
the target's biology requires cannot answer localisation-dependent questions at all,
irrespective of taxonomic similarity.

### 5.2 Filamentous vs unicellular growth
Five candidates are filamentous (*F. venenatum*, *T. reesei*, *A. niger*, *A. oryzae*,
*R. microsporus*), three unicellular (*S. cerevisiae*, *Y. lipolytica*, *K. phaffii*). Mycelium
is a transport network with its own architecture [Fricker MD et al., Microbiology spectrum, 2017; PMID:28524023 doi:10.1128/microbiolspec.FUNK-0033-2017], now amenable to 3D modelling of
fusion, branching and nutrient transport [Palmer BJ et al., Physical review. E, 2025; PMID:41116360 doi:10.1103/xbjp-zqj1], and morphology is a manipulable
process variable [Wu X et al., Food research international (Ottawa, Ont.), 2025; PMID:41214985 doi:10.1016/j.foodres.2025.117498]. Stoichiometric FBA is morphology-blind. **Practical rule:
never use a yeast GEM as the proxy for a filamentous target if the question involves growth
rate, maintenance, oxygen transfer or biomass yield** -- restrict yeast proxies to
pathway-topology questions.

### 5.3 Genome and proteome scale
Reference-proteome sizes span 5038 (*K. phaffii* GS115) to 14069 (*A. niger* CBS 513.88-lineage)
proteins. KEGG gene counts show the same split: 5040 (ppa) to 14516 (fvn). A GEM's gene coverage
sets how much of the target's metabolism can even be addressed; a proxy with half the target's
gene complement cannot represent target-specific catabolic breadth. The *A. oryzae* reference
proteome additionally reports only **83.6%** BUSCO completeness (and the non-strain-pinned
*A. oryzae* entries in UniProt sit near 59%), the weakest genomic foundation in the panel -- a
caution for using *A. oryzae* as a proxy at all.

---

## 6. Summary of correction burden per proposed transfer

| Target <- proxy | Score | Blockers requiring model surgery | Residual confidence |
|---|---|---|---|
| *F. venenatum* <- *A. niger* | 0.71 | biomass eq. (protein/chitin), ethanol overflow, ATPM, close citrate export | Medium |
| *F. venenatum* <- *A. oryzae* | 0.69 | as above + weakest proteome completeness (83.6% BUSCO) | Medium-low |
| *T. reesei* <- *A. niger* | 0.69 | secreted-cellulase sink + ATP cost, respiro-fermentative balance, close citrate export; **documented lossy** [Li J et al., Journal of fungi (Basel, Switzerland), 2022; PMID:36547648 doi:10.3390/jof8121315] | Medium-low |
| *T. reesei* <- *A. oryzae* | 0.68 | as above + proteome completeness | Low-medium |
| *R. microsporus* <- *A. niger* | 0.43 | cytosolic rTCA + fumarate export, LDH + lactate export, cytosolic NADH rebalance, Mucoromycota wall/biomass, solid-state growth unmodelled | **Low -- cross-phylum, outside validated envelope** |
| *R. microsporus* <- *Mucor circinelloides* iWV1213 (off-matrix) | n/a | same subphylum and order; oleaginous-lipid bias to constrain; still not *Rhizopus* | **Recommended over any Ascomycota proxy -- verify first** |

All three gap organisms score their nearest neighbour among organisms that *also* lack a usable
GEM (*F. venenatum* <-> *T. reesei* at 0.83; *R. microsporus*'s
nearest relative absent from the panel entirely). Proxy assignment is therefore a two-objective
problem -- similarity and model quality -- and the two objectives disagree for every one of the
three targets.
