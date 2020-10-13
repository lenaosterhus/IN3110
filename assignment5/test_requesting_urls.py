from requesting_urls import get_html
import pytest


@pytest.mark.parametrize("url", ("https://en.wikipedia.org/wiki/Studio_Ghibli", 
                                 "https://en.wikipedia.org/wiki/Star_Wars", 
                                 "https://en.wikipedia.org/wiki/Dungeons_%26_Dragons"))
@pytest.mark.parametrize("output", ("Studio_Ghibli",
                                    "Star_Wars",
                                    "Dungeons_%26_Dragons"))
def test_get_html_no_params(url, output):
    # Tests get_html() without any paramaters, and writes to file

    response = get_html(url, output=output)

    assert response.url == url


@pytest.mark.parametrize("params, output", [({"title": "Main_Page", "action": "info"}, "Main_Page"),
                                            ({"title": "Hurricane_Gonzalo", "oldid": "983056166"}, "Hurricane_Gonzalo")])
def test_get_html_params(params, output):
    # Tests get_html() with paramaters, and writes to file

    url = "https://en.wikipedia.org/w/index.php"

    response = get_html(url, params=params, output=output)
    
    key_list = list(params.keys())
    val_list = list(params.values())
    expected_url = f"{url}?{key_list[0]}={val_list[0]}&{key_list[1]}={val_list[1]}"

    assert response.url == expected_url
