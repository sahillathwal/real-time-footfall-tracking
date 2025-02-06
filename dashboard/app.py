import dash
from dash import dcc, html
import plotly.graph_objs as go

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Live Footfall Tracking"),
    dcc.Graph(
        id="footfall_chart",
        figure=go.Figure(data=[go.Scatter(x=[], y=[], mode="lines+markers")])
    )
])

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)
