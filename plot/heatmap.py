from abstract_plot import AbstractPlot
import seaborn as sns


class HeatMap(AbstractPlot):

    def create_heatmap(self, data, annot=False, fmt=".1f", cmap=None, vmin=None, vmax=None, linewidth=.0, linecolor="white"):
        sns.heatmap(data=data, annot=annot, fmt=fmt,
                    cmap=cmap, vmin=vmin, vmax=vmax, linewidth=linewidth, linecolor=linecolor)
