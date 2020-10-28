# Assignment 5

This assignment was solved using macOS.

All functions not mentioned in the assignment text have names starting with an underscore.

## Dependencies
All packages can be installed using `pip`.

Pythons `request module (2.24.0)` is used to send HTTP requests.
```bash
pip install requests
```

`BeautifulSoup (4.9.1)` is used to parse HTML.
```bash
pip install beautifulsoup4
```

The `matplotlib (3.2.2)` package is used for plotting.
```bash
pip install matplotlib
```

The built-in python package `re` is used for the regex solutions.

## 5.1 Sending URL requests
The script `requesting_urls.py` includes one public function `get_html(url, params, output)`.

When run as a script the following URLs are requested without parameters:
- https://en.wikipedia.org/wiki/Studio_Ghibli
- https://en.wikipedia.org/wiki/Star_Wars
- https://en.wikipedia.org/wiki/Dungeons_%26_Dragons

and https://en.wikipedia.org/w/index.php is requested using the following parameters:
- title=Main Page and action=info
- title=Hurricane Gonzalo and oldid=983056166

The output (URL and HTML as .txt files) of these examples can be found in the `requesting_urls` folder.

How to run examples:
```bash
python3 requesting_urls.py
```

## 5.2 Regex for filtering URLs
The script `filter_urls.py` includes two public functions `find_urls(html, base)` and `find_articles(html, base, language, output)`.

When run as a script the following URLs are given to `find_articles` with base="https://en.wikipedia.org" and no language:
- https://en.wikipedia.org/wiki/Nobel_Prize
- https://en.wikipedia.org/wiki/Bundesliga
- https://en.wikipedia.org/wiki/2019%E2%80%9320_FIS_Alpine_Ski_World_Cup

The output (all URLs and only Wikipedia articles as .txt files) of these examples can be found in the `filter_urls` folder.

How to run examples:
```bash
python3 filter_urls.py
```

## 5.3 Regex for finding dates
The script `collect_dates.py` includes one public function `find_dates(html, output)`.

Note that year must be between 0000 - 2999.

When run as a script the following URLs are given to `find_dates`:
- https://en.wikipedia.org/wiki/Linus_Pauling
- https://en.wikipedia.org/wiki/Rafael_Nadal
- https://en.wikipedia.org/wiki/J._K._Rowling
- https://en.wikipedia.org/wiki/Richard_Feynman
- https://en.wikipedia.org/wiki/Hans_Rosling

The output (all dates found as .txt files) of these examples can be found in the `filter_dates_regex` folder.

How to run examples:
```bash
python3 collect_dates.py
```

## 5.4 Filtering datetime objects using soup
The script `time_planner.py` includes one public function `extract_events(soup_table)`.

When run as a script "https://en.wikipedia.org/wiki/2019%E2%80%9320_FIS_Alpine_Ski_World_Cup" is used as an example.

The output (a betting slip as .md file) of this example can be found in the `datetime_filter` folder.

How to run examples:
```bash
python3 time_planner.py
```

## 5.5 NBA Player Statistics Season 2019/2020
The script `fetch_player_statistics.py` includes one public function `extract_url(table)`.

When run as a script "https://en.wikipedia.org/wiki/2020_NBA_playoffs" is used as an example.

The output (three plots of the players over the points/blocks/rebounds per game) of this example can be found in the `NBA_player_statistics` folder.

How to run examples:
```bash
python3 fetch_player_statistics.py
```