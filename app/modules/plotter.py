import pandas as pd
import plotly.graph_objects as go
from dataclasses import dataclass
from plotly.subplots import make_subplots

@dataclass
class Plotter:
    df: pd.DataFrame

    def __post_init__(self):
        self.multiline_plot(self.df)


    @staticmethod
    def multiline_plot(df):
        fig = make_subplots(rows=3, cols=1)

        fig.add_trace(go.Scatter(x=df.index.tolist(), y=df["balance"].tolist()), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index.tolist(), y=df["Close"].tolist()), row=2, col=1)
        fig.add_trace(go.Scatter(x=df.index.tolist(), y=df["active"].tolist()), row=3, col=1)

        fig.update_layout(autosize=True, title_text="darkman-bot performance")
        fig.show()
