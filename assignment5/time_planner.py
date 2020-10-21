from requesting_urls import get_html
from bs4 import BeautifulSoup
import re
import datetime


def extract_events(soup_table):
    """Extracts the events from the table provided

    Args:
        soup_table (bs4.element.Tag): A BeautifulSoup-tag representing the table

    Returns:
        list of dictionaries: A list of events represented as dictionaries
    """
    all_data = []

    # Disciplines
    disciplines_string = soup_table.find('caption').text
    disciplines_pattern = r'([A-Z]{2}) – ([\w ]*),?'
    disciplines = dict(re.findall(disciplines_pattern, disciplines_string))

    soup_rows = soup_table.find_all('tr')

    # Used to find discipline data
    discipline_pattern = r'^([A-Z]{2})[a-z0-9]{3}'

    for row_n, row in enumerate(soup_rows[1:]):
        event = {}

        cells = [td.get_text(strip=True) for td in row.find_all(['td', 'th'])]

        for cell_n, cell in enumerate(cells):

            # Remove footnotes = "[xyz]"
            cell = re.sub(r'\[[a-zA-Z0-9 ]+\] ?', '', cell)

            # Check if cell is date
            if re.match(r'\d{1,2} [A-Z][a-z]{2,7} \d{4}', cell):
                date_obj = datetime.datetime.strptime(
                    cell, '%d %B %Y').date()
                
                event['Date'] = date_obj

                # If next cell is discipline, use venue of the previous row
                next_cell = cells[cell_n+1]

                if re.match(discipline_pattern, next_cell):
                    # Next cell is discipline (not Venue) - use value of previous row for Venue
                    event['Venue'] = all_data[row_n-1]['Venue']

                else:
                    event['Venue'] = next_cell

                continue
                
            # Check if cell is discipline
            discipline_match = re.match(discipline_pattern, cell)
            if discipline_match:
                event['Discipline'] = disciplines[discipline_match.group(1)]

        all_data.append(event)

    # Clean up empty rows
    return [event for event in all_data if len(event) > 0]
    

def get_tables(url):
    """Gets the 'wikitable plainrowheaders'-tables from URL

    Args:
        url (string): The URL to parse for 'wikitable plainrowheaders'-tables

    Returns:
        bs4.element.ResultSet: The tables found in the URL
    """
    html = get_html(url).text
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find_all('table', class_="wikitable plainrowheaders")


def create_betting_slip(events):
    """Creates a betting slip with all events

    Creates a betting slip as a Markdown-file with information about 
    the date, venue and discipline of the events

    Args:
        events (list of dictionaries): The list of all events as dictionaries
    """
    with open(f"./datetime_filter/betting_slip_empty.md", "w") as file:
        file.write(f"# BETTING SLIP\n\n")
        file.write(f"Name: _____________________________\n\n")

        file.write("| DATE | VENUE | DISCIPLINE | Who Wins? |\n")
        file.write("|------|-------|------------|-----------|\n")

        for event in events:
            file.write(f"|{event['Date']}|{event['Venue']}|{event['Discipline']}| |\n")


if __name__ == "__main__":
    all_events = []
    for table in get_tables("https://en.wikipedia.org/wiki/2019%E2%80%9320_FIS_Alpine_Ski_World_Cup"):
        all_events += extract_events(table)
    
    sorted_list = sorted(all_events, key = lambda i: i['Date']) # Sorted by date

    create_betting_slip(sorted_list)

