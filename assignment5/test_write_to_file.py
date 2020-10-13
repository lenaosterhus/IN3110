from requesting_urls import get_html
from filter_urls import *

import pytest
import re

class TestRequestingUrls:
    
    @pytest.mark.parametrize("url, output", [("https://en.wikipedia.org/wiki/Studio_Ghibli", "Studio_Ghibli"),
                                             ("https://en.wikipedia.org/wiki/Star_Wars", "Star_Wars"),
                                             ("https://en.wikipedia.org/wiki/Dungeons_%26_Dragons", "Dungeons_%26_Dragons")])
    def test_get_html_no_params(self, url, output):
        # Tests get_html() without any paramaters, and writes to file

        response = get_html(url, output=output)

        assert response.url == url


    @pytest.mark.parametrize("params, output", [({"title": "Main_Page", "action": "info"}, "Main_Page"),
                                                ({"title": "Hurricane_Gonzalo", "oldid": "983056166"}, "Hurricane_Gonzalo")])
    def test_get_html_params(self, params, output):
        # Tests get_html() with paramaters, and writes to file

        url = "https://en.wikipedia.org/w/index.php"

        response = get_html(url, params=params, output=output)
        
        key_list = list(params.keys())
        val_list = list(params.values())
        expected_url = f"{url}?{key_list[0]}={val_list[0]}&{key_list[1]}={val_list[1]}"

        assert response.url == expected_url


class TestFilterUrls:

    @pytest.mark.parametrize("url, output", [("https://en.wikipedia.org/wiki/Nobel_Prize", "Nobel_Prize"),
                                             ("https://en.wikipedia.org/wiki/Bundesliga", "Bundesliga"),
                                             ("https://en.wikipedia.org/wiki/2019%E2%80%9320_FIS_Alpine_Ski_World_Cup", "World Cup")])
    def test_find_articles(self, url, output):
        
        html = get_html(url).text

        articles = find_articles(html, base="https://en.wikipedia.org", output=output)

        pattern_wiki = r'.*\.wikipedia\.org/.*'

        assert re.findall(pattern_wiki, articles[0])

