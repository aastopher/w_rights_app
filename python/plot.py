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

        # Split null data to be added on a seperate trace
        na_list = data.law_data[data.law_data[feature].isnull()]['state']
        z_list = [0 for i in range(len(na_list))]

        # Configure non-null data graph object
        non_null_data = go.Choropleth(
            locations=data.law_data[~data.law_data[feature].isnull()]['state'], # Spatial coordinates
            z = data.law_data[~data.law_data[feature].isnull()][feature], # Data to be color-coded
            locationmode = 'USA-states',
            colorscale = cmap,
            marker_line_color='black',
            text=data.law_data[~data.law_data[feature].isnull()].apply(lambda row: f"state: {row['state']}<br>year: {row[feature]}", axis=1),
            hoverinfo="text"
        )

        # Configure null data graph object
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

        # Instatiate blank graph object and add each defined object as a trace
        fig = go.Figure()
        fig.add_trace(non_null_data)
        fig.add_trace(null_data)

        # Configure layout
        fig.update_geos(visible=False)
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                        geo_scope='usa',
                        geo = dict(showlakes=False),
                        legend=dict(y=0.009,x=-.03))

        # Set colorbar position and title
        fig.data[0].colorbar.x=-0.1
        fig.data[0].colorbar.title='Year<br>Range<br><sup>&nbsp;</sup>'

        return fig