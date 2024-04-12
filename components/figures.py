import plotly.graph_objs as go

def create_line_chart(data, title, line_colors, names):
    """
    Generalized function to create line charts with provided data.

    Args:
    - data (list of dicts): List of dictionaries with 'time' and 'value' keys for each trace.
    - title (str): Title for the y-axis.
    - line_colors (list): List of colors for each trace.
    - names (list): List of names for each trace.

    Returns:
    - go.Figure: Plotly figure object for the line chart.
    """
    fig = go.Figure()
    for i, trace_data in enumerate(data):
        if len(trace_data) == 0:
            continue
        fig.add_trace(
            go.Scatter(
                x=[item['time'] for item in trace_data],
                y=[item['value'] for item in trace_data],
                mode='lines',
                name=names[i],
                line=dict(color=line_colors[i]),
            )
        )
    fig.update_layout(
        autosize=True,
        margin=dict(l=0, r=20, t=10, b=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="rgb(100,116,139)"),
        xaxis={"showticklabels": False, "title": "", "showgrid": False},
        yaxis={"title": title, "showgrid": False, "zerolinecolor": "rgb(148, 163, 184)"},
        showlegend=False,
    )
    return fig
