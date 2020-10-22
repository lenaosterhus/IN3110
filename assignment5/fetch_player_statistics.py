from requesting_urls import get_html
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np

def extract_table(url, title):

    html = get_html(url).text
    soup = BeautifulSoup(html, 'lxml')

    title = soup.find(id=title)

    if title is None:
        return None
    return title.find_all_next("table")[0]  # <class 'bs4.element.Tag'>

def extract_url(table):
    rows = table.findAll("tr")

    # Conference semifinals rows start at 4, then skip with 2, then 10, then 2 ...
    i = 4
    skip = 2

    # TODO: Kan gjøres om til liste dersom det ikke er behov for navn!
    teams_conference_semi = {}
    while i < len(rows):
        a_tag = rows[i].a
        team_name = a_tag.contents[0]
        team_url = a_tag['href']
        teams_conference_semi[team_name] = "https://en.wikipedia.org" + team_url

        i += skip
        skip = 10 if skip == 2 else 2

    return teams_conference_semi

def extract_points(table):
    """[summary]

    Args:
        table (bs4.element.Tag): A BeautifulSoup-tag representing the table

    Returns:
        dict: A dictionary with string keys representing the score type 
            and float values representing the score
    """
    rows = table.find_all("tr")

    # Find which column the points are located, in case something changes with the table
    headers = [th.get_text(strip=True)
                for th in rows[0].find_all("th")]
    ppg_index = headers.index('PPG')  # Points per game
    bpg_index = headers.index('BPG')  # Blocks per game
    rpg_index = headers.index('RPG')  # Rebounds per game

    for row in rows[::-1]:
        cells = row.find_all('td')

        if len(cells) > 0 and cells[0].get_text(strip=True) == "2019–20":

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

            return dict([("PPG", ppg), ("BPG", bpg), ("RPG", rpg)])
    return None


def create_plot(top_players_in_teams, type_points, title):
    # type_points = PPG, BPG, RPG
    _, ax = plt.subplots()

    for team in top_players_in_teams:
        players = top_players_in_teams[team]
        names = list(players.keys())

        ppg_values = [value[type_points] for value in list(players.values())]

        team_bars = ax.bar(names, ppg_values, label=team, zorder=3)
        team_bars.set_label(team)

    ax.set_title(title)
    ax.legend(title='Teams', bbox_to_anchor=(1.05, 1))
    
    plt.grid(b=True, which='major', axis='y', zorder=0)
    plt.xticks(rotation=90)
    plt.savefig(f"NBA_player_statistics/players_over_{type_points.lower()}.png", bbox_inches='tight')



if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/2020_NBA_playoffs"

    table = extract_table(url, "Bracket")
    teams = extract_url(table)

    players_in_teams = {}
    top_players_in_teams = {}

    for team in teams:
            roster_table = extract_table(teams[team], "Roster")
            players_table = roster_table.find("table")

            players = {}
            top_players = {}
            a_tags = players_table.findAll('a')
            i = 1
            while i < len(a_tags):
                a_tag = a_tags[i]
                player_name = a_tag.contents[0]
                player_url = a_tag['href']
                players[player_name] = "https://en.wikipedia.org" + player_url
                i += 3
            players_in_teams[team] = players

            # Replace URL with dict of PPG, BPG, RPG
            for player in players:
                reg_season_table = extract_table(players[player], "Regular_season")

                if reg_season_table is None:
                    # No scores
                    continue

                points = extract_points(reg_season_table)
                if points is not None:
                    top_players[player] = points

            # Players = {{},{}}
            # top_3_players = [(string, dict), (...)]
            top_3_players = dict(sorted(top_players.items(),
                                key=lambda k_v: k_v[1]["PPG"], reverse=True)[:3])  # Sorted by PPG
            
            top_players_in_teams[team] = top_3_players
    
    # Plotting
    create_plot(top_players_in_teams, 'PPG',
                "Points per game for top players in NBA 2019-20")



    
