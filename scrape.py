import requests
from bs4 import BeautifulSoup
import re
from dateutil.parser import parse
import insertdata as ins
from random import randint


# This function extracts the subdirectories for each game's wiki page
def scrape_subdir(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    output = []
    h4 = soup.find_all('h4')

    for num in range(len(h4)):
        temp = h4[num]
        key = temp.find_all(text=True)[0]
        output.append(key)

    # Ignore games under "Chronological" header and only
    # extract the games under the "List by genre" header
    headers = []
    restricted_headers = ["Tabletop games", "Upcoming", "Cancelled"]
    for header in output:
        if header not in restricted_headers:
            headers.append(header)

    # Replace spaces in genre names with underscores so
    # can find them by id in the HTML <span> tags
    header_ids = []
    for h in headers:
        header_id = h.replace(" ", "_")
        header_ids.append(header_id)

    # Find all the games along with their dates (year
    # only) based on the genres we found
    game_links = []
    for h_id in header_ids:
        for i in soup.findAll("span", id=str(h_id)):
            ul = i.findNext('ul')
            v = [li.a.get('href') for li in ul.findAll('li')]
            for j in v:
                if j not in game_links:
                    game_links.append(j)
    return game_links


# This is a function for scrape_game(), used to extract the text in HTML tag(s)
def text_scrape(source, tag1):
    scraped_text = []
    div = source.find('div', class_="pi-data-value pi-font")
    for i in div.find_all(tag1):
        text = re.sub(r'\[.*?\]', '', i.text)
        if text != '':
            scraped_text.append(text)

    if len(scraped_text) == 0:
        scraped_text.append(div.text)

    return scraped_text


# This is a function that scrapes the data from each individual game using their wiki page
def scrape_game(url):
    # Access the website of the specific game
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    # Extract the Game Title
    game_title = soup.find('h1', class_="page-header__title").text.strip('\n')

    game_developers = []
    # Find the Developer(s)
    try:
        dev = soup.find("div", attrs={"data-source": "developer"})
        game_developers = text_scrape(dev, 'a')
    except:
        game_developers.append(None)

    # Find the Publisher(s)
    finally:
        pub = soup.find("div", attrs={"data-source": "publisher"})
        game_publishers = text_scrape(pub, 'a')

    # Find the Release Date(s)
    release_dates = []
    rel = soup.find("div", attrs={"data-source": "released"})
    for small in rel.find('div', class_="pi-data-value pi-font").find_all('small'):
        release_text = re.sub(r'\[.*?\]', '', small.next_sibling.text)
        if release_text != '':
            try:
                release_dates.append(parse(release_text, fuzzy=False))
            except ValueError:
                # print("Not a valid date")
                pass

    if len(release_dates) == 0:
        release_text = re.sub(r'\[.*?\]', '', rel.find('div',
                                                       class_="pi-data-value pi-font").text)
        try:
            release_dates.append(parse(release_text, fuzzy=False))
        except ValueError:
            # print('Not a valid date')
            pass

    # Find the earliest release date
    oldest_date = min(release_dates)

    # Find the Platform(s)
    plat = soup.find("div", attrs={"data-source": "platforms"})
    game_platforms = text_scrape(plat, 'a')

    return game_title, game_developers, game_publishers, oldest_date, game_platforms


def random_with_N_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1

    return randint(range_start, range_end)


if __name__ == '__main__':
    
    domain = "https://sonic.fandom.com"
    game_list_subdir = "/wiki/List_of_games"

    subdirectory_list = scrape_subdir(domain + game_list_subdir)

    gID_list = []
    cID_list = []
    consoles = []
    for subdirectory in subdirectory_list:
        t, developers, publishers, release_date, platforms = scrape_game(
            domain + subdirectory)
        title = re.sub(' +', ' ', t)
        publisher = re.sub(' +', ' ', publishers[0])

        game_id = 'g' + str(random_with_N_digits(5))
        while (1):
            if game_id not in gID_list:
                gID_list.append(game_id)
                break
            else:
                game_id = 'g' + str(random_with_N_digits(5))

        for console in platforms:
            if console not in consoles:
                consoles.append(console)
                console_id = 'c' + str(random_with_N_digits(5))

                while 1:
                    if console_id not in cID_list:
                        cID_list.append(console_id)
                        break
                    else:
                        console_id = 'c' + str(random_with_N_digits(5))
                ins.insert_console(console_id, console)
            else:
                continue

        if developers[0] is not None:
            print(title + '\n' + developers[0] + '\n' + publishers[0] + '\n' + str(release_date) + '\n')
            ins.insert_game(game_id, title, 1, publisher, release_date)
        else:
            print(title + '\n' + publishers[0] + '\n' + str(release_date) + '\n')
            ins.insert_game(game_id, title, 0, publisher, release_date)
        print(domain+subdirectory)
        print('\n')