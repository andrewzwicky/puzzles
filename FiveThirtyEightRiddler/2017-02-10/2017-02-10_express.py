from matplotlib import animation
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
import matplotlib.cbook as cbook
import matplotlib.patches as patches
import itertools
from scipy.misc import imread
import os
from matplotlib import rcParams
rcParams['font.family'] = 'monospace'

V_SWIM = 100 / 75
V_RUN = 100 / 15
STEP = 1


def time_to_reach(v_swim, v_walk, walking_dist):
    walk_time = walking_dist / v_walk
    swim_time = sqrt(100 ** 2 + (100 - walking_dist) ** 2) / v_swim
    return walk_time, swim_time


def create_axes():
    fig = plt.figure(figsize=(6, 12), facecolor="#FFFFFF")
    beach_axis = plt.subplot2grid((2, 12), (1, 0), colspan=12, zorder=1)
    plot_axis = plt.subplot2grid((2, 12), (0, 1), colspan=10, zorder=2)

    fig.suptitle("Total Time to Reach Swimmer vs. Walking Distance")
    plot_axis.xaxis.tick_top()
    plot_axis.xaxis.set_label_position('top')
    beach_axis.set_xticklabels([])
    beach_axis.set_yticklabels([])
    [sp.set_visible(False) for sp in beach_axis.spines.values()]
    beach_axis.tick_params(axis='both', which='both', bottom='off', top='off', left='off', right='off')

    fig.subplots_adjust(hspace=0)

    dot_kwargs = {'marker':'o', 'markerfacecolor':'k', 'fillstyle':'full', 'linestyle':'-', 'markersize':7, 'color':'k'}
    v_line_props = {'color': 'k', 'linestyle':'--'}
    plot_line_props = {'color':'k'}

    dists = np.arange(0, 100+STEP, STEP)
    split_times = [time_to_reach(V_SWIM, V_RUN, dist) for dist in dists]
    times = list(map(sum, split_times))
    plot_axis.plot(dists, times, **plot_line_props)
    dot, = plot_axis.plot(dists[0],times[0],**dot_kwargs)
    plot_axis.set_xlim([0, 100])

    plot_bbox = plot_axis.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    beach_bbox = beach_axis.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    width_ratio = beach_bbox.width/plot_bbox.width
    axis_adjustment = ((width_ratio*100)-100)/2

    beach_axis.set_xlim([0-axis_adjustment, 100 + axis_adjustment])
    beach_axis.set_ylim([-10, 110])

    prev_plot_y_lims = plot_axis.get_ylim()

    beach_vline, = beach_axis.plot([dists[0], dists[0]], [0, 200], **v_line_props)
    plot_vline, = plot_axis.plot([dists[0], dists[0]], [0, times[0]], **v_line_props)
    plot_axis.set_ylim(prev_plot_y_lims)

    plot_axis.set_xlabel("Walking Distance [m]")
    plot_axis.set_ylabel("Total Time [s]")

    div = 12
    r1 = patches.Rectangle((0 - axis_adjustment, -10), 100 + 2*axis_adjustment, div, facecolor='#C2B280', edgecolor='#C2B280')
    r2 = patches.Rectangle((0 - axis_adjustment, -10+div), 100 + 2 * axis_adjustment, 105-(-10+div), facecolor='#87CEEB', edgecolor='#87CEEB')
    beach_axis.add_patch(r1)
    beach_axis.add_patch(r2)

    line, = beach_axis.plot([0, 0, 100], [0, 0, 100],**dot_kwargs)

    walk_time_text = beach_axis.text(0, 70, "")
    swim_time_text = beach_axis.text(0, 65, "")
    total_time_text = beach_axis.text(0, 60, "")

    return fig, dists, split_times, line, dot, beach_vline, plot_vline, walk_time_text, swim_time_text, total_time_text


def update_axes(frame_num, dists, split_times, line, dot, beach_vline, plot_vline, walk_time_text, swim_time_text, total_time_text):
    dist = next(dists)
    walk_time, swim_time = next(split_times)
    line.set_xdata([0, dist, 100])
    line.set_ydata([0, 0, 100])

    dot.set_xdata([dist])
    dot.set_ydata([walk_time + swim_time])

    beach_vline.set_xdata([dist, dist])

    plot_vline.set_xdata([dist, dist])
    plot_vline.set_ydata([0, walk_time + swim_time])

    walk_time_text.set_text(" walk time: {: >6.2f}s".format(walk_time))
    swim_time_text.set_text(" swim time: {: >6.2f}s".format(swim_time))
    total_time_text.set_text("total time: {: >6.2f}s".format(walk_time + swim_time))

    plt.draw()


def create_animation(output_file):
    fig, dists, times, line, dot, beach_vline, plot_vline, walk_time_text, swim_time_text, total_time_text = create_axes()
    dists_gen = itertools.cycle(dists)
    times_gen = itertools.cycle(times)
    line_ani = animation.FuncAnimation(fig,
                                       update_axes,
                                       frames=len(dists),
                                       fargs=(dists_gen,
                                              times_gen,
                                              line,
                                              dot,
                                              beach_vline,
                                              plot_vline,
                                              walk_time_text,
                                              swim_time_text,
                                              total_time_text),
                                       repeat=True,
                                       save_count=len(dists))

    line_ani.save(output_file, writer="imagemagick", fps=10)


if __name__ == "__main__":
    create_animation('test.gif')
