import os
import pandas as pd
import dash
from dash import dcc, html
import plotly.graph_objects as go

# ---------- Load data (prefer ./output/output.csv, else fallback to data/processed_sales.csv)
data_path = "./output/output.csv" if os.path.exists("./output/output.csv") else "./data/processed_sales.csv"
df = pd.read_csv(data_path)

# ---------- Ensure correct types
# date -> datetime, sales -> numeric
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["sales"] = pd.to_numeric(df["sales"], errors="coerce")

# Drop any bad rows
df = df.dropna(subset=["date", "sales"])

# Aggregate to total sales per day (single smooth line like your screenshot)
daily = df.groupby("date", as_index=False)["sales"].sum().sort_values("date")

# ---------- Build figure
fig = go.Figure()

# sales line
fig.add_trace(go.Scatter(
    x=daily["date"],
    y=daily["sales"],
    mode="lines",
    name="Sales"
))

# Vertical dashed line on price increase date
price_increase_date = pd.Timestamp("2021-01-15")

# Draw the vertical line as a shape (robust with datetimes)
fig.add_shape(
    type="line",
    x0=price_increase_date,
    x1=price_increase_date,
    y0=0,
    y1=1,
    xref="x",
    yref="paper",
    line=dict(color="black", width=2, dash="dash"),
)

# Separate annotation for the label
fig.add_annotation(
    x=price_increase_date,
    y=1,
    xref="x",
    yref="paper",
    text="Price Increase",
    showarrow=False,
    yshift=10,
    align="left"
)

fig.update_layout(
    title="Pink Morsel Sales Over Time",
    xaxis_title="Date",
    yaxis_title="Sales",
    title_x=0.5,
    margin=dict(l=40, r=20, t=60, b=40)
)

# ---------- Dash app
app = dash.Dash(__name__)
app.layout = html.Div(
    children=[
        html.H1("Pink Morsel Visualizer", style={"textAlign": "center", "color": "blue"}),
        dcc.Graph(id="sales-graph", figure=fig),
    ],
    style={"maxWidth": "1000px", "margin": "0 auto"}
)

if __name__ == "__main__":
    app.run(debug=True)
