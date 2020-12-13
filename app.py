import dash
import dash_html_components as html


app = dash.Dash(__name__, external_scripts="Stylesheet.css")

app.layout=html.Div(children=[
    html.Div(className="grid-container",
    children=[
        html.Div(className="Tab1",
            children=[html.P("Dashboard")]),
        html.Div(className="Tab2",
            children=[html.P("Vorhersagealgorithmus")])
    ])
])

#@app.route("/")
#def main():
#    return "Welcome!"

if __name__ == "__main__":
    app.run_server(debug=True)