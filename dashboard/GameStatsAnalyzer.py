import os
import random
import dash
import dash_bootstrap_components as dbc
from dash import html
from config.AppProperties import *
from pyspark.sql import SparkSession
from config.SparkConn import jdbcUrl, connectionProperties

# os.environ["PYSPARK_PYTHON"] = "C:Users\siyuan\AppData\Local\Programs\Python\Python38\python.exe"
# Init Spark
spark = SparkSession.builder \
    .appName("gcloud_sql") \
    .config("spark.jars", "../postgresql-42.6.0.jar") \
    .master("local").getOrCreate()

df = spark.read.jdbc(url=jdbcUrl, table="game_data", properties=connectionProperties)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([

    html.H1("Dashboard on RIC Game Stats", style={'marginBottom': '20px'}),
    html.H2("Win Rate Table"),

    html.Div(
        style=centered_table_style,
        children=[
            html.Table(
                # Apply the table style
                [html.Tr([html.Td(random.randint(0, 9), style=cell_style) for _ in range(9)]) for _ in range(9)],
                style=table_style
            )
        ]
    )
])

if __name__ == "__main__":
    app.run_server(debug=True)