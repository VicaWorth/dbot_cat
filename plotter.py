import matplotlib.pyplot as plt
import numpy as np
from pandas.plotting import table 
import pandas as pd

class Plotter:
    def __init__(self, tables : list, chartNames : list, imageName):
        self.tables = tables
        self.imageName = imageName
        
        # pd.set_option("display.max_column" , None)
        # pd.set_option("display.max_colwidth", None)
        # pd.set_option('display.width', -1)
        # pd.set_option('display.max_rows', None)

        self.table_to_image(chartNames)

    def table_to_image(self, chartNames : list):
        lenPlots = len(self.tables)
        fig, axs = plt.subplots(lenPlots)

        fig.patch.set_visible(False)
        counter = 0
        for table in self.tables:
            axs[counter].set_title(chartNames[counter])
            axs[counter].axis('off')
            axs[counter].axis('tight')
            tableDrawn = axs[counter].table(cellText=table.values, colLabels=table.columns, loc="center")
        
            tableDrawn.set_fontsize(14)
            tableDrawn.scale(1,4)
            counter += 1
        
        fig.tight_layout()
        plt.savefig(f'tables/{self.imageName}.png')