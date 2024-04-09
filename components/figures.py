from dash import html, dcc
import plotly.express as px
import dash_echarts as dec
import plotly.graph_objs as go
from data.store import results_df
# def gen_randlist(num):
#     return random.sample(range(num), 7)

# def echartsComponent():
#     return html.Div(
#         [
#             dec.DashECharts(
#                 option={
#                     "xAxis": {
#                         "type": "category",
#                         "data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
#                     },
#                     "yAxis": {"type": "value"},
#                     "tooltip": {},
#                     "series": [
#                         {"data": gen_randlist(200), "type": "line", "smooth": True},
#                         {"data": gen_randlist(200), "type": "line", "smooth": True},
#                     ],
#                 },
#                 # id='echarts',
#                 style={
#                     "width": "25dvw",
#                     "height": "25dvh",
#                 },
#             )
#         ],
#         className="w-full h-full echarts-container relative",
#     )

def visualisationFiguresGrid():
    cumReturnLineFig = go.Figure()
    cumReturnLineFig.add_trace(
        go.Scatter(
            x=results_df["Date"],
            y=results_df["portfolio_returns"].cumsum(),
            mode="lines",
            name="Benchmark",
            line=dict(color="rgb(16, 185, 129)"),
        )
    )
    cumReturnLineFig.add_trace(
        go.Scatter(
            x=results_df["Date"],
            y=results_df["cumulative_portfolio_strategy"],
            mode="lines",
            name="Strategy",
            line=dict(color="rgb(244, 63, 94)"),
        )
    )
    for stock, color in zip(
        ["AAPL", "AMZN", "GOOGL", "NFLX", "META"],
        ["#636EFA", "#AB63FA", "#19D3F3", "#FF6692", "#FF97FF", "#FECB52"],
    ):
        cumReturnLineFig.add_trace(
            go.Scatter(
                x=results_df["Date"],
                y=results_df[f"strategy_returns_{stock}"].cumsum(),
                mode="lines",
                name=f"{stock} Strategy",
                line=dict(color=color),  #! use px color
            )
        )
    cumReturnLineFig.update_layout(
        autosize=True,
        margin=dict(l=0, r=20, t=10, b=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="rgb(100,116,139)"),
        xaxis={"showticklabels": False, "title": "Date", "showgrid": False},
        yaxis={
            "title": "Cumulative Return",
            "showgrid": False,
            "zerolinecolor": "rgb(148, 163, 184)",
        },
        showlegend=False,
    )

    drawDownFig = go.Figure()
    drawDownFig.add_trace(
        go.Scatter(
            x=results_df["Date"],
            y=results_df["cum_max"],
            mode="lines",
            name="cum_max",
            line=dict(color="rgb(16, 185, 129)"),
        )
    )
    drawDownFig.add_trace(
        go.Scatter(
            x=results_df["Date"],
            y=results_df["cumulative_portfolio_strategy"],
            mode="lines",
            name="Return",
            line=dict(color="rgb(244, 63, 94)"),
        )
    )

    drawDownFig.update_layout(
        autosize=True,
        margin=dict(l=0, r=20, t=10, b=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="rgb(100,116,139)"),
        xaxis={"showticklabels": False, "title": "Date", "showgrid": False},
        yaxis={
            "title": "Drawdown",
            "showgrid": False,
            "zerolinecolor": "rgb(148, 163, 184)",
        },
        showlegend=False,
    )
    # daily std
    RollingStdFig = go.Figure()
    RollingStdFig.add_trace(
        go.Scatter(
            x=results_df["Date"],
            y=results_df["portfolio_returns"].rolling(21).std(),
            mode="lines",
            name="Benchmark",
            line=dict(color="rgb(16, 185, 129)"),
        )
    )
    RollingStdFig.add_trace(
        go.Scatter(
            x=results_df["Date"],
            y=results_df["portfolio_strategy"].rolling(21).std(),
            mode="lines",
            name="Strategy",
            line=dict(color="rgb(244, 63, 94)"),
        )
    )
    RollingStdFig.update_layout(
        autosize=True,
        margin=dict(l=0, r=20, t=10, b=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="rgb(100,116,139)"),
        xaxis={"showticklabels": False, "title": "Date", "showgrid": False},
        yaxis={
            "title": "Rolling Std",
            "showgrid": False,
            "zerolinecolor": "rgb(148, 163, 184)",
        },
        showlegend=False,
    )
    # distribution of daily strategy returns
    dailyReturnDistFig = px.histogram(
        results_df,
        x="portfolio_strategy",
        nbins=100,
        histnorm="probability",
    )
    dailyReturnDistFig.update_layout(
        autosize=True,
        margin=dict(l=0, r=20, t=10, b=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="rgb(100,116,139)"),
        xaxis={"showgrid": False, "title": "Daily Strategy Returns"},
        yaxis={"showgrid": False, "title": "Probability"},
    )
    return [
        html.Div(
            [
                html.Div(
                    [
                        # return
                        dcc.Graph(
                            figure=cumReturnLineFig,
                            config={"displayModeBar": False},
                            className="w-full h-full",
                        )
                    ],
                    className="h-[45%] w-full relative overflow-hidden zoomable shadow-lg hover:shadow-2xl rounded-lg bg-slate-800 transition duration-300 ease-in-out flex flex-col justify-center items-center p-1",
                ),
                html.Div(
                    [
                        # return
                        dcc.Graph(
                            figure=dailyReturnDistFig,
                            config={"displayModeBar": False},
                            className="w-full h-full",
                        )
                    ],
                    className="h-[45%] w-full relative overflow-hidden zoomable shadow-lg hover:shadow-2xl rounded-lg bg-slate-800 transition duration-300 ease-in-out flex flex-col justify-center items-center p-1",
                ),
            ],
            className="flex flex-col justify-evenly items-center p-0 h-full w-[45%] animate-fade-in animate-500",
        ),
        html.Div(
            [
                html.Div(
                    [
                        # return
                        dcc.Graph(
                            figure=drawDownFig,
                            config={"displayModeBar": False},
                            className="w-full h-full",
                        )
                    ],
                    className="h-[45%] w-full relative overflow-hidden zoomable shadow-lg hover:shadow-2xl rounded-lg bg-slate-800 transition duration-300 ease-in-out flex flex-col justify-center items-center p-1",
                ),
                html.Div(
                    [
                        # return
                        dcc.Graph(
                            figure=RollingStdFig,
                            config={"displayModeBar": False},
                            className="w-full h-full",
                        )
                    ],
                    className="h-[45%] w-full relative overflow-hidden zoomable shadow-lg hover:shadow-2xl rounded-lg bg-slate-800 transition duration-300 ease-in-out flex flex-col justify-center items-center p-1",
                ),
            ],
            className="flex flex-col justify-evenly items-center p-0 h-full w-[45%] animate-fade-in animate-500",
        ),
    ]



def bar():
    dec.DashECharts(
        option={
            "xAxis": {
                "type": "category",
                # rolling 200 days
                "data": results_df["Date"].iloc[::200].to_list(),
            },
            "yAxis": {"type": "value"},
            "tooltip": {},
            "series": [
                {
                    "data": results_df["cumulative_portfolio_returns"]
                    .iloc[::200]
                    .to_list(),
                    "type": "bar",
                    "smooth": True,
                },
                {
                    "data": results_df["cumulative_portfolio_strategy"]
                    .iloc[::200]
                    .to_list(),
                    "type": "bar",
                    "smooth": True,
                },
            ],
        },
        style={
            "width": "25dvw",
            "height": "33dvh",
        },
    )
