from requesting_urls import get_html
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np


def extract_table(url, title):
    """Extracts the first table after title in HTML.

    Args:
        url (str): The URL to request and get table from.
        title (str): The title of the table.

    Returns:
        bs4.element.Tag: The first table after title. If not found, None is returned.
    """

    html = get_html(url).text
    soup = BeautifulSoup(html, "lxml")

    soup_title = soup.find(id=title)

    if soup_title is None:
        return None
    return soup_title.find_all_next("table")[0]

def extract_url(table):
    """Extracts the url of the teams in the Conference Semifinals from Bracket table.

    Args:
        table (bs4.element.Tag): The 'Bracket' table contatining the teams.

    Returns:
        dict of str: str: A dictionary mapping the team name to the team URL.
    """
    rows = table.findAll("tr")

    # Conference semifinals rows start at 4, then skips by 2, then 10, then 2 ...
    i = 4
    skip = 2

    teams_conference_semi = {}

    while i < len(rows):
        a_tag = rows[i].a
        team_name = a_tag.contents[0]
        team_url = a_tag["href"]
        teams_conference_semi[team_name] = "https://en.wikipedia.org" + team_url

        i += skip
        skip = 10 if skip == 2 else 2

    return teams_conference_semi

def extract_player_url(table):
    """Extracts the players url from the team roster.

    Args:
        table (bs4.element.Tag): The table containing all infomration about all the players on the team roster.

    Returns:
        dict of str: str: A dictionary mapping the players name to the players URL.
    """
    players = {}

    a_tags = table.findAll("a")

    # There are 3 a-tags per row. Player names & URL are the 2. a-tag. Skip by 3 to get next
    i = 1
    while i < len(a_tags):
        a_tag = a_tags[i]

        player_name = a_tag.contents[0]
        player_url = a_tag["href"]
        players[player_name] = "https://en.wikipedia.org" + player_url
        
        i += 3

    return players

def extract_points(table, season):
    """Extracts the points from the players Regular Season table.

    Args:
        table (bs4.element.Tag): A BeautifulSoup-tag representing the players Regular Season table.
        season (str): The season to extract points from.

    Returns:
        list of floats: A list of floats representing the score [ppg, bpg, rpg]. 
            If the player does not have any scores, None is returned.
    """
    rows = table.find_all("tr")

    # Find which column the points are located, in case something changes with the table.
    headers = [th.get_text(strip=True)
                for th in rows[0].find_all("th")]
    ppg_index = headers.index("PPG")  # Points per game
    bpg_index = headers.index("BPG")  # Blocks per game
    rpg_index = headers.index("RPG")  # Rebounds per game

    for row in rows[::-1]:
        cells = row.find_all("td")

        if len(cells) > 0 and cells[0].get_text(strip=True) == season:

            try:
                ppg = float(cells[ppg_index].get_text(strip=True))
            except ValueError:
                ppg = 0.0
            try:
                bpg = float(cells[bpg_index].get_text(strip=True))
            except ValueError:
                bpg = 0.0
            try:
                rpg = float(cells[rpg_index].get_text(strip=True))
            except ValueError:
                rpg = 0.0

            return [ppg, bpg, rpg]
    return None

def extract_top_3_players(players, season):
    """Extracts the top 3 players on the team, based on PPG.

    Args:
        players (dict of str: str): A dictionary of players names mapped to their URL.
        season (str): The season to extract points from.

    Returns:
        dict of str: list of floats: A dictionary with players names as keys, and a 
            list with the scores [ppg, bpg, rpg] as values.
    """
    top_players = {}

    for player in players:
        reg_season_table = extract_table(players[player], "Regular_season")

        if reg_season_table is None:
            # No scores - not a top player...
            continue

        points = extract_points(reg_season_table, season)

        if points is not None:
            top_players[player] = points

    top_3_players = dict(sorted(top_players.items(),
                                key=lambda k_v: k_v[1][0], reverse=True)[:3])  # Sorted by PPG

    return top_3_players

def create_plot(top_players_in_teams, type_points, title):
    """Creates a plot of top players in teams for given type of points.
    
    Plot is saved to NBA_player_statistics directory as png.

    Args:
        top_players_in_teams (dict of str: dict of str: dict: of str: float): 
            A dictionary with team names as keys, and a dictionary with players names as keys, 
            and a dictionary with the score type as keys and float values representing the score as values.
        type_points (str): The type of points to plot. Should be PPG, BPG or RPG.
        title (str): The statistics title to use for plot.
    """
    _, ax = plt.subplots()

    index = (type_points == "PPG" and 0) or (
             type_points == "BPG" and 1) or (
             type_points == "RPG" and 2)

    for team in top_players_in_teams:
        players = top_players_in_teams[team]
        names = list(players.keys())

        values = [value[index] for value in list(players.values())]

        team_bars = ax.bar(names, values, label=team, zorder=3)
        team_bars.set_label(team)

    ax.set_title(title)
    ax.legend(title="Teams", bbox_to_anchor=(1.05, 1))
    
    plt.grid(b=True, which="major", axis="y", zorder=0)
    plt.xticks(rotation=90)
    plt.savefig(f"NBA_player_statistics/players_over_{type_points.lower()}.png", bbox_inches="tight")



if __name__ == "__main__":

    url = "https://en.wikipedia.org/wiki/2020_NBA_playoffs"

    table = extract_table(url, "Bracket")
    teams = extract_url(table)

    top_players_in_teams = {}

    for team in teams:
        roster_table = extract_table(teams[team], "Roster") # Contains multiple tables
        players_table = roster_table.find("table")

        players = extract_player_url(players_table)
        top_players_in_teams[team] = extract_top_3_players(players, "2019–20")

    # Plotting
    create_plot(top_players_in_teams, "PPG",
                "Points per game for top players in NBA 2019-20")
    create_plot(top_players_in_teams, "BPG",
                "Blocks per game for top players in NBA 2019-20")
    create_plot(top_players_in_teams, "RPG",
                "Rebounds per game for top players in NBA 2019-20")

    print("Finished plotting")
