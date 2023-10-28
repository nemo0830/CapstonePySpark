import os
import dash
import dash_bootstrap_components as dbc
from dash import dash_table
from dash import html, dcc
from api import Callbacks
from config.AppProperties import *
from pyspark.sql import SparkSession
from config.SparkConn import jdbcUrl, connectionProperties
from transformer.WinRateTransformer import WinRateTransformer

os.environ["PYSPARK_PYTHON"] = "C:Users\siyuan\AppData\Local\Programs\Python\Python38\python.exe"
# Init Spark
spark = SparkSession.builder \
    .appName("gcloud_sql") \
    .config("spark.jars", "../postgresql-42.6.0.jar") \
    .master("local").getOrCreate()

# Prepare game data
df = spark.read.jdbc(url=jdbcUrl, table="game_data_big", properties=connectionProperties)
transformer = WinRateTransformer()
df_matrix = transformer.process_matrix(transformer.read_table_and_transform(df))
df_win_rate = transformer.calculate_win_rate_and_assign_tiers(df_matrix)
header = [""] + transformer.columns

# Register callbacks
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
Callbacks.register_callbacks(app, df_win_rate)

app.layout = html.Div([
    html.H1("Dashboard on RIC Game Stats", style={'marginBottom': '20px'}),
    html.H2("Team Performance Browser"),
    html.Div([
        html.Label('Top Or Bottom'),
        dcc.Dropdown(id='top_or_bottom', options=top_or_bottom_options, value='top', style={'width': '40%'}),
    ], style={'display': 'flex', 'flexDirection': 'row'}),
    html.Div([
        html.Label('Query num teams:'),
        dcc.Input(id='input-param', type='number', value=0),
        html.Button('Submit', id='submit-button', n_clicks=0)
    ]),
    html.Div([
        dcc.Graph(id='team-score-plot')
    ]),
    html.H2("Win Loss Table (left Host, top Oppo)"),
    html.Div(
        children=[
            html.Table(
                [html.Tr([html.Td(team, style=cell_style) for team in header])] +
                [html.Tr([html.Td(team_name, style=cell_style)] +
                         [html.Td(num, style=cell_style_red if num == 0 else cell_style_green) if i != j else html.Td("-", style=cell_style_yellow) for j, num in enumerate(row)]) for i, (row, team_name) in enumerate(zip(df_matrix, transformer.columns))],
                style=table_style
            )
        ]
    ),
    html.H2("Team Random Allocation (based on tiers)"),
    html.Button("Generate", id="submit-button-alloc", n_clicks=0),
    # Table to display the random numbers
    dash_table.DataTable(
        id='table',
        columns=[{'name': tier_list[i], 'id': f'col_{i}'} for i in range(len(tier_list))],
        data=[],
    ),
])

if __name__ == "__main__":
    app.run_server(debug=True)