from abstract_plot import AbstractPlot
from matplotlib import pyplot as plt

Wedges = list[int]
Labels = list[str]


class PieChart(AbstractPlot):

    def create_pie(self, wedges: Wedges, labels: Labels, autopct: str, colors=None):
        plt.pie(x=wedges, labels=labels, colors=colors, autopct=autopct)
