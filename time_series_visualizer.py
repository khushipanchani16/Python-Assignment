import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# 1. Import data
df = pd.read_csv(
    "fcc-forum-pageviews.csv",
    parse_dates=["date"],
    index_col="date"
)

# 2. Clean data (remove top 2.5% and bottom 2.5%)
df = df[
    (df["value"] >= df["value"].quantile(0.025)) &
    (df["value"] <= df["value"].quantile(0.975))
]


# 3. Draw Line Plot
def draw_line_plot():
    df_line = df.copy()

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df_line.index, df_line["value"], color="red")

    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    fig.savefig("line_plot.png")
    return fig


# 4. Draw Bar Plot
def draw_bar_plot():
    df_bar = df.copy()

    # Create year and month columns
    df_bar["year"] = df_bar.index.year
    df_bar["month"] = df_bar.index.month
    df_bar["month_name"] = df_bar.index.strftime("%b")

    # Group by year and month
    df_grouped = df_bar.groupby(["year", "month", "month_name"])["value"].mean().reset_index()

    # Pivot table
    df_pivot = df_grouped.pivot(index="year", columns="month_name", values="value")

    # Correct month order
    months_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    df_pivot = df_pivot[months_order]

    fig = df_pivot.plot(kind="bar", figsize=(12, 8)).figure

    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    plt.legend(title="Months")

    fig.savefig("bar_plot.png")
    return fig


# 5. Draw Box Plot
def draw_box_plot():
    df_box = df.copy().reset_index()

    # Prepare data
    df_box["year"] = df_box["date"].dt.year
    df_box["month"] = df_box["date"].dt.strftime("%b")

    # Ensure correct month order
    months_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    df_box["month"] = pd.Categorical(df_box["month"], categories=months_order, ordered=True)

    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    # Year-wise box plot
    sns.boxplot(x="year", y="value", data=df_box, ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    # Month-wise box plot
    sns.boxplot(x="month", y="value", data=df_box, ax=axes[1])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    fig.savefig("box_plot.png")
    return fig
