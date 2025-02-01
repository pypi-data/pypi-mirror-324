from collections.abc import Iterator
from typing import List

import matplotlib as mpl
from cycler import cycler

# Color palette suitable for color vision deficiency
COLORS = {
    "primary": "#0077BB",  # Blue
    "secondary": "#EE7733",  # Orange
    "tertiary": "#009988",  # Teal
    "quaternary": "#CC3311",  # Red
    "quinary": "#33BBEE",  # Cyan
    "gray": "#BBBBBB",  # Gray
}

# https://gist.github.com/thriveth/8560036
COLORBLIND_COLORS = {
    "blue": "#377eb8",
    "orange": "#ff7f00",
    "green": "#4daf4a",
    "pink": "#f781bf",
    "brown": "#a65628",
    "purple": "#984ea3",
    "gray": "#999999",
    "red": "#e41a1c",
    "yellow": "#dede00",
}

# Standard sizes for different figure elements
SIZES = {
    "figure": (6, 4),  # Standard figure size in inches
    "font": {"tiny": 8, "small": 12, "medium": 16, "large": 20, "xlarge": 24},
    "linewidth": 1.5,
    "markersize": 6,
    "tick_length": 4,
}


def cb_colors_list() -> List[str]:
    return list(COLORBLIND_COLORS.values())


def cb_colors_iter() -> Iterator[str]:
    return iter(COLORBLIND_COLORS.values())


def cb_colors() -> dict[str, str]:
    return COLORBLIND_COLORS


def set_style(font_scale=1.0) -> None:
    """
    Set the default style for all subsequent plots.

    Parameters:
    -----------
    font_scale : float
        Scale factor for all font sizes (default: 1.0)
    """
    # set for mpl
    mpl.style.use("seaborn-v0_8-whitegrid")

    # Set font properties
    mpl.rcParams["font.family"] = "sans-serif"
    mpl.rcParams["font.sans-serif"] = ["Arial"]
    mpl.rcParams["font.size"] = SIZES["font"]["medium"] * font_scale

    # Set figure properties
    mpl.rcParams["figure.figsize"] = SIZES["figure"]
    mpl.rcParams["figure.dpi"] = 300

    # Set axes properties
    mpl.rcParams["axes.linewidth"] = SIZES["linewidth"]
    mpl.rcParams["axes.labelsize"] = SIZES["font"]["large"] * font_scale
    mpl.rcParams["axes.titlesize"] = SIZES["font"]["xlarge"] * font_scale

    # Set tick properties
    mpl.rcParams["xtick.major.size"] = SIZES["tick_length"]
    mpl.rcParams["ytick.major.size"] = SIZES["tick_length"]
    mpl.rcParams["xtick.labelsize"] = SIZES["font"]["medium"] * font_scale
    mpl.rcParams["ytick.labelsize"] = SIZES["font"]["medium"] * font_scale

    # Set legend properties
    mpl.rcParams["legend.fontsize"] = SIZES["font"]["small"] * font_scale
    mpl.rcParams["legend.frameon"] = True
    mpl.rcParams["legend.edgecolor"] = "gray"

    # Set grid properties
    mpl.rcParams["grid.linewidth"] = 0.5
    mpl.rcParams["grid.alpha"] = 0.3

    # Set the color cycler
    mpl.rcParams["axes.prop_cycle"] = cycler("color", cb_colors_list())


def apply_style(ax, title=None, xlabel=None, ylabel=None, legend=True) -> None:
    """
    Apply the journal style to a specific axes object.

    Parameters:
    -----------
    ax : matplotlib.axes.Axes
        The axes object to style
    title : str, optional
        Title for the plot
    xlabel : str, optional
        Label for x-axis
    ylabel : str, optional
        Label for y-axis
    legend : bool, optional
        Whether to show the legend (default: True)
    """
    # Set labels if provided
    if title:
        ax.set_title(title)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)

    # Configure legend
    if legend and ax.get_legend():
        ax.legend(frameon=True, edgecolor="gray")

    # Configure grid
    ax.grid(True, alpha=0.3, linewidth=0.5)

    # Set spine visibility and width
    for spine in ax.spines.values():
        spine.set_linewidth(SIZES["linewidth"])
