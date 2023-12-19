import matplotlib.pyplot as plt
from pandas.plotting import table 
import pandas as pd

class Plotter:
    def __init__(self, table, name):
        self.table = table
        self.name = name
        self.table_to_image()
        pd.set_option("display.max_column" , None)
        pd.set_option("display.max_colwidth", None)
        pd.set_option('display.width', -1)
        pd.set_option('display.max_rows', None)

    def table_to_image(self):
        fig, ax = plt.subplots()
        fig.patch.set_visible(False)
        ax.axis('off')
        ax.axis('tight')

        table = ax.table(cellText=self.table.values, colLabels=self.table.columns, loc="center")
        
        table.set_fontsize(14)
        table.scale(1,4)
        
        fig.tight_layout()
        plt.savefig(f'{self.name}.png')

    # def table_styler(self, styler):
    #     styler.set_caption("Test")
    #     styler.format()

# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.plot(range(100))
# fig.savefig('graph.png')

# newcat = Cat('F', "Snuggles", True)
# print(newcat.get_genes())
# newPlot = Plotter(newcat.get_genes())