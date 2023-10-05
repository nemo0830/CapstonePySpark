from dash.dependencies import Input, Output, State
import plotly.express as px

def register_callbacks(app, win_rate_data):

    @app.callback(
        Output(component_id='team-score-plot', component_property='figure'),
        State(component_id='top_or_bottom', component_property='value'),
        Input(component_id='submit-button', component_property='n_clicks'),
        State(component_id='input-param', component_property='value'),
    )
    def update_top_x_score(top_or_bottom, n_clicks, input_param, df=win_rate_data): ## must be Pandas df, param orders need to exactly follow the order in decorators
        if top_or_bottom == "top":
            df = df.head(input_param)
        else:
            df = df.tail(input_param)
        fig = px.bar(df, x="team_name", y="win_rate",
                     hover_data=['team_name', 'win_rate'], color='win_rate',
                     labels={'pop': ''}, height=450,
                     title=top_or_bottom + " " + str(input_param) + " teams and their win rates") \
            .update_layout(title_font_size=30)
        return fig
