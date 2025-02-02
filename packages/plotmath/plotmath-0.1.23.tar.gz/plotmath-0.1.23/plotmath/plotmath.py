import pathlib

import numpy as np
import matplotlib.pyplot as plt
import shutil
import platform
import warnings

# Check if LaTeX is available
if platform.system() == "Windows":
    latex_available = shutil.which("latex.exe") is not None
else:
    latex_available = shutil.which("latex") is not None


if latex_available:
    try:
        plt.rc("text", usetex=True)
    except (FileNotFoundError, RuntimeError):
        plt.rc("text", usetex=False)
else:
    plt.rc("text", usetex=False)


colors = ["#029386", "#C875C4", "#E50000", "blue", "purple", "orange"]
# colors = np.random.permutation(colors)
plt.rcParams["axes.prop_cycle"] = plt.cycler(color=colors)


def show():
    plt.show()


def _get_figure_and_axis():
    fig, ax = plt.subplots()
    ax.spines["left"].set_position("zero")
    ax.spines["right"].set_color("none")
    ax.spines["bottom"].set_position("zero")
    ax.spines["top"].set_color("none")

    ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
    ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)

    ax.set_xlabel(r"$x$", fontsize=16, loc="right")
    ax.set_ylabel(r"$y$", fontsize=16, loc="top", rotation="horizontal")

    return fig, ax


def _set_ticks(xmin, xmax, ymin, ymax):

    xticks = list(np.arange(xmin + 1, xmax, 1))
    if len(xticks) > 10:
        if xmin % 2 == 0:
            xmin = xmin + 1
        if xmax % 2 == 0:
            xmax = xmax - 1

        n_step = 1
        while len(xticks) > 11:
            n_step *= 2
            xticks = list(np.arange(xmin + 1, xmax, n_step))

    if 0 in xticks:
        xticks.remove(0)
    plt.xticks(xticks, fontsize=16)

    yticks = list(np.arange(ymin + 1, ymax, 1))
    if len(yticks) > 11:
        if ymin % 2 == 0:
            ymin = ymin + 1
        if ymax % 2 == 0:
            ymax = ymax - 1

        n_step = 1
        while len(yticks) > 10:
            n_step *= 2
            yticks = list(np.arange(ymin + 1, ymax, n_step))

    if 0 in yticks:
        yticks.remove(0)
    plt.yticks(yticks, fontsize=16)

    return None


def plot(
    functions,
    fn_labels=True,
    xmin=-6,
    xmax=6,
    ymin=-6,
    ymax=6,
    ticks=True,
    alpha=0.7,
    grid=True,
    domain=None,
):
    fig, ax = _get_figure_and_axis()

    if ticks:
        _set_ticks(xmin, xmax, ymin, ymax)
    else:
        plt.xticks([])
        plt.yticks([])

    # If domain is provided
    if domain:
        a, b = domain
        try:
            tmp = [f(a) for f in functions]
            tmp = [f(b) for f in functions]
        except:
            raise ValueError(
                f"One of the provided functions is not defined on the provided domain: {domain}"
            )
    else:
        a = -25
        b = 25
        try:
            tmp = [f(a) for f in functions]
            tmp = [f(b) for f in functions]
        except:
            raise ValueError(
                f"One of the provided functions is not defined on the default domain: {[a, b]}. Provide an appropriate domain"
            )

    x = np.linspace(a, b, int(2**12))

    if isinstance(fn_labels, bool) and fn_labels:  # If True, automatically set labels
        fn_labels = [f"${fn.__name__}$" for fn in functions]
    elif isinstance(fn_labels, bool) and not fn_labels:  # If False, disable labels
        fn_labels = None
    # Otherwise the code will apply user-specified labels

    if fn_labels is not None:
        for f, label in zip(functions, fn_labels):
            ax.plot(x, f(x), lw=2, alpha=alpha, label=label)

        ax.legend(fontsize=16)

    else:
        for f in functions:
            ax.plot(x, f(x), lw=2, alpha=alpha)

    plt.ylim(ymin, ymax)
    plt.xlim(xmin, xmax)

    if grid:
        plt.grid(True, linestyle="--", alpha=0.6)

    plt.tight_layout()

    return fig, ax


def savefig(dirname, fname):
    dir = pathlib.Path(dirname)
    dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(f"{dir}/{fname}")

    return None


def plot_polygon(*points, ax, color="teal", alpha=0.1):
    points = [*points]
    points.append(points[0])

    x, y = zip(*points)
    ax.fill(x, y, color=color, alpha=0.1)
    ax.plot(x, y, color="black", alpha=1, lw=1.5)
    ax.plot(x, y, "ko", markersize=8, alpha=0.7)

    return None


def histogram(
    xmin,
    frequencies,
    binsizes,
    xlabel=None,
    ylabel=None,
    rotation=0,
    fontsize=16,
    norwegian=True,
):
    heights = [f / b for f, b in zip(frequencies, binsizes)]
    fig, ax = _get_figure_and_axis()

    x = [xmin]
    for i, binsize in enumerate(binsizes):
        x.append(x[i] + binsize)

    xticks = x[:]
    if 0 in xticks:
        xticks.remove(0)

    ax.set_xticks(xticks)
    ax.set_xticklabels([f"${i}$" for i in xticks], fontsize=fontsize, rotation=0)

    yticks = list(np.arange(1, max(heights) + 1, 1))
    ax.set_yticks(yticks)
    ax.set_yticklabels([f"${int(i)}$" for i in yticks], fontsize=fontsize, rotation=0)

    if ylabel:
        ax.set_ylabel(
            ylabel,
            fontsize=fontsize,
            rotation=0,
            loc="top",
        )
    else:
        if norwegian:
            ax.set_ylabel(
                r"$\displaystyle \frac{\mathrm{Frekvens}}{\mathrm{Klassebredde}}$",
                fontsize=fontsize,
                rotation=0,
                loc="top",
            )
        else:
            ax.set_ylabel(
                r"$\displaystyle \frac{\mathrm{Frequency}}{\mathrm{Binsize}}$",
                fontsize=fontsize,
                rotation=0,
                loc="top",
            )

    if xlabel:
        ax.set_xlabel(xlabel, fontsize=16, loc="right")
    else:
        ax.set_xlabel(r"$x$", fontsize=16, loc="right")

    plt.xlim(-1, x[-1] + 4)
    plt.ylim(-0.5, max(heights) + 1)

    for i in range(len(x) - 1):
        ax.plot(
            [x[i], x[i + 1]], [heights[i], heights[i]], color="teal", lw=2, alpha=0.7
        )
        ax.plot([x[i], x[i]], [0, heights[i]], color="teal", lw=2, alpha=0.7)
        ax.plot([x[i + 1], x[i + 1]], [0, heights[i]], color="teal", lw=2, alpha=0.7)

        ax.fill(
            [x[i], x[i + 1], x[i + 1], x[i]],
            [0, 0, heights[i], heights[i]],
            color="teal",
            alpha=0.3,
        )

    ax.grid(False)

    plt.subplots_adjust(
        left=0.25,
        bottom=0.068,
        top=0.885,
    )

    return fig, ax
