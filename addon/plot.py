import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from .voxelizer import Voxelizer
from matplotlib.ticker import LinearLocator
matplotlib.use('Agg')

# Define type aliases for convenience
Labels = list[str]
Ticks = list[int]


# Base class for creating different types of plots
class AbstractPlot:

    def __init__(self):
        # Clear current figure
        plt.clf()

    # Function to set the legend on the plot
    def set_legend(self, **kwargs) -> None:
        # Various ways to call legend, based on what's passed in kwargs
        if ('labels' in kwargs and 'handles' in kwargs):
            plt.legend(labels=kwargs['labels'], handles=kwargs['handles'])
        elif ('labels' in kwargs and not 'handles' in kwargs):
            plt.legend(labels=kwargs['labels'])
        elif (not 'labels' in kwargs and 'handles' in kwargs):
            plt.legend(handles=kwargs['handles'])

    # Remaining methods are self-explanatory setters for title, labels, ticks,
    # etc.
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


# Subclass for creating pie charts
class PieChart(AbstractPlot):

    # Function to create a pie chart
    def create_pie(self, wedges: Wedges, labels: Labels,
                   autopct: str, colors=None):
        plt.pie(x=wedges, labels=labels, colors=colors, autopct=autopct)

######## bar_chart ##########


# Subclass for creating heatmaps
class HeatMap(AbstractPlot):

    # Function to create a heatmap
    def create_heatmap(self, data, annot=False, fmt=".1f", cmap=None,
                       vmin=None, vmax=None, linewidth=.0, linecolor="white"):
        sns.heatmap(data=data, annot=annot, fmt=fmt,
                    cmap=cmap, vmin=vmin, vmax=vmax, linewidth=linewidth, linecolor=linecolor)


# Subclass for creating scatter plots
class ScatterPlot(AbstractPlot):

    # Function to create a scatter plot
    def create_scatter(self, x, y, z, s=30, c=None, marker='o', cmap=None, norm=None, vmin=None, vmax=None,
                       alpha=None, linewidths=None, verts=None, edgecolors=None, *, plotnonfinite=False, data=None, **kwargs):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.scatter3D(x, y, z, color="green")
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')

# Subclass for creating voxel plots (currently not implemented)


class VoxelPlot(AbstractPlot):

    """
    NOT IMPLEMENTED
    """

    def create_voxel(self, voxelarray, colors=None, facecolors=None, edgecolors=None,
                     shade=True, norm=None, vmin=None, vmax=None, linewidth=0.0, edgecolor=None, **kwargs):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')

        ax.voxels(np.array(voxelarray), facecolors=facecolors, edgecolors=edgecolors,
                  shade=shade, norm=norm, vmin=vmin, vmax=vmax, linewidth=linewidth, edgecolor=edgecolor, **kwargs)
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


# Subclass for creating surface charts
class BubblePlot(AbstractPlot):

    # Function to create a surface chart
    def create_bubble(self, x, y):
        plt.figure()
        plt.scatter(x, y, color='darkblue')
        plt.xlabel('X label')
        plt.ylabel('Y label')
