import pandas as pd
import plotly.graph_objects as go
from dataclasses import dataclass
from plotly.subplots import make_subplots


@dataclass
class Plotter:
    df: pd.DataFrame
    plot_name: str

    def __post_init__(self):
        {
            "strategy_base": self.strategy_base,
            "strategy_simple": self.strategy_simple
        }.get(self.plot_name)(self.df)

    @staticmethod
    def strategy_base(df):
        fig = make_subplots(rows=3, cols=1)

        fig.add_trace(go.Scatter(x=df["Date"], y=df["balance"]), row=1, col=1)
        fig.add_trace(go.Scatter(x=df["Date"], y=df["close"]), row=2, col=1)
        fig.add_trace(go.Scatter(x=df["Date"], y=df["active"]), row=3, col=1)

        fig.update_layout(autosize=True, title_text="darkman-bot performance")
        fig.show()


    @staticmethod
    def strategy_simple(df):
        fig = make_subplots(rows=3, cols=1)

        fig.add_trace(go.Scatter(x=df["Date"], y=df["balance"]), row=1, col=1)

        fig.add_trace(go.Scatter(x=df["Date"], y=df["close"]), row=2, col=1)
        fig.add_trace(go.Scatter(x=df["Date"], y=df["short_mavg"]), row=2, col=1)
        fig.add_trace(go.Scatter(x=df["Date"], y=df["long_mavg"]), row=2, col=1)

        fig.add_trace(go.Scatter(x=df["Date"], y=df["active"]), row=3, col=1)

        fig.update_layout(autosize=True, title_text="darkman-bot performance")
        fig.show()
