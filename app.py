import os
import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------
# Load data (prefer ./output/output.csv)
# -----------------------------
DATA_PRIMARY = "./output/output.csv"
DATA_FALLBACK = "./data/processed_sales.csv"
data_path = DATA_PRIMARY if os.path.exists(DATA_PRIMARY) else DATA_FALLBACK

df = pd.read_csv(data_path)
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["sales"] = pd.to_numeric(df["sales"], errors="coerce")
df = df.dropna(subset=["date", "sales"]).sort_values("date")

# Some inputs might miss region; create a single bucket
if "region" not in df.columns:
    df["region"] = "all"

PRICE_INCREASE_DATE = pd.Timestamp("2021-01-15")

# -----------------------------
# App
# -----------------------------
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(
    className="page",
    children=[
        html.H1("Pink Morsel Visualizer", className="title"),
        html.P(
            "Sales trends before and after the price increase on 15 Jan 2021.",
            className="subtitle"
        ),

        html.Div(
            className="controls",
            children=[
                html.Label("Region", className="label"),
                dcc.RadioItems(
                    id="region-radio",
                    options=[
                        {"label": "North", "value": "north"},
                        {"label": "East",  "value": "east"},
                        {"label": "South", "value": "south"},
                        {"label": "West",  "value": "west"},
                        {"label": "All",   "value": "all"},
                    ],
                    value="all",
                    className="radio-group",
                    inputClassName="radio-input",
                    labelClassName="radio-label",
                ),
            ],
        ),

        html.Div(
            className="card",
            children=[
                dcc.Graph(id="sales-graph", config={"displayModeBar": False})
            ],
        ),

        html.Footer("Built with Dash • Quantium mini-project", className="footer"),
    ],
)

# -----------------------------
# Callback
# -----------------------------
@app.callback(
    Output("sales-graph", "figure"),
    Input("region-radio", "value")
)
def update_graph(region_choice: str):
    # Filter and aggregate
    if region_choice == "all":
        use_df = df.copy()
    else:
        use_df = df[df["region"].str.lower() == region_choice]

    daily = (
        use_df.groupby("date", as_index=False)["sales"]
        .sum()
        .sort_values("date")
    )

    # Build base line
    fig = px.line(
        daily,
        x="date", y="sales",
        title="Pink Morsel Sales Over Time",
    )

    # Vertical marker for the price increase (use shapes for robustness)
    fig.add_shape(
        type="line",
        x0=PRICE_INCREASE_DATE, x1=PRICE_INCREASE_DATE,
        y0=0, y1=1,
        xref="x", yref="paper",
        line=dict(color="black", width=2, dash="dash"),
    )
    fig.add_annotation(
        x=PRICE_INCREASE_DATE, y=1,
        xref="x", yref="paper",
        text="Price Increase",
        showarrow=False,
        yshift=10
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Sales",
        title_x=0.5,
        margin=dict(l=40, r=20, t=60, b=40),
        hovermode="x unified",
    )

    return fig

# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
