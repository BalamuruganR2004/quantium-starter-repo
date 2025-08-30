import os
import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# -----------------------------
# Load data (prefer ./output/output.csv, fallback to ./data/processed_sales.csv)
# -----------------------------
DATA_PRIMARY = "./output/output.csv"
DATA_FALLBACK = "./data/processed_sales.csv"
data_path = DATA_PRIMARY if os.path.exists(DATA_PRIMARY) else DATA_FALLBACK

df = pd.read_csv(data_path)

if "date" not in df.columns or "sales" not in df.columns:
    raise ValueError(
        f"Expected columns ['sales','date','region'] in {data_path}. "
        "Re-run process_data.py to generate the proper output."
    )

df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["sales"] = pd.to_numeric(df["sales"], errors="coerce")

if "region" not in df.columns:
    df["region"] = "all"
df["region"] = df["region"].str.lower().fillna("all")

df = df.dropna(subset=["date", "sales"]).sort_values("date")

PRICE_INCREASE_DATE = pd.Timestamp("2021-01-15")

# -----------------------------
# App
# -----------------------------
app = dash.Dash(__name__)
server = app.server

REGION_OPTIONS = [
    {"label": "North", "value": "north"},
    {"label": "East",  "value": "east"},
    {"label": "South", "value": "south"},
    {"label": "West",  "value": "west"},
    {"label": "All",   "value": "all"},
]

app.layout = html.Div(
    className="page",
    children=[
        html.H1("Pink Morsel Visualizer", id="header", className="title"),
        html.P(
            "Sales trends before and after the price increase on 15 Jan 2021.",
            className="subtitle"
        ),

        html.Div(
            className="controls",
            children=[
                html.Label("Region", className="label"),
                dcc.RadioItems(
                    id="region-picker",   # ✅ matches tests
                    options=REGION_OPTIONS,
                    value="all",
                    className="radio-group",
                    inputClassName="radio-input",
                    labelClassName="radio-label",
                ),
            ],
        ),

        html.Div(className="card", children=[dcc.Graph(id="sales-graph", config={"displayModeBar": False})]),

        html.Div(
            className="kpi-row",
            children=[
                html.Div(className="kpi", children=[
                    html.Div("Total Sales BEFORE 15 Jan 2021", className="kpi-label"),
                    html.Div(id="kpi-before", className="kpi-value"),
                ]),
                html.Div(className="kpi", children=[
                    html.Div("Total Sales AFTER 15 Jan 2021", className="kpi-label"),
                    html.Div(id="kpi-after", className="kpi-value"),
                ]),
                html.Div(className="kpi", children=[
                    html.Div("Δ (After - Before)", className="kpi-label"),
                    html.Div(id="kpi-delta", className="kpi-value"),
                ]),
                html.Div(className="kpi", children=[
                    html.Div("% Change", className="kpi-label"),
                    html.Div(id="kpi-pct", className="kpi-value"),
                ]),
            ]
        ),

        html.Div(id="kpi-verdict", className="verdict"),

        html.Footer("Built with Dash • Quantium mini-project", className="footer"),
    ],
)

# -----------------------------
# Helpers
# -----------------------------
def filter_and_aggregate(region_choice: str) -> pd.DataFrame:
    if region_choice == "all":
        use_df = df
    else:
        use_df = df[df["region"] == region_choice]
    daily = use_df.groupby("date", as_index=False)["sales"].sum().sort_values("date")
    return daily

def compute_kpis(daily: pd.DataFrame):
    before_total = daily.loc[daily["date"] < PRICE_INCREASE_DATE, "sales"].sum()
    after_total  = daily.loc[daily["date"] >= PRICE_INCREASE_DATE, "sales"].sum()
    delta = after_total - before_total
    pct = (delta / before_total * 100) if before_total != 0 else float("inf")
    verdict = (
        "Sales were HIGHER AFTER the price increase"
        if after_total > before_total
        else "Sales were HIGHER BEFORE the price increase"
        if after_total < before_total
        else "No change in sales across the split"
    )
    return before_total, after_total, delta, pct, verdict

# -----------------------------
# Callback
# -----------------------------
@app.callback(
    Output("sales-graph", "figure"),
    Output("kpi-before", "children"),
    Output("kpi-after", "children"),
    Output("kpi-delta", "children"),
    Output("kpi-pct", "children"),
    Output("kpi-verdict", "children"),
    Input("region-picker", "value"),
)
def update_view(region_choice: str):
    daily = filter_and_aggregate(region_choice)

    fig = px.line(daily, x="date", y="sales", title="Pink Morsel Sales Over Time")
    fig.add_shape(
        type="line",
        x0=PRICE_INCREASE_DATE, x1=PRICE_INCREASE_DATE,
        y0=0, y1=1,
        xref="x", yref="paper",
        line=dict(color="black", width=2, dash="dash"),
    )
    fig.add_annotation(
        x=PRICE_INCREASE_DATE, y=1, xref="x", yref="paper",
        text="Price Increase", showarrow=False, yshift=10
    )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Sales",
        title_x=0.5,
        margin=dict(l=40, r=20, t=60, b=40),
        hovermode="x unified",
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True),
    )

    before_total, after_total, delta, pct, verdict = compute_kpis(daily)
    money = lambda x: f"${x:,.0f}"
    pct_str = "∞" if pct == float("inf") else f"{pct:.1f}%"

    return (
        fig,
        money(before_total),
        money(after_total),
        money(delta),
        pct_str,
        f"Conclusion: {verdict}",
    )

if __name__ == "__main__":
    app.run(debug=True)
