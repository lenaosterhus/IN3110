import re

def find_urls(html, base=None):
    """[summary]

    Args:
        html (string): The html code to search for URLs
        base (string): The base URL for relative URLs

    Returns:
        list: The list of all URLs found in the html-string
    """

    regex_url = r"<a(?:[^href]*)href=\"([a-zA-Z0-9\/-_@:%.\+()]+)(?:#*[a-zA-Z0-9\/-_@:%.\+()]*)\""

    # Absolute and relative URLs
    urls = re.findall(regex_url, html, flags=re.M)

    # Partial URLs start with only one /
    pattern_partial_url = r'^(/[^/]+)'
    
    if base is None:
        # Remove relative URLs
        urls[:] = [url for url in urls if not re.match(pattern_partial_url, url)]
    else:
        # Add base to relative URLs
        urls[:] = [re.sub(pattern_partial_url, fr'{base}\g<1>', url) for url in urls]

    # Add 'http:' to broken URLs
    # E.g.: //en.wikipedia.org/wiki/Wikipedia:Contact_us
    pattern_broken_url = r'^(//[^/]+)'
    urls[:] = [re.sub(pattern_broken_url, fr'https:\g<1>', url) for url in urls]

    return urls


def find_articles(html, base=None, language="", output=None):

    urls = find_urls(html, base)


    pattern_wiki = fr'.*{language}\.wikipedia\.org/.*'
    urls[:] = [url for url in urls if re.match(pattern_wiki, url)]

    if output is not None:
        with open(f"./filter_urls/{output}.txt", "w") as file:
            file.write("\n".join(urls))

    return urls

