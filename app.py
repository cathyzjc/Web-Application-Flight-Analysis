import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import main
import plotly.graph_objects as go # or plotly.express as px
import base64

fig = go.Figure() # or any Plotly Express function e.g. px.bar(...)

# drop down list for use in airport codes
from controls import city_df, airport_df, routes_df, airlines_df
from distance import distance_df_final

# setup app with stylesheets
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# Create map template
mapbox_access_token = "pk.eyJ1IjoiY2F0aHl6amMiLCJhIjoiY2todTE5bDZ6MTVnZDMxbnRsOThkdHZuNSJ9.OoCm90AgzgZYCOR3jraSZw"


controls = dbc.Card(
    [
        dbc.FormGroup(
            [
                dbc.Label("Start City"),
                dcc.Dropdown(
                    options=[{"label": col, "value": col} for col in city_df['City']],
                    value="San Francisco",
                    id="start-city"
                ),
            ]
        ),

        dbc.FormGroup(
            [
                dbc.Label("Start Airport"),
                dcc.Dropdown(id="start-airport"),
            ]
        ),

        dbc.FormGroup(
            [
                dbc.Label("Destination City"),
                dcc.Dropdown(id="destination-city", value="New York"),
            ]
        ),

        dbc.FormGroup(
            [
                dbc.Label("Destination Airport"),
                dcc.Dropdown(id="end-airport"),
            ]
        ),

        dbc.Button("Submit", id="Submit-button", outline=True, color="primary", className="mr-1"),
    ],
    body=True, color="light",
)

distance_control = dbc.Card(
    [
        dbc.CardBody(
            [
                dcc.Markdown(id='display-selected-values', style={'color': '#4B5658', 'fontSize': 20, 'marginLeft': 15})
            ],
        ),
    ],
    color="light",
)

image_filename_1 = 'graph/departures.PNG' # replace with your own image
encoded_image_1 = base64.b64encode(open(image_filename_1, 'rb').read())
airport_1 = dbc.Card(
    [
        dbc.CardImg(src='data:image/png;base64,{}'.format(encoded_image_1.decode()), top=True),
        dbc.CardBody(
            [
                html.H4(id='departure-1', className="card-title"),
                dcc.Markdown(id='departure-2', className="card-text"),
                dcc.Markdown(id='departure-3', className="card-text"),
                #dbc.Button("Go somewhere", color="primary"),
            ]
        ),
    ],
    style={"width": "35rem"},
)

image_filename_2 = 'graph/arrivals.PNG' # replace with your own image
encoded_image_2 = base64.b64encode(open(image_filename_2, 'rb').read())
airport_2 = dbc.Card(
    [
        dbc.CardImg(src='data:image/png;base64,{}'.format(encoded_image_2.decode()), top=True),
        dbc.CardBody(
            [
                html.H4(id='arrival-1', className="card-title"),
                dcc.Markdown(id='arrival-2', className="card-text"),
                dcc.Markdown(id='arrival-3', className="card-text"),
                # dbc.Button("Go somewhere", color="primary"),
            ]
        ),
    ],
    style={"width": "35rem"},
)

image_filename_3 = 'graph/COVID.PNG' # replace with your own image
encoded_image_3 = base64.b64encode(open(image_filename_3, 'rb').read())
covid = dbc.Card(
    [
        dbc.CardImg(src='data:image/png;base64,{}'.format(encoded_image_3.decode()), top=True),
        dbc.CardBody(
            [
                html.H4("Travel During COVID-19", className="card-title"),
                dcc.Markdown('''Travel increases your chance of getting and spreading COVID-19. 
                **Staying home is the best way to protect yourself and others from COVID-19.**''',
                             className="card-text"),
                dbc.CardLink("More Info", href="https://www.cdc.gov/coronavirus/2019-ncov/travelers/travel-during-covid19.html"),
                # dbc.Button("Go somewhere", color="primary"),
            ]
        ),
    ],
    style={"width": "35rem"},
)


app.layout = dbc.Container(
    [
        dbc.Row(
            [dbc.Col(
                html.H1("Kartemap - An Airport Network Analysis Application",style={'color':'#4B5658'}),
            )],
            style={'marginTop': 50, 'marginLeft': 40, 'marginRight': 40},
        ),
        dbc.Row(
            [dbc.Col(
                html.H3("Designed by Zhijiao Chen", style={'color':'#4B5658'}),
            )],
            style={'marginTop': 10, 'marginBottom': 20, 'marginLeft': 40, 'marginRight': 40},
        ),
        dbc.Row(
            [
                dbc.Col(controls, md=4),
                dbc.Col(dcc.Graph(id="map"), md=8)
            ],
            align="top", style={'marginTop': 20, 'marginLeft': 40,'marginRight': 40},
        ),
        dbc.Row(
            [
                dbc.Col(distance_control, md=12)
            ],
            align = "top",style={'marginTop': 30, 'marginBottom': 20, 'marginLeft': 40,'marginRight': 40},
        ),
        dbc.Row(
            [
                dbc.Col(airport_1, md=4),
                dbc.Col(airport_2, md=4),
                dbc.Col(covid, md=4)
            ],
            align="Top", style={'marginTop': 30, 'marginBottom': 80, 'marginLeft': 40,'marginRight': 40},
        ),
    ],
    id="main-container",
    style={"display": "flex", "flex-direction": "column"},
    fluid=True
)


# Decide destination city by removing start city
@app.callback(Output('destination-city','options'),
              Input('start-city','value'))
def populate_city_controls(start_city):
    destination_city_options = [{"label": col, "value": col} for col in city_df['City']]
    destination_city_options.remove({"label": start_city, "value": start_city})
    return destination_city_options


# Set initial value of destination city
@app.callback(Output('destination-city', 'value'),
              Input('destination-city', 'options'))
def populate_city_value(available_options):
    return available_options[105]['value']


# Decide start airport by start city
@app.callback(Output('start-airport','options'),
              Input('start-city','value'))
def populate_airport_controls(start_city):
    start_airport_options = [{"label": col, "value": col} for col in airport_df.loc[airport_df['City'] == start_city,'IATA']]
    return start_airport_options


# Set initial value of first start airport
@app.callback(Output('start-airport', 'value'),
              Input('start-airport', 'options'))
def populate_city_value(available_options):
    return available_options[0]['value']


# Decide end airport by end city
@app.callback(Output('end-airport','options'),
              Input('destination-city','value'))
def populate_airport_controls_end(destination_city):
    end_airport_options = [{"label": col, "value": col} for col in airport_df.loc[airport_df['City'] == destination_city,'IATA']]
    return end_airport_options


# Set initial value of end airport
@app.callback(Output('end-airport', 'value'),
              Input('end-airport', 'options'))
def populate_city_value_end(available_options):
    return available_options[0]['value']



# Draw the map
@app.callback(Output('map', 'figure'),
              Output('display-selected-values','children'),
              Output('departure-1','children'),
              Output('departure-2','children'),
              Output('departure-3','children'),
              Output('arrival-1','children'),
              Output('arrival-2','children'),
              Output('arrival-3','children'),
              Input('Submit-button', 'n_clicks'),
              Input('start-city', 'value'),
              Input('destination-city', 'value'),
              State('start-airport', 'value'),
              State('end-airport', 'value'))

def make_map(n_clicks, start_city,destination_city, start_airport, end_airport):
    fig = go.Figure()
    for name, df in airport_df.groupby('City'):
        if name in [start_city, destination_city]:
            fig.add_trace(go.Scattermapbox(
                lon=df['Longitude'],
                lat=df['Latitude'],
                text=df['Name'],
                showlegend=False,
                marker=dict(
                    size=20
                ),
            ))
        #else:
            #fig.add_trace(go.Scattermapbox(
            #    lon=df['Longitude'],
            #    lat=df['Latitude'],
            #    text=df['City'],
            #    showlegend=False,
             #   marker=dict(
            #        size=10,
            #        opacity=0.5,
            #    ),
           # ))

    df = distance_df_final
    df_choose = df.loc[(df['Start_airport'] == start_airport) & (df['End_airport'] == end_airport),:]
    if len(df_choose) > 0:
        airports = [df_choose.iloc[0].Start_airport, df_choose.iloc[0].End_airport]
        distance = round(df_choose.iloc[0].Distance)
    else:
        network = main.main(start_airport, end_airport)
        airports = network[2]
        distance = network[3]

    if start_airport is None or end_airport is None or airports is None or distance is None:
        fig.update_layout(
            margin={'l': 10, 't': 50, 'b': 10, 'r': 10},
            mapbox={
                'center': {'lon': -95.7, 'lat': 37},
                'accesstoken': mapbox_access_token,
                'style': "outdoors",
                'zoom': 3},
            autosize=True,
            hovermode="closest",
            plot_bgcolor="#F9F9F9",
            paper_bgcolor="#F9F9F9",
            legend=dict(font=dict(size=10), orientation="h"),
            title="Flight Network",
            title_font_size=20
        )
        conclusion = u'There is no flight between {} and {}.'.format(start_airport, end_airport)
        departure_1, departure_2, departure_3, arrival_1, arrival_2, arrival_3 = None, None, None, None, None, None

    else:

        lat = []
        lon = []
        text = []
        start_airport_name = airport_df[airport_df.IATA == start_airport].iloc[0].Name
        end_airport_name = airport_df[airport_df.IATA == end_airport].iloc[0].Name
        start_airport_city = airport_df[airport_df.IATA == start_airport].iloc[0].City
        start_airport_country = airport_df[airport_df.IATA == start_airport].iloc[0].Country
        start_airport_timezone_1 = airport_df[airport_df.IATA == start_airport].iloc[0].Timezone
        start_airport_timezone_2 = airport_df[airport_df.IATA == start_airport].iloc[0]["Tz database time zone"]

        end_airport_city = airport_df[airport_df.IATA == end_airport].iloc[0].City
        end_airport_country = airport_df[airport_df.IATA == end_airport].iloc[0].Country
        end_airport_timezone_1 = airport_df[airport_df.IATA == end_airport].iloc[0].Timezone
        end_airport_timezone_2 = airport_df[airport_df.IATA == end_airport].iloc[0]["Tz database time zone"]

        for trace in airports:
            df = airport_df[airport_df["IATA"].isin([trace])]
            lat.append(df.iloc[0].Latitude)
            lon.append(df.iloc[0].Longitude)
            text.append(df.iloc[0].Name)

        fig = fig.add_trace(go.Scattermapbox(
            mode="markers+lines",
            lon=lon,
            lat=lat,
            marker={'size': 20, 'symbol': 'airport'},
            text=text,
            textposition="bottom right"))

        fig.update_layout(
            margin={'l': 10, 't': 50, 'b': 10, 'r': 10},
            mapbox={
                'center': {'lon':-95.7, 'lat':37},
                'accesstoken': mapbox_access_token,
                'style': "outdoors",
                'zoom': 3},
            autosize=True,
            hovermode="closest",
            plot_bgcolor="#F9F9F9",
            paper_bgcolor="#F9F9F9",
            legend=dict(font=dict(size=10), orientation="h"),
            title="Flight Network",
            title_font_size=20
        )
        conclusion = '''The overall distance from **{}** to **{}** is {} km, and **{}** stop(s) between arrival and departure.'''\
            .format(start_airport,end_airport,distance,len(airports)-2)
        departure_1 = u'{}'.format(start_airport_name)
        departure_2 = u'**Location**: {},  {}'.format(start_airport_city,start_airport_country)
        departure_3 = u'**Timezone**: {},  {}'.format(start_airport_timezone_1,start_airport_timezone_2)
        arrival_1 = u'{}'.format(end_airport_name)
        arrival_2 = u'**Location**: {},  {}'.format(end_airport_city, end_airport_country)
        arrival_3 = u'**Timezone**: {},  {}'.format(end_airport_timezone_1, end_airport_timezone_2)

    return fig, conclusion, departure_1, departure_2, departure_3 ,arrival_1, arrival_2, arrival_3


# Main
if __name__ == "__main__":
    app.run_server(debug=True)
