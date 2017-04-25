from matplotlib import pyplot as plt
import matplotlib.patches as patches


def plot_sims(years, simulations, ylims):
    fig, ax = plt.subplots(figsize=(14, 10))
    fig.patch.set_facecolor('white')
    plt.subplots_adjust(wspace=0)

    ax1 = plt.subplot2grid((1, 3), (0, 0), colspan=2)

    for sim in simulations:
        ax1.plot(years, sim, linewidth=2, alpha=0.02, color='k')

    ax1.set_xlim([0,years[-1]])
    ax1.set_ylim(ylims)

    ax2 = plt.subplot2grid((1, 3), (0, 2))
    ax2.xaxis.tick_top()
    ax2.tick_params(axis='y', which='both', labelleft='off', labelright='on')
    ax2.set_ylim(ax1.get_ylim())

    ax2.hist([sim[-1] for sim in simulations], normed=1, orientation='horizontal', color='k', alpha=0.6)

    ax2.yaxis.set_label_position('right')
    ax2.xaxis.set_label_position('top')

    ax1.set_xlabel('year')
    ax1.set_ylabel('empty seats [count]')
    ax2.set_xlabel('probability')
    ax2.set_ylabel(ax1.get_ylabel())

    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
    plt.show()


def stacked_plot_bench_over_time(years, bench_stacks, mean, color_trans, party_enum):
    fig, ax = plt.subplots(1, facecolor='white', figsize=(14,6))
    plt.tight_layout(pad=0, w_pad=0.5, h_pad=0)

    labels = [""] + [e.name for e in party_enum]
    colors = ["white"] + [color_trans[e] for e in party_enum]


    k = ax.stackplot(years, bench_stacks, colors=colors, labels=labels)

    ax.plot(years, mean, 'white', linewidth=6)
    ax.plot(years, mean, 'k', linewidth=3, label = "average empty seats")

    ax.set_xlim([years[0],years[-1]])
    ax.set_ylim([0,9])
    ax.set_xlabel("year")
    ax.set_ylabel("seats [count]")
    ax.set_title("court breakdown over time")

    bbox_props = dict(boxstyle="square,pad=0.3", fc="white", ec="k", lw=1)

    ax.annotate('{0:0.5f} average empty seats'.format(mean[-1]),
                xy=(years[-1], mean[-1]),
                size=15,
                xytext=(years[3*len(years)//5], 3),
                arrowprops=dict(facecolor='white', shrink=0.05),
                bbox=bbox_props)

    ax.legend()
    plt.show()

def stacked_plot_bench_over_time_with_parties(years,
                                              bench_stacks,
                                              pres_parties,
                                              sen_parties,
                                              color_trans,
                                              party_enum):

    fig, ax = plt.subplots(figsize=(14, 10))
    fig.patch.set_facecolor('white')
    plt.subplots_adjust(hspace=0)

    ax1 = plt.subplot2grid((10, 1), (0, 0), rowspan=9)

    labels = [""] + [e.name for e in party_enum]
    colors = ["white"] + [color_trans[e] for e in party_enum]

    k = ax1.stackplot(years, bench_stacks, colors=colors, labels=labels)

    ax1.tick_params(axis='x', which='both', labelbottom='off', labeltop='off')
    ax1.set_xlim([years[0],years[-1]])
    ax1.set_ylim([0,9])

    ax1.set_ylabel("seats [count]")
    ax1.set_title("court breakdown over time")

    ax1.legend()

    ax2 = plt.subplot2grid((10, 1), (9, 0))

    ax2.set_ylim([0,2])

    ax2.set_xlim(ax1.get_xlim())
    ax2.tick_params(axis='y', which='both', left='off', right='off')
    ax2.yaxis.set_ticks([0.5, 1.5])
    ax2.set_yticklabels(['President', 'Senate'])
    ax2.set_xlabel("year")

    for i, p in enumerate(pres_parties):
        ax2.add_patch(
            patches.Rectangle(
                (i, 0),   # (x,y)
                1,          # width
                1,          # height
                color=color_trans[p]
            )
        )

    for i, p in enumerate(sen_parties):
        ax2.add_patch(
            patches.Rectangle(
                (i, 1),   # (x,y)
                1,          # width
                1,          # height
                color=color_trans[p]
            )
        )


    plt.show()
