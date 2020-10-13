import requests as req

def get_html(url, params=None, output=None):

    response = req.get(url, params=params)

    if output is not None:
        with open(f"./requesting_urls/{output}.txt", "w") as file:
            file.write(f"URL: {response.url}\n\n")
            file.write(response.text)
    
    return response
    
    
