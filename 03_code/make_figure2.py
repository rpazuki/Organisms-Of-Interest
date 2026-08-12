"""Round-1 deliverable figure 2: model selection metric and burden modelling."""

import matplotlib.pyplot as plt
import numpy as np

SHORT = {
    "S_cerevisiae": "S. cerevisiae", "Y_lipolytica": "Y. lipolytica",
    "K_phaffii": "K. phaffii", "A_niger": "A. niger", "A_oryzae": "A. oryzae",
    "R_microsporus": "R. microsporus", "F_venenatum": "F. venenatum (proxy)",
    "T_reesei": "T. reesei",
}


def build(scores, final, envelopes, style_fns, out="fig_selection_burden.png"):
    apply_figure_style, focal_palette, panel_letter = style_fns
    apply_figure_style()

    fig = plt.figure(figsize=(7.2, 7.4))
    gs = fig.add_gridspec(3, 2, height_ratios=[1.15, 1.0, 1.0],
                          hspace=0.75, wspace=0.35)

    # -- (a) candidate score distribution per organism, chosen model marked ----
    ax = fig.add_subplot(gs[0, :])
    orgs = list(final.organism)
    chosen_names = dict(zip(final.organism, final.census_model_id))
    census_org = {
        "S_cerevisiae": "Saccharomyces cerevisiae",
        "Y_lipolytica": "Yarrowia lipolytica",
        "K_phaffii": "Komagataella phaffii",
        "A_niger": "Aspergillus niger",
        "A_oryzae": "Aspergillus oryzae",
        "R_microsporus": "Rhizopus microsporus",
        "F_venenatum": "Fusarium graminearum (proxy)",
        "T_reesei": "Trichoderma reesei",
    }
    for i, org in enumerate(orgs):
        sub = scores[scores.organism == census_org[org]]
        if not len(sub):
            continue
        ax.scatter(sub.score, [i] * len(sub), s=18, facecolors="none",
                   edgecolors="0.55", linewidths=0.8, zorder=2)
        pick = sub[sub.model_id == chosen_names[org]]
        if len(pick):
            ax.scatter(pick.score, [i], s=52, color="#1f4e79", zorder=3,
                       marker="D", edgecolors="white", linewidths=0.7)
    ax.set_yticks(range(len(orgs)))
    ax.set_yticklabels([SHORT[o] for o in orgs], fontsize=6.6, style="italic")
    ax.invert_yaxis()
    ax.set_xlabel("composite selection score (0-1)")
    ax.set_title("Selection metric ranks every candidate reconstruction;\n"
                 "the adopted model (filled) is not always the top-scoring one",
                 loc="left")
    ax.scatter([], [], s=18, facecolors="none", edgecolors="0.55",
               label="candidate")
    ax.scatter([], [], s=52, color="#1f4e79", marker="D", label="adopted")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.28), frameon=False,
              fontsize=6, ncol=2)
    ax.set_ylim(len(orgs) - 0.4, -0.6)
    panel_letter(ax, "a")

    # -- (b) two empirical gates the structural score cannot replace ----------
    ax = fig.add_subplot(gs[1, 0])
    y = np.arange(len(final))
    pct = final.pctC_biomass.astype(float).to_numpy()
    ok = final.per_gDW.fillna(False).to_numpy().astype(bool)
    ax.axvspan(42, 53, color="#476a47", alpha=0.13, zorder=0)
    ax.barh(y, np.nan_to_num(pct), color=np.where(ok, "#1f4e79", "#855050"),
            height=0.6, zorder=2)
    for i, v in enumerate(pct):
        if v != v:
            ax.text(2, i, "no formulas", fontsize=5.4, va="center", color="0.45")
    ax.set_yticks(y)
    ax.set_yticklabels([SHORT[o] for o in final.organism], fontsize=6,
                       style="italic")
    ax.invert_yaxis()
    ax.set_xlabel("carbon in biomass (% of dry weight)")
    ax.set_title("Gate 1: biomass\nnormalisation", loc="left")
    ax.text(47.5, -0.75, "valid 42-53%", fontsize=5.6,
            color="0.3", ha="center", va="center")
    ax.set_ylim(len(final) - 0.4, -1.1)
    panel_letter(ax, "b")

    ax = fig.add_subplot(gs[1, 1])
    atp = final.max_ATP_per_glc.astype(float).to_numpy()
    egc = final.EGC_suspected.fillna(False).to_numpy().astype(bool)
    ax.barh(y, atp, color=np.where(egc, "#855050", "#1f4e79"), height=0.6,
            zorder=2)
    ax.axvline(32, color="0.25", lw=0.9, ls="--", zorder=3)
    ax.text(33.5, -0.75, "thermodynamic max ~32", fontsize=5.6, color="0.3",
            va="center")
    ax.set_yticks(y)
    ax.set_yticklabels([])
    ax.set_ylim(len(final) - 0.4, -1.1)
    ax.set_xlabel("max ATP per glucose")
    ax.set_title("Gate 2: energy-\ngenerating cycles", loc="left")
    panel_letter(ax, "c")

    # -- (d) burden envelopes -------------------------------------------------
    ax = fig.add_subplot(gs[2, :])
    # K. phaffii is the reference secretion host for this product, so it is the
    # focal series; the rest are context.
    keys = list(envelopes)
    cols = focal_palette(keys, "K_phaffii", "#1f4e79")
    cols = [cols[k] for k in keys] if isinstance(cols, dict) else cols
    for (org, env), c in zip(envelopes.items(), cols):
        feas = env[env.feasible]
        ax.plot(feas.product_flux * 1000, feas.growth / env.growth.iloc[0],
                marker="o", ms=2.6, lw=1.1, color=c, label=SHORT[org])
    ax.set_xlabel("lysozyme synthesis flux (umol gDW$^{-1}$ h$^{-1}$)")
    ax.set_ylabel("growth, fraction of\nproduct-free rate")
    ax.set_title("Burden: every host pays growth rate for product, and the "
                 "slope discriminates hosts", loc="left")
    ax.legend(frameon=False, fontsize=5.6, ncol=4, loc="lower left")
    ax.set_ylim(0, 1.05)
    panel_letter(ax, "d")

    fig.savefig(out, dpi=300, bbox_inches="tight")
    return fig
