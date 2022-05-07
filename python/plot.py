from python.data import Data
import plotly.graph_objects as go 

# Read data
data = Data()
data.get_data()

class Plot():
    
    def __init__(self):
        self.data = data

    @staticmethod
    def plot_choro(self, cmap, feature):

        na_list = data.law_data[data.law_data[feature].isnull()]['state']
        z_list = [0 for i in range(len(na_list))]

        non_null_data = go.Choropleth(
            locations=data.law_data[~data.law_data[feature].isnull()]['state'], # Spatial coordinates
            z = data.law_data[~data.law_data[feature].isnull()][feature], # Data to be color-coded
            locationmode = 'USA-states',
            colorscale = cmap,
            marker_line_color='black',
            text=data.law_data[~data.law_data[feature].isnull()].apply(lambda row: f"state: {row['state']}<br>year: {row[feature]}", axis=1),
            hoverinfo="text"
        )

        null_data = go.Choropleth(
            locations=na_list, # Spatial coordinates
            z = z_list, # Data to be color-coded
            locationmode = 'USA-states', # set of locations match entries in `locations`
            colorscale = [[0, 'black'],[1, 'black']],
            colorbar=None,
            name = 'null data',
            showlegend = True,
            showscale = False,
            marker_line_color='white',
            
            text=data.law_data[data.law_data[feature].isnull()].apply(lambda row: f"state: {row['state']}<br>year: {row[feature]}", axis=1),
            hoverinfo="text"
        )

        fig = go.Figure()
        fig.add_trace(non_null_data)
        fig.add_trace(null_data)

        fig.update_geos(visible=False)
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
            geo_scope='usa',  # Plot only the USA instead of globe
            geo = dict(showlakes=False),
            legend=dict(y=0.009,x=-.03),
            )

        fig.data[0].colorbar.x=-0.1
        fig.data[0].colorbar.title='Year<br>Range<br><sup>&nbsp;</sup>'

        return fig