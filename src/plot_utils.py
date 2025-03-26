import plotly.graph_objects as go
import matplotlib.pyplot as plt
from statsmodels.distributions.empirical_distribution import ECDF
import numpy as np

# The two lines below mitigate the issue with MathJax rendering in Kaleido and messing up plotly plots.
import plotly.io as pio   
pio.kaleido.scope.mathjax = None

plt.rcParams["figure.figsize"] = [8.5, 4.5]

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = 'Clear Sans'

plt.style.use('fivethirtyeight')

plt.rcParams['axes.linewidth'] = 1

plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False

plt.rcParams['grid.linestyle'] = '--'

plt.rcParams['ytick.color'] = '#333333'
plt.rcParams['xtick.color'] = '#333333'

plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

plt.rcParams['axes.edgecolor'] = '#333333'

plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['savefig.facecolor'] = 'white'
plt.rcParams['figure.facecolor'] = 'white'

plt.rcParams['xtick.major.size'] = 12
plt.rcParams['xtick.minor.size'] = 8
plt.rcParams['ytick.major.size'] = 12
plt.rcParams['ytick.minor.size'] = 8

plt.rcParams['xtick.major.pad'] = 15
plt.rcParams['ytick.major.pad'] = 15

plt.rcParams['axes.grid.which'] = 'major'

plt.rcParams['font.size'] = 20

plt.rcParams['lines.linewidth'] = 4

plt.rcParams['xtick.labelsize'] = 18
plt.rcParams['ytick.labelsize'] = 18

plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42


colors = {
    "red": "#ee443a",
    "blue": "#42bbf1",
    "dark_blue": "#1a4fec",
    "green": "#50be61",
    "grey": "#b7b7b7",
    "orange": "#f28222",
    "purple": "#6e18ee",
    "brown": "#a65628",
    "white": "#ffffff",
    "light_purple": "#cab2d6"
}


def get_plotly_layout(width, height):
    layout = go.Layout(
        template="simple_white",
        font=dict(size=22, family="Clear Sans"),
        margin=go.layout.Margin(
            l=10,  # left margin
            r=10,  # right margin
            b=10,  # bottom margin
            t=10,  # top margin
        ),
        width=width,
        height=height,
        xaxis=dict(
            minor_ticks="inside", showgrid=True, griddash="dash", minor_griddash="dot"
        ),
        yaxis=dict(
            minor_ticks="inside", showgrid=True, griddash="dash", minor_griddash="dot"
        ),
    )
    return layout


def update_plotly_layout_in_place(fig, width, height):
    fig.update_layout(
        template="simple_white",
        font=dict(size=18, family="Clear Sans"),
        margin=go.layout.Margin(
            l=10,  # left margin
            r=10,  # right margin
            b=10,  # bottom margin
            t=10,  # top margin
        ),
        width=width,
        height=height,
        xaxis=dict(
            minor_ticks="inside", showgrid=True, griddash="dash", minor_griddash="dot"
        ),
        yaxis=dict(
            minor_ticks="inside", showgrid=True, griddash="dash", minor_griddash="dot"
        ),
    )


def plot_cdf(
    data,
    width=850,
    height=450,
    xlog=False,
    xaxis_title="",
    color=colors["blue"],
    filename=False,
    line_name="",
    fig=None,
):
    if not fig:
        fig = go.Figure(layout=get_plotly_layout(width=width, height=height))
    ecdf = ECDF(data)
    fig.add_trace(
        go.Scatter(x=ecdf.x, y=ecdf.y, line=dict(
            color=color, width=5, dash=None), name=line_name)
    )
    if xlog:
        fig.update_xaxes(type="log")
    fig.update_yaxes(range=[0, 1], tickformat=",.0%")
    fig.update_layout(xaxis_title=xaxis_title, yaxis_title="CDF")

    if filename:
        fig.savefig(filename, bbox_inches="tight")
    return fig


def plot_line_chart(
    votes_for,
        votes_against,
        line_name='',
        line_width=3,
        line_style='solid',
        color=colors['blue'],
        x_axis_title="Percentage of for votes",
        y_axis_title="Percentage of against votes",
        width=850,
        height=450,
        fig=None):
    if not fig:
        fig = go.Figure(layout=get_plotly_layout(width=width, height=height))

    fig.add_trace(go.Scatter(x=votes_for, y=votes_against, name=line_name,
                             line=dict(color=color, width=line_width, dash=line_style)))

    fig.update_layout(xaxis=dict(title=x_axis_title, tickformat=".0%", range=[0, 0.5]), yaxis=dict(
        title=y_axis_title, tickformat=".0%", range=[0, 0.5]))

    fig.add_annotation(x=.1, y=.25,
                       text="Defeated",
                       showarrow=False,
                       font=dict(color=colors['red'])
                       )
    fig.add_annotation(x=.33, y=.1,
                       text="Succeeded",
                       showarrow=False,
                       font=dict(color=colors['green'])
                       )

    return fig


def plot_ohlc(series, title="", width=850, height=450):
    fig = go.Figure(layout=get_plotly_layout(width=width, height=height))
    fig.add_trace(go.Candlestick(x=series.index,
                                 open=series['open'],
                                 high=series['high'],
                                 low=series['low'],
                                 close=series['close'], name='OHLC'))
    fig.update_layout(autosize=True, title=title)
    fig.update_layout(yaxis_title='Price (in USD)',
                      xaxis_rangeslider_visible=False, template='plotly_white')
    return fig


def plot_heatmap_votes(df, zmin=0, zmax=2, tickvals=[0, 1, 2], xgap=1, ygap=1, colorbarlen=200, colorscale=None, ticktext=['Against', 'In-favor', 'Abstain']):
    fig = go.Figure(layout=get_plotly_layout(width=1540, height=380))
    if colorscale is None:
        colorscale = [
            [0, colors['red']],
            [0.1, colors['red']],
            [0.1, colors['red']],
            [0.2, colors['red']],
            [0.2, colors['red']],
            [0.3, colors['red']],

            [0.3,  colors['green']],
            [0.4,  colors['green']],

            [0.4,  colors['green']],
            [0.5,  colors['green']],

            [0.5,  colors['green']],
            [0.6,  colors['green']],

            [0.6, colors['green']],
            [0.7, colors['green']],

            [0.7, colors['blue']],
            [0.8, colors['blue']],

            [0.8, colors['blue']],
            [0.9, colors['blue']],

            [0.9, colors['blue']],
            [1.0, colors['blue']]
        ]

    fig.add_trace(go.Heatmap(y=df.index,
                             x=df.columns,
                             z=df.values,
                             hoverongaps=False,
                             colorscale=colorscale,
                             zmin=zmin,
                             zmax=zmax,
                             hovertemplate='Proposal ID' +
                             ': %{x}<br>' + 'Voter' + ': %{y}<br>' +
                             'Vote'+': %{z}<extra></extra>',
                             ))

    fig.update_traces(showscale=True,
                      colorbar=dict(lenmode='pixels',
                                    len=colorbarlen,
                                    thickness=15,
                                    tickvals=tickvals,
                                    ticktext=ticktext,
                                    title='',
                                    orientation='h',
                                    xanchor='center',
                                    x=0.5,
                                    yanchor='top',
                                    y=1.25),
                      xgap=xgap, ygap=ygap)

    fig.update_layout(
        xaxis_title='Proposal ID',
        yaxis_title='Voter',
        legend=dict(xanchor='center', x=0.5, y=1.1, orientation='h'),
        xaxis=dict(tickmode='linear', tick0=0, dtick=20),
    )

    return fig


def plot_heatmap(data, title='',
                 yaxis_title='',
                 xaxis_title='',
                 freq_text='Count',
                 font_size_z=20,
                 xaxis_rangeslider_visible=False,
                 annotation=True):
    colorscale = [
        [0, colors['white']],
        [0.1, colors['white']],
        [0.1, colors['white']],
        [0.2, colors['white']],
        [0.2, colors['white']],
        [0.3, colors['white']],

        [0.3,  colors['white']],
        [0.4,  colors['white']],

        [0.4,  colors['white']],
        [0.5,  colors['white']],

        [0.5,  colors['white']],
        [0.6,  colors['white']],

        [0.6, colors['white']],
        [0.7, colors['blue']],

        [0.7, colors['blue']],
        [0.8, colors['blue']],

        [0.8, colors['blue']],
        [0.9, colors['blue']],

        [0.9, colors['blue']],
        [1.0, colors['blue']]
    ]

    z_text = None
    if annotation:
        z_text = np.round(data.values, 3)

    fig = go.Figure(layout=get_plotly_layout(width=1540, height=380),
                    data=go.Heatmap(x=data.index,
                                    y=data.index,
                                    z=data,
                                    text=z_text,
                                    texttemplate="<b>%{text}</b>",
                                    textfont=dict(size=font_size_z),
                                    colorscale=colorscale,
                    hovertemplate=xaxis_title +
                                    ': %{x}<br>' + yaxis_title + ': %{y}<br>' +
                                    freq_text+': %{z}<extra></extra>',
                    colorbar=dict(title='Range')))
    fig.update_layout(yaxis_title=yaxis_title, xaxis_title=xaxis_title,
                      xaxis_rangeslider_visible=xaxis_rangeslider_visible, title=title)

    return fig
