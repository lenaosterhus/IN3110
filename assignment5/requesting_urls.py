import requests as req

def get_html(url, params=None, output=None):

    response = req.get(url, params=params)

    if output is not None:
        with open(f"./requesting_urls/{output}.txt", "w") as file:
            file.write(f"URL: {response.url}\n\n")
            file.write(response.text)
    
    return response
    
    
if __name__ == "__main__":

    # Test without params
    urls = ["https://en.wikipedia.org/wiki/Studio_Ghibli",
             "https://en.wikipedia.org/wiki/Star_Wars",
             "https://en.wikipedia.org/wiki/Dungeons_%26_Dragons"]

    outputs = ["Studio_Ghibli", "Star_Wars", "Dungeons_%26_Dragons"]

    for url, output in zip(urls, outputs):
        get_html(url, output=output)

    
    # Test with params
    url = "https://en.wikipedia.org/w/index.php"

    params = [{"title": "Main_Page", "action": "info"}, 
              {"title": "Hurricane_Gonzalo", "oldid": "983056166"}]
    outputs = ["Main_Page", "Hurricane_Gonzalo"]

    for param, output in zip(params, outputs):
        get_html(url, params=param, output=output)
