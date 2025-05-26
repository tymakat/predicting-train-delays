import pandas as pd
import matplotlib.pyplot as plt


def filter_by_column_value(dataset: pd.DataFrame, column: str, value) -> pd.DataFrame:
    return dataset[dataset[column] == value]

def filter_by_column_value_over_under(dataset: pd.DataFrame, column: str, over: bool, value) -> pd.DataFrame:
    return dataset[dataset[column] > value] if over else dataset[dataset[column] <= value]

def plot_range_pie(df, column, ranges):
    #create a pie chart to visualize different delay ranges in dataset
    #to get an insight about the delays, to later evenly split it for classification.
    total = len(df)

    # counts per slice
    counts = [df[column].between(lo, hi, inclusive="both").sum()
              for lo, hi in ranges]

    # overall % per slice (share of ALL rows)
    percentages = [cnt / total * 100 for cnt in counts]

    # formatted strings: "<range> - <percentage>, <occurrences>"
    summary_strings = [
        f"{lo}–{hi} - {pct:.1f}%, {cnt}"
        for (lo, hi), pct, cnt in zip(ranges, percentages, counts)
    ]

    # ------ PLOT -------
    fig, ax = plt.subplots()
    wedges, _, _ = ax.pie(
        counts,
        startangle=90,
        autopct=lambda pct: f"{pct:.1f}%",  # keeps wedge labels
        textprops={'weight': 'bold'}
    )
    ax.legend(
        wedges,
        [f"{lo}–{hi}" for lo, hi in ranges],
        title="Ranges",
        loc="center left",
        bbox_to_anchor=(1, 0.5)
    )
    ax.set_title(f"Distribution of '{column}' (N={total})")
    ax.axis("equal")
    plt.tight_layout()
    plt.show()

    # ------ PRINT LIST -------
    for s in summary_strings:
        print(s)

    # also return it for programmatic use
    return summary_strings


def count_nulls(df, col):
    n = df[col].isna().sum()
    print(f"Nulls: {n}")
    return n

def count_nulls_debug(df, col):
    null_rows = df[df[col].isna()]
    print(f"Rows with nulls in '{col}': {len(null_rows)}")
    return null_rows