from abstract_plot import AbstractPlot
from matplotlib import pyplot as plt


class BarChart(AbstractPlot):

    def create_bar(self, bar_position: int, data: list, width: float, bottom=0, align='center', color=None):
        plt.bar(bar_position, data, color=color,
                width=width, bottom=bottom, align=align)
