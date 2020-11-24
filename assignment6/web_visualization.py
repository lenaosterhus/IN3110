import os
import re
import pandas as pd
import altair as alt
from flask import Flask, render_template, request
import tempfile

# Colors for plots
color_reported = "#088da5"
color_cumulative = "#a52008"


def plot_reported_cases(data,
                        county="Alle fylker",
                        start="2020-02-21",
                        end="2020-11-23"):
    """Creates a bar chart of all reported cases of Covic-19 in given county.

    Args:
        data (pandas.core.frame.DataFrame): The data to be plotted.
        county (str, optional): The county to be plotted.
            Defaults to "Alle fylker".
        start (str, optional): The start date for the time range (inclusive).
            Format: YYYY-MM-DD. Defaults to "2020-02-21".
        end (str, optional): The end date for the time range (inclusive).
            Format: YYYY-MM-DD. Defaults to "2020-11-23".

    Returns:
        altair.vegalite.v4.api.Chart: The plotted bar chart.
    """
    data = data.loc[(data["Fylke"] == county) & (
        data["Dato"] >= start) & (data["Dato"] <= end)]

    chart = alt.Chart(data).mark_bar(color=color_reported, size=2).encode(
        x="Dato",
        y="Nye tilfeller",
        tooltip=["Dato", "Nye tilfeller"]
    ).properties(
        title=f"Antall meldte nye covid-19 tilfeller etter prøvetakingsdato for: {county}",
        width=600
    ).interactive(bind_y=False)

    return chart


def plot_cumulative_cases(data,
                          county="Alle fylker",
                          start="2020-02-21",
                          end="2020-11-23"):
    """Creates a line chart of cumulative cases of Covic-19 in given county.

    Args:
        data (pandas.core.frame.DataFrame): The data to be plotted.
        county (str, optional): The county to be plotted.
            Defaults to "Alle fylker".
        start (str, optional): The start date for the time range (inclusive).
            Format: YYYY-MM-DD. Defaults to "2020-02-21".
        end (str, optional): The end date for the time range (inclusive).
            Format: YYYY-MM-DD. Defaults to "2020-11-23".

    Returns:
        altair.vegalite.v4.api.Chart: The plotted line chart.
    """
    data = data.loc[(data["Fylke"] == county) & (
        data["Dato"] >= start) & (data["Dato"] <= end)]

    # Create a selection that chooses the nearest point & selects based on date
    nearest = alt.selection(type="single", nearest=True,
                            on="mouseover", fields=["Dato"], empty="none")

    line = alt.Chart(data).mark_line(color=color_cumulative).encode(
        x="Dato",
        y="Kumulativt antall:Q",
    )

    # Draws a circle on the line and displays information (tooltip)
    points = alt.Chart(data).mark_circle(
        color=color_cumulative, 
        size=50
    ).encode(
        x="Dato",
        y="Kumulativt antall:Q",
        opacity=alt.condition(nearest, alt.value(1), alt.value(0)),
        tooltip=["Dato", "Kumulativt antall:Q"]
    ).add_selection(
        nearest
    )

    chart = alt.layer(
        line, points
    ).properties(
        title=f"Kumulativt antall meldte covid-19 tilfeller etter prøvetakingsdato for: {county}",
        width=600
    ).interactive(bind_y=False)

    return chart


def plot_both(data,
              county="Alle fylker",
              start="2020-02-21",
              end="2020-11-23"):
    """Creates a plot displaying both bars for reported cases and a line for 
        cumulative cases of Covic-19 in given county.

    Args:
        data (pandas.core.frame.DataFrame): The data to be plotted.
        county (str, optional): The county to be plotted.
            Defaults to "Alle fylker".
        start (str, optional): The start date for the time range (inclusive).
            Format: YYYY-MM-DD. Defaults to "2020-02-21".
        end (str, optional): The end date for the time range (inclusive).
            Format: YYYY-MM-DD. Defaults to "2020-11-23".

    Returns:
        altair.vegalite.v4.api.Chart: The plotted chart.
    """
    data = data.loc[(data["Fylke"] == county) & (
        data["Dato"] >= start) & (data["Dato"] <= end)]

    base = alt.Chart(data).encode(
        x="Dato"
    ).properties(
        title=f"Antall meldte covid-19 tilfeller etter prøvetakingsdato for: {county}",
        width=600
    )

    reported = base.mark_bar(color=color_reported, size=2).encode(
        y=alt.Y("Nye tilfeller",
                axis=alt.Axis(titleColor=color_reported)),
        tooltip=["Dato", "Nye tilfeller"]
    ).interactive(
        bind_y=False
    )

    cumulative = base.mark_line(stroke=color_cumulative).encode(
        y=alt.Y("Kumulativt antall",
                axis=alt.Axis(titleColor=color_cumulative)),
        tooltip=["Dato", "Kumulativt antall"]
    ).interactive(
        bind_y=False
    )

    chart = alt.layer(reported, cumulative).resolve_scale(
        y="independent"
    )

    return chart

    
def _read_csv(directory):
    """Reads and combines all .csv files in given directory to one Dataframe.

    The .csv files are named with the index of the corresponding county in the
    counties list: ["Alle fylker", "Agder", "Innlandet", "Møre og Romsdal",
                    "Nordland", "Oslo", "Rogaland", "Troms og Finnmark",
                    "Trøndelag", "Vestfold og Telemark", "Vestland", "Viken"]

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


def plot_norway():
    """Creates a plot displaying the reported COVID-19 rate per 100000 
        inhabitants by county in Norway.
    
    The data was last updated 11.11.2020.

    Returns:
        altair.vegalite.v4.api.Chart: The plotted chart.
    """
    data = pd.read_csv("antall-meldte-tilfeller.csv", sep=";")

    # topojson of norways counties
    counties = alt.topo_feature("https://raw.githubusercontent.com/deldersveld/topojson/master/countries/norway/norway-new-counties.json", 
                                "Fylker")

    # Used for highlighting
    nearest = alt.selection(type="single", on="mouseover", 
                            fields=["properties.navn"], empty="none")

    fig = alt.Chart(counties).mark_geoshape().encode(
        tooltip=[
            alt.Tooltip("properties.navn:N", title="Fylke"),
            alt.Tooltip("Insidens:Q", title="Tilfeller per 100 000"),
        ],
        color=alt.Color("Insidens:Q", scale=alt.Scale(scheme="reds"),
                        legend=alt.Legend(title="Tilfeller per 100 000", 
                                          direction="horizontal", 
                                          orient="bottom",
                                          gradientLength=375)),
        stroke=alt.condition(nearest, alt.value("grey"), alt.value(None)),
        opacity=alt.condition(nearest, alt.value(1), alt.value(0.8)),

    # Map cases to counties
    ).transform_lookup(
        lookup="properties.navn",
        from_=alt.LookupData(data, "Category", ["Insidens"])
    ).properties(
        width=375,
        height=450,
        title={"text": "Antall tilfeller per 100 000 innbyggere i hvert fylke",
               "subtitle": "Oppdatert 11.11.2020",
               "subtitleColor": "lightgray"}
    ).add_selection(
        nearest
    ).configure_view(
        strokeOpacity=0 #  Removes borders
    )

    return fig


app = Flask(__name__)
data = _read_csv("./reported_cases")
county = "Alle fylker"


@app.route('/')
def root():
    """Creates the root page.

    Returns:
        str: The HTML from template 'plot.html'.
    """
    return render_template("plot.html", selected_county=county)


@app.route('/', methods=['POST'])
def select_county():
    """Updates the root page with selected county.

    Returns:
        str: The HTML from template 'plot.html' with selected county.
    """
    global county 
    county = request.form["fylke"]
    return render_template("plot.html", selected_county=county)


@app.route('/help')
def display_help():
    """Creates the help page.

    Returns:
        str: The HTML from template 'web_visualization.html'.
    """
    return render_template("web_visualization.html")


# -------------- Methods for creating JSON figures --------------
def _get_json(fig):
    tmp = tempfile.NamedTemporaryFile(suffix=".json")
    fig.save(tmp.name)

    with open(tmp.name) as file:
        return file.read()


@app.route('/plot_reported.json')
def _plot_reported_json():
    fig = plot_reported_cases(data, county)
    return _get_json(fig)


@app.route('/plot_cumulative.json')
def _plot_cumulative_json():
    fig = plot_cumulative_cases(data, county)
    return _get_json(fig)


@app.route('/plot_both.json')
def _plot_both_json():
    fig = plot_both(data, county)
    return _get_json(fig)


@app.route('/plot_norway.json')
def _plot_norway_json():
    fig = plot_norway()
    return _get_json(fig)


if __name__ == "__main__":
    app.run(debug=True)
