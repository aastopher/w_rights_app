from python.data import Data
import plotly.graph_objects as go 
import numpy as np

# Read data
data = Data()
data.get_data()

class Plot():
    
    def __init__(self):
        self.data = data

    @staticmethod
    def plot_choro(self, cmap, feature):

        # Collect na locations and values
        na_locations = data.law_data[data.law_data[feature].isnull()]['state']
        na_z = [0 for i in range(len(na_locations))]

        # Collect non null locations and values
        nn_locations = data.law_data[~data.law_data[feature].isnull()]['state']
        nn_z = data.law_data[~data.law_data[feature].isnull()][feature]

        # Define consistent tick values
        tick_vals = np.round(np.linspace(min(nn_z), max(nn_z), 8)).astype(int)

        # Configure non-null data graph object
        non_null_data = go.Choropleth(
            locations=nn_locations,
            z = nn_z,
            locationmode = 'USA-states',
            colorscale = cmap,
            colorbar = dict(title='Year<br>Range<br><sup>&nbsp;</sup>',
                            x=-0.1,
                            y=0.52,
                            tickmode='array',
                            tickvals=tick_vals,
                            ticktext=tick_vals
                            ),
            marker_line_color='black',
            text=data.law_data[~data.law_data[feature].isnull()].apply(lambda row: f"state: {row['state']}<br>year: {row[feature]}", axis=1),
            hoverinfo="text"
        )

        # Configure null data graph object
        null_data = go.Choropleth(
            locations=na_locations,
            z = na_z,
            locationmode = 'USA-states',
            colorscale = [[0, 'black'],[1, 'black']],
            colorbar=None,
            name = 'null data',
            showlegend = True,
            showscale = False,
            marker_line_color='white',

            # Apply formating to hover info
            text=data.law_data[data.law_data[feature].isnull()].apply(lambda row: f"state: {row['state']}<br>year: {row[feature]}", axis=1),
            hoverinfo="text"
        )

        # Instatiate blank graph object and add each defined object as a trace
        fig = go.Figure()
        fig.add_trace(non_null_data)
        fig.add_trace(null_data)

        # Configure layout
        fig.update_geos(visible=False)
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                        geo_scope='usa',
                        geo = dict(showlakes=False),
                        legend = dict(y=0.009,x=-.03),
                        )

        return fig