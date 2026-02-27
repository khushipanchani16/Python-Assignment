import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
import numpy as np


def draw_plot():
    # 1. Import data
    df = pd.read_csv("epa-sea-level.csv")

    # 2. Create scatter plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(df["Year"], df["CSIRO Adjusted Sea Level"])

    # 3. First line of best fit (1880 - latest year)
    res = linregress(df["Year"], df["CSIRO Adjusted Sea Level"])

    years_extended = np.arange(df["Year"].min(), 2051)
    sea_level_predicted = res.slope * years_extended + res.intercept

    ax.plot(years_extended, sea_level_predicted, 'r')

    # 4. Second line of best fit (2000 - latest year)
    df_recent = df[df["Year"] >= 2000]

    res_recent = linregress(df_recent["Year"], df_recent["CSIRO Adjusted Sea Level"])

    years_recent_extended = np.arange(2000, 2051)
    sea_level_recent_predicted = (
        res_recent.slope * years_recent_extended + res_recent.intercept
    )

    ax.plot(years_recent_extended, sea_level_recent_predicted, 'green')

    # 5. Labels and title
    ax.set_xlabel("Year")
    ax.set_ylabel("Sea Level (inches)")
    ax.set_title("Rise in Sea Level")

    # Save and return
    fig.savefig("sea_level_plot.png")
    return fig
