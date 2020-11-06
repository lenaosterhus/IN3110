from requesting_urls import get_html
import re


def _get_num_month(text):
    """Returns the numerical value of month as string.

    Args:
        text (str): The month as a string. E.g. "Jan" or "January".

    Returns:
        str: The numerical value of the month as a string.
    """

    #Shortened this method down to a list
    months = ["Jan", "Feb", "Mar",
              "Apr", "May", "Jun", 
              "Jul", "Aug", "Sep",
              "Oct", "Nov", "Dec"]

    for i, month in enumerate(months):
        if month in text:
            if i+1 < 10: return "0" + str(i+1)
            return str(i+1)
    return ""

def _get_correct_day(day):
    """Returns the day with two digits as string.

    Args:
        day (str): The day E.g. "5" or "15".

    Returns:
        str: The day as a string with two digits. E.g. "05" or "15".
    """
    if len(day) == 2:
        return day
    if len(day) == 1:
        return "0" + day
    return ""

def find_dates(html, output=None):
    """Finds the dates in a string, and optionally saves the list to a file.

    The following date formats are supported:
        DMY: 13 October 2020 AND October 2020
        MDY: October 13, 2020 AND October, 2020
        YMD: 2020 October 13
        ISO: 2020-10-13

    Year must be between 0000 - 2999
    
    Args:
        html (str): The string 
        output (str, optional): The filename for saving the list of dates. Defaults to None.

    Returns:
        list of str: A list of the dates, sorted and without duplicates.
    """

    dates = []

    # Regex patterns
    # Date can be single digit
    date = r"((?:0?[1-9])|(?:[12][0-9])|(?:3[01]))"
    # Month can be abbreviated
    month = r"((?:(?:Jan)|(?:Feb)|(?:Mar)|(?:Apr)|(?:May)|(?:Jun)|(?:Jul)|(?:Aug)|(?:Sep)|(?:Oct)|(?:Nov)|(?:Dec))[a-z]{0,6})"
    # Year must be between 0000 - 2999
    year = r"([012][0-9]{3})"

    # DMY (date optional)
    pattern_DMY = fr"\b{date}? ?{month} {year}\b"
    dates += [f"{date[2]}/{_get_num_month(date[1])}/{_get_correct_day(date[0])}"
              if len(date[0]) != 0 else f"{date[2]}/{_get_num_month(date[1])}"
              for date in re.findall(pattern_DMY, html, flags=re.M)]
    
    # MDY (date optional)
    pattern_MDY = fr"\b{month} ?{date}?, {year}\b"
    dates += [f"{date[2]}/{_get_num_month(date[0])}/{_get_correct_day(date[1])}"
              if len(date[1]) != 0 else f"{date[2]}/{_get_num_month(date[0])}" 
              for date in re.findall(pattern_MDY, html, flags=re.M)]
    
    # YMD
    pattern_YMD = fr"\b{year} {month} {date}\b"
    dates += [f"{date[0]}/{_get_num_month(date[1])}/{_get_correct_day(date[2])}"
              if len(date[2]) != 0 else f"{date[0]}/{_get_num_month(date[1])}"
              for date in re.findall(pattern_YMD, html, flags=re.M)]
    
    # ISO (date can't be single digit)
    pattern_ISO = fr"\b{year}-((?:0[1-9])|(?:1[0-2]))-((?:0[1-9])|(?:[12][0-9])|(?:3[01]))\b"
    dates += [f"{date[0]}/{date[1]}/{date[2]}"
              for date in re.findall(pattern_ISO, html, flags=re.M)]

    # Sort and remove duplicates
    dates_sorted = sorted(set(dates))

    if output is not None:
        with open(f"./filter_dates_regex/{output}.txt", "w") as file:
            file.write("\n".join(dates_sorted))

    return dates_sorted
    

if __name__ == "__main__":
    urls = ["https://en.wikipedia.org/wiki/Linus_Pauling",
            "https://en.wikipedia.org/wiki/Rafael_Nadal",
            "https://en.wikipedia.org/wiki/J._K._Rowling",
            "https://en.wikipedia.org/wiki/Richard_Feynman",
            "https://en.wikipedia.org/wiki/Hans_Rosling"]

    outputs = ["Linus_Pauling", "Rafael_Nadal", "JK_Rowling", "Richard_Feynman", "Hans_Rosling"]

    for url, output in zip(urls, outputs):
        html = get_html(url).text
        find_dates(html, output)
