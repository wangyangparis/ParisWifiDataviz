import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import json
import pandas as pd


def get_fig_map(df):
    """
    get the fig map layout
    :param df:
    :return:
    """
    fig = px.scatter_mapbox(df,
                            lon='lon',
                            lat='lat',
                            size='session_count',
                            color='session_count',
                            title='paris wifi map',
                            hover_name='site_name',
                            hover_data=['site_code', 'site_name', 'session_count'],
                            mapbox_style="carto-positron",
                            color_continuous_scale=px.colors.carto.Bluyl
                            )

    fig.update_layout(
        mapbox={'center': {'lat': 48.853499, 'lon': 2.3493147}, 'zoom': 11},
        margin={'l': 0, 'r': 0, 't': 0, 'b': 0})
    return fig


def get_fig_map_choropleth(df):
    with open('./data/arrondissements.geojson') as file:
        geojson_paris = json.load(file)
    fig = px.choropleth(df,
                        geojson=geojson_paris,
                        color="count",
                        color_continuous_scale=px.colors.carto.Bluyl,
                        locations="postal_code",
                        featureidkey="properties.c_arinsee",
                        projection="mercator",
                        hover_data=["postal_code", "count"]
                        )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig


def get_fig_3d_plot(df):
    df_3d = df.copy()
    df_3d['date'] = df.index.date
    df_3d['hour'] = df.index.hour
    df_3d = pd.DataFrame.pivot_table(df_3d, values='session_count', columns='hour', index='date')

    z = df_3d.values
    x = df_3d.columns
    y = df_3d.index

    fig = go.Figure(data=[go.Surface(z=z, x=x, y=y)])
    fig.update_layout(title='3d plot',
                      autosize=True,
                      margin=dict(l=0, r=0, b=0, t=0),
                      scene=dict(
                          xaxis_title='hour',
                          yaxis_title='date',
                          zaxis_title='session count')
                      )

    return fig


def get_fig_polar_bar(df):
    """
    get the fig polar bar layout
    :param df:
    :return:
    """
    sess_counts = df.session_count.tolist()
    # r, _ = np.mgrid[1:7:7j, 0:(360 / 7 * 6):7j]
    r = np.array([["week " + str(w - 2) for w in range(7)] for h in range(7)]).transpose()
    theta = np.array(
        [['Monday'] * 7, ['Tuesday'] * 7, ['Wednesday'] * 7, ['Thursday'] * 7, ['Friday'] * 7, ['Saturday'] * 7,
         ['Sunday'] * 7]).transpose()

    # take data of weeks in march from 03-02 to 03-29
    color = sess_counts[1:29]
    color = np.asarray(color)
    whitecolor = np.zeros(21, dtype=int)
    color = np.append(whitecolor, color)

    fig = px.bar_polar(
        r=r.ravel(),
        theta=theta.ravel(),
        color=color.ravel(),
        title="Radical Weekly Wifi Connection Periodic Viz",
        labels={1: "cool"},
        start_angle=360 / 14,
        color_continuous_scale=[
            "rgb(255, 255, 255)",
            "#fbe6c5", "#f5ba98", "#ee8a82", "#dc7176", "#c8586c", "#9c3f5d", "#70284a",
        ]  # color from px.colors.carto.Buryl
    )
    fig.update_traces(text=np.mgrid[6.5:7:7j])
    fig.update_layout(polar_bargap=0,
                      polar=dict(radialaxis=dict(showticklabels=False))
                      )

    return fig


def get_fig_polar_bar_hourly(df):
    """
    get the fig polar bar layout
    :param df:
    :return:
    """
    sess_counts = df.session_count.tolist()
    r = np.array([["March " + str(d-1) for d in range(33)] for h in range(24)]).transpose()
    theta = np.array([[str(h) + "h" for h in range(24)] for d in range(33)])
    # take data of hours
    color = sess_counts  # 24*31

    color = np.asarray(color)
    whitecolor = np.zeros(48, dtype=int)
    color = np.append(whitecolor, color)

    fig = px.bar_polar(
        r=r.ravel(),
        theta=theta.ravel(),
        color=color.ravel(),
        title="Radical Hourly Wifi Connection Periodic Viz",
        start_angle=360 / 48,
        color_continuous_scale=[
            "rgb(255, 255, 255)",
            "#fbe6c5", "#f5ba98", "#ee8a82", "#dc7176", "#c8586c", "#9c3f5d", "#70284a",
        ]  # color from px.colors.carto.Buryl
    )
    fig.update_layout(polar_bargap=0,
                      polar=dict(radialaxis=dict(showticklabels=False)))

    return fig


def get_fig_dist(df):
    colors = px.colors.qualitative.Pastel
    colors.append(px.colors.qualitative.Prism)
    colors.append(px.colors.qualitative.Safe)
    fig = go.Figure()
    for column in df:
        fig.add_trace(go.Bar(
            y=df.index,
            x=df[column],
            name=column,
            orientation='h',
            marker_color=colors[df.columns.get_loc(column)]
        ))
    fig.update_yaxes(nticks=31)
    fig.update_layout(barmode='stack', xaxis_title='Number of connections', yaxis_title='Date', height=800)
    return fig
