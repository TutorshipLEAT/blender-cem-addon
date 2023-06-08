import seaborn as sns
import matplotlib.pyplot as plt
import os
import matplotlib
from matplotlib.ticker import LinearLocator
matplotlib.use('Agg')

Labels = list[str]
Ticks = list[int]


class AbstractPlot:

    def __init__(self):
        plt.clf()

    def set_legend(self, **kwargs) -> None:
        if ('labels' in kwargs and 'handles' in kwargs):
            plt.legend(labels=kwargs['labels'], handles=kwargs['handles'])
        elif ('labels' in kwargs and not 'handles' in kwargs):
            plt.legend(labels=kwargs['labels'])
        elif (not 'labels' in kwargs and 'handles' in kwargs):
            plt.legend(handles=kwargs['handles'])

    def set_title(self, title: str) -> None:
        plt.title(title)

    def set_xlabel(self, label: str) -> None:
        plt.xlabel(label)

    def set_ylabel(self, label: str) -> None:
        plt.ylabel(label)

    def set_xticks(self, ticks: Ticks):
        plt.xticks(ticks)

    def set_yticks(self, ticks: Ticks):
        plt.yticks(ticks)

    def show(self):
        plt.show()

    def save_to_png(self, *args, **kwargs) -> None:
        plt.savefig(*args, **kwargs)

######## pie_chart ##########


Wedges = list[int]
Labels = list[str]


class PieChart(AbstractPlot):

    def create_pie(self, wedges: Wedges, labels: Labels, autopct: str, colors=None):
        plt.pie(x=wedges, labels=labels, colors=colors, autopct=autopct)

######## bar_chart ##########


class BarPlot(AbstractPlot):

    def create_bar(self, bar_position: int, data: list, width: float, bottom=0, align='center', color=None):
        plt.bar(bar_position, data, color=color,
                width=width, bottom=bottom, align=align)


class HeatMap(AbstractPlot):

    def create_heatmap(self, data, annot=False, fmt=".1f", cmap=None, vmin=None, vmax=None, linewidth=.0, linecolor="white"):
        sns.heatmap(data=data, annot=annot, fmt=fmt,
                    cmap=cmap, vmin=vmin, vmax=vmax, linewidth=linewidth, linecolor=linecolor)


class ScatterPlot(AbstractPlot):

        def create_scatter(self, x, y, z, s=30, c=None, marker='o', cmap=None, norm=None, vmin=None, vmax=None, alpha=None, linewidths=None, verts=None, edgecolors=None, *, plotnonfinite=False, data=None, **kwargs):
            fig = plt.figure()
            ax = fig.add_subplot(projection='3d')
            ax.scatter3D(x, y, z, color = "green")
            ax.set_xlabel('X Label')
            ax.set_ylabel('Y Label')
            ax.set_zlabel('Z Label')

class SurfaceChart(AbstractPlot):

    def create_surface(self, x, y, z):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        surf = ax.plot_trisurf(x, y, z, linewidth=0, antialiased=False)
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')
        ax.zaxis.set_major_locator(LinearLocator(10))
        ax.zaxis.set_major_formatter('{x:.02f}')
        fig.colorbar(surf, shrink=0.5, aspect=5)