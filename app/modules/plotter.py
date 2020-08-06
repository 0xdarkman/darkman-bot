import pandas as pd
import plotly.express as px
pd.options.plotting.backend = "plotly"
from dataclasses import dataclass
from plotly.subplots import make_subplots

@dataclass
class Plotter:
    df: pd.DataFrame

    def __post_init__(self):
        self.multiline_plot(self.df)

    @staticmethod
    def single_line_plot(df):
        fig = px.line(df, x='Date', y='High')
        fig.add_scatter(x=df['Date'], y=df['balance'])
        fig.show()

    @staticmethod
    def multiline_plot(df):
        df = df.set_index("Date")
        subfig = make_subplots(specs=[[{"secondary_y": True}]])

        # create two independent figures with px.line each containing data from multiple columns
        fig = px.line(df, y=df["balance"], render_mode="webgl", )
        fig2 = px.line(df, y=df["Close"], render_mode="webgl", )
        fig3 = px.line(df, y=df["ma"], render_mode="webgl", )

        fig.update_traces(yaxis="y1")
        fig2.update_traces(yaxis="y2")
        fig3.update_traces(yaxis="y2")

        subfig.add_traces(fig.data + fig2.data + fig3.data)
        subfig.layout.xaxis.title = "Time"
        subfig.layout.yaxis.title = "Close"
        subfig.layout.yaxis2.type = "log"
        subfig.layout.yaxis2.title = "Balance"
        subfig.for_each_trace(lambda t: t.update(line=dict(color=t.marker.color)))
        subfig.show()
