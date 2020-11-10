import os
import re
import pandas as pd
import altair as alt


def plot_reported_cases(data,
                        county="Alle fylker",
                        start="2020-02-21",
                        end="2020-11-08"):
    """Creates a bar chart of all reported cases of Covic-19 in given county.

    Args:
        data (pandas.core.frame.DataFrame): The data to be plotted.
        county (str, optional): The county to be plotted.
            Defaults to "Alle fylker".
        start (str, optional): The start date for the time range (inclusive).
            Format: YYYY-MM-DD. Defaults to "2020-02-21".
        end (str, optional): The end date for the time range (inclusive).
            Format: YYYY-MM-DD. Defaults to "2020-11-08".

    Returns:
        altair.vegalite.v4.api.Chart: The plotted bar chart.
    """
    data = data.loc[(data["Fylke"] == county) & (
        data["Dato"] >= start) & (data["Dato"] <= end)]

    chart = alt.Chart(data).mark_bar().encode(
        x="Dato",
        y="Nye tilfeller",
        color="Fylke"
    ).properties(
        title="Antall meldte covid-19 tilfeller etter prøvetakingsdato"
    )

    return chart


def plot_cumulative_cases(data,
                          county="Alle fylker",
                          start="2020-02-21",
                          end="2020-11-08"):
    """Creates a line chart of cumulative cases of Covic-19 in given county.

    Args:
        data (pandas.core.frame.DataFrame): The data to be plotted.
        county (str, optional): The county to be plotted.
            Defaults to "Alle fylker".
        start (str, optional): The start date for the time range (inclusive).
            Format: YYYY-MM-DD. Defaults to "2020-02-21".
        end (str, optional): The end date for the time range (inclusive).
            Format: YYYY-MM-DD. Defaults to "2020-11-08".

    Returns:
        altair.vegalite.v4.api.Chart: The plotted line chart.
    """
    data = data.loc[(data["Fylke"] == county) & (
        data["Dato"] >= start) & (data["Dato"] <= end)]

    chart = alt.Chart(data).mark_line().encode(
        x="Dato",
        y="Kumulativt antall",
        color="Fylke"
    ).properties(
        title="Antall meldte covid-19 tilfeller etter prøvetakingsdato"
    )

    return chart


def _read_csv(directory):
    """Reads and combines all .csv files in given directory to one Dataframe.

    Args:
        directory (str): The directory path.

    Returns:
        pandas.core.frame.DataFrame: The combined data from all .csv files.
    """

    counties = ["Alle fylker", "Agder", "Innlandet", "Møre og Romsdal",
                "Nordland", "Oslo", "Rogaland", "Troms og Finnmark",
                "Trøndelag", "Vestfold og Telemark", "Vestland", "Viken"]

    master_df = pd.DataFrame()

    for file in os.listdir(directory):
        file_name, file_ext = os.path.splitext(file)

        if file_ext != ".csv":
            continue

        county_no = int(re.findall(
            fr"antall-meldte-covid-19-t-(.*)", file_name)[0])

        county_data = pd.read_csv(directory + "/" + file,
                                  sep=";", parse_dates=["Dato"], dayfirst=True)
        county_data['Fylke'] = counties[county_no]

        master_df = master_df.append(county_data)

    return master_df


if __name__ == "__main__":

    data = _read_csv("./reported_cases")

    plot_reported_cases(data)

    plot_cumulative_cases(data)
