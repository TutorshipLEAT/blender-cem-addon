from matplotlib import pyplot as plt

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

    def save_to_png(self, path: str) -> None:
        plt.savefig(f'{path}.png')
