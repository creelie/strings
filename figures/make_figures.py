"""Figures of the paper on the Dwork quintic.

Writes fig_labels.png, fig_masses.png, fig_hodge.png and fig_landscape.png
into ../paper/figures as flattened 256-colour PNG files about 1600 pixels wide.
Run from any directory: python3 figures/make_figures.py
"""
import itertools
import math
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "paper", "figures")
WIDTH_PX = 1600

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif"],
    "mathtext.fontset": "dejavuserif",
    "font.size": 11,
    "axes.titlesize": 12,
})

TYPE_COLOURS = {
    (1, 1, 1, 1, 1): "#222222",
    (2, 1, 1, 1, 0): "#1f77b4",
    (2, 2, 1, 0, 0): "#2ca02c",
    (3, 1, 1, 0, 0): "#ff7f0e",
    (3, 2, 0, 0, 0): "#d62728",
}
TYPE_NAMES = {
    (1, 1, 1, 1, 1): r"$\{1,1,1,1,1\}$ (1)",
    (2, 1, 1, 1, 0): r"$\{2,1,1,1,0\}$ (20)",
    (2, 2, 1, 0, 0): r"$\{2,2,1,0,0\}$ (30)",
    (3, 1, 1, 0, 0): r"$\{3,1,1,0,0\}$ (30)",
    (3, 2, 0, 0, 0): r"$\{3,2,0,0,0\}$ (20)",
}


def save(fig, name):
    """Save at about WIDTH_PX pixels wide, flattened to a 256-colour palette."""
    w_in = fig.get_size_inches()[0]
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=WIDTH_PX / w_in, facecolor="white")
    plt.close(fig)
    img = Image.open(path).convert("RGB")
    img = img.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    img.save(path, optimize=True)
    print(name, Image.open(path).size, os.path.getsize(path), "bytes")


def labels():
    return [b for b in itertools.product(range(4), repeat=5) if sum(b) == 5]


def ltype(b):
    return tuple(sorted(b, reverse=True))


def sigma(b):
    t = ltype(b)
    if max(b) <= 2:
        return tuple(2 - x for x in b), 0
    if t == (3, 1, 1, 0, 0):
        return tuple(3 if x == 3 else 1 - x for x in b), 1
    return tuple(2 if x == 3 else 3 if x == 2 else 0 for x in b), 2


def character(b):
    """Class of b in (Z/5)^5 / <1>, normalised so that the last entry is 0."""
    return tuple((b[i] - b[4]) % 5 for i in range(3))


def fig_labels():
    B = labels()
    assert len(B) == 101
    chars = {character(b): b for b in B}
    assert len(chars) == 101
    perms = {character(p) for p in itertools.permutations(range(5))}
    assert len(perms) == 24 and not perms & set(chars)

    fig = plt.figure(figsize=(11.0, 5.2))
    ax = fig.add_subplot(1, 2, 1, projection="3d")
    for c, b in chars.items():
        ax.scatter(*c, s=34, color=TYPE_COLOURS[ltype(b)], depthshade=False,
                   edgecolors="k", linewidths=0.3)
    for c in perms:
        ax.scatter(*c, s=34, facecolors="white", edgecolors="#555555",
                   linewidths=0.9, depthshade=False)
    for i in range(5):
        for j in range(5):
            for a, bb in ((0, 1), (0, 2), (1, 2)):
                pass
    for x in (0, 4):
        for y in (0, 4):
            ax.plot([x, x], [y, y], [0, 4], color="#bbbbbb", lw=0.6)
            ax.plot([x, x], [0, 4], [y, y], color="#bbbbbb", lw=0.6)
            ax.plot([0, 4], [x, x], [y, y], color="#bbbbbb", lw=0.6)
    ax.set_xticks(range(5)); ax.set_yticks(range(5)); ax.set_zticks(range(5))
    ax.set_xlabel(r"$b_0-b_4$", labelpad=1)
    ax.set_ylabel(r"$b_1-b_4$", labelpad=1)
    ax.set_zlabel(r"$b_2-b_4$", labelpad=1)
    ax.view_init(elev=22, azim=-58)
    ax.set_title(r"characters of $\Gamma\cong(\mathbb{Z}/5)^3$", pad=0)
    handles = [plt.Line2D([], [], marker="o", ls="", color=col, markeredgecolor="k",
                          markeredgewidth=0.3, label=TYPE_NAMES[t])
               for t, col in TYPE_COLOURS.items()]
    handles.append(plt.Line2D([], [], marker="o", ls="", markerfacecolor="white",
                              markeredgecolor="#555555", label="permutations (24)"))
    ax.legend(handles=handles, loc="upper left", fontsize=8, frameon=False,
              bbox_to_anchor=(-0.08, 1.0))

    ax2 = fig.add_subplot(1, 2, 2)
    order = sorted(B, key=lambda b: (list(TYPE_COLOURS).index(ltype(b)), b))
    ring = [b for b in order if b != (1, 1, 1, 1, 1)]
    pos = {}
    for k, b in enumerate(ring):
        th = 2 * math.pi * k / len(ring)
        pos[b] = (math.cos(th), math.sin(th))
    pos[(1, 1, 1, 1, 1)] = (0.0, 0.0)
    chord = {0: "#222222", 1: "#1f4fbf", 2: "#c62828"}
    done = set()
    for b in ring:
        c, r = sigma(b)
        assert sigma(c)[0] == b and c != b and ltype(c) == ltype(b)
        if (c, b) in done:
            continue
        done.add((b, c))
        (x0, y0), (x1, y1) = pos[b], pos[c]
        t = np.linspace(0, 1, 60)
        mx, my = 0.25 * (x0 + x1), 0.25 * (y0 + y1)
        xs = (1 - t) ** 2 * x0 + 2 * t * (1 - t) * mx + t ** 2 * x1
        ys = (1 - t) ** 2 * y0 + 2 * t * (1 - t) * my + t ** 2 * y1
        ax2.plot(xs, ys, color=chord[r], lw=0.9, alpha=0.85)
    for b, (x, y) in pos.items():
        ax2.scatter(x, y, s=22, color=TYPE_COLOURS[ltype(b)], edgecolors="k",
                    linewidths=0.3, zorder=3)
    ax2.annotate(r"$h$", (0, 0), xytext=(0.07, 0.07), fontsize=12)
    for r, lab in ((0, r"$1$"), (1, r"$\psi$"), (2, r"$\psi^2$")):
        ax2.plot([], [], color=chord[r], lw=1.5, label="coupling " + lab)
    ax2.legend(loc="lower right", fontsize=9, frameon=False, bbox_to_anchor=(1.12, -0.04))
    ax2.set_aspect("equal"); ax2.axis("off")
    ax2.set_title(r"the involution $\sigma$", pad=4)
    fig.subplots_adjust(left=0.0, right=0.97, top=0.93, bottom=0.03, wspace=0.05)
    save(fig, "fig_labels.png")


def fig_masses():
    fig = plt.figure(figsize=(11.0, 4.8))
    ax = fig.add_subplot(1, 2, 1)
    t = np.linspace(0, 0.999, 400)
    ax.plot(t, np.ones_like(t), color="#222222", lw=2, label="51 labels: $1$")
    ax.plot(t, t, color="#1f4fbf", lw=2, label=r"30 labels: $|\psi|$")
    ax.plot(t, t ** 2, color="#c62828", lw=2, label=r"20 labels: $|\psi|^2$")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1.08)
    ax.set_xlabel(r"$|\psi|$"); ax.set_ylabel("mass scale")
    ax.legend(loc="upper left", bbox_to_anchor=(0.02, 0.92), frameon=False)
    ax.set_title("three scales of the mass map")
    ax.grid(alpha=0.25)

    ax2 = fig.add_subplot(1, 2, 2, projection="3d")
    n = 161
    x = np.linspace(-1.35, 1.35, n)
    X, Y = np.meshgrid(x, x)
    R = np.hypot(X, Y)
    Z = 101 - 50 * np.exp(-(R / 0.06) ** 2)
    ax2.plot_wireframe(X, Y, Z, rstride=8, cstride=8, color="#7f97bd", linewidth=0.5)
    ax2.plot([0, 0], [0, 0], [51, 101], color="#c62828", lw=1.5)
    ax2.scatter([0], [0], [51], color="#c62828", s=30, depthshade=False)
    th = np.linspace(0, 2 * np.pi, 200)
    ax2.plot(np.cos(th), np.sin(th), 101.3 * np.ones_like(th), color="#ff7f0e", lw=0.8)
    for k in range(5):
        a = 2 * np.pi * k / 5
        ax2.scatter(np.cos(a), np.sin(a), 101.6, color="#ff7f0e", s=40, edgecolors="k",
                    linewidths=0.4, depthshade=False)
    ax2.text(0.08, 0.0, 49, r"$\psi=0$: rank $51$", fontsize=10, color="#c62828")
    ax2.text(1.3, -0.45, 103, r"$\psi^5=1$", fontsize=10, color="#b35900")
    ax2.text2D(0.08, 0.80, r"rank $101$", transform=ax2.transAxes, fontsize=10)
    ax2.set_xlabel(r"$\mathrm{Re}\,\psi$"); ax2.set_ylabel(r"$\mathrm{Im}\,\psi$")
    ax2.set_zlabel("rank", labelpad=2)
    ax2.set_zlim(40, 106)
    ax2.view_init(elev=24, azim=-52)
    ax2.set_title("rank of the mass map on the pencil", pad=0)
    fig.subplots_adjust(left=0.06, right=0.98, top=0.92, bottom=0.11, wspace=0.12)
    save(fig, "fig_masses.png")


def fig_hodge():
    fig = plt.figure(figsize=(11.0, 4.8))
    ax = fig.add_subplot(1, 2, 1, projection="3d")
    # Real slice of the Fermat quintic: z1^5 + z2^5 = 1 in C^2, after Hanson.
    n = 5
    a = np.linspace(-1.0, 1.0, 26)
    b = np.linspace(0, np.pi / 2, 26)
    A, Bt = np.meshgrid(a, b)
    alpha = 0.55
    for k1 in range(n):
        for k2 in range(n):
            u = A + 1j * Bt
            z1 = np.exp(2j * np.pi * k1 / n) * (np.cosh(u) ** (2.0 / n) + 0j)
            z2 = np.exp(2j * np.pi * k2 / n) * ((-1j * np.sinh(u)) ** (2.0 / n) + 0j)
            Xs = z1.real
            Ys = z2.real
            Zs = np.cos(alpha) * z1.imag + np.sin(alpha) * z2.imag
            col = plt.cm.Blues(0.35 + 0.55 * ((k1 + 2 * k2) % n) / (n - 1))
            ax.plot_surface(Xs, Ys, Zs, color=col, linewidth=0, antialiased=True,
                            shade=True, alpha=0.95)
    ax.set_axis_off()
    ax.view_init(elev=18, azim=35)
    ax.set_box_aspect((1, 1, 0.8))
    ax.set_title(r"the curve $z_1^5+z_2^5=1$ on the Fermat quintic", pad=0)

    ax2 = fig.add_subplot(1, 2, 2, projection="3d")
    h = {(0, 0): 1, (3, 0): 1, (0, 3): 1, (3, 3): 1, (1, 1): 1, (2, 2): 1,
         (2, 1): 101, (1, 2): 101}
    for p in range(4):
        for q in range(4):
            v = h.get((p, q), 0)
            if v == 0:
                ax2.bar3d(p - 0.3, q - 0.3, 0, 0.6, 0.6, 0.6, color="#eeeeee",
                          edgecolor="#bbbbbb", linewidth=0.3, shade=False)
                continue
            col = "#c62828" if v == 101 else "#1f4fbf"
            ax2.bar3d(p - 0.3, q - 0.3, 0, 0.6, 0.6, 1 + 0.6 * math.log2(v), color=col,
                      edgecolor="k", linewidth=0.3, shade=True, alpha=0.95)
            if v > 1:
                ax2.text(p, q, 1.9 + 0.6 * math.log2(v), str(v), ha="center", fontsize=12,
                         zorder=10)
    ax2.set_xticks(range(4)); ax2.set_yticks(range(4))
    ax2.set_xlabel(r"$p$"); ax2.set_ylabel(r"$q$")
    ax2.set_zticks([])
    ax2.view_init(elev=30, azim=-118)
    ax2.set_title(r"Hodge numbers $h^{p,q}$ (height $\sim\log$)", pad=0)
    fig.subplots_adjust(left=0.0, right=0.98, top=0.93, bottom=0.03, wspace=0.02)
    save(fig, "fig_hodge.png")


def smoothstep(x):
    x = np.clip(x, 0, 1)
    return x * x * x * (10 - 15 * x + 6 * x * x)


def fig_landscape():
    fig = plt.figure(figsize=(11.0, 5.2))
    ax = fig.add_subplot(1, 1, 1, projection="3d")
    n = 201
    x = np.linspace(-3.2, 3.2, n)
    y = np.linspace(-2.4, 2.4, n)
    X, Y = np.meshgrid(x, y)
    # rho is even in X, so S is invariant under the reflection mu: X -> -X.
    rho = 0.12 * (X ** 2 + Y ** 2) + 0.5 + 0.35 * np.cos(1.4 * X) * np.cos(1.9 * Y + 0.6)
    r = 1.6
    f = X ** 2 + Y ** 2
    chi = 1 - smoothstep((f - r ** 2 / 4) / (r ** 2 / 4))
    c = r ** 2 / 4
    S = chi * f + (1 - chi) * (c + rho)
    floor = -0.9
    ax.plot_surface(X, Y, S, cmap="cividis", rstride=3, cstride=3, linewidth=0.1,
                    edgecolor="#555555", antialiased=True, alpha=0.9)
    ax.contour(X, Y, S, levels=14, zdir="z", offset=floor, cmap="cividis", linewidths=0.6)
    ax.scatter([0], [0], [0], color="#c62828", s=46, depthshade=False, zorder=10)
    ax.plot([0, 0], [-2.4, 2.4], [floor, floor], color="#1f4fbf", lw=1.6, ls="--")
    th = np.linspace(0, 2 * np.pi, 200)
    for rad in (r / 2, r / math.sqrt(2)):
        ax.plot(rad * np.cos(th), rad * np.sin(th), floor * np.ones_like(th),
                color="#c62828", lw=1.0)
    ax.text2D(0.53, 0.40, r"$\mathcal{V}^\star$", transform=ax.transAxes, fontsize=15,
              color="#c62828", zorder=100)
    ax.text2D(0.33, 0.12, r"fixed set of $\mu$", transform=ax.transAxes, fontsize=10,
              color="#1f4fbf")
    ax.text2D(0.55, 0.30, r"radii $r/2$ and $r/\sqrt{2}$ of the cut-off", transform=ax.transAxes,
              fontsize=10, color="#c62828", zorder=100)
    ax.text2D(0.70, 0.78, r"$c+\rho$ away from $\mathcal{V}^\star$", transform=ax.transAxes,
              fontsize=10)
    ax.set_zlabel(r"$\mathcal{S}$", labelpad=-6)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
    ax.set_zlim(floor, 3.2)
    ax.view_init(elev=24, azim=-62)
    ax.set_box_aspect((1.6, 1.2, 0.85))
    fig.subplots_adjust(left=-0.05, right=1.05, top=1.06, bottom=-0.06)
    save(fig, "fig_landscape.png")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    which = sys.argv[1:] or ["labels", "masses", "hodge", "landscape"]
    for w in which:
        globals()["fig_" + w]()
