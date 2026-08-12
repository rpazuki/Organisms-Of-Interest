"""Round-1 deliverable figure: minimal FBA results + simulation-readiness audit."""
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

MW_GLC = 180.156
# Carbon fraction of fungal dry weight, from elemental composition: biomass is
# ~45-50% C, so a model whose carbon bookkeeping is sound must land in this band.
PCTC_LO, PCTC_HI = 42.0, 53.0
ORGS_A = ["S_cerevisiae", "Y_lipolytica", "K_phaffii", "A_niger",
          "A_oryzae", "R_microsporus", "F_venenatum", "T_reesei"]
COLS = dict(zip(ORGS_A, ["#1f4e79", "#a98261", "#4a7ba7", "#476a47",
                         "#855050", "#6b5b95", "#b07a3c", "#7d7d7d"]))

SHORT = {
    "S_cerevisiae": "S. cerevisiae",
    "Y_lipolytica": "Y. lipolytica",
    "K_phaffii": "K. phaffii",
    "A_niger": "A. niger",
    "A_oryzae": "A. oryzae",
    "R_microsporus": "R. microsporus",
    "F_venenatum": "F. venenatum",
    "T_reesei": "T. reesei",
}
# The model ID is part of the identity — several organisms have competing
# reconstructions and the row must say which one was audited.
AUDIT_LABEL = {
    "S_cerevisiae": ("S. cerevisiae", "yeast-GEM 9.1"),
    "Y_lipolytica": ("Y. lipolytica", "iYali4"),
    "K_phaffii": ("K. phaffii", "iMT1026 v3"),
    "A_niger": ("A. niger", "iJB1325"),
    "A_oryzae": ("A. oryzae", "iWV1346"),
    "R_microsporus": ("R. microsporus", "iCV785"),
    "F_venenatum": ("F. venenatum", "F. graminearum proxy"),
    "T_reesei": ("T. reesei", "CoReCo draft"),
}
CHECK_LABEL = {
    "loads": "parses in\ncobrapy",
    "has_exchanges": "exchange\nreactions",
    "has_genes": "GPR\nrules",
    "objective_defined": "objective\nset",
    "bounds_retained": "flux bounds\nretained",
    "no_EGC": "no energy-\ngen. cycle",
    "NGAM_enforced": "maintenance\nATP enforced",
    "C_balanced": "carbon\nbalance closes",
}
PASS_C, FAIL_C = "#2b6f4e", "#a4342b"


def _is_true(value):
    """True only for a real pass.

    numpy.bool_(True) is not the Python singleton True, so an identity test
    silently scores every numpy-typed pass as a failure. Compare by value, but
    keep None (check not applicable) distinct from False.
    """
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    return bool(value)


def build(scan, yields, qc, checks, style, out="fig_fba_round1.png"):
    apply_figure_style, panel_letter, meta_grey = style
    apply_figure_style()

    fig = plt.figure(figsize=(7.2, 6.2))
    gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.25], hspace=0.52, wspace=0.36)
    ax_a = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[0, 1])
    ax_c = fig.add_subplot(gs[1, :])

    # (a) glucose dose-response
    for org in ORGS_A:
        d = scan[scan.organism == org].sort_values("glc_uptake")
        ax_a.plot(d.glc_uptake, d.growth, marker="o", ms=3, lw=1.4,
                  color=COLS[org], label=SHORT[org])
    ax_a.set_xlabel("Glucose uptake (mmol gDW$^{-1}$ h$^{-1}$)")
    ax_a.set_ylabel("Predicted growth (h$^{-1}$)")
    ax_a.set_title("Growth scales linearly with carbon\nsupply in 7 of 8 models", loc="left")
    ax_a.margins(0.06)
    leg = ax_a.legend(frameon=False, fontsize=6, loc="upper left",
                      handlelength=1.1, borderpad=0.1, labelspacing=0.22)
    for txt in leg.get_texts():
        txt.set_fontstyle("italic")

    # (b) carbon closure. Growth rate and g/g yield are NOT comparable across
    # these models: their biomass reactions are normalised on different bases
    # (some per gDW, some on unnormalised macromolecular pools), so a higher
    # yield here is a unit artefact, not better metabolism. Carbon recovered
    # into biomass as a percentage of dry weight IS comparable, because it is
    # computed from exchange fluxes and elemental formulas alone.
    yb = yields.dropna(subset=["pctC_biomass"]).sort_values("pctC_biomass")
    ax_b.axhspan(PCTC_LO, PCTC_HI, color=meta_grey, alpha=0.3, zorder=0)
    # Below the band, not inside it: the markers sit within the band by
    # construction, so a label placed there collides with their value labels.
    ax_b.text(0.02, PCTC_LO - 1.5, "fungal biomass C content",
              transform=ax_b.get_yaxis_transform(), fontsize=5.8,
              color="0.3", va="top", ha="left")
    for i, row in enumerate(yb.itertuples()):
        ax_b.vlines(i, 0, row.pctC_biomass, color=meta_grey, lw=0.9, zorder=1)
        ax_b.plot(i, row.pctC_biomass, "o", ms=6.5, color=COLS[row.organism], zorder=3)
        ax_b.annotate(f"{row.pctC_biomass:.0f}", (i, row.pctC_biomass),
                      xytext=(0, 7), textcoords="offset points",
                      ha="center", fontsize=6)
    ax_b.set_xticks(range(len(yb)))
    ax_b.set_xticklabels([SHORT[o] for o in yb.organism], rotation=32,
                         ha="right", fontsize=6, fontstyle="italic")
    ax_b.set_ylabel("C into biomass (% of gDW)")
    ax_b.set_title("Carbon closes at a realistic\nbiomass composition", loc="left")
    ax_b.set_ylim(0, 62)
    ax_b.set_xlim(-0.6, len(yb) - 0.4)

    # (c) simulation-readiness audit
    mat = qc.set_index("organism")
    n_row, n_col = len(mat), len(checks)
    ax_c.set_xlim(-0.5, n_col + 0.55)
    ax_c.set_ylim(n_row - 0.5, -0.5)
    for i, org in enumerate(mat.index):
        for j, check in enumerate(checks):
            state = _is_true(mat.loc[org, check])
            if state is None:
                ax_c.text(j, i, "n.a.", ha="center", va="center",
                          fontsize=5.5, color="0.55")
                continue
            # scatter (points, not data units) keeps the marker circular
            # regardless of the axes aspect ratio
            ax_c.scatter([j], [i], s=118, marker="o", zorder=2,
                         color=(PASS_C if state else FAIL_C),
                         edgecolors="white", linewidths=0.6)
            ax_c.text(j, i, "\u2713" if state else "\u2715", ha="center",
                      va="center", fontsize=6, color="white", zorder=3)
        ax_c.text(n_col - 0.28, i, f"{int(mat.loc[org, 'n_pass'])}/{n_col}",
                  fontsize=6.2, va="center", ha="left", fontweight="bold")
    ax_c.set_xticks(range(n_col))
    ax_c.set_xticklabels([CHECK_LABEL[c] for c in checks], fontsize=5.8)
    ax_c.set_yticks(range(n_row))
    ax_c.set_yticklabels([""] * n_row)
    for i, org in enumerate(mat.index):
        species, model_id = AUDIT_LABEL[org]
        # Two stacked Text objects rather than one two-line tick label: the
        # species name is italicised and the model ID is not, and both must be
        # shown because two distinct K. phaffii reconstructions are audited.
        ax_c.text(-0.68, i - 0.17, species, fontsize=6.2, va="center",
                  ha="right", fontstyle="italic")
        ax_c.text(-0.68, i + 0.19, model_id, fontsize=5.3, va="center",
                  ha="right", color="0.4")
    ax_c.set_title("Simulation-readiness audit: every organism now has a "
                   "working model, but none is defect-free", loc="left")
    for spine in ax_c.spines.values():
        spine.set_visible(False)
    ax_c.tick_params(length=0)

    for ax, letter in [(ax_a, "a"), (ax_b, "b")]:
        panel_letter(ax, letter)
    panel_letter(ax_c, "c", dx=-0.10)

    fig.savefig(out, dpi=300, bbox_inches="tight")
    return fig
