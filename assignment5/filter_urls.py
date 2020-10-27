from requesting_urls import get_html
import re

def find_urls(html, base=None):
    """Finds URLs in HTML string.

    Args:
        html (str): The HTML code to search for URLs.
        base (str, optional): The base URL for relative URLs. Defaults to None.

    Returns:
        list of str: The list of all URLs found in the HTML string.
    """

    regex_url = r"<a(?:[^href]*)href=\"([a-zA-Z0-9\/-_@:%.\+()]+)(?:#*[a-zA-Z0-9\/-_@:%.\+()]*)\""

    # Absolute and relative URLs
    urls = re.findall(regex_url, html, flags=re.M)

    # Partial URLs start with only one /
    pattern_partial_url = r"^(/[^/]+)"
    
    if base is None:
        # Remove relative URLs
        urls = [url for url in urls if not re.match(pattern_partial_url, url)]
    else:
        # Add base to relative URLs
        urls = [re.sub(pattern_partial_url, fr"{base}\g<1>", url) for url in urls]

    # Add "http:" to incomplete URLs
    # E.g.: //en.wikipedia.org/wiki/Wikipedia:Contact_us
    pattern_incomplete_url = r"^(//[^/]+)"
    urls = [re.sub(pattern_incomplete_url, fr"https:\g<1>", url) for url in urls]

    # Remove duplicates and sort
    urls = sorted(set(urls))

    return urls


def find_articles(html, base=None, language="", output=None):
    """Finds URLs for Wikipedia articles in the HTML.

    Args:
        html (str): The HTML as string.
        base (str, optional): The base URL to be used for partial URLs. Defaults to None.
        language (str, optional): The language of wikipedia articles to find. E.g. "en" or "no". 
            Defaults to "".
        output (str, optional): Filename if articles should be written to txt file. Defaults to None.

    Returns:
        list of str: A list of URLs for Wikipedia articles.
    """

    urls = find_urls(html, base)

    # Remove URLs that are not normal Wikipedia articles (no special namespace articles or files)
    pattern_wiki = fr".*{language}\.wikipedia\.org/[^:]*$"
    articles = [url for url in urls if re.match(pattern_wiki, url)]

    if output is not None:
        with open(f"./filter_urls/{output}.txt", "w") as file:
            file.write(f"find_urls found {len(urls)} URLs\n")
            file.write("\n".join(urls))
            file.write("")
            file.write(f"\n\nfind_articles found {len(articles)} articles\n")
            file.write("\n".join(articles))

    return articles


if __name__ == "__main__":
    
    urls = ["https://en.wikipedia.org/wiki/Nobel_Prize",
            "https://en.wikipedia.org/wiki/Bundesliga",
            "https://en.wikipedia.org/wiki/2019%E2%80%9320_FIS_Alpine_Ski_World_Cup"]

    outputs = ["Nobel_Prize", "Bundesliga", "World Cup"]

    for url, output in zip(urls, outputs):
        html = get_html(url).text

        find_articles(html, base="https://en.wikipedia.org", output=output)
