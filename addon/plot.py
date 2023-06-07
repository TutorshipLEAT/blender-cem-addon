import seaborn as sns
import matplotlib.pyplot as plt
import os
import matplotlib
matplotlib.use('Agg')

Labels = list[str]
Ticks = list[int]


class AbstractPlot:

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
        plt.clf()
        plt.pie(x=wedges, labels=labels, colors=colors, autopct=autopct)

######## bar_chart ##########


class BarPlot(AbstractPlot):

    def create_bar(self, bar_position: int, data: list, width: float, bottom=0, align='center', color=None):
        plt.clf()
        plt.bar(bar_position, data, color=color,
                width=width, bottom=bottom, align=align)
        


class HeatMap(AbstractPlot):

    def create_heatmap(self, data, annot=False, fmt=".1f", cmap=None, vmin=None, vmax=None, linewidth=.0, linecolor="white"):
        plt.clf()
        sns.heatmap(data=data, annot=annot, fmt=fmt,
                    cmap=cmap, vmin=vmin, vmax=vmax, linewidth=linewidth, linecolor=linecolor)
        plt.legend(numpoints=1)

