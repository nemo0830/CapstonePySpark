import os
import random
import dash
import dash_bootstrap_components as dbc
from dash import html
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

df = spark.read.jdbc(url=jdbcUrl, table="game_data", properties=connectionProperties)
df_win = WinRateTransformer().read_table_and_transform(df)
df_matrix = WinRateTransformer().process_matrix(df_win)
header = [""] + WinRateTransformer().columns

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([

    html.H1("Dashboard on RIC Game Stats", style={'marginBottom': '20px'}),
    html.H2("Win Loss Table"),

    html.Div(
        # style=centered_table_style,
        children=[
            html.Table(
                [html.Tr([html.Td(num, style=cell_style_red if num == 0 else cell_style_green) for num in df_matrix[i]]) for i in range(len(df_matrix))],
                style=table_style
            )
        ]
    )
])

if __name__ == "__main__":
    app.run_server(debug=True)