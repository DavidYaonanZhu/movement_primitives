import numpy as np
import matplotlib.pyplot as plt


def plot_trajectory_in_rows(trajectory, t=None, label=None, axes=None, subplot_shape=None, transpose=False, **kwargs):
    """TODO doc

    Note that you have to manually activate the legend for one plot if you
    need it.

    Parameters
    ----------
    transpose : optional (default: False)
        Fill first column first, then second column and so on. Typically
        matplotlib fills rows before columns.
    """
    n_steps, n_dims = trajectory.shape

    if subplot_shape is None:
        subplot_shape = (n_dims, 1)

    newaxes = axes is None
    if newaxes:
        axes = create_axes(n_dims, subplot_shape, transpose)

    if t is not None:
        xlabel = "Time [s]"
    else:
        t = range(n_steps)
        xlabel = "Step"

    for i in range(n_dims):
        axes[i].plot(t, trajectory[:, i], label=label, **kwargs)

    if newaxes:
        layout_axes(axes, n_dims, subplot_shape, xlabel, (t[0], t[-1]), transpose)

    return axes


def plot_distribution_in_rows(mean, std_dev, t=None, label=None, axes=None, std_factors=[1, 2, 3], fill_between=True, subplot_shape=None, transpose=False, **kwargs):
    """TODO doc

    Note that you have to manually activate the legend for one plot if you
    need it.
    """
    n_steps, n_dims = mean.shape

    if subplot_shape is None:
        subplot_shape = (n_dims, 1)

    newaxes = axes is None
    if newaxes:
        axes = create_axes(n_dims, subplot_shape, transpose)

    if t is None:
        t = range(n_steps)
        xlabel = "Step"
    else:
        xlabel = "Time [s]"

    if "color" in kwargs:
        color = kwargs["color"]
    else:
        color = None
    if "alpha" in kwargs:
        alpha = kwargs.pop("alpha")
    else:
        alpha = 0.1

    for i in range(n_dims):
        axes[i].plot(t, mean[:, i], **kwargs)
        for f_idx, f in enumerate(std_factors):
            if fill_between:
                axes[i].fill_between(
                    t, mean[:, i] - f * std_dev[:, i], mean[:, i] + f * std_dev[:, i],
                    color=color, alpha=alpha, label=label if f_idx == 0 else None)
            else:
                axes[i].plot(t, mean[:, i] - f * std_dev[:, i], color, ls="--", label=label if f_idx == 0 else None)
                axes[i].plot(t, mean[:, i] + f * std_dev[:, i], color, ls="--")

    if newaxes:
        layout_axes(axes, n_dims, subplot_shape, xlabel, (t[0], t[-1]), transpose)

    return axes


def create_axes(n_dims, subplot_shape, transpose):
    h, w = subplot_shape
    if transpose:
        dim_order = [(i % h) * w + i // h for i in range(n_dims)]
    else:
        dim_order = range(n_dims)
    return [plt.subplot(h, w, 1 + i) for i in dim_order]


def layout_axes(axes, n_dims, subplot_shape, xlabel, xlim, transpose):
    for i in range(n_dims):
        axes[i].set_title("Dimension #%d" % i, loc="left", y=0)
        if not transpose and subplot_shape[0] * subplot_shape[1] - i in range(1, subplot_shape[1] + 1):
            axes[i].set_xlabel(xlabel)
        elif transpose and i % subplot_shape[0] == subplot_shape[0] - 1:
            axes[i].set_xlabel(xlabel)
        else:
            axes[i].set_xticks(())
        axes[i].set_xlim(xlim)
    plt.tight_layout(h_pad=0)
